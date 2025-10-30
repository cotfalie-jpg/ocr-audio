import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from deep_translator import GoogleTranslator
import streamlit as st

# ============================
# 🌸 CONFIGURACIÓN DE LA APP
# ============================
st.set_page_config(
    page_title="Lectura Mágica para Bebés",
    page_icon="🧸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# 🌈 ESTILO VISUAL “BAE”
# ============================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #FFF6FB 0%, #FDE2FF 40%, #F8E6FF 100%);
        font-family: 'Poppins', sans-serif;
        color: #5E3B76;
    }

    h1, h2, h3, h4 {
        color: #B0578D;
        text-align: center;
        font-weight: 700;
    }

    .main-header {
        font-size: 3rem;
        background: linear-gradient(90deg, #D988B9, #B0578D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .sub {
        text-align: center;
        font-size: 1.2rem;
        color: #865D92;
        margin-bottom: 2rem;
    }

    .upload-box {
        background: #FFFFFF90;
        border: 3px dashed #D988B9;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 20px rgba(176, 87, 141, 0.1);
    }

    .result-box {
        background: rgba(255,255,255,0.7);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1.5rem;
        border: 2px solid #F5C6EC;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05);
    }

    .stButton>button {
        background: linear-gradient(135deg, #B0578D, #D988B9);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        background: linear-gradient(135deg, #D988B9, #B0578D);
    }

    .audio-box {
        text-align: center;
        background: #FFF4F9;
        border-radius: 20px;
        padding: 1rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================
# 🧸 CABECERA
# ============================
st.markdown('<h1 class="main-header">Lectura Mágica para Bebés</h1>', unsafe_allow_html=True)
st.markdown('<div class="sub">Sube o captura una palabra y escucha una dulce historia narrada 💤</div>', unsafe_allow_html=True)

# ============================
# 📸 CARGA DE IMAGEN
# ============================
col1, col2 = st.columns([2, 1])
text = ""

with col1:
    st.markdown('<div class="upload-box">📷 <br><strong>Sube una imagen o usa la cámara</strong></div>', unsafe_allow_html=True)
    cam_option = st.radio("Selecciona la fuente", ["📸 Cámara", "📂 Subir imagen"], horizontal=True)

    if cam_option == "📸 Cámara":
        img_file_buffer = st.camera_input("Toma una foto del texto o dibujo del bebé")
        filtro = st.radio("¿Aplicar filtro para mejorar lectura?", ["Sí", "No"], horizontal=True)
    else:
        img_file_buffer = None
        uploaded_file = st.file_uploader("Sube una imagen (JPG, PNG)", type=["jpg", "jpeg", "png"])
        filtro = "No"

# ============================
# 🧠 PROCESAMIENTO OCR
# ============================
with col2:
    if cam_option == "📸 Cámara" and img_file_buffer:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        if filtro == "Sí":
            cv2_img = cv2.bitwise_not(cv2_img)
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)

    elif cam_option == "📂 Subir imagen" and uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_container_width=True)
        cv2_img = np.array(image)
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)

# ============================
# 💬 TRADUCCIÓN Y AUDIO
# ============================
if text.strip():
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("✨ Palabra Detectada")
    st.write(f"**{text.strip()}**")

    # Traducir texto
    translated = GoogleTranslator(source='auto', target='es').translate(text)
    story_prompt = f"Cuenta una historia breve y tierna para bebés inspirada en la palabra: {translated}"
    
    st.subheader("🧚 Historia mágica")
    story = f"Había una vez un pequeño {translated} que vivía en un bosque lleno de colores. Cada mañana saludaba al sol y jugaba con las mariposas hasta quedarse dormido bajo un arcoíris. 🌈✨"
    st.write(story)

    # Generar audio
    tts = gTTS(story, lang='es')
    os.makedirs("temp", exist_ok=True)
    audio_path = "temp/story.mp3"
    tts.save(audio_path)

    # Mostrar audio
    st.markdown('<div class="audio-box">', unsafe_allow_html=True)
    st.audio(audio_path, format="audio/mp3")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("💡 Toma una foto o sube una imagen para comenzar la historia mágica 🎨")

# ============================
# 🧼 LIMPIAR ARCHIVOS VIEJOS
# ============================
def remove_old_audios(days=3):
    now = time.time()
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < now - days * 86400:
            os.remove(f)

remove_old_audios()


