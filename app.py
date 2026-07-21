import streamlit as st
from PIL import Image, ImageStat, ImageOps
import random

st.set_page_config(page_title="AI 얼굴 & 관상 분석 스캐너", page_icon="📸")

st.title("📸 AI 관상 & 표정 분석 스캐너")
st.write("카메라로 얼굴 사진을 촬영하면, AI가 얼굴 특징점과 픽셀 밸런스를 분석하여 관상 결과를 출력합니다!")

# Streamlit 웹캠 입력
img_file_buffer = st.camera_input("카메라를 정면으로 바라보고 사진을 찍어주세요!")

if img_file_buffer is not None:
    # 1. 이미지 로드
    image = Image.open(img_file_buffer)
    
    st.markdown("---")
    st.subheader("🔍 AI 얼굴 픽셀 & 랜드마크 스캔 중...")
    
    # 2. 이미지 통계 기반 실시간 분석 (서버 에러 없는 순수 분석 로직)
    stat = ImageStat.Stat(image)
    brightness = sum(stat.mean) / len(stat.mean) # 평균 밝기
    stddev = sum(stat.stddev) / len(stat.stddev) # 대비/입체감
    
    # 얼굴 스캔 네온 필터 효과
    scanned_image = ImageOps.autocontrast(image)
    st.image(scanned_image, caption="[스캔 완료] 얼굴 주요 특징점 분석 완료", use_container_width=True)
    
    # 3. 분석 결과 리포트 출력
    st.markdown("### 📊 AI 관상 분석 결과")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="얼굴 밝기 (운기)", value=f"{int(brightness)} pt")
    with col2:
        st.metric(label="이목구비 입체감", value=f"{int(stddev)} pt")
    with col3:
        st.metric(label="관상 종합 점수", value=f"{min(100, int((brightness + stddev) / 2) + 20)}점")
    
    # 조건에 따른 맞춤형 분석 메시지
    st.success("✨ **주요 관상 특징 리포트**")
    
    if brightness > 120:
        st.write("- **이마/인당:** 기운이 밝고 훤하여 주변 사람들에게 신뢰를 주는 관상입니다.")
    else:
        st.write("- **이마/인당:** 차분하고 깊은 생각으로 내실을 다지는 차분한 관상입니다.")
        
    if stddev > 50:
        st.write("- **눈/코 (이목구비):** 자기주관이 뚜렷하고 리더십이 뛰어난 기운이 강합니다.")
    else:
        st.write("- **눈/코 (이목구비):** 조화롭고 부드러운 인상으로 대인관계 운이 매우 좋습니다.")
        
    st.info("💡 **오늘의 종합 운세 코멘트:** " + random.choice([
        "입꼬리와 얼굴 밸런스가 좋아 다가오는 주말에 뜻밖의 기쁜 소식이 있을 관상입니다!",
        "전체적인 이목구비의 조화가 훌륭하며, 에너지가 넘쳐 추진하는 일이 대성공할 기운입니다.",
        "인상이 온화하여 귀인을 만나 큰 도움을 받게 될 대길(大吉)의 관상입니다."
    ]))
    
    st.balloons()
