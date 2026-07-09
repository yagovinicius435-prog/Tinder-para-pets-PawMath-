import streamlit as st
from services.usuario_service import criar_usuario, buscar_usuario_por_email
from services.pet_service import criar_pet

def tela_cadastro():
    st.title("➕ Criar perfil")

    with st.form("cadastro"):
        st.subheader("Dados do tutor")

        nome = st.text_input("Nome")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        telefone = st.text_input("Telefone")
        cidade = st.text_input("Cidade")
        bio = st.text_area("Bio")

        st.subheader("Dados do pet")

        nome_pet = st.text_input("Nome do pet")
        raca = st.text_input("Raça")
        idade = st.number_input("Idade", min_value=0, step=1)
        sexo = st.selectbox("Sexo", ["Macho", "Fêmea"])
        status_vacinal = st.selectbox("Status vacinal", ["Completo", "Incompleto"])
        documentacao = st.selectbox("Documentação", ["Em dia", "Pendente"])
        foto = st.text_input("Link da foto")

        enviar = st.form_submit_button("Criar conta")

    if enviar:
        if buscar_usuario_por_email(email):
            st.error("Já existe usuário com esse e-mail.")
            return

        pet = criar_pet(
            nome_pet,
            raca,
            idade,
            sexo,
            status_vacinal,
            documentacao,
            foto
        )

        novo_usuario = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "telefone": telefone,
            "cidade": cidade,
            "bio": bio,
            "box_pets": [pet]
        }

        criar_usuario(novo_usuario)

        st.success("Conta criada com sucesso! Faça login para entrar.")