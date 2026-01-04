import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from fpdf import FPDF

# Configuração da página
st.set_page_config(page_title="Defesa Civil - Cidade Ocidental", page_icon="🛡️")

# Estilo Visual (Cores da Defesa Civil)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { background-color: #00008B; color: white; width: 100%; font-weight: bold; height: 3.5em; border-radius: 10px; }
    h1 { color: #00008B; border-bottom: 3px solid #FF8C00; }
    .stCheckbox { margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Topo com Logo (Se o arquivo estiver no GitHub com esse nome)
try:
    st.image("IMG-20250908-WA0093-removebg-preview.png", width=120)
except:
    st.write("🛡️ **DEFESA CIVIL - CIDADE OCIDENTAL**")

st.title("Cautela de Viatura")

# --- FORMULÁRIO ---
col1, col2 = st.columns(2)
with col1:
    agente = st.text_input("Nome do Agente")
    vtr = st.selectbox("Viatura", ["VTR-01", "VTR-02", "VTR-03", "Resgate", "Administrativo"])
with col2:
    km = st.number_input("KM Atual", min_value=0, step=1)
    data_hoje = datetime.now().strftime("%d/%m/%Y %H:%M")

st.subheader("Checklist de Inspeção")
c1, c2 = st.columns(2)
with c1:
    oleo = st.checkbox("Óleo do Motor OK")
    agua = st.checkbox("Líquido Arrefecimento OK")
with c2:
    pneus = st.checkbox("Pneus e Estepe OK")
    luzes = st.checkbox("Sinalização e Luzes OK")

avarias = st.text_area("Observações / Avarias Externas")

# --- FUNÇÃO DO PDF ---
def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "DEFESA CIVIL - CIDADE OCIDENTAL", ln=True, align='C')
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, f"COMPROVANTE DE CAUTELA - {dados['id']}", ln=True, align='C')
    pdf.ln(10)
    
    # Dados
    pdf.set_font("Arial", "", 12)
    pdf.cell(95, 10, f"Data/Hora: {dados['data']}", border=1)
    pdf.cell(95, 10, f"Viatura: {dados['vtr']}", border=1, ln=True)
    pdf.cell(95, 10, f"Agente: {dados['agente']}", border=1)
    pdf.cell(95, 10, f"KM: {dados['km']}", border=1, ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Resultado da Inspeção:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 10, f"- Óleo Motor: {dados['oleo']}", ln=True)
    pdf.cell(190, 10, f"- Arrefecimento: {dados['agua']}", ln=True)
    pdf.cell(190, 10, f"- Pneus/Estepe: {dados['pneus']}", ln=True)
    pdf.cell(190, 10, f"- Luzes/Sinalização: {dados['luzes']}", ln=True)
    
    if dados['obs']:
        pdf.ln(5)
        pdf.multi_cell(190, 10, f"Observações: {dados['obs']}", border=1)
    
    pdf.ln(20)
    pdf.cell(190, 10, "__________________________________________", ln=True, align='C')
    pdf.cell(190, 10, "Assinatura do Agente", ln=True, align='C')
    
    return pdf.output()

# --- BOTÃO FINALIZAR ---
if st.button("SALVAR E GERAR PDF"):
    if agente and km > 0:
        id_cautela = str(uuid.uuid4())[:8].upper()
        
        info = {
            "id": id_cautela,
            "data": data_hoje,
            "agente": agente,
            "vtr": vtr,
            "km": km,
            "oleo": "✅ OK" if oleo else "❌ PENDENTE",
            "agua": "✅ OK" if agua else "❌ PENDENTE",
            "pneus": "✅ OK" if pneus else "❌ PENDENTE",
            "luzes": "✅ OK" if luzes else "❌ PENDENTE",
            "obs": avarias
        }
        
        # Gerar o arquivo PDF
        pdf_out = gerar_pdf(info)
        
        st.success(f"✅ Cautela {id_cautela} registrada!")
        
        # Botão de Download do PDF
        st.download_button(
            label="📥 Baixar PDF da Cautela",
            data=bytes(pdf_out),
            file_name=f"cautela_{id_cautela}.pdf",
            mime="application/pdf"
        )
        
        # DICA PARA O COORDENADOR:
        st.info("Agente: Após baixar, envie o PDF para o grupo de coordenação.")
    else:
        st.error("Preencha o Nome e o KM da viatura.")
