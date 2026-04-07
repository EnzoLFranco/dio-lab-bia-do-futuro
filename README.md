# CentavoBot: Assistente Financeiro de Controle de Gastos

Este projeto foi desenvolvido como parte de um desafio de IA Generativa focado na criação de agentes inteligentes. O **CentavoBot** é um assistente proativo que resolve o problema da fricção no registro manual de despesas diárias, utilizando IA local para extrair dados de texto livre e integrá-los a uma base de dados local de forma segura e estruturada.

---

## 🚀 Como Executar o Projeto

**1. Requisitos:**
- Python 3.10+
- [Ollama](https://ollama.ai/) instalado e rodando localmente (com o modelo `llama3.2`)

**2. Instalação das dependências:**
Abra o terminal e execute o comando abaixo para instalar as bibliotecas necessárias:
```bash
pip install streamlit pandas requests datasets --user
```

**3. Preparação da Base de Dados:**
Antes de iniciar o chat, execute o script de ETL para gerar o histórico inicial de transações e os limites de orçamento simulados:

```Bash
python scripts/preparar_dados_hf.py
```

**4. Iniciando a Interface:**
Com os dados criados, suba a aplicação web interativa:

```Bash
python -m streamlit run src/app.py
```

## 🛠️ Arquitetura e Funcionalidades
**1. Caso de Uso**

O CentavoBot atua como um companheiro de bolso. O usuário envia mensagens simples como "Gastei 50 no mercado hoje" e a IA executa as seguintes ações em segundo plano:

Identifica o valor (50.00) e a categoria (Alimentação).

Salva os dados estruturados em um arquivo CSV.

Consulta um arquivo JSON de limites de orçamento definidos previamente.

Responde no chat avisando se o gasto está dentro do planejado ou se o teto foi atingido.

**2. Stack Tecnológica**
**Backend:** Python com a biblioteca Pandas para lógica determinística (cálculo de saldo e manipulação de arquivos).

**Interface:** Streamlit para interação rápida via chat.

**LLM Local:** Ollama (Llama 3.2 3B) para extração de entidades (Function Calling). Garante processamento ágil, sem custo de tokens de API em nuvem e com total privacidade dos dados financeiros.

**Armazenamento:** Arquivos locais (.csv e .json), garantindo leveza e portabilidade (fácil exportação para o Excel).

**3. Estratégia Anti-Alucinação (Segurança)**

**Double-Call:** A primeira chamada de IA é exclusiva para estruturar dados (retornando apenas um JSON válido). A lógica matemática (soma de gastos e limite) é feita pelo Python (Pandas), não pela IA. A IA só volta a atuar para gerar o texto final.

**Escopo Fechado:** O sistema é instruído via System Prompt a recusar perguntas sobre investimentos complexos, limitando-se ao fluxo de caixa diário.

**Confirmação Visual:** O bot é forçado a sempre repetir o valor e a categoria compreendidos na resposta, permitindo a validação imediata do usuário.

## 📂 Estrutura de Pastas

```
📁 lab-agente-financeiro/
│
├── 📄 README.md          # Esta documentação
│
├── 📁 data/                          # Armazenamento Local
│   ├── orcamento_mensal.json         # Limites por categoria 
│   └── historico_transacoes.csv      # Histórico salvo pelo Pandas
│
├── 📁 scripts/                       # Pipelines
│   └── preparar_dados_hf.py          # Script gerador de mock data financeiro
│
└── 📁 src/                           # Código Fonte Principal
    ├── app.py                        # Interface do Chatbot (Streamlit)
    └── agente.py                     # Orquestração do LLM e lógica do Pandas
```