import streamlit as st
import json
from openai import OpenAI, OpenAIError
from config import OPENAI_API_KEY, CHAT_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

system_prompt_base = """
Você é um corretor automatizado especialista na Matriz de Referência da Redação do ENEM 2024, avaliando textos dissertativo-argumentativos conforme os critérios oficiais do INEP.

Antes de tudo, verifique se a redação deve ser anulada (nota 0 total) por algum destes motivos:
- Fuga total ao tema
- Não atendimento ao tipo textual dissertativo-argumentativo
- Texto com até 7 linhas
- Parte deliberadamente desconectada do tema
- Texto ilegível ou em branco
- Presença de impropérios, desenhos ou sinais de identificação
- Texto escrito em língua estrangeira
- Cópia integral ou parcial dos textos motivadores (linhas copiadas devem ser desconsideradas)

Se houver anulação, retorne nota 0 em todas as competências.

Caso contrário, avalie as 5 competências, atribuindo nota entre 0 e 200 conforme a cartilha oficial. Justifique com base no texto.

As competências são:
1. Domínio da modalidade escrita formal da língua portuguesa
2. Compreensão do tema e aplicação de conhecimentos
3. Seleção e organização de argumentos
4. Coesão textual
5. Proposta de intervenção

Além disso, informe as seguintes métricas:
- metrica_um: erros de pontuação
- metrica_dois: erros de acentuação
- metrica_tres: erros de grafia
- metrica_quatro: erros de concordância verbal
- metrica_cinco: erros de concordância nominal
- metrica_seis: nota da coerência textual
- metrica_sete: quantidade de conectivos usados
- metrica_oito: variedade vocabular do vocabulário
- metrica_nove: quantidade geral de erros gramaticais
- metrica_dez: comprimento do texto em número de palavras
- metrica_onze: sentimento predominante no texto (positivo, neutro ou negativo)

Retorne **apenas** um JSON no formato:

{
  "nota_final": c1 + c2 + c3 +c 4 + c5,
  "nota_c1": valor,
  "nota_c2": valor,
  "nota_c3": valor,
  "nota_c4": valor,
  "nota_c5": valor,
  "metrica_um": valor,
  "metrica_dois": valor,
  "metrica_tres": valor,
  "metrica_quatro": valor,
  "metrica_cinco": valor,
  "metrica_seis": valor,
  "metrica_sete": valor,
  "metrica_oito": valor,
  "metrica_nove": valor,
  "metrica_dez": valor,
  "metrica_onze": valor,
  "anulacao": ""  // use string vazia se não houver anulação
}

Não inclua texto, explicações ou qualquer outro conteúdo além deste JSON.
"""

@st.cache_resource
def correct_text(user_text: str, system_context: str = "") -> str:
    prompt = system_prompt_base.strip()
    if system_context:
        prompt += "\n\nContexto adicional:\n" + system_context

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_text.strip()}
    ]

    try:
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages
        )
        return response.choices[0].message.content.strip()
    except (OpenAIError, json.JSONDecodeError) as e:
        st.error(f"Erro na API ou na conversão do JSON: {e}")
        return "{}"

