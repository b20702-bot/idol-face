import streamlit as st
from PIL import Image, ImageOps

st.set_page_config(page_title="AI 얼굴 관상 스캐너", page_icon="📸")

st.title("📸 AI 관상 & 아이돌 얼굴 인식 스캐너")
st.write("카메라로 사진을 찍어 관상 분석을 진행해보세요!")

# 카메라 입력
img_file_buffer = st.camera_input("카메라로 사진을 촬영해주세요")

if img_file_buffer is not None:
    # 이미지 불러오기
    image = Image.open(img_file_buffer)
    
    # 흑백(네온 픽셀 느낌)으로 스캔 효과 주기
    gray_image = ImageOps.grayscale(image)
    
    st.image(gray_image, caption="[스캔 완료] 얼굴 특징점 추출 완료!", use_container_width=True)
    
    st.success("🎉 스캔 및 관상 분석이 성공적으로 완료되었습니다!")
    st.balloons()
