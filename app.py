import streamlit as st
from openai import OpenAI

# ==============================
# CONFIGURACIÓN DE PÁGINA
# ==============================
st.set_page_config(
    page_title="Cuentos BAE",
    page_icon="🍼",
    layout="centered"
)

# ==============================
# ESTILO VISUAL BAE (pastel)
# ==============================
st.markdown("""
<style>
    body, .stApp {
        background-color: #FFF8EA;
        color: #403D39;
        font-family: 'Poppins', sans-serif;
    }

    .main-title {
        font-size: 2.8rem;
        text-align: center;
        font-weight: 800;
        color: #403D39;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #7E746C;
        margin-bottom: 2rem;
    }

    /* Caja principal */
    .main-box {
        background-color: #FFFDF5;
        border-radius: 20px;
        border: 2px solid #DD8E6B;
        padding: 2rem;
        box-shadow: 0 8px 25px rgba(221,142,107,0.1);
    }

    /* Botones estilo pastel */
    .stButton > button {
        background-color: #DD8E6B;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(221,142,107,0.2);
        width: 100%;
    }

    .stButton > button:hover {
        background-color: #C67856;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(221,142,107,0.3);
    }

    /* Caja de resultado */
    .story-box {
        background-color: #FFF2C3;
        border: 2px solid #DD8E6B;
        border-radius: 16px;
        padding: 1.5rem;
        color: #403D39;
        margin-top: 2rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    }

    /* Input pastel */
    .stTextInput > div > div > input, .stTextArea textarea {
        background-color: #FFFDF5;
        border: 2px solid #DD8E6B;
        border-radius: 12px;
        color: #403D39;
        font-size: 1rem;
    }

    .stTextInput > div > div > input:focus, .stTextArea textarea:focus {
        border-color: #C6E2E3;
        box-shadow: 0 0 10px rgba(198,226,227,0.5);
    }

    /* Divider */
    .divider {
        border-top: 2px solid #F3D5B5;
        margin: 2rem 0;
    }

    /* Cabeceras pequeñas */
    .section-title {
        color: #DD8E6B;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-align: center;
    }

</style>
""", unsafe_allow_html=True)

# ==============================
# ENCABEZADO
# ==============================
st.markdown('<div class="main-title">🍼 Cuentos para Bebés - BAE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Historias dulces para calmar, dormir o sonreír junto a tu bebé</div>', unsafe_allow_html=True)

# ==============================
# PANEL PRINCIPAL
# ==============================
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">✨ Crea tu cuento personalizado</div>', unsafe_allow_html=True)

    nombre_bebe = st.text_input("👶 Nombre del bebé:")
    tema = st.text_input("🌈 Tema del cuento (ej. animales, amistad, dormir, aventura):")
    duracion = st.slider("⏳ Duración aproximada (minutos)", 1, 10, 3)
    tono = st.selectbox("💛 Tono del cuento", ["Tierno", "Aventurero", "Educativo", "Para dormir"])

    api_key = st.text_input("🔑 Clave de OpenAI", type="password")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.button("🎧 Generar cuento"):
        if not api_key:
            st.warning("Por favor ingresa tu clave de OpenAI para continuar 🧸")
        elif not nombre_bebe or not tema:
            st.warning("Por favor escribe el nombre del bebé y el tema del cuento ✨")
        else:
            with st.spinner("🍼 Creando una historia mágica para tu bebé..."):
                client = OpenAI(api_key=api_key)
                prompt = f"""
                Crea un cuento breve y tierno para un bebé llamado {nombre_bebe}.
                Tema: {tema}.
                Duración: {duracion} minutos aproximadamente.
                Estilo: {tono}, con lenguaje suave, frases cortas y ritmo calmado.
                El cuento debe transmitir cariño, seguridad y valores positivos.
                Escribe en español.
                """

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800
                )

                cuento = response.choices[0].message.content
                st.markdown('<div class="story-box">', unsafe_allow_html=True)
                st.markdown("### 🧸 Cuento Generado")
                st.write(cuento)
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


