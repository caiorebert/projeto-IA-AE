import json
from typing import Optional
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile

def load_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_json_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return json.dumps(data, ensure_ascii=False, indent=2)

def load_uploaded_file(uploaded_file: UploadedFile) -> str:
    raw = uploaded_file.read().decode("utf-8")
    if (uploaded_file.type=="application/json" 
        or uploaded_file.name.lower().endswith(".json")):
        try:
            df = pd.read_json(raw)
            return df.to_string(index=False)
        except ValueError:
            data = json.loads(raw)
            return json.dumps(data, ensure_ascii=False, indent=2)
    return raw

def get_user_text(uploaded_file: Optional[UploadedFile], direct_input: str) -> str:
    if uploaded_file is not None:
        return load_uploaded_file(uploaded_file)
    return direct_input or ""
