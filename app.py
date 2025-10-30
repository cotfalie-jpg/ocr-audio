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

# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(
    page_title="Baby Story Reader BAE",
    page_icon="🧸",
    layout="centered",
)

# ==============================
# ESTILO BAE — Rosa Suave & Moderno
# ==============================
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        text-align: center;
        background: linear-gradient(135deg, #F48FB1, #F06292);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #9C27B0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .stButton>button {
        background: linear-gradient(135deg, #F48FB1, #EC407A);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #F06292, #E91E63);
    }
    .text-box {
        background-color: #FFF0F5;
        border: 2px solid #F8BBD0;
        border-radius: 12px;
        padding: 1rem;
        color: #6A1B9A;
        font-size: 1rem;
        font-weight: 500;
    }
    .audio-box {
        background: #FCE4EC;
        border: 2px solid #F48FB1;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        color: #AD1457;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# FUNCIÓN AUXILIAR
# ==============================
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

try:
    os.mkdir("temp")
except:
    pass

remove_files(7)

# ==============================
# CABECERA
# ==============================
st.markdown('<div class="main-title">🧸 Baby Story Reader</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Convierte textos en dulces cuentos narrados para tu bebé 💕</div>', unsafe_allow_html=True)

# ==============================
# FUENTE DE IMAGEN
# ==============================
st.markdown("### 📸 Captura o carga una imagen con texto")
source = st.radio("Selecciona una fuente:", ["Usar cámara", "Cargar imagen"], horizontal=True)

img_data = None
if source == "Usar cámara":
    img_file = st.camera_input("Toma una foto del texto")
    if img_file:
        img_data = np.frombuffer(img_file.getvalue(), np.uint8)
else:
    img_file = st.file_uploader("Carga una imagen (png, jpg, jpeg)", type=["png", "jpg", "jpeg"])
    if img_file:
        img_data = np.frombuffer(img_file.read(), np.uint8)

# ==============================
# DETECCIÓN DE TEXTO
# ==============================
text = ""
if img_data is not None:
    img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    if text.strip():
        st.markdown("### 📝 Texto Detectado")
        st.markdown(f'<div class="text-box">{text}</div>', unsafe_allow_html=True)
    else:
        st.warning("No se detectó texto, intenta con otra imagen.")

# ==============================
# OPCIONES DE VOZ Y TRADUCCIÓN
# ==============================
if text.strip():
    st.markdown("### 🌍 Selecciona idioma y estilo de voz")
    col1, col2 = st.columns(2)

    with col1:
        out_lang = st.selectbox(
            "Idioma para el cuento:",
            ("Español", "Inglés", "Francés", "Portugués", "Italiano"),
        )

    with col2:
        estilo = st.selectbox(
            "Estilo del cuento:",
            ("Tierno y calmado 🧸", "Aventurero 🚀", "Para dormir 🌙"),
        )

    # Diccionario de idiomas
    lang_map = {
        "Español": "es",
        "Inglés": "en",
        "Francés": "fr",
        "Portugués": "pt",
        "Italiano": "it"
    }
    lg = lang_map[out_lang]

    # Botón principal
    if st.button("🎧 Convertir en Cuento"):
        with st.spinner("Generando el cuento y la voz mágica... ✨"):
            # Traducción del texto
            try:
                story_text = GoogleTranslator(source="auto", target=lg).translate(text)
            except Exception as e:
                st.error(f"Error al traducir: {e}")
                story_text = text

            # Personalizar estilo
            if estilo == "Tierno y calmado 🧸":
                story_text = f"💤 Había una vez un pequeño osito que aprendía palabras nuevas. {story_text} 🌼"
            elif estilo == "Aventurero 🚀":
                story_text = f"🚀 En un bosque lleno de estrellas, comenzó una gran aventura: {story_text}"
            else:
                story_text = f"🌙 En un mundo de sueños suaves, este cuento te arrullará: {story_text}"

            # Generar voz
            tts = gTTS(story_text, lang=lg)
            filename = "temp/baby_story.mp3"
            tts.save(filename)

            # Mostrar resultado
            st.markdown("### 🎵 Audio del Cuento")
            audio_file = open(filename, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.markdown(f'<div class="audio-box">{story_text}</div>', unsafe_allow_html=True)
else:
    st.info("💡 Captura o sube una imagen con texto para crear un cuento de bebé.")

