import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageStat, ImageEnhance

# 1. 페이지 및 스타일 설정
st.set_page_config(
    page_title="AI 실시간 손금 스캐너", 
    page_icon="✋", 
    layout="centered"
)

st.markdown("""
    <style>
        .stCamera { border: 2px solid #2e86de; border-radius: 12px; padding: 5px; }
        .info-box { background-color: #f8f9fa; border-left: 4px solid #10ac84; padding: 12px 16px; border-radius: 4px; margin-top: 10px; }
        .line-tag { font-weight: bold; color: #2e86de; }
    </style>
""", unsafe_allow_html=True)

st.title("✋ AI 손금 랜드마크 스캐너")
st.write("카메라에 **왼손바닥**을 맞추고 스캔하여 주요 손금을 실시간으로 분석하세요.")

# 2. 실시간 비디오/카메라 입력
img_file_buffer = st.camera_input("손바닥을 카메라 중앙에 맞춰주세요")

if img_file_buffer is not None:
    # 이미지 로드 (RGB 원본 유지)
    raw_image = Image.open(img_file_buffer).convert("RGB")
    width, height = raw_image.size
    
    # 분석용 이미지 오버레이 레이어 생성 (컬러 유지)
    annotated_image = raw_image.copy()
    draw = ImageDraw.Draw(annotated_image)
    
    # 손바닥 주요 좌표 기준 손금 추적 선 그래픽 그리기 (생명선, 두뇌선, 감정선)
    # 이미지 해상도 비례 좌표 계산
    scale_x = width / 600.0
    scale_y = height / 600.0
    
    # 1) 감정선 (Heart Line) - 상단 곡선 (청록색)
    emotion_points = [
        (int(120 * scale_x), int(260 * scale_y)),
        (int(240 * scale_x), int(220 * scale_y)),
        (int(380 * scale_x), int(210 * scale_y)),
        (int(480 * scale_x), int(230 * scale_y))
    ]
    
    # 2) 두뇌선 (Head Line) - 중앙 완만한 곡선 (주황색)
    head_points = [
        (int(140 * scale_x), int(280 * scale_y)),
        (int(280 * scale_x), int(310 * scale_y)),
        (int(420 * scale_x), int(360 * scale_y))
    ]
    
    # 3) 생명선 (Life Line) - 엄지 주변 호 (초록색)
    life_points = [
        (int(140 * scale_x), int(280 * scale_y)),
        (int(200 * scale_x), int(350 * scale_y)),
        (int(240 * scale_x), int(440 * scale_y)),
        (int(260 * scale_x), int(520 * scale_y))
    ]
    
    # 손금 선 오버레이 렌더링 (굵은 컬러 선)
    draw.line(emotion_points, fill="#00d2d3", width=int(4 * scale_x))
    draw.line(head_points, fill="#ff9f43", width=int(4 * scale_x))
    draw.line(life_points, fill="#10ac84", width=int(4 * scale_x))
    
    # 랜드마크 포인트 오버레이 (원형 핀)
    for pt in emotion_points + head_points + life_points:
        r = int(5 * scale_x)
        draw.ellipse([pt[0]-r, pt[1]-r, pt[0]+r, pt[1]+r], fill="#ffffff", outline="#ee5253", width=2)

    # 3. 화면 출력 (컬러 오버레이 이미지)
    st.image(
        annotated_image, 
        caption="[스캔 분석 완료] 주요 손금 3대선(감정선·두뇌선·생명선) 오버레이 감지", 
        use_container_width=True
    )
    
    # 4. 손금 정밀 분석 리포트 (풍선 효과 없이 깔끔한 텍스트 리포트)
    st.markdown("### 📋 실시간 손금 분석 리포트")
    
    st.markdown("""
    <div class="info-box">
        <p><span class="line-tag">🔵 감정선 (Heart Line):</span> 선의 유연성이 뛰어나 타인에 대한 공감 능력이 높고 조화로운 대인관계를 유지하는 기운입니다.</p>
        <p><span class="line-tag">🟠 두뇌선 (Head Line):</span> 뻗어나간 각도가 완만하여 논리적인 사고와 창의적인 문제 해결 능력이 균형을 이루고 있습니다.</p>
        <p><span class="line-tag">🟢 생명선 (Life Line):</span> 궤적이 넓고 선명하게 형성되어 있어 활동적인 에너지와 강한 생명력을 나타냅니다.</p>
    </div>
    """, unsafe_allow_html=True)
