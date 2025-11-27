import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
    
import streamlit as st
from rag.embeddings import init_vector_store, retrieve_context
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
    user_text, submit = render_sidebar()
    df_rubric, index = init_vector_store()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

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
