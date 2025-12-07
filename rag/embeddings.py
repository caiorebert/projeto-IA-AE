import pandas as pd
import numpy as np
import faiss
import streamlit as st
import google.generativeai as genai
from config import EMBEDDING_MODEL, RUBRIC_CSV_PATH

def load_rubric_embeddings(
    rubric_csv_path: str = RUBRIC_CSV_PATH,
    embed_model: str = EMBEDDING_MODEL
) -> tuple[pd.DataFrame, faiss.Index]:
    df = pd.read_csv(rubric_csv_path)
    texts = df["criteria"].astype(str).tolist()

    embeddings = []
    for text in texts:
        try:
            # A chamada do Gemini para embeddings
            res = genai.embed_content(
                model=embed_model,
                content=text,
                task_type="retrieval_document" # Otimiza para documentos sendo indexados
            )
            emb = np.array(res['embedding'], dtype="float32")
            embeddings.append(emb)
        except Exception as e:
            st.error(f"Erro ao gerar embedding para '{text[:30]}...': {e}")
            # Fallback para dimensão 768 (padrão do text-embedding-004)
            if embeddings:
                dim = embeddings[0].shape[0]
            else:
                dim = 768 
            embeddings.append(np.zeros(dim, dtype="float32"))

    emb_matrix = np.vstack(embeddings)
    if emb_matrix.ndim == 1:
        emb_matrix = emb_matrix.reshape(1, -1)

    faiss.normalize_L2(emb_matrix)

    dim = emb_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(emb_matrix)

    return df, index

# A função init_vector_store permanece igual, chamando a load_rubric_embeddings
def init_vector_store() -> tuple[pd.DataFrame, faiss.Index]:
    return load_rubric_embeddings()