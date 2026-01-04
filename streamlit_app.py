import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="Defesa Civil - Cidade Ocidental", page_icon="🛡️")

# Estilo Visual (Identidade Defesa Civil: Azul e Laranja)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { 
        background-color: #00008B; 
        color: white; 
        width: 100%; 
        font-weight: bold; 
        height: 3.5em; 
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover { background-color: #FF8C00; color: white; }
    h1 { color: #00008B; border-bottom: 3px solid #FF8C00; }
    h3 { color: #00008B; }
    .stCheckbox { margin-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Exibição da Logo
col_logo, _ = st.columns([1, 2])
with col_logo:
    try:
        # Tenta carregar o arquivo que você subiu no GitHub
        st.image("IMG-20250908-WA0093-removebg-preview.png", width=150)
    except:
        st.write("🛡️ **DEFESA CIVIL**")

st.title("Cautela de Viatura")
st.write("Preencha os dados abaixo para gerar o relatório de inspeção.")

# --- FORMULÁRIO DE IDENTIFICAÇÃO ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        agente = st.text_input("Nome do Agente", placeholder="Ex: João Silva")
        vtr = st.selectbox("Viatura", ["VTR-01", "VTR-02", "VTR-03", "Resgate-01", "Administrativo"])
    with col2:
        km = st.number_input("Quilometragem Atual", min_value=0, step=1)
        data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        st.info(f"📅 {data_hoje}")

st.write("---")

# --- CHECKLIST DE INSPEÇÃO ---
st.subheader("📋 Itens de Inspeção")
c1, c2 = st.columns(2)
with c1:
    oleo = st.checkbox("Nível de Óleo do Motor OK")
    agua = st.checkbox("Líquido de Arrefecimento OK")
    freio = st.checkbox("Fluido de Freio OK")
with c2:
    pneus = st.checkbox("Pneus e Estepe OK")
    luzes = st.checkbox("Sinalização/Giroflex OK")
    limpeza = st.checkbox("Limpeza Interna/Externa OK")

avarias = st.text_area("Observações ou Novas Avarias", placeholder="Descreva riscos, batidas ou problemas mecânicos, se houver.")

# --- FUNÇÃO PARA GERAR PDF ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho formatado
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 0, 139) # Azul Marinho
    pdf.cell(190, 10, "DEFESA CIVIL - CIDADE OCIDENTAL", ln=True, align='C')
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(255, 140, 0) # Laranja
    pdf.cell(190, 10, f"RELATÓRIO DE CAUTELA: {dados['id']}", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0) # Preto
    
    # Tabela de Dados Principais
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 10, "DATA/HORA:", border=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(55, 10, dados['data'], border=1)
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 10, "VIATURA:", border=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(55, 10, dados['vtr'], border=1, ln=True)
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 10, "AGENTE:", border=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(55, 10, dados['agente'], border=1)
    
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(40, 10, "KM AT
