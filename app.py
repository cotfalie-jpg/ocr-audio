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

# -------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------------
st.set_page_config(
    page_title="BAE | Cuento Dulce para Bebés",
    page_icon="🧸",
    layout="centered"
)

# -------------------------------------------------------
# 🌼 ESTILO VISUAL BAE PASTEL
# -------------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #FFF7C2 0%, #FFD6A5 40%, #BDE0FE 100%);
        font-family: 'Poppins', sans-serif;
        color: #4B4B4B;
    }

    h1, h2, h3 {
        color: #7FB77E;
        font-weight: 700;
    }

    /* Título principal */
    .main-title {
        font-size: 2.8rem;
        text-align: center;
        background: linear-gradient(90deg, #7FB77E, #FFD6A5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #4B4B4B;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Caja principal */
    .upload-box {
        background-color: #fffef7dd;
        border: 3px dashed #FFD6A5;
        border-radius: 25px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(255, 214, 165, 0.3);
    }

    .result-box {
        background-color: #fffef8;
        border: 2px solid #BDE0FE;
        border-radius: 25px;
        padding: 1.8rem;
        margin-top: 2rem;
        box-shadow: 0 8px 20px rgba(189, 224, 254, 0.2);
    }

    /* Botones */
    .stButton>button {
        background: linear-gradient(135deg, #FFD6A5, #7FB77E);
        color: white;
        border: none;
        border-radius: 18px;
        padding: 0.9rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #7FB77E, #FFD6A5);
        transform: scale(1.02);
    }

    /* Caja de audio */
    .audio-box {
        background-color: #FFF7C2;
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
        margin-top: 1rem;
        border: 1px solid #FFD6A5;
    }

    /* Texto informativo */
    .info-text {
        text-align: center;
        color: #4B4B4B;
        font-size: 1rem;
        margin-top: 1rem;
    }

    textarea, input {
        border-radius: 12px !important;
        border: 1px solid #FFD6A580 !important;
        background-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# CABECERA
# -------------------------------------------------------
st.markdown('<div class="main-title">🧸 BAE - Cuento Dulce para Bebés</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Convierte una palabra o dibujo en un cuento narrado con ternura 💛</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# SECCIÓN DE IMAGEN
# -------------------------------------------------------
col1, col2 = st.columns([2, 1])
text = ""

with col1:
    st.markdown('<div class="upload-box">📸 <br><strong>Sube una imagen o toma una foto</strong></div>', unsafe_allow_html=True)
    cam_option = st.radio("Fuente de imagen", ["Usar cámara", "Subir archivo"], horizontal=True)

    if cam_option == "Usar cámara":
        img_file_buffer = st.camera_input("Toma una foto (de una palabra o dibujo del bebé)")
        filtro = st.radio("¿Aplicar filtro para mejorar lectura?", ["Sí", "No"], horizontal=True)
    else:
        img_file_buffer = None
        uploaded_file = st.file_uploader("Sube una imagen (JPG, PNG)", type=["jpg", "jpeg", "png"])
        filtro = "No"

# -------------------------------------------------------
# PROCESAMIENTO OCR
# -------------------------------------------------------
with col2:
    if cam_option == "Usar cámara" and img_file_buffer:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        if filtro == "Sí":
            cv2_img = cv2.bitwise_not(cv2_img)
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)

    elif cam_option == "Subir archivo" and uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_container_width=True)
        cv2_img = np.array(image)
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)

# -------------------------------------------------------
# GENERAR HISTORIA
# -------------------------------------------------------
if text.strip():
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("🌼 Palabra Detectada")
    palabra = text.strip().split()[0]
    st.write(f"**{palabra}**")

    traducida = GoogleTranslator(source='auto', target='es').translate(palabra)

    # Historia bebé estilo BAE
    historia = f"""
    Había una vez un pequeño {traducida} que vivía en un mundo lleno de colores suaves.
    Le encantaba despertar con el canto de los pajaritos y jugar entre las nubes de algodón.
    Cuando el sol se dormía, se acurrucaba bajo una manta amarillita y soñaba con risas, abrazos y melodías dulces. 🌙💤
    """

    st.subheader("🧚 Cuento para el Bebé")
    st.write(historia)

    # Generar audio
    os.makedirs("temp", exist_ok=True)
    tts = gTTS(historia, lang='es')
    audio_path = "temp/cuento.mp3"
    tts.save(audio_path)

    st.markdown('<div class="audio-box">', unsafe_allow_html=True)
    st.audio(audio_path, format="audio/mp3")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("💡 Sube o toma una imagen con una palabra para generar un cuento dulce 🌈")

# -------------------------------------------------------
# LIMPIAR ARCHIVOS ANTIGUOS
# -------------------------------------------------------
def remove_old(days=2):
    now = time.time()
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < now - days * 86400:
            os.remove(f)

remove_old()

