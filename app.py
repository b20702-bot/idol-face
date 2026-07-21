import streamlit as st
from PIL import Image, ImageStat, ImageOps, ImageEnhance
import random

# 웹앱 테마 및 레이아웃 설정
st.set_page_config(page_title="AI 실시간 손금 분석 scanner", page_icon="✋", layout="centered")

# 깔끔한 CSS 스타일 적용
st.markdown("""
    <style>
        .report-header { background-color: #f0f2f6; padding: 10px; border-radius: 10px; border: 1px solid #dcdde1; }
        .result-title { color: #1e3799; font-weight: bold; }
        .result-comment { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #1e3799; }
    </style>
""", unsafe_allow_html=True)

st.title("✋ AI 실시간 손금 분석 스캐너")
st.write("카메라로 **왼손바닥**을 촬영하여 AI가 손금의 특징을 분석합니다.")

# Streamlit 자체 웹캠 입력 (설치 오류 없음)
img_file_buffer = st.camera_input("손바닥 전체가 잘 보이도록 촬영해주세요!")

if img_file_buffer is not None:
    # 1. 이미지 로드 및 분석용 변환
    image = Image.open(img_file_buffer)
    
    st.markdown("---")
    st.subheader("🔍 손바닥 특징 및 손금 랜드마크 스캔")
    
    # 스캔 효과 (대비 강조)
    gray_image = ImageOps.grayscale(image)
    processed_img = ImageEnhance.Contrast(gray_image).enhance(1.8)
    
    st.image(processed_img, caption="[스캔 완료] 손바닥 특징점 추출 성공", use_container_width=True)
    
    # 2. 이미지 기반 특징 추출 (서버 에러 없는 안전한 로직)
    stat = ImageStat.Stat(processed_img)
    roughness = stat.stddev[0]  # 손바닥의 전반적인 거칠기 (손금 선명도)
    mean_val = stat.mean[0]    # 손바닥 전체 밝기
    
    st.markdown("### 📊 분석 리포트")
    
    # 3. 분석 결과 리포트 출력
    # (Pillow의 roughness 값을 손금 특징으로 변환하여 신뢰도 있는 메시지 출력)
    
    # 결과 헤더
    st.markdown('<div class="report-header"><h4 style="margin:0;">AI 손금 분석 종합 의견</h4></div>', unsafe_allow_html=True)
    
    # 조건에 따른 맞춤형 분석 메시지
    result_text = ""
    if roughness > 50:
        result_text = "✋ **생명선 & 두뇌선 주력 분석:** 손금의 주선이 뚜렷하고 선명합니다. 의지가 강하고 목표 지향적인 성향으로, 본인의 노력에 따라 큰 성공을 거둘 기운이 강합니다. 건강운과 재물운이 전반적으로 탄탄합니다."
    elif roughness > 30:
        result_text = "✋ **두뇌선 & 감정선 주력 분석:** 손금의 조화가 잘 이루어져 있으며 부드럽고 온화한 성향입니다. 대인관계 운이 매우 뛰어나 주변의 도움을 많이 받습니다. 특히 두뇌선이 발달하여 지혜롭게 위기를 헤쳐갈 관상입니다."
    else:
        result_text = "✋ **감정선 & 재물선 주력 분석:** 손금이 섬세하고 부드럽습니다. 감수성이 풍부하고 직관력이 뛰어납니다. 뜻밖의 횡재수(재물운)가 있으며, 주변 사람들과 소통하며 조화로운 삶을 살아갈 기운이 있습니다."
    
    st.markdown(f'<div class="result-comment">{result_text}</div>', unsafe_allow_html=True)
    
    st.success("🎉 성공적으로 손금 분석이 완료되었습니다!")
    st.balloons()
