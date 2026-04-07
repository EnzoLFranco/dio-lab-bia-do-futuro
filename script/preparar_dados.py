import pandas as pd
import random
from datetime import datetime, timedelta
import os
import json

# Garantir que a diretoria de dados existe
os.makedirs('../data', exist_ok=True)

def executar_geracao_dados():
    print("1. Gerando dados sintéticos de transações (Mock Data)...")
    
    categorias = ['Alimentacao', 'Transporte', 'Lazer', 'Saude', 'Moradia', 'Outros']
    descricoes = {
        'Alimentacao': ['iFood', 'Mercado', 'Padaria', 'Restaurante', 'Lanchonete'],
        'Transporte': ['Uber', 'Posto de Gasolina', 'Metrô', 'Estacionamento'],
        'Lazer': ['Cinema', 'Netflix', 'Spotify', 'Show', 'Barzinho'],
        'Saude': ['Farmácia', 'Consulta Médica', 'Academia', 'Suplementos'],
        'Moradia': ['Conta de Luz', 'Internet', 'Aluguel', 'Condomínio', 'Água'],
        'Outros': ['Presente', 'Petshop', 'Papelaria', 'Manutenção']
    }
    
    dados = []
    hoje = datetime.now()
    
    # Gerar 200 transações espalhadas pelos últimos 90 dias
    for _ in range(200):
        categoria = random.choice(categorias)
        descricao = random.choice(descricoes[categoria])
        
        # Gerar valores realistas com base na categoria
        if categoria == 'Moradia':
            valor = round(random.uniform(100.0, 1500.0), 2)
        elif categoria in ['Transporte', 'Alimentacao']:
            valor = round(random.uniform(15.0, 250.0), 2)
        else:
            valor = round(random.uniform(20.0, 150.0), 2)
            
        dias_atras = random.randint(0, 90)
        data_transacao = hoje - timedelta(days=dias_atras)
        
        dados.append({
            'data': data_transacao.strftime('%Y-%m-%d'),
            'descricao': descricao,
            'categoria': categoria,
            'valor': valor
        })
    
    print("2. Transformando e ordenando os dados...")
    df = pd.DataFrame(dados)
    # Ordenar por data (da mais antiga para a mais recente)
    df = df.sort_values(by='data').reset_index(drop=True)
    
    print("3. Carregando os dados no arquivo local (Load)...")
    caminho_csv = '../data/historico_transacoes.csv'
    df.to_csv(caminho_csv, index=False)
    print(f"✅ Sucesso! {len(df)} registros salvos em {caminho_csv}")

    # Criar o arquivo de orçamento (JSON)
    orcamento_base = {
        "limites": {
            "Alimentacao": 800.00,
            "Transporte": 400.00,
            "Lazer": 300.00,
            "Saude": 200.00,
            "Moradia": 1500.00,
            "Outros": 200.00
        }
    }
    
    caminho_json = '../data/orcamento_mensal.json'
    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(orcamento_base, f, indent=4)
    print(f"✅ Arquivo {caminho_json} criado com sucesso!")

if __name__ == "__main__":
    executar_geracao_dados()