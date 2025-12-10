import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Corretor de Redações",
    layout="wide",
    initial_sidebar_state="expanded",
)

GEMINI_API_KEY = st.secrets.get("gemini_api_key")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

EMBEDDING_MODEL = "models/text-embedding-004"
CHAT_MODEL      = "models/gemini-2.5-flash"

RUBRIC_CSV_PATH = r"data/rubric.csv"
K_NEIGHBORS     = 3