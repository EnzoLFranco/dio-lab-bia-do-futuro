import streamlit as st
from agent import processar_gasto

# Configuração da página
st.set_page_config(
    page_title="CentavoBot - Controle de Gastos",
    page_icon="🪙",
    layout="centered"
)

st.title("🪙 CentavoBot")
st.markdown("O seu assistente financeiro rápido e sem atrito para o dia a dia! 🚀")

# Histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Saudação inicial (conforme a persona que documentamos)
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Opa! Tudo certo? Mandou, anotou. Qual foi o gasto de hoje?"
    })

# Renderizar as mensagens anteriores na tela
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input do usuário
if prompt := st.chat_input("Ex: Gastei 45 no iFood agora..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
    with st.chat_message("assistant"):
        with st.spinner("Processando e anotando na planilha..."):
            try:
                resposta_bot = processar_gasto(prompt)
                st.write(resposta_bot)
            except Exception as e:
                resposta_bot = f"Vish, deu um erro interno aqui: {e}"
                st.write(resposta_bot)
                
    st.session_state.messages.append({"role": "assistant", "content": resposta_bot})