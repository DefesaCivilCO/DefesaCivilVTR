import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="Defesa Civil - Cidade Ocidental", page_icon="🛡️")

# Estilo Visual
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { 
        background-color: #00008B; color: white; width: 100%; 
        font-weight: bold; height: 3.5em; border-radius: 10px;
    }
    h1 { color: #00008B; border-bottom: 3px solid #FF8C00; }
    </style>
    """, unsafe_allow_html=True)

# Exibição da Logo
try:
    st.image("IMG-20250908-WA0093-removebg-preview.png", width=120)
except:
    st.subheader("🛡️ DEFESA CIVIL - CIDADE OCIDENTAL")

st.title("Cautela de Viatura")

# --- CAMPOS DO FORMULÁRIO ---
col1, col2 = st.columns(2)
with col1:
    agente = st.text_input("Nome do Agente")
    vtr = st.selectbox("Viatura", ["VTR-01", "VTR-02", "VTR-03", "Resgate-01", "Adm"])
with col2:
    km = st.number_input("KM Atual", min_value=0, step=1)
    data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.write(f"📅 **{data_hoje}**")

st.write("---")
st.subheader("📋 Itens de Inspeção")
c1, c2 = st.columns(2)
with c1:
    oleo = st.checkbox("Óleo do Motor OK")
    agua = st.checkbox("Arrefecimento OK")
    freio = st.checkbox("Fluido de Freio OK")
with c2:
    pneus = st.checkbox("Pneus/Estepe OK")
    luzes = st.checkbox("Giroflex/Luzes OK")
    limpeza = st.checkbox("Limpeza OK")

obs = st.text_area("Observações/Avarias")

# --- FUNÇÃO DO PDF ---
def gerar_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(190, 10, "DEFESA CIVIL - CIDADE OCIDENTAL", ln=True, align='C')
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(190, 10, f"CAUTELA ID: {d['id']}", ln=True, align='C')
    pdf.ln(10)
    
    # Dados em tabela
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(95, 10, f"Data: {d['data']}", border=1)
    pdf.cell(95, 10, f"Viatura: {d['vtr']}", border=1, ln=True)
    pdf.cell(95, 10, f"Agente: {d['agente']}", border=1)
    pdf.cell(95, 10, f"KM Atual: {d['
