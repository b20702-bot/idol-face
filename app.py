import cv2
import math
import numpy as np
import streamlit as st
import mediapipe as mp

# ==========================================
# 1. 페이지 설정 및 사이버펑크 Dark CSS 적용
# ==========================================
st.set_page_config(
    page_title="Cyber-Face Matrix",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이버펑크 스타일 Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0d0f18;
        color: #00f3ff;
        font-family: 'Courier New', Courier, monospace;
    }
    h1, h2, h3 {
        color: #ff007f !important;
        text-shadow: 0 0 10px #ff007f, 0 0 20px #ff007f;
    }
    .card {
        background: rgba(16, 18, 27, 0.8);
        border: 1px solid #00f3ff;
        box-shadow: 0 0 15px rgba(0, 243, 255, 0.3);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .synergy-card {
        background: linear-gradient(135deg, rgba(255, 0, 127, 0.15), rgba(0, 243, 255, 0.15));
        border: 2px solid #ff007f;
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.5);
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
    .streamlit-expanderHeader {
        background-color: #1a1c29 !important;
        color: #00f3ff !important;
        border: 1px solid #00f3ff;
    }
    .highlight {
        color: #ffe600;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. 수학적 기하학 함수 (3D Euclidean & Vector)
# ==========================================
def calculate_3d_distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

def calculate_angle_3d(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


# ==========================================
# 3. 메인 파이프라인 및 UI 레이아웃
# ==========================================
st.title("🔮 Cyber-Face Matrix")
st.caption("3D Facial Landmark Geometry & Idol Physiognomy Scanner")

# 학술 보고서 (Scientific Expander)
with st.expander("🔬 [학술 보고서] 3D FaceMesh & 관상 기하학 원리 분석"):
    st.markdown("""
    ### 1. MediaPipe FaceMesh & 3D Coordinate Mapping
    * 본 시스템은 **Google MediaPipe FaceMesh** 모델을 활용하여 얼굴 표면의 **468개 3차원 랜드마크(X, Y, Z)**를 실시간 추적합니다.
    * 양 눈동자 중심간 거리(Landmark #33 ~ #263)를 기준 단위(**Standard Unit**)로 설정하여 모든 유클리디안 스케일을 **정규화(Normalization)**합니다.

    ### 2. ROI(Region of Interest) 파셀레이션 및 매개변수 산출 공식
    * **상안부 (도화궁 - 눈):** $Eye Aspect Ratio = \\frac{d(159, 145)}{d(33, 133)}$
    * **중안부 (재백궁 - 코):** $Nose Ratio = \\frac{d(168, 2)}{d(129, 358)}$
    * **하안부 (관록궁 - 턱관절):** 좌/우 턱관절과 턱 끝(#172, #152, #397) 간 3차원 내각
    """)

st.write("---")

col_cam, col_result = st.columns([1.2, 1])

with col_cam:
    st.subheader("📷 Real-time HUD Scanner")
    img_file_buffer = st.camera_input("카메라 가이드라인 박스 안에 얼굴을 맞춰 스캔하세요.")

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    h, w, c = cv_img.shape
    rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    
    results = face_mesh.process(rgb_img)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        # 1. 상안부 (눈 종횡비)
        eye_height = calculate_3d_distance(landmarks[159], landmarks[145])
        eye_width = calculate_3d_distance(landmarks[33], landmarks[133])
        eye_ratio = eye_height / eye_width if eye_width > 0 else 0

        # 2. 중안부 (코 비율)
        nose_length = calculate_3d_distance(landmarks[168], landmarks[2])
        nose_width = calculate_3d_distance(landmarks[129], landmarks[358])
        nose_ratio = nose_length / nose_width if nose_width > 0 else 0

        # 3. 하안부 (턱관절 각도)
        jaw_angle = calculate_angle_3d(landmarks[172], landmarks[152], landmarks[397])

        # HUD 시각화
        overlay = cv_img.copy()
        box_margin_w, box_margin_h = int(w * 0.2), int(h * 0.1)
        cv2.rectangle(overlay, (box_margin_w, box_margin_h), (w - box_margin_w, h - box_margin_h), (255, 243, 0), 2)
        
        target_pts = [33, 133, 159, 145, 168, 2, 129, 358, 172, 152, 397]
        for pt_idx in target_pts:
            px, py = int(landmarks[pt_idx].x * w), int(landmarks[pt_idx].y * h)
            cv2.circle(overlay, (px, py), 3, (255, 0, 127), -1)

        cv2.addWeighted(overlay, 0.7, cv_img, 0.3, 0, cv_img)

        with col_cam:
            st.image(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB), use_container_width=True, caption="Matrix Tracking Overlay")

        # 판정 로직
        if eye_ratio >= 0.28:
            eye_idol, eye_desc = "장원영", "대중의 사랑을 한 몸에 받는 치명적인 도화 매력과 독보적 스타성(인기운)"
        elif 0.23 <= eye_ratio < 0.28:
            eye_idol, eye_desc = "안유진", "당차고 열정적인 눈빛, 팀을 이끄는 리더십과 거침없는 성공운"
        else:
            eye_idol, eye_desc = "해린 (뉴진스)", "고양이 같은 신비로운 눈매, 예리한 관찰력과 트렌드를 이끄는 감각운"

        if nose_ratio >= 1.3:
            nose_idol, nose_desc = "카리나", "세련되고 곧게 뻗은 코, 자산을 단단하게 지켜내고 증식시키는 황금 재백운"
        elif 1.1 <= nose_ratio < 1.3:
            nose_idol, nose_desc = "윈터", "오똑하고 깔끔한 비율, 주변에 귀인이 끊이지 않고 명예가 따르는 귀인운"
        else:
            nose_idol, nose_desc = "수지", "원만하고 도톰한 코, 사람들의 호감을 사고 안정을 유지하는 대중 호감운"

        if jaw_angle < 85:
            jaw_idol, jaw_desc = "카리나", "단호하고 샤프한 V라인, 난관을 뚫고 목표를 달성하는 강력한 결단력/사업운"
        elif 85 <= jaw_angle < 100:
            jaw_idol, jaw_desc = "윈터", "유연하고 부드러운 턱선, 원만한 대인관계와 말년이 평탄한 안성맞춤 안정운"
        else:
            jaw_idol, jaw_desc = "안유진", "묵직하고 건강한 하관, 어떠한 시련에도 굴하지 않는 강인한 끈기와 추진운"

        with col_result:
            st.subheader("📊 부위별 관상 분석 리포트")

            st.markdown(f"""
            <div class="card">
                <h4>👁️ 상안부 (도화궁): <span class="highlight">{eye_idol}</span></h4>
                <p><b>측정 눈 종횡비:</b> {eye_ratio:.3f}</p>
                <p><b>관상 운세:</b> {eye_desc}</p>
            </div>
            <div class="card">
                <h4>👃 중안부 (재백궁): <span class="highlight">{nose_idol}</span></h4>
                <p><b>측정 코 비율:</b> {nose_ratio:.3f}</p>
                <p><b>관상 운세:</b> {nose_desc}</p>
            </div>
            <div class="card">
                <h4>🗣️ 하안부 (관록궁): <span class="highlight">{jaw_idol}</span></h4>
                <p><b>측정 턱관절 각도:</b> {jaw_angle:.1f}°</p>
                <p><b>관상 운세:</b> {jaw_desc}</p>
            </div>
            <div class="synergy-card">
                <h3>⚡ 최종 시너지 콤보 카드</h3>
                <h4 style="color: #00f3ff;">[{eye_idol}의 눈] + [{nose_idol}의 코] + [{jaw_idol}의 하관]</h4>
                <hr style="border-color: #ff007f;">
                <p>✨ <b>Cyber-Matrix 총평:</b> {eye_idol}의 스타성, {nose_idol}의 단단한 운세, {jaw_idol}의 에너지 조합을 모두 갖춘 최상위 아우라입니다!</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        with col_result:
            st.warning("⚠️ 얼굴을 인식하지 못했습니다. 카메라 중앙에 얼굴이 오도록 조정해 주세요.")
else:
    with col_result:
        st.info("👈 왼쪽 웹캠 스캐너의 카메라 권한을 승인하고 사진을 촬영하면 AI 관상 분석이 시작됩니다.")