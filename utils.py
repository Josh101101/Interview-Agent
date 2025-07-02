import json
from PyPDF2 import PdfReader
from docx import Document
import ast
import streamlit as st

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file) -> str:
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def get_resume_text(uploaded_file, filetype: str = "text") -> str:
    if filetype == "pdf":
        try:
            return extract_text_from_pdf(uploaded_file)
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return ""
    elif filetype == "docx":
        try:
            return extract_text_from_docx(uploaded_file)
        except Exception as e:
            st.error(f"Error reading DOCX: {e}")
            return ""
    else:
        try:
            return uploaded_file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Error reading text file: {e}")
            return ""

def extract_json_from_output(output):
    if hasattr(output, "result"):
        result = output.result
        if isinstance(result, str):
            return result
        elif isinstance(result, (list, dict)):
            return json.dumps(result)
    if hasattr(output, "output"):
        out = output.output
        if isinstance(out, str):
            return out
        elif isinstance(out, (list, dict)):
            return json.dumps(out)
    if isinstance(output, (list, dict)):
        return json.dumps(output)
    return str(output)
