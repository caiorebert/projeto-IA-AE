import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
    
import streamlit as st
from rag.embeddings import init_vector_store
from rag.retriever import retrieve_context
from rag.chat import correct_text
from ui.sidebar import render_sidebar
from ui.chat_window import render_chat_window
from ui.dashboard import render_dashboard
import json
import re

# --- CONFIGURAÇÃO DE SEGURANÇA ---
# Se a IA falhar, usamos estes valores para não quebrar o gráfico
DEFAULT_METRICS = {
    "nota_final": 0,
    "nota_c1": 0, "nota_c2": 0, "nota_c3": 0, "nota_c4": 0, "nota_c5": 0,
    "metrica_um": 0, "metrica_dois": 0, "metrica_tres": 0,
    "metrica_quatro": 0, "metrica_cinco": 0, "metrica_seis": 0,
    "metrica_sete": 0, "metrica_oito": 0, "metrica_nove": 0,
    "metrica_dez": 0, "metrica_onze": "Neutro",
    "anulacao": ""
}

def extract_metrics_from_response(response: str) -> dict:
    try:
        return json.loads(response)
    except Exception:
        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except Exception:
                return {}
        return {}

def main():
    # 1. INJEÇÃO DE CSS (Tema Escuro)
    st.markdown(
        """
        <style>
        .main { background-color: #1a1a1a; color: #e0e0e0; }
        .st-emotion-cache-pzb4s5, .st-emotion-cache-121ab-8u, .st-emotion-cache-163m6m5 { 
            background-color: #262626 !important; color: #cccccc; 
        }
        h1, h2, h3, h4 { color: #64ffda; }
        .stButton>button {
            background-color: #00897B; border: none; color: white;
            border-radius: 8px; padding: 10px 24px;
        }
        .stButton>button:hover { background-color: #006b5b; }
        .stTextArea, .stTextInput > div > div > input, .stTextInput > div > div > textarea {
            background-color: #333333 !important; color: #E0E0E0 !important;
            border-radius: 5px; padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    user_text, submit = render_sidebar()
    df_rubric, index = init_vector_store()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 2. HEADER
    st.markdown(
        """
        <div style='padding: 20px; border-radius: 12px; background-color: #2e2e2e; border-left: 5px solid #64FFDA; box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.4);'>
            <h1 style='color: #64FFDA; margin-bottom: 5px; font-size: 30px;'>RAG ENEM Dashboard | IA</h1>
            <p style='color: #DDDDDD; font-size: 16px; margin-top: 0;'>
                Bem-vindo(a), <b>Caio Rebert</b>!
                <br>
                Ferramenta de correção de redações com Gemini AI e RAG.
            </p>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )
    
    if submit and user_text.strip():
        with st.spinner("Analisando redação com IA..."):
            context = retrieve_context(user_text, index, df_rubric)
            corrected = correct_text(user_text, context)
            
            # --- CORREÇÃO DO ERRO KEYERROR ---
            extracted = extract_metrics_from_response(corrected)
            
            # Começa com os zeros padrão e atualiza se a IA mandou algo válido
            final_metrics = DEFAULT_METRICS.copy()
            if extracted:
                final_metrics.update(extracted)
            
            final_metrics["texto_original"] = user_text
            final_metrics["Interação"] = len(st.session_state.chat_history) + 1
            
            st.session_state.chat_history.append(final_metrics)

    #render_chat_window(st.session_state.chat_history)
    render_dashboard(st.session_state.chat_history)

if __name__ == "__main__":
    main()