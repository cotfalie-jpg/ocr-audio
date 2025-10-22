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

# Configuración de la página
st.set_page_config(
    page_title="OCR Translator Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2E7D32, #4CAF50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.4rem;
        color: #388E3C;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .section-header {
        font-size: 1.2rem;
        color: #43A047;
        margin: 1.5rem 0 0.5rem 0;
        font-weight: 600;
        border-left: 4px solid #4CAF50;
        padding-left: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #E8F5E9;
    }
    .stRadio > div {
        flex-direction: row;
        align-items: center;
    }
    .stRadio > label {
        font-weight: 500;
        color: #2E7D32;
    }
    .result-box {
        background-color: #E8F5E9;
        border-radius: 12px;
        padding: 1.5rem;
        border-left: 5px solid #4CAF50;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .camera-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
        border: 2px solid #4CAF50;
    }
    .upload-container {
        border: 2px dashed #4CAF50;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        background-color: #F1F8E9;
        margin: 1rem 0;
    }
    .divider {
        border-top: 2px solid #C8E6C9;
        margin: 1.5rem 0;
    }
    .success-box {
        background-color: #C8E6C9;
        color: #2E7D32;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FFF9C4;
        color: #F57F17;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 25px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #388E3C;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .language-box {
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #A5D6A7;
    }
</style>
""", unsafe_allow_html=True)

text = ""

def text_to_speech(input_language, output_language, text, tld):
    if not text.strip():
        return "no_text", "No hay texto para convertir"
    
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20].replace(" ", "_")
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

# Inicialización
remove_files(7)
translator = Translator()

# Header principal
st.markdown('<h1 class="main-header">🔍 OCR Translator Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem; margin-bottom: 2rem;">Extrae texto de imágenes y conviértelo a audio en múltiples idiomas</p>', unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="sub-header">📷 Fuente de Imagen</h2>', unsafe_allow_html=True)
    
    # Selección de fuente
    cam_ = st.radio(
        "Selecciona la fuente de la imagen:",
        ["📁 Cargar archivo", "📷 Usar cámara"],
        horizontal=True
    )
    
    if cam_ == "📷 Usar cámara":
        st.markdown('<div class="camera-container">', unsafe_allow_html=True)
        img_file_buffer = st.camera_input("Toma una foto del texto")
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("⚙️ Configuración de cámara"):
            filtro = st.radio("Aplicar filtro de inversión:", ['Sí', 'No'], horizontal=True)
    else:
        img_file_buffer = None
        st.markdown('<div class="upload-container">', unsafe_allow_html=True)
        bg_image = st.file_uploader("📤 Arrastra o selecciona una imagen", type=["png", "jpg", "jpeg"])
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<h2 class="sub-header">🎯 Configuración</h2>', unsafe_allow_html=True)
    
    # Procesamiento de imagen de cámara
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        
        if filtro == 'Sí':
            cv2_img = cv2.bitwise_not(cv2_img)
            
        img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)
    
    # Procesamiento de imagen cargada
    if 'bg_image' in locals() and bg_image is not None:
        st.image(bg_image, caption='Imagen cargada', use_column_width=True)
        with open(bg_image.name, 'wb') as f:
            f.write(bg_image.read())
        
        img_cv = cv2.imread(bg_image.name)
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb)
        st.markdown(f'<div class="success-box">✅ Imagen procesada: {bg_image.name}</div>', unsafe_allow_html=True)

# Mostrar texto detectado
if text.strip():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">📄 Texto Detectado</h2>', unsafe_allow_html=True)
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.text_area("Texto extraído:", text, height=150, key="texto_detectado")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="warning-box">⚠️ No se ha detectado texto aún. Toma una foto o carga una imagen con texto.</div>', unsafe_allow_html=True)

# Sidebar para traducción y audio
with st.sidebar:
    st.markdown('<h2 class="sub-header">🌍 Configuración de Traducción</h2>', unsafe_allow_html=True)
    
    try:
        os.mkdir("temp")
    except:
        pass
    
    # Selección de idiomas
    st.markdown('<div class="section-header">Idiomas</div>', unsafe_allow_html=True)
    
    col_lang1, col_lang2 = st.columns(2)
    
    with col_lang1:
        st.markdown('<div class="language-box">', unsafe_allow_html=True)
        in_lang = st.selectbox(
            "Idioma de entrada",
            ("Ingles", "Español", "Bengali", "Coreano", "Mandarin", "Japones"),
            key="input_lang"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_lang2:
        st.markdown('<div class="language-box">', unsafe_allow_html=True)
        out_lang = st.selectbox(
            "Idioma de salida",
            ("Ingles", "Español", "Bengali", "Coreano", "Mandarin", "Japones"),
            key="output_lang"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Mapeo de idiomas
    language_map = {
        "Ingles": "en", "Español": "es", "Bengali": "bn",
        "Coreano": "ko", "Mandarin": "zh-cn", "Japones": "ja"
    }
    
    input_language = language_map.get(in_lang, "en")
    output_language = language_map.get(out_lang, "es")
    
    # Configuración de acento
    st.markdown('<div class="section-header">Configuración de Voz</div>', unsafe_allow_html=True)
    english_accent = st.selectbox(
        "Acento para inglés:",
        ("Default", "India", "United Kingdom", "United States", "Canada", "Australia"),
        key="accent"
    )
    
    accent_map = {
        "Default": "com", "India": "co.in", "United Kingdom": "co.uk",
        "United States": "com", "Canada": "ca", "Australia": "com.au"
    }
    tld = accent_map.get(english_accent, "com")
    
    # Opciones adicionales
    st.markdown('<div class="section-header">Opciones</div>', unsafe_allow_html=True)
    display_output_text = st.checkbox("Mostrar texto traducido", value=True)
    
    # Botón de conversión
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if st.button("🎵 Convertir a Audio", use_container_width=True):
        if text.strip():
            with st.spinner('🔄 Traduciendo y generando audio...'):
                result, output_text = text_to_speech(input_language, output_language, text, tld)
                
                if result != "no_text":
                    audio_file = open(f"temp/{result}.mp3", "rb")
                    audio_bytes = audio_file.read()
                    
                    st.markdown("## 🎧 Audio Generado")
                    st.audio(audio_bytes, format="audio/mp3", start_time=0)
                    
                    if display_output_text:
                        st.markdown("## 📝 Texto Traducido")
                        st.markdown(f'<div class="result-box">{output_text}</div>', unsafe_allow_html=True)
                else:
                    st.error("No hay texto para convertir")
        else:
            st.error("Por favor, primero captura o carga una imagen con texto")

# Información de la aplicación
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem; background-color: #F1F8E9; border-radius: 10px;'>
        <strong>OCR Translator Pro</strong> | Extrae texto de imágenes y conviértelo a audio en diferentes idiomas<br>
        Tecnologías: Streamlit • OpenCV • Tesseract OCR • gTTS
    </div>
    """, 
    unsafe_allow_html=True
)
