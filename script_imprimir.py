import streamlit as st
import fitz  # PyMuPDF

st.title("Visualizador de la Primera Página de PDFs")

uploaded_files = st.file_uploader("Sube uno o varios archivos PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        st.subheader(f"Archivo: {file.name}")
        try:
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                first_page = doc.load_page(0)  # Carga la primera página
                pix = first_page.get_pixmap()  # Renderiza la página a imagen
                img_bytes = pix.tobytes("png")  # Convierte a PNG
                st.image(img_bytes, caption=f"Primera página de {file.name}", use_container_width=True)
                
                # Botón para descargar la imagen
                st.download_button(
                    label="Descargar imagen de la primera página",
                    data=img_bytes,
                    file_name=f"first_page_{file.name}.png",
                    mime="image/png"
                )
                
        except Exception as e:
            st.error(f"No se pudo procesar el archivo {file.name}: {e}")
