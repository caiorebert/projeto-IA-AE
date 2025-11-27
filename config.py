import streamlit as st

# configurações da página
st.set_page_config(
    page_title="RAG ENEM Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# chave da OpenAI (definida em st.secrets)
OPENAI_API_KEY = st.secrets.get("openai_api_key")

# modelos utilizados
EMBEDDING_MODEL = "text-embedding-ada-002"
CHAT_MODEL     = "gpt-4o-mini"

# caminhos e constantes
RUBRIC_CSV_PATH = r"data/rubric.csv"
K_NEIGHBORS     = 3
