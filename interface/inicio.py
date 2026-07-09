import streamlit as st
from services.usuario_service import login

def tela_inicio():
    st.title("🐾 PawMatch")
    st.subheader("O app de relacionamento para pets")

    st.write("Entre, explore pets, dê curtidas, receba matches e converse com outros tutores.")

    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = login(email, senha)

        if usuario:
            st.session_state.usuario_logado = str(usuario["_id"])
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("E-mail ou senha inválidos.")