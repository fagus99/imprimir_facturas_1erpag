import streamlit as st
import fitz  # PyMuPDF
import zipfile
from io import BytesIO

st.title("Visualizador de la Primera Página de PDFs")

uploaded_files = st.file_uploader("Sube uno o varios archivos PDF", type="pdf", accept_multiple_files=True)

# Lista para almacenar las imágenes
images_to_download = []

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"Archivo: {file.name}")
        try:
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                first_page = doc.load_page(0)  # Carga la primera página
                pix = first_page.get_pixmap()  # Renderiza la página a imagen
                img_bytes = pix.tobytes("png")  # Convierte a PNG
                image_name = f"first_page_{file.name}.png"
                
                # Añadir la imagen a la lista de imágenes para descargar
