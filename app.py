import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from googletrans import Translator
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import tempfile
import os

st.set_page_config(page_title="Scanned PDF → Urdu", layout="centered")

st.title("Scanned PDF to Urdu (Layout-Aware)")
st.write("Upload an image-based PDF. Output will be a translated Urdu PDF.")

uploaded_file = st.file_uploader("Upload scanned PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing PDF..."):
        images = convert_from_bytes(uploaded_file.read(), dpi=300)

        translator = Translator()

        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        c = canvas.Canvas(temp_pdf.name, pagesize=A4)

        for img in images:
            text = pytesseract.image_to_string(img, lang="eng")

            if text.strip():
                urdu_text = translator.translate(text, dest="ur").text
            else:
                urdu_text = ""

            text_object = c.beginText(40, 800)
            text_object.setFont("Helvetica", 10)

            for line in urdu_text.split("\n"):
                text_object.textLine(line)

            c.drawText(text_object)
            c.showPage()

        c.save()

    st.success("Translation complete.")

    with open(temp_pdf.name, "rb") as f:
        st.download_button(
            label="Download Urdu PDF",
            data=f,
            file_name="translated_urdu.pdf",
            mime="application/pdf"
        )

    os.unlink(temp_pdf.name)
