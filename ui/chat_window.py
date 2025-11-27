import streamlit as st

def render_chat_window(chat_history: list[dict]):
    for i, entry in enumerate(chat_history, start=1):
        orig = entry.get("texto_original", "")
        st.markdown(f"**Interação {i}**")
        st.markdown("**Texto Original:**")
        st.write(orig)
        st.markdown("**Métricas e Correção (JSON):**")
        st.json({k: v for k, v in entry.items() if k != "texto_original"})
        st.markdown("---")
