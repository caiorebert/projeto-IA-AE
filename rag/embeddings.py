import pandas as pd
import numpy as np
import faiss
import streamlit as st
from openai import OpenAI, OpenAIError
from config import OPENAI_API_KEY, EMBEDDING_MODEL, RUBRIC_CSV_PATH

client = OpenAI(api_key=OPENAI_API_KEY)

def load_rubric_embeddings(
    rubric_csv_path: str = RUBRIC_CSV_PATH,
    embed_model: str = EMBEDDING_MODEL
) -> tuple[pd.DataFrame, faiss.Index]:
    df = pd.read_csv(rubric_csv_path)
    texts = df["criteria"].astype(str).tolist()

    embeddings = []
    for text in texts:
        try:
            res = client.embeddings.create(input=text, model=embed_model)
            emb = np.array(res.data[0].embedding, dtype="float32")
            embeddings.append(emb)
        except OpenAIError as e:
            st.error(f"Erro ao gerar embedding para '{text[:30]}...': {e}")
            if embeddings:
                dim = embeddings[0].shape[0]
            else:
                dim = 1536
            embeddings.append(np.zeros(dim, dtype="float32"))

    emb_matrix = np.vstack(embeddings)
    if emb_matrix.ndim == 1:
        emb_matrix = emb_matrix.reshape(1, -1)

    faiss.normalize_L2(emb_matrix)

    dim = emb_matrix.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(emb_matrix)

    return df, index

def init_vector_store() -> tuple[pd.DataFrame, faiss.Index]:
    return load_rubric_embeddings()

def retrieve_context(query: str, _index: faiss.Index, df: pd.DataFrame, embed_model: str = EMBEDDING_MODEL) -> str:
    res = client.embeddings.create(input=query, model=embed_model)
    emb = np.array(res.data[0].embedding, dtype="float32")

    if emb.ndim == 1:
        emb = emb.reshape(1, -1)

    faiss.normalize_L2(emb)

    D, I = _index.search(emb, 1)

    idx = I[0][0]
    if idx < 0 or idx >= len(df):
        return ""

    return df.iloc[idx]["criteria"]
