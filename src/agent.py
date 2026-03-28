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
def gerar_resposta_ollama(dados_json, status_orcamento):
    """Passo 2: Pede para o LLM gerar a resposta amigável do CentavoBot."""
    contexto = f"""
    [Dados Registrados no Sistema]
    Valor: R$ {dados_json['valor']}
    Categoria: {dados_json['categoria']}
    Status do Orçamento: {status_orcamento}
    """
    
    prompt = f"{SYSTEM_PROMPT_BOT}\n\n{contexto}\n\nGere a resposta para o usuário confirmando o registro."
    
    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": False
    }
    
    resposta = requests.post(OLLAMA_URL, json=payload)
    return resposta.json()['response']

# Orquestrador
def processar_gasto(mensagem_usuario):
    print("1. Extraindo dados da mensagem...")
    dados = extrair_json_ollama(mensagem_usuario)
    print(f"   -> JSON Extraído: {dados}")
    
    status_mockado = "O usuário ainda tem folga no orçamento desta categoria."
    
    print("2. Gerando resposta do CentavoBot...")
    resposta_final = gerar_resposta_ollama(dados, status_mockado)
    
    return resposta_final

# Teste rápido
if __name__ == "__main__":
    msg_teste = "Paguei 25 reais num lanche na padaria agora"
    print(f"Mensagem do usuário: '{msg_teste}'\n")
    
    resultado = processar_gasto(msg_teste)
    
    print("\n--- RESPOSTA DO CENTAVOBOT ---")
    print(resultado)
