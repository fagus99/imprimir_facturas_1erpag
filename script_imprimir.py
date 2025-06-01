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
                images_to_download.append((image_name, img_bytes))
                
                # Mostrar la imagen en la app
                st.image(img_bytes, caption=f"Primera página de {file.name}", use_container_width=True)
        
        except Exception as e:
            st.error(f"No se pudo procesar el archivo {file.name}: {e}")

    # Si hay imágenes para descargar, crear el botón de descarga
    if images_to_download:
        with BytesIO() as zip_buffer:
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for image_name, img_bytes in images_to_download:
                    zip_file.writestr(image_name, img_bytes)  # Añadir la imagen al ZIP
            zip_buffer.seek(0)  # Reiniciar el puntero del buffer para la descarga

            # Botón de descarga para el archivo ZIP
            st.download_button(
                label="Descargar todas las imágenes (ZIP)",
                data=zip_buffer,
                file_name="imagenes_primeras_paginas.zip",
                mime="application/zip"
            )
