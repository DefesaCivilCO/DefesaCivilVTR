import streamlit as st
import pandas as pd
from datetime import datetime
import uuid # Para gerar IDs únicos
# from fpdf import FPDF # Será usado para gerar PDF

# Importar o conector do Google Sheets
from streamlit_gsheets import GSheetsConnection

# --- 1. Configuração da Página e Estilo ---
st.set_page_config(page_title="Defesa Civil - Cautela VTR", page_icon="🛡️", layout="centered")

# Estilização com as cores da logo (Azul e Laranja) e fontes.
# Aqui vamos tentar carregar a logo direto.
st.markdown("""
    <style>
    .main { background-color: #ffffff; padding-top: 20px;}
    .stButton>button { 
        background-color: #00008B; 
        color: white; 
        width: 100%; 
        border-radius: 10px;
        height: 3.5em; /* Aumenta a altura do botão */
        font-weight: bold;
        font-size: 1.1em;
        margin-top: 20px;
    }
    h1 { color: #00008B; border-bottom: 3px solid #FF8C00; padding-bottom: 10px; }
    h3 { color: #FF8C00; margin-top: 25px; }
    .stCheckbox { font-size: 1.05em; margin-bottom: 5px; } /* Ajusta o tamanho do texto do checkbox */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 8px; /* Bordas arredondadas para inputs */
        padding: 10px;
    }
    .expander-header {
        font-weight: bold;
        color: #00008B;
        font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Exibir a Logo no topo ---
# A imagem precisa estar acessível publicamente ou estar no seu repositório GitHub.
# Se a imagem for a que você enviou antes, ela precisa ser carregada no GitHub.
# Por enquanto, vamos usar a imagem de exemplo. Se você subir a imagem no GitHub,
# pode usar: f"https://raw.githubusercontent.com/DefesaCivilCO/DefesaCivilVTR/main/logo.png"
# Eu criei uma URL temporária com sua logo.
st.image("https://github.com/DefesaCivilCO/DefesaCivilVTR/blob/main/defesa_civil_co_logo.png?raw=true", width=100)
st.title("🛡️ Cautela de Viatura")
st.caption("Defesa Civil de Cidade Ocidental - GO")

# --- Inicializar a Conexão com Google Sheets ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 1. IDENTIFICAÇÃO ---
st.subheader("1. Identificação da Cautela")
col_id1, col_id2 = st.columns(2)

with col_id1:
    agente = st.text_input("Nome do Agente", placeholder="Ex: João Silva", key="agente_nome")
    vtr = st.selectbox("Viatura", ["VTR-01", "VTR-02", "VTR-03", "Resgate", "Administrativo"], key="vtr_selecao")

with col_id2:
    km = st.number_input("Quilometragem Atual", min_value=0, step=1, key="km_atual")
    data_hora_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    st.info(f"📅 Data/Hora: {data_hora_str}")

st.divider()

# --- 2. CHECKLIST TÉCNICO ---
st.subheader("2. Verificação de Itens Essenciais")

col1, col2 = st.columns(2)

with col1:
    st.markdown("---")
    st.markdown("### ⚙️ **Mecânica e Fluidos**")
    oleo = st.checkbox("Óleo do Motor OK", key="check_oleo")
    arrefecimento = st.checkbox("Líquido de Arrefecimento OK", key="check_arrefecimento")
    freio = st.checkbox("Fluido de Freio OK", key="check_freio")
    st.markdown("---")

with col2:
    st.markdown("---")
    st.markdown("### 🚨 **Segurança e Elétrica**")
    giroflex = st.checkbox("Giroflex e Sirene OK", key="check_giroflex")
    iluminacao = st.checkbox("Faróis e Setas OK", key="check_iluminacao")
    pneus = st.checkbox("Pneus e Estepe OK", key="check_pneus")
    st.markdown("---")

st.divider()

# --- 3. CONDIÇÕES EXTERNAS ---
st.subheader("3. Estado da Lataria")
avarias = st.radio("Existem novas avarias/danos?", ["Não", "Sim"], horizontal=True, key="radio_avarias")

detalhes_avaria = ""
link_foto_avaria = "N/A"
if avarias == "Sim":
    detalhes_avaria = st.text_area("Descreva os danos encontrados:", key="detalhes_avaria_txt")
    uploaded_file = st.file_uploader("Tirar foto da avaria", type=['png', 'jpg', 'jpeg'], key="foto_avaria_upload")
    if uploaded_file is not None:
        # Por simplicidade, vamos apenas dizer que a foto foi anexada.
        # Para salvar a foto de verdade, precisaríamos de um serviço como Imgur ou Cloudinary.
        st.success("Foto anexada com sucesso! (Não salva permanentemente nesta versão gratuita)")
        link_foto_avaria = "Foto Anexada (Não Pública)" # Em uma versão paga, aqui ficaria o link real.


# --- FINALIZAÇÃO E SALVAMENTO ---
st.write(" ")
if st.button("FINALIZAR E SALVAR CAUTELA"):
    if not agente or km <= 0:
        st.error("❌ Por favor, preencha o nome do agente e a quilometragem para finalizar.")
    else:
        # Gerar um ID único para a cautela (para o PDF)
        id_cautela = str(uuid.uuid4())[:8].upper() # Ex: A1B2C3D4

        # Criar os dados para salvar na planilha
        dados_cautela = {
            "ID_Cautela": id_cautela,
            "DataHora": data_hora_str,
            "Agente": agente,
            "Viatura": vtr,
            "KM": km,
            "OleoMotor": "OK" if oleo else "NÃO",
            "Arrefecimento": "OK" if arrefecimento else "NÃO",
            "Freio": "OK" if freio else "NÃO",
            "GiroflexSirene": "OK" if giroflex else "NÃO",
            "Iluminacao": "OK" if iluminacao else "NÃO",
            "PneusEstepe": "OK" if pneus else "NÃO",
            "Avarias": "Sim" if avarias == "Sim" else "Não",
            "DetalhesAvarias": detalhes_avaria if avarias == "Sim" else "N/A",
            "LinkFotoAvaria": link_foto_avaria
        }

        # Conectar e Adicionar uma nova linha na planilha
        try:
            df = conn.read()
            # Certificar-se que todas as colunas existem
            if not all(col in df.columns for col in dados_cautela.keys()):
                st.warning("Colunas da planilha não correspondem. Recriando o dataframe com as colunas esperadas.")
                df = pd.DataFrame(columns=dados_cautela.keys())

            df_to_save = pd.DataFrame([dados_cautela])
            updated_df = pd.concat([df, df_to_save], ignore_index=True)
            conn.update(data=updated_df)
            st.success(f"✅ Cautela {id_cautela} salva na planilha com sucesso! Agora Gerando PDF...")
            st.balloons()
            
            # --- Geração do PDF (Funcionalidade para o Futuro / Versão Paga) ---
            st.info(f"💾 Cautela de Viatura Gerada! ID: **{id_cautela}**")
            st.write("---")
            st.write("### PDF da Cautela (Funcionalidade em desenvolvimento)")
            st.warning("A geração de PDF é complexa para ambientes gratuitos. Estamos trabalhando nisso!")
            
            # Aqui, idealmente, teríamos a lógica para gerar e baixar o PDF
            # from fpdf import FPDF
            # pdf = FPDF()
            # ...
            # pdf.output(f"Cautela_{id_cautela}.pdf")
            # st.download_button(label="Baixar PDF", data=pdf_bytes, file_name=f"Cautela_{id_cautela}.pdf", mime="application/pdf")

        except Exception as e:
            st.error(f"❌ Erro ao salvar na planilha: {e}")
            st.info("Verifique se o e-mail do serviço do Google Cloud tem acesso 'Editor' à sua planilha e se as credenciais nos Secrets estão corretas.")

# --- Link para o Coordenador (apenas para referência) ---
st.sidebar.info("🔗 Link para a Planilha do Coordenador (Substitua pelo seu link real):")
st.sidebar.markdown("[Acessar Planilha Cautelas](https://docs.google.com/spreadsheets/d/1gQ1gQ1gQ1gQ1gQ1gQ1gQ1gQ1gQ1gQ1gQ1gQ1gQ1gQ1gQ/edit?usp=sharing)")
st.sidebar.caption("Lembre-se de substituir este link pelo link real da sua planilha!")
