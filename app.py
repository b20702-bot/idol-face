import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.set_page_config(page_title="AI 얼굴 관상 & FaceMesh 스캐너", page_icon="🕸️")

st.title("🕸️ AI 얼굴 랜드마크 & 관상 스캐너")
st.write("카메라로 사진을 찍으면 MediaPipe가 얼굴 특징점(Face Mesh)을 정밀하게 추출합니다!")

# Streamlit 카메라 입력
img_file_buffer = st.camera_input("카메라로 사진 찍기")

if img_file_buffer is not None:
    # 1. 찍은 사진을 OpenCV 이미지로 변환
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # 2. MediaPipe FaceMesh 설정 (원래 만드셨던 로직 그대로!)
    mp_face = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    
    # 얼굴 랜드마크 추적
    with mp_face.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face:
        image_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        results = face.process(image_rgb)

        if results.multi_face_landmarks:
            for lm in results.multi_face_landmarks:
                # 원래 코드의 mp_face.FACEMESH_TESSELATION 그물망 그리기
                mp_drawing.draw_landmarks(
                    image=cv2_img,
                    landmark_list=lm,
                    connections=mp_face.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )
            
            # 결과 화면 출력
            st.image(cv2_img, channels="BGR", caption="[스캔 완료] 얼굴 메쉬 랜드마크 추출 성공!", use_container_width=True)
            st.success("🎉 성공적으로 얼굴 특징점(468개)을 스캔했습니다!")
            st.balloons()
        else:
            st.warning("⚠️ 얼굴을 인식하지 못했습니다. 조명이 밝은 곳에서 정면을 바라보고 다시 찍어주세요!")
