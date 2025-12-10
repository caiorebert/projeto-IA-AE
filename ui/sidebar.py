import streamlit as st

def render_sidebar(user_name="Usuário"):
    sb = st.sidebar

    if "history" not in st.session_state:
        st.session_state.history = []

    with sb.form(key='sidebar_form'):
        st.markdown("### 1. Upload de Arquivos")
        uploaded_files = st.file_uploader(
            "Envie arquivos de texto (.txt) ou JSON (.json)", 
            type=["txt", "json"], 
            accept_multiple_files=True
        )
        
        st.markdown("### 2. Ou cole o texto")
        user_text = st.text_area(
            "Cole sua redação aqui:", 
            height=200,
            placeholder="Digite ou cole seu texto..."
        )
        
        submit = st.form_submit_button("Enviar para Correção")

    return uploaded_files, user_text, submit