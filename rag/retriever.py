import streamlit as st
import numpy as np
import faiss
import google.generativeai as genai

import config

def retrieve_context(user_text: str, index: faiss.Index, df_rubric: any, k: int = config.K_NEIGHBORS) -> str:
    try:
        # Gera embedding da pergunta do usuário
        res = genai.embed_content(
            model=config.EMBEDDING_MODEL,
            content=user_text,
            task_type="retrieval_query" # Otimiza para a pergunta de busca
        )
        emb = np.array(res['embedding'], dtype="float32")
        
        if emb.ndim == 1:
            emb = emb.reshape(1, -1)
        
        faiss.normalize_L2(emb)
        
        # Realiza a busca no índice FAISS
        _, I = index.search(emb, k)
        contexts = df_rubric.iloc[I[0]]["criteria"].tolist()
        return "\n".join(contexts)

    except Exception as e:
        st.error(f"Erro ao gerar embedding do usuário: {e}")
        return ""