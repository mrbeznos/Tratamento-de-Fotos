
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import io

st.set_page_config(page_title="Tratador de Fotos", layout="centered")

st.title("🎨 Tratamento Automático de Imagens")
st.write("Envie suas fotos, escolha o estilo de tratamento e baixe o resultado.")

preset = st.selectbox("Escolha o estilo de tratamento:", ["natural", "vibrant", "moody"])
uploaded_files = st.file_uploader("Envie suas imagens (JPG ou PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Funções de tratamento
def aplicar_natural(image):
    image = image.filter(ImageFilter.SMOOTH_MORE)
    image = ImageEnhance.Brightness(image).enhance(1.05)
    image = ImageEnhance.Color(image).enhance(1.0)
    return image

def aplicar_vibrant(image):
    image = ImageEnhance.Contrast(image).enhance(1.3)
    image = ImageEnhance.Color(image).enhance(1.4)
    image = ImageEnhance.Sharpness(image).enhance(1.2)
    return image

def aplicar_moody(image):
    image = ImageEnhance.Brightness(image).enhance(0.85)
    image = ImageEnhance.Contrast(image).enhance(1.2)
    image = ImageEnhance.Color(image).enhance(0.8)
    return image

presets = {
    "natural": aplicar_natural,
    "vibrant": aplicar_vibrant,
    "moody": aplicar_moody
}

if uploaded_files:
    st.markdown("### 📥 Resultados:")
    tratamento = presets.get(preset, aplicar_natural)

    for file in uploaded_files:
        img = Image.open(file).convert("RGB")
        tratada = tratamento(img)

        buf = io.BytesIO()
        tratada.save(buf, format="JPEG")
        byte_im = buf.getvalue()

        st.image(tratada, caption=f"Imagem tratada ({preset})", use_column_width=True)
        st.download_button(label="📩 Baixar imagem", data=byte_im,
                           file_name=f"{file.name.split('.')[0]}_{preset}.jpg", mime="image/jpeg")
