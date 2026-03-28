import json
import requests
import pandas as pd
from datetime import datetime

# Configuração
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2" 

# Prompts
PROMPT_EXTRACAO = """
Você é um extrator de dados financeiro. Extraia o valor e a categoria da mensagem do usuário.
Responda APENAS com um objeto JSON válido. Não adicione nenhum texto antes ou depois do JSON.
Categorias permitidas: Alimentacao, Transporte, Lazer, Saude, Moradia, Outros.

Mensagem: "{mensagem}"
Saída Esperada: {{"valor": 45.0, "categoria": "Alimentacao"}}
"""

SYSTEM_PROMPT_BOT = """
Você é o CentavoBot, um assistente financeiro rápido e descontraído, especializado em controle de gastos diários.
REGRAS:
1. Tom informal, use 1 ou 2 emojis.
2. Responda em NO MÁXIMO 3 linhas.
3. SEMPRE repita o valor e a categoria que você registrou.
4. Baseie-se no status do orçamento fornecido para dar um breve conselho.
"""

# Conexão
def extrair_json_ollama(mensagem_usuario):
    """Passo 1: Pede para o LLM extrair os dados e devolver um JSON."""
    prompt = PROMPT_EXTRACAO.format(mensagem=mensagem_usuario)
    
    payload = {
        "model": MODELO,
        "prompt": prompt,
        "format": "json", 
        "stream": False
    }
    
    resposta = requests.post(OLLAMA_URL, json=payload)
    dados = resposta.json()['response']
    
    try:
        return json.loads(dados)
    except json.JSONDecodeError:
        return {"valor": 0.0, "categoria": "Outros"}

