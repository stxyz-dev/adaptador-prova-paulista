import streamlit as st
import pandas as pd
from pypdf import PdfReader
import io
import re

st.set_page_config(page_title="Adaptador Prova Paulista", layout="wide")

st.title("📘 Adaptador Prova Paulista")
st.write("Envie os PDFs do currículo/provas.")

uploaded_files = st.file_uploader(
    "Arraste os PDFs aqui",
    type=["pdf"],
    accept_multiple_files=True
)

def extrair_texto(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    textos = []

    # lê apenas primeiras 25 páginas (rápido e seguro)
    for i, page in enumerate(reader.pages[:25]):
        try:
            txt = page.extract_text()
            if txt:
                textos.append((i, txt))
        except:
            pass

    return textos

def detectar_disciplina(nome):
    nome = nome.lower()
    if "mat" in nome: return "Matemática"
    if "lp" in nome: return "Português"
    if "geo" in nome: return "Geografia"
    if "his" in nome: return "História"
    if "cie" in nome: return "Ciências"
    if "bio" in nome: return "Biologia"
    if "fis" in nome: return "Física"
    if "qui" in nome: return "Química"
    if "ing" in nome: return "Inglês"
    if "arte" in nome: return "Arte"
    return "Geral"

def detectar_segmento(nome):
    if "af" in nome.lower():
        return "Fundamental"
    if "em" in nome.lower():
        return "Ensino Médio"
    return "Outro"

if uploaded_files:

    registros = []

    for file in uploaded_files:
        bytes_data = file.read()
        paginas = extrair_texto(bytes_data)

        disciplina = detectar_disciplina(file.name)
        segmento = detectar_segmento(file.name)

        for pag, txt in paginas:
            registros.append({
                "arquivo": file.name,
                "disciplina": disciplina,
                "segmento": segmento,
                "pagina": pag,
                "texto_inicio": txt[:400]
            })

    df = pd.DataFrame(registros)

    st.success(f"{len(uploaded_files)} PDFs processados")

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar CSV", csv, "base_curriculo.csv")