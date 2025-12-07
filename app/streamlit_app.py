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
    # 1. INJEÇÃO DE CSS PARA O NOVO TEMA ESCURO
    st.markdown(
        """
        <style>
        /* 1. Fundo Principal */
        .main {
            background-color: #1a1a1a; /* Fundo bem escuro */
            color: #e0e0e0;
        }
        /* 2. Sidebar (fundo e cor) */
        /* Nota: Seletor pode variar dependendo da versão do Streamlit, mas este é o mais comum */
        .st-emotion-cache-pzb4s5, .st-emotion-cache-121ab-8u, .st-emotion-cache-163m6m5 { 
            background-color: #262626 !important; 
            color: #cccccc;
        }
        /* 3. Estilo dos cabeçalhos e texto de destaque */
        h1, h2, h3, h4 {
            color: #64ffda; /* Verde água vibrante para destaque */
        }
        /* 4. Estilo dos botões */
        .stButton>button {
            background-color: #00897B;
            border: none;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
        }
        .stButton>button:hover {
            background-color: #006b5b;
        }
        /* 5. Cores das caixas de texto/input */
        .stTextArea, .stTextInput > div > div > input, .stTextInput > div > div > textarea {
            background-color: #333333 !important;
            color: #E0E0E0 !important;
            border-radius: 5px;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    user_text, submit = render_sidebar()
    df_rubric, index = init_vector_store()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 2. HEADER PERSONALIZADO (REAPAGINADO)
    st.markdown(
        """
        <div style='padding: 20px; border-radius: 12px; background-color: #2e2e2e; border-left: 5px solid #64FFDA; box-shadow: 0 4px 12px 0 rgba(0, 0, 0, 0.4);'>
            <h1 style='color: #64FFDA; margin-bottom: 5px; font-size: 30px;'>RAG ENEM Dashboard | IA</h1>
            <p style='color: #DDDDDD; font-size: 16px; margin-top: 0;'>
                Bem-vindo(a), Caio Rebert
                <br>
                Esta é a sua ferramenta de correção de redações baseada em Gemini e Retrieval-Augmented Generation (RAG).
                Insira sua redação na barra lateral e visualize a análise detalhada abaixo.
            </p>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )
    
    if submit and user_text.strip():
        context = retrieve_context(user_text, index, df_rubric)
        corrected = correct_text(user_text, context)
        metrics = extract_metrics_from_response(corrected)
        metrics["texto_original"] = user_text
        metrics["Interação"] = len(st.session_state.chat_history) + 1
        st.session_state.chat_history.append(metrics)

    #render_chat_window(st.session_state.chat_history)
    render_dashboard(st.session_state.chat_history)

if __name__ == "__main__":
    main()