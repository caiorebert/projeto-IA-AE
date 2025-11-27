import streamlit as st
import numpy as np
import faiss
from openai import OpenAI
from openai import OpenAIError

import config
from rag.embeddings import init_vector_store

client = OpenAI(api_key=config.OPENAI_API_KEY)

def retrieve_context(user_text: str, index: faiss.Index, df_rubric: any, k: int = config.K_NEIGHBORS) -> str:
    try:
        res = client.embeddings.create(input=user_text, model=config.EMBEDDING_MODEL)
        emb = np.array(res.data[0].embedding, dtype="float32")
        if emb.ndim == 1:
            emb = emb.reshape(1, -1)
        faiss.normalize_L2(emb)
    except OpenAIError as e:
        st.error(f"Erro ao gerar embedding do usuário: {e}")
        return ""

    _, I = index.search(emb, k)
    contexts = df_rubric.iloc[I[0]]["criteria"].tolist()
    return "\n".join(contexts)
