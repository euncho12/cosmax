import base64
import io
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

# ------------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------------
st.set_page_config(
    page_title="실험 잘 되어가나요?",
    page_icon="🧪",
    layout="wide",
)

# Streamlit 기본 여백/헤더를 없애서 index.html이 전체 화면을 쓰도록 함
st.markdown(
    """
    <style>
        .block-container {padding: 0 !important; max-width: 100% !important;}
        header[data-testid="stHeader"] {display: none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

BASE_DIR = Path(__file__).parent
HTML_PATH = BASE_DIR / "index.html"
# 히어로 배경으로 쓸 고화질 와이드 이미지
IMAGE_PATH = BASE_DIR / "분자사진고화질.png"
JPEG_QUALITY = 85  # 화질 손실을 최소화하면서 용량을 줄이기 위한 값


@st.cache_data(show_spinner=False)
def load_html() -> str:
    html = HTML_PATH.read_text(encoding="utf-8")

    # index.html은 배경 이미지를 상대경로(분자사진2.jpg)로 참조합니다.
    # Streamlit은 components.html을 iframe(srcdoc)으로 렌더링하기 때문에
    # 상대경로 파일을 불러올 수 없어, 이미지를 base64로 인코딩해
    # HTML 안에 직접 삽입(data URI)해줍니다.
    #
    # 원본 PNG(약 1.7MB)를 그대로 넣으면 페이지가 무거워지므로,
    # 화질 저하가 거의 없는 수준(quality=85)의 JPEG로 변환해 용량을 줄입니다.
    if IMAGE_PATH.exists():
        img = Image.open(IMAGE_PATH).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=JPEG_QUALITY, optimize=True)
        img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{img_b64}"
        html = html.replace('url("분자사진2.jpg")', f'url("{data_uri}")')

    return html


html_content = load_html()

# 원본 페이지 길이가 길어질 수 있으므로 넉넉하게 높이를 잡고 스크롤 허용
components.html(html_content, height=2400, scrolling=True)
