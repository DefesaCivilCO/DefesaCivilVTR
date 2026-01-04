import streamlit as st
import pandas as pd
from datetime import datetime
import uuid
from fpdf import FPDF

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Defesa Civil Municipal - Cautela", page_icon="🛡️")

# 2. PERSONALIZAÇÃO DE CORES (FUNDO BRANCO, TEXTO AZUL MARINHO E LARANJA)
st.markdown("""
    <style>
    /* Fundo do app Branco */
    .stApp { background-color: #ffffff; }
    
    /* Container para alinhar Logo e Texto Lado a Lado */
    .header-box {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding: 20px;
        width: 100%;
    }

    /* Cores dos Títulos */
    .title-blue { color: #000033; font-size: 2.2em; font-weight: bold; margin: 0; }
    .highlight-orange { color: #FF8C00; }
    .subtitle-blue { color: #000033; font-size: 1.2em; margin: 0; opacity: 0.8; }

    /* Estilo dos rótulos (Labels) */
    label { 
        color: #000033 !important; 
        font-weight: bold !important;
    }
    
    /* Texto dos Checkboxes */
    .stCheckbox label p {
        color: #000033 !important;
    }

    /* Estilo dos Botões */
    div.stButton {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }

    .stButton>button {
        background-color: #000033;
        color: #ffffff;
        border-radius: 8px;
        border: 2px solid #FF8C00;
        height: 3.5em;
        font-size: 1.1em;
        font-weight: bold;
        width: 100%;
        max-width: 400px;
    }
    
    .stButton>button:hover {
        background-color: #FF8C00;
        color: #ffffff;
    }

    /* Mensagem de sucesso */
    .success-msg {
        background-color: #f0fff4;
        border: 1px solid #FF8C00;
        color: #000033;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }

    /* Cor das bordas dos inputs */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border-color: #000033 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CABEÇALHO LADO A LADO E CENTRALIZADO
col_logo, col_txt = st.columns([1, 2])

with col_logo:
    try:
        st.image("logo.png", width=150)
    except:
        st.markdown("<h1 style='text-align: right;'>🛡️</h1>", unsafe_allow_html=True)

with col_txt:
    st.markdown(f"""
        <div style='display: flex; flex-direction: column; justify-content: center; height: 150px;'>
            <div class='title-blue'>
                <span class='highlight-orange'>DEFESA</span> CIVIL<br>
                <span class='highlight-orange'>MUNICIPAL</span>
            </div>
            <div class='subtitle-blue'>Cidade Ocidental - GO</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #FF8C00'>", unsafe_allow_html=True)

# 4. FORMULÁRIO DE CAUTELA
st.markdown("### 📝 Identificação")
col_ident1, col_ident2 = st.columns([3, 1])
with col_ident1:
    agente = st.text_input("Nome do Agente Responsável")
with col_ident2:
    matricula = st.text_input("Matrícula")

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

# 5. FUNÇÃO DO PDF
def gerar_pdf(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho do PDF
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 0, 51) # Azul Marinho
    pdf.cell(190, 10, "DEFESA CIVIL MUNICIPAL", ln=True, align='C')
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "CIDADE OCIDENTAL - GO", ln=True, align='C')
    pdf.ln(5)
    
    # ID em Laranja (aproximado no PDF)
    pdf.set_text_color(255, 140, 0)
    pdf.cell(190, 10, f"CAUTELA ID: {d['id']}", ln=True, align='C')
    pdf.ln(10)
    
    # Informações Técnicas
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 11)
    
    pdf.cell(40, 10, "Data/Hora:", border=1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(150, 10, d['data'], border=1, ln=True)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 10, "Agente:", border=1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(150, 10, f"{d['agente']} (Mat: {d['matricula']})", border=1, ln=True)
    
    pdf.set_font("Arial", "B", 11)
    pdf.cell(40, 10, "VTR / KM:", border=1)
    pdf.set_font("Arial", "", 11)
    pdf.cell(150, 10, f"{d['vtr']} - KM {d['km']}", border=1, ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "ITENS VERIFICADOS:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(190, 8, f"Oleo: {d['oleo']} | Agua: {d['agua']} | Freio: {d['freio']}\nPneus: {d['pneus']} | Luzes: {d['luzes']} | Limpeza: {d['limpeza']}", border=1)
    
    if d['obs']:
        pdf.ln(5)
        pdf.multi_cell(190, 8, f"Obs: {d['obs']}", border=1)
    
    # Assinatura
    pdf.ln(30)
    pdf.cell(190, 10, "________________________________________", ln=True, align='C')
    pdf.set_font("Arial", "B", 11)
    pdf.cell(190, 7, d['agente'].upper(), ln=True, align='C')
    pdf.set_font("Arial", "", 10)
    pdf.cell(190, 5, "Assinatura do Agente", ln=True, align='C')
    
    return bytes(pdf.output())

# 6. BOTÃO DE ENVIO
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 FINALIZAR E GERAR PDF"):
    if agente and km > 0:
        id_c = str(uuid.uuid4())[:8].upper()
        data_f = datetime.now().strftime("%d/%m/%Y %H:%M")
        info = {
            "id": id_c, "data": data_f, "agente": agente, "matricula": matricula, 
            "vtr": vtr, "km": km,
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
                    ✅ <b>CAUTELA {id_c} REGISTRADA!</b><br>
                    O documento foi gerado com sucesso.
                </div>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label="📥 BAIXAR DOCUMENTO PDF", 
                data=pdf_bytes, 
                file_name=f"Cautela_{vtr}_{id_c}.pdf", 
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
    else:
        st.error("⚠️ Por favor, preencha o Nome do Agente e a KM.")
