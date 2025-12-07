import google.generativeai as genai
import os
import toml

# Tenta carregar a API Key do arquivo secrets.toml
try:
    secrets = toml.load(".streamlit/secrets.toml")
    api_key = secrets.get("gemini_api_key")
    if not api_key:
        print("❌ Chave 'gemini_api_key' não encontrada no secrets.toml")
        exit()
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"❌ Erro ao ler secrets.toml: {e}")
    exit()

print("🔍 Listando modelos disponíveis para sua chave...\n")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Modelo de Chat: {m.name}")
        if 'embedContent' in m.supported_generation_methods:
            print(f"🔹 Modelo de Embedding: {m.name}")
except Exception as e:
    print(f"❌ Erro ao conectar na API: {e}")