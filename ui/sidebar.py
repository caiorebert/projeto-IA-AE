import streamlit as st

def render_sidebar(user_name="Usuário"):
    # injeta CSS para dark theme, largura fixa, bolhas e input estilizado
    st.markdown(
        """
        <style>
          /* sidebar escura + largura fixa */
          [data-testid="stSidebar"] {
            background-color: #202124 !important;
            width: 450px !important;
          }
          /* texto geral branco */
          [data-testid="stSidebar"] * {
            color: #ffffff !important;
          }
          /* saudação centralizada */
          .sidebar-greeting {
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1.2rem;
            padding: 1rem 0;
          }
          /* container do chat */
          .chat-container {
            height: 60vh;
            padding: 0 0.5rem;
            overflow-y: auto;
          }
          /* bolhas de mensagem */
          .chat-bubble {
            padding: 0.6rem 1rem;
            margin: 0.4rem 0;
            border-radius: 1rem;
            max-width: 80%;
            line-height: 1.4;
          }
          .chat-bubble.user {
            background: #4A90E2;
            color: #fff;
            margin-left: auto;
          }
          .chat-bubble.assistant {
            background: #3c4043;
            color: #fff;
            margin-right: auto;
          }
          /* textarea estilo input de chat */
          [data-testid="stSidebar"] .stTextArea textarea {
            background: #303134 !important;
            border: none !important;
            border-radius: 1rem !important;
            padding: 0.8rem !important;
            min-height: 100px;
            color: #fff !important;
          }
          /* botão full‑width arredondado */
          [data-testid="stSidebar"] .stButton>button {
            background-color: #4A90E2 !important;
            border: none !important;
            border-radius: 1rem !important;
            width: 100% !important;
            padding: 0.6rem 0 !important;
            font-size: 1rem !important;
            color: #fff !important;
            margin-top: 0.5rem !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

    sb = st.sidebar

    # 1) saudação
    sb.markdown(
        f'<div class="sidebar-greeting">Hi, Clézio</div>',
        unsafe_allow_html=True
    )

    # 2) histórico de mensagens
    if "history" not in st.session_state:
        st.session_state.history = []

    chat_area = sb.container()
    chat_area.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.history:
        role = msg["role"]        # "user" ou "assistant"
        content = msg["content"]
        bubble = f'<div class="chat-bubble {role}">{content}</div>'
        chat_area.markdown(bubble, unsafe_allow_html=True)
    chat_area.markdown('</div>', unsafe_allow_html=True)

    # 3) campo de input
    user_text = sb.text_area(
        "", 
        placeholder="Insert Text", 
        key="chat_input"
    )
    submit = sb.button("Send")

    return user_text, submit
