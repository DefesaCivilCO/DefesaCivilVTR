
Python

import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from fpdf import FPDF

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Defesa Civil Municipal - Cautela", page_icon="🛡️")

# 2. PERSONALIZAÇÃO DE CORES E CENTRALIZAÇÃO TOTAL
st.markdown("""
    <style>
    /* Fundo do app Azul Marinho Noturno */
    .stApp { background-color: #000033; }
    
    /* Centralização de todos os elementos de texto e imagens */
    .center-all {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        width: 100%;
    }

    h1 { color: #FF8C00 !important; font-size: 2.5em !important; margin-bottom: 0px; text-align: center; }
    h3 { color: #ffffff !important; margin-top: 0px; font-weight: normal; text-align: center; }

    /* Estilo dos rótulos (Labels) */
    label { 
        color: #FF8C00 !important; 
        font-weight: bold !important;
    }
    
    /* Texto dos Checkboxes */
    .stCheckbox label p {
        color: #ffffff !important;
    }

    /* Centralização dos Botões */
    div.stButton {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }

    .stButton>button {
        background-color: #FF8C00;
        color: white;
        border-radius: 12px;
        border: 2px solid #ffffff;
        height: 4.5em;
        font-size: 1.1em;
        font-weight: bold;
        width: 85%;
    }
    
    .stButton>button:hover {
        background-color: #ffffff;
        color: #FF8C00;
        border: 2px solid #FF8C00;
    }

    /* Mensagem de sucesso personalizada */
    .success-msg {
        background-color: rgba(0, 255, 0, 0.1);
        border: 1px solid #00ff00;
        color: #00ff00;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
        font-weight: bold;
        width: 100%;
    }

    input { color: #000033 !important; }

    /* Centralizar imagem via Streamlit nativo */
    [data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO TOTALMENTE CENTRALIZADO
st.markdown('<div class="center-all">', unsafe_allow_html=True)
try:
    st.image("logo.png", width=250)
except:
    st.write("🛡️")

st.markdown('<h1>Defesa Civil Municipal</h1>', unsafe_allow_html=True)
st.markdown('<h3>Cidade Ocidental - GO</h3>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #FF8C00'>", unsafe_allow_html=True)

# 4. FORMULÁRIO DE CAUTELA
st.markdown("### 📝 Identificação")
agente = st.text_input("Nome do Agente Responsável")

c1, c2 = st.columns(2)
with c1:
    vtr = st.selectbox("Viatura", ["VTR-01", "VTR-02", "VTR-03", "RESGATE", "ADM"])
with c2:
    km = st.number_input("Quilometragem Atual", min_value=0, step=1)

st.write(" ")

st.markdown("### 📋 Checklist de Inspeção")
col_a, col_b = st.columns(2)

with col_a:
    oleo = st.checkbox("⚙️ Óleo do Motor OK")
    agua = st.checkbox("💧 Arrefecimento OK")
    freio = st.checkbox("🛑 Fluido de Freio OK")
with col_b:
    pneus = st.checkbox("🛞 Pneus e Estepe OK")
    luzes = st.checkbox("🚨 Giroflex e Luzes OK")
    limpeza = st.checkbox("🧹 Limpeza Geral OK")

st.write(" ")
obs = st.text_area("🗒️ Observações / Avarias")

# 5. FUNÇÃO DO PDF (VERSÃO COMPATÍVEL)
def gerar_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 0, 51)
    pdf.cell(190, 10, "DEFESA CIVIL MUNICIPAL", ln=True, align='C')
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "CIDADE OCIDENTAL - GO", ln=True, align='C')
    pdf.ln(5)
    pdf.set_text_color(255, 140, 0)
    pdf.cell(190, 10, f"CAUTELA ID: {d['id']}", ln=True, align='C')
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 10, "Data/Hora:", border=1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(150, 10, d['data'], border=1, ln=True)
    pdf.cell(40, 10, "Agente:", border=1)
    pdf.cell(150, 10, d['agente'], border=1, ln=True)
    pdf.cell(40, 10, "VTR / KM:", border=1)
    pdf.cell(150, 10, f"{d['vtr']} - KM {d['km']}", border=1, ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "ITENS VERIFICADOS:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(190, 8, f"Oleo: {d['oleo']} | Agua: {d['agua']} | Freio: {d['freio']}\nPneus: {d['pneus']} | Luzes: {d['luzes']} | Limpeza: {d['limpeza']}", border=1)
    if d['obs']:
        pdf.ln(5)
        pdf.multi_cell(190, 8, f"Observacoes: {d['obs']}", border=1)
    pdf.ln(25)
    pdf.cell(190, 10, "________________________________________", ln=True, align='C')
    pdf.cell(190, 10, "Assinatura do Agente", ln=True, align='C')
    
    return bytes(pdf.output())

# 6. BOTÃO DE ENVIO E CONFIRMAÇÃO
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 FINALIZAR E GERAR PDF"):
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
        
        try:
            pdf_bytes = gerar_pdf(info)
            st.balloons()
            st.markdown(f"""
                <div class="success-msg">
                    ✅ CAUTELA {id_c} REGISTRADA COM SUCESSO!<br>
                    O arquivo está pronto para download.
                </div>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label="📥 CLIQUE PARA DESCARREGAR PDF", 
                data=pdf_bytes, 
                file_name=f"Cautela_{vtr}_{id_c}.pdf", 
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
    else:
        st.error("⚠️ Preencha Nome e KM antes de gerar o PDF.")
