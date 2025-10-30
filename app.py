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

# --- Configuración de página ---
st.set_page_config(
    page_title="BAE OCR Audio 🍼",
    page_icon="🧸",
    layout="wide"
)

# --- Estilo BAE pastel ---
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #FFF9EC, #FFFDF7);
        color: #444;
        font-family: "Poppins", sans-serif;
    }
    .main-header {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        color: #2F3E46;
        margin-top: 1rem;
        background: linear-gradient(90deg, #F4A261, #F6C667);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #52796F;
        margin-bottom: 2rem;
    }
    .baby-box {
        background: #FFF8EB;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 2px solid #F4A261;
    }
    .stButton > button {
        background: linear-gradient(135deg, #F6C667, #F4A261);
        color: #2F3E46;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(246,198,103,0.4);
    }
    .result-box {
        background: #E7F5F2;
        border-left: 6px solid #52796F;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        font-size: 1.05rem;
        color: #2F3E46;
    }
    .divider {
        border-top: 2px dashed #F4A261;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Título y descripción ---
st.markdown('<div class="main-header">BAE OCR Audio 🍼</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Convierte imágenes o textos en audios suaves para tu bebé 💛</div>', unsafe_allow_html=True)

# --- Preparar carpeta temporal ---
os.makedirs("temp", exist_ok=True)

# --- Función para limpiar audios viejos ---
def remove_old_files(days=3):
    now = time.time()
    cutoff = now - days * 86400
    for f in glob.glob("temp/*.mp3"):
        if os.stat(f).st_mtime < cutoff:
            os.remove(f)
remove_old_files()

# --- Función de traducción y audio ---
def translate_and_speak(text, source_lang="es", target_lang="en"):
    if not text.strip():
        return None, None
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        tts = gTTS(translated, lang=target_lang)
        filename = f"temp/audio_{int(time.time())}.mp3"
        tts.save(filename)
        return filename, translated
    except Exception as e:
        st.error(f"Error al traducir o generar audio: {e}")
        return None, None

# --- Layout principal ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📸 Carga o toma una foto")
    source_option = st.radio("Selecciona la fuente de imagen:", ["📁 Subir imagen", "🎥 Cámara"], horizontal=True)
    
    if source_option == "🎥 Cámara":
        img_file_buffer = st.camera_input("Toma una foto del texto")
    else:
        img_file_buffer = st.file_uploader("Carga una imagen", type=["png", "jpg", "jpeg"])

with col2:
    st.markdown("### 🌈 Configuración")
    input_lang = st.selectbox("Idioma del texto detectado:", ["Español", "Inglés"], index=0)
    output_lang = st.selectbox("Idioma para el audio:", ["Español", "Inglés"], index=1)
    langs = {"Español": "es", "Inglés": "en"}
    src = langs[input_lang]
    tgt = langs[output_lang]

# --- Procesamiento OCR ---
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("### ✏️ Texto Detectado")
    st.text_area("Texto encontrado:", text, height=200)

    if st.button("🎧 Generar Audio con Traducción"):
        with st.spinner("Generando audio suave... 💤"):
            audio_path, translated_text = translate_and_speak(text, src, tgt)
            if audio_path:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown("### 🍼 Audio Generado para tu Bebé")
                st.audio(audio_path, format="audio/mp3")
                st.markdown(f'<div class="result-box">🗣️ <strong>Traducción:</strong><br>{translated_text}</div>', unsafe_allow_html=True)
else:
    st.info("👶 Carga una imagen o toma una foto para comenzar.")

# --- Información final ---
st.markdown("""
<div style="text-align:center; margin-top:2rem; color:#52796F;">
Hecho con 💛 por <b>BAE</b> | Audio y lectura asistida para bebés 🌼
</div>
""", unsafe_allow_html=True)

