import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from fpdf import FPDF

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Defesa Civil - Cautela VTR", page_icon="🛡️")

# 2. PERSONALIZAÇÃO DE CORES (CSS)
st.markdown("""
    <style>
    /* Fundo do app */
    .stApp { background-color: #f0f2f6; }
    
    /* Títulos em Azul Marinho */
    h1, h2, h3 { color: #00008B !important; font-family: 'Arial'; }
    
    /* Botão Principal Laranja */
    .stButton>button {
        background-color: #FF8C00;
        color: white;
        border-radius: 12px;
        border: none;
        height: 4em;
        font-size: 1.2em;
        font-weight: bold;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #e67e00;
        transform: scale(1.02);
    }
    
    /* Estilo dos cards de identificação */
    div.stBlock {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #00008B;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO COM LOGO
col_logo, col_txt = st.columns([1, 3])
with col_logo:
    try:
        st.image("logo.png", width=120)
    except:
        st.title("🛡️")

with col_txt:
    st.write("# Defesa Civil")
    st.write("### Cidade Ocidental - GO")

st.divider()

# 4. FORMULÁRIO DE CAUTELA
with st.container():
    st.markdown("### 📝 Identificação")
    agente = st.text_input("Nome do Agente", placeholder="Quem está assumindo a VTR?")
    
    c1, c2 = st.columns(2)
    with c1:
        vtr = st.selectbox("Viatura", ["VTR-01", "VTR-02", "VTR-03", "RESGATE", "ADM"])
    with c2:
        km = st.number_input("KM Atual", min_value=0, step=1)

st.write(" ")

with st.container():
    st.markdown("### 📋 Checklist de Inspeção")
    col_a, col_b = st.columns(2)
    
    with col_a:
        oleo = st.checkbox("⚙️ Óleo do Motor")
        agua = st.checkbox("💧 Arrefecimento")
        freio = st.checkbox("🛑 Fluido de Freio")
    with col_b:
        pneus = st.checkbox("🛞 Pneus e Estepe")
        luzes = st.checkbox("🚨 Giroflex e Luzes")
        limpeza = st.checkbox("🧹 Limpeza Geral")

st.write(" ")
obs = st.text_area("🗒️ Observações ou Avarias")

# 5. FUNÇÃO DO PDF (DADOS PARA O COORDENADOR)
def gerar_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho do PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(190, 10, "DEFESA CIVIL - CIDADE OCIDENTAL", ln=True, align='C')
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, f"COMPROVANTE DE CAUTELA: {d['id']}", ln=True, align='C')
    pdf.ln(10)
    
    # Informações básicas
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 10, "Data:", border=1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(150, 10, d['data'], border=1, ln=True)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 10, "Agente:", border=1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(150, 10, d['agente'], border=1, ln=True)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 10, "VTR / KM:", border=1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(150, 10, f"{d['vtr']} - KM {d['km']}", border=1, ln=True)
    
    # Checklist
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "ITENS VERIFICADOS:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.cell(190, 8, f"Oleo: {d['oleo']} | Agua: {d['agua']} | Freio: {d['freio']}", ln=True)
    pdf.cell(190, 8, f"Pneus: {d['pneus']} | Luzes: {d['luzes']} | Limpeza: {d['limpeza']}", ln=True)
    
    if d['obs']:
        pdf.ln(5)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(190, 10, "Observacoes:", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(190, 8, d['obs'], border=1)
        
    pdf.ln(20)
    pdf.cell(190, 10, "________________________________________", ln=True, align='C')
    pdf.cell(190, 10, "Assinatura do Agente", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# 6. BOTÃO DE ENVIO
st.write("---")
if st.button("🚀 FINALIZAR E GERAR COMPROVANTE"):
    if agente and km > 0:
        id_c = str(uuid.uuid4())[:8].upper()
        data_f = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        info = {
            "id": id_c, "data": data_f, "agente": agente, "vtr": vtr, "km": km,
            "oleo": "OK" if oleo else "PEN", "agua": "OK" if agua else "PEN",
            "freio": "OK" if freio else "PEN", "pneus": "OK" if pneus else "PEN",
            "luzes": "OK" if luzes else "PEN", "limpeza": "OK" if limpeza else "PEN",
            "obs": obs
        }
        
        pdf_bytes = gerar_pdf(info)
        st.balloons()
        st.success(f"### Cautela Registrada! ID: {id_c}")
        
        st.download_button(
            label="📥 BAIXAR PDF (ENVIAR PARA COORDENAÇÃO)",
            data=pdf_bytes,
            file_name=f"Cautela_{vtr}_{id_c}.pdf",
            mime="application/pdf"
        )
    else:
        st.error("⚠️ Preencha seu NOME e a QUILOMETRAGEM atual.")
