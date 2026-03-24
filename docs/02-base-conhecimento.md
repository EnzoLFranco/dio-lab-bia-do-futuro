# Base de Conhecimento

## Dados Utilizados
A base foi estruturada em arquivos locais visando a leitura ágil e a manipulação em memória.

| Arquivo                     | Formato | Utilização no Agente |
|----------------------------|--------|----------------------|
| historico_transacoes.csv   | CSV    | Armazenar e consultar os gastos diários do usuário para cálculo de saldo e análise de tendências. |
| orcamento_mensal.json      | JSON   | Definir os tetos de gastos por categoria (ex: Alimentação, Lazer) estabelecidos pelo usuário. |
| regras_financeiras.json    | JSON   | Base de conhecimento com dicas de economia e boas práticas para embasar as recomendações geradas. |

> [!TIP]
> Quer um dataset mais robusto? O histórico inicial de testes foi populado utilizando recortes do dataset público **mitulshah/transaction-categorization (Hugging Face)**.  
> Os dados foram filtrados via script para representar o histórico de consumo realista de um jovem trabalhador durante 3 meses.

---

## Adaptações nos Dados

Você modificou ou expandiu os dados mockados? Descreva aqui.

A base de dados original do desafio (focada em investimentos e perfis de risco) foi totalmente substituída para se alinhar ao domínio de controle de gastos.

- **Perfil do Usuário:**  
  O JSON perdeu campos estáticos como `perfil_investidor` e `produtos_financeiros`, passando a armazenar chaves dinâmicas de limites, como `limite_categoria`.

- **Transações:**  
  O CSV foi expandido com dados sintéticos de consumo do dia a dia (supermercado, streamings, transporte) para permitir que a IA identifique padrões e faça projeções.  
  Exemplo: *"Atenção, você gasta em média 30% da sua renda em transporte".*

---

## Estratégia de Integração

### Como os dados são carregados?
Descreva como seu agente acessa a base de conhecimento.

Os arquivos CSV e JSON são lidos em memória pelo backend em Python utilizando a biblioteca **Pandas** no momento em que a requisição do usuário chega.  
O script realiza sumarizações prévias (ex: agrupar gastos do mês por categoria) para evitar sobrecarga de tokens e poupar a IA de realizar cálculos matemáticos complexos.

---

### Como os dados são usados no prompt?
Os dados vão no system prompt? São consultados dinamicamente?

A base de dados nunca é enviada na íntegra.  
O backend formata um resumo contextualizado (contendo apenas o mês vigente, o status do orçamento e as últimas 3 transações) e injeta esse bloco dinamicamente como uma variável no **System Prompt** do LLM, orientando a resposta antes de processar a mensagem do usuário.

---

## Exemplo de Contexto Montado

Mostre um exemplo de como os dados são formatados para o agente.

```plaintext
Dados do Cliente e Contexto Interno:
- Mês Atual: Outubro/2025
- Orçamento de Alimentação: R$ 800,00 (Gasto: R$ 650,00 | Resta: R$ 150,00)
- Orçamento de Lazer: R$ 300,00 (Gasto: R$ 320,00 | Status: ESTOURADO em R$ 20,00)

Últimas 3 transações registradas:
- 25/10: Combustível (Transporte) - R$ 250,00
- 20/10: Academia (Saúde) - R$ 99,00
- 15/10: Conta de Luz (Moradia) - R$ 180,00

Diretriz de recomendação do sistema: O usuário ultrapassou o teto de lazer. Sugira economia nos próximos dias.

[Mensagem do Usuário]
"Acabei de gastar 80 conto numa pizza no iFood"
