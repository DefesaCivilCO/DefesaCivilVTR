import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Defesa Civil - Cidade Ocidental", page_icon="🛡️")

# Estilização básica corrigida
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { background-color: #00008B; color: white; width: 100%; border-radius: 8px; }
    h1 { color: #00008B; border-bottom: 2px solid #FF8C00; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Cautela de Viatura")
st.subheader("Defesa Civil - Cidade Ocidental/GO")

# --- IDENTIFICAÇÃO ---
with st.expander("1. Identificação", expanded=True):
    agente = st.text_input("Nome do Agente")
    vtr = st.selectbox("Viatura (Prefixo)", ["VTR-01", "VTR-02", "Resgate-01", "Adm-01"])
    km = st.number_input("Quilometragem Atual", step=1, min_value=0)

# --- CHECKLIST TÉCNICO ---
st.write("### 2. Inspeção Técnica")
col1, col2 = st.columns(2)

with col1:
    st.write("**Níveis e Fluidos**")
    oleo = st.checkbox("Óleo do Motor OK")
    arrefecimento = st.checkbox("Líquido de Arrefecimento OK")
    freio = st.checkbox("Fluido de Freio OK")

with col2:
    st.write("**Segurança/Elétrica**")
    giroflex = st.checkbox("Giroflex/Sirene OK")
    iluminacao = st.checkbox("Faróis/Sinalização OK")
    pneus = st.checkbox("Pneus/Estepe OK")

# --- CONDIÇÕES EXTERNAS ---
st.write("### 3. Estado da Lataria")
avarias = st.radio("Existem novas avarias?", ["Não", "Sim"])
if avarias == "Sim":
    detalhes_avaria = st.text_area("Descreva as avarias detectadas:")
    foto = st.file_uploader("Anexar foto da avaria", type=['png', 'jpg', 'jpeg'])

# --- FINALIZAÇÃO ---
if st.button("Finalizar e Salvar Cautela"):
    if agente and km > 0:
        st.success(f"✅ Cautela da {vtr} registrada com sucesso por {agente}!")
        st.balloons()
    else:
        st.error("❌ Por favor, preencha o nome do agente e a quilometragem.")
