import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image

st.title("아이돌 관상 / 얼굴 인식 스캐너 📸")

# Streamlit 전용 웹캠 카메라 입력
img_file_buffer = st.camera_input("카메라로 얼굴을 촬영해주세요!")

if img_file_buffer is not None:
    # 촬영된 이미지를 OpenCV 형식으로 변환
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # MediaPipe Face Mesh 설정
    mp_face = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    
    with mp_face.FaceMesh(refine_landmarks=True) as face:
        image_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        results = face.process(image_rgb)

        if results.multi_face_landmarks:
            for lm in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    cv2_img,
                    lm,
                    mp_face.FACEMESH_TESSELATION
                )
            
            # 결과를 웹 화면에 출력
            st.image(cv2_img, channels="BGR", caption="스캔 완료!")
            st.success("얼굴 인식 성공! 과제 제출 준비 완료 🎉")
        else:
            st.warning("얼굴이 인식되지 않았습니다. 다시 촬영해 보세요!")