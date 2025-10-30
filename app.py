import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="BAE Aprendizaje Visual",
    page_icon="🧸",
    layout="wide"
)

# =========================
# ESTILO BAE
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #FFF8EA;
    color: #3C3C3C;
    font-family: 'Poppins', sans-serif;
}
.main-title {
    font-size: 2.8rem;
    color: #DD8E6B;
    text-align: center;
    font-weight: 700;
    margin-bottom: 0.3rem;
}
.subtitle {
    font-size: 1.2rem;
    color: #4D797A;
    text-align: center;
    margin-bottom: 2rem;
}
.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #DD8E6B;
    border-left: 5px solid #F0D192;
    padding-left: 10px;
    margin-top: 1.5rem;
}
.info-box {
    background: #FFF;
    border-radius: 16px;
    border: 1px solid #F0D192;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    margin-top: 1rem;
}
.success-box {
    background: #FFF9E6;
    border-radius: 12px;
    padding: 1rem;
    color: #4D797A;
    border-left: 6px solid #DD8E6B;
    margin: 1rem 0;
}
.stButton>button {
    background: linear-gradient(135deg, #F9E79F, #F5CBA7);
    border: none;
    color: #3C3C3C;
    font-weight: 600;
    border-radius: 12px;
    padding: 0.8rem 2rem;
    width: 100%;
    box-shadow: 0 6px 15px rgba(221,142,107,0.25);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #F5CBA7, #FAD7A0);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(221,142,107,0.35);
}
</style>
""", unsafe_allow_html=True)

# =========================
# FUNCIONES
# =========================
def text_to_speech(input_language, output_language, text, tld):
    if not text.strip():
        return "no_text", "No hay texto para convertir"

    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    my_file_name = text[:20].replace(" ", "_") or "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    now = time.time()
    n_days = n * 86400
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)

try:
    os.mkdir("temp")
except:
    pass

translator = Translator()
remove_files(7)

# =========================
# ENCABEZADO
# =========================
st.markdown('<div class="main-title">🧸 BAE Aprendizaje Visual</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Convierte objetos y textos en cuentos hablados para bebés 💛</div>', unsafe_allow_html=True)

# =========================
# INTERFAZ
# =========================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-title">📸 Fuente de Imagen</div>', unsafe_allow_html=True)
    fuente = st.radio("Selecciona cómo obtener la imagen:", ["Usar cámara", "Cargar archivo"], horizontal=True)

    text = ""

    if fuente == "Usar cámara":
        st.markdown('<div class="info-box">Toma una foto de un libro, juguete o palabra para que BAE la lea en voz alta.</div>', unsafe_allow_html=True)
        img_file_buffer = st.camera_input("Captura una imagen")
        filtro = st.radio("¿Aplicar filtro para texto claro?", ['Sí', 'No'], horizontal=True)

        if img_file_buffer:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            if filtro == 'Sí':
                cv2_img = cv2.bitwise_not(cv2_img)
            img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(img_rgb)
    else:
        bg_image = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg"])
        if bg_image:
            st.image(bg_image, caption="Imagen cargada", use_container_width=True)
            img_cv = cv2.imdecode(np.frombuffer(bg_image.read(), np.uint8), cv2.IMREAD_COLOR)
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            text = pytesseract.image_to_string(img_rgb)

with col2:
    st.markdown('<div class="section-title">🎧 Voz y Traducción</div>', unsafe_allow_html=True)
    
    in_lang = st.selectbox("Idioma del texto detectado", ("Español", "Inglés", "Francés", "Japonés"))
    out_lang = st.selectbox("Idioma para lectura", ("Español", "Inglés", "Francés", "Japonés"))
    
    language_map = {"Español": "es", "Inglés": "en", "Francés": "fr", "Japonés": "ja"}
    input_language = language_map[in_lang]
    output_language = language_map[out_lang]
    
    st.markdown('<div class="section-title">🗣️ Acento</div>', unsafe_allow_html=True)
    accent = st.selectbox("Acento para inglés", ("Default", "India", "Reino Unido", "Estados Unidos", "Australia"))
    accent_map = {"Default": "com", "India": "co.in", "Reino Unido": "co.uk", "Estados Unidos": "com", "Australia": "com.au"}
    tld = accent_map[accent]

# =========================
# RESULTADOS
# =========================
if text.strip():
    st.markdown('<div class="section-title">📖 Texto Detectado</div>', unsafe_allow_html=True)
    st.text_area("Texto extraído:", text, height=200)

    if st.button("✨ Leer en voz alta"):
        with st.spinner("Generando lectura..."):
            result, output_text = text_to_speech(input_language, output_language, text, tld)
            if result != "no_text":
                audio_file = open(f"temp/{result}.mp3", "rb")
                audio_bytes = audio_file.read()
                st.markdown('<div class="success-box">¡Texto leído con voz suave! 💛</div>', unsafe_allow_html=True)
                st.audio(audio_bytes, format="audio/mp3")
                st.markdown('<div class="section-title">🧠 Texto traducido</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="info-box">{output_text}</div>', unsafe_allow_html=True)
            else:
                st.warning("No se detectó texto para convertir")
else:
    st.info("📷 Toma una foto o carga una imagen para empezar")

# =========================
# PIE DE PÁGINA
# =========================
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #4D797A; padding: 1rem;'>
        🌼 <strong>BAE Aprendizaje Visual</strong> — IA que estimula el lenguaje y la curiosidad en los primeros años 💛
    </div>
    """,
    unsafe_allow_html=True
)
