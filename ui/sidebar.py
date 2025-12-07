import streamlit as st

def render_sidebar(user_name="Usuário"):
    
    sb = st.sidebar

    if "history" not in st.session_state:
        st.session_state.history = []

    with sb.form(key='sidebar_form'):
        user_text = st.text_area(
            "Digite sua redação aqui:", 
            height=300,
            placeholder="Cole seu texto aqui..."
        )
        submit = st.form_submit_button("Enviar para Correção")

    return user_text, submit