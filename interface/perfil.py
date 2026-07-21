import streamlit as st
from interface.utils import usuario_atual, logout
from services.usuario_service import atualizar_usuario, excluir_usuario
from services.redis_service import listar_historico
from services.pet_service import (
    criar_pet,
    adicionar_pet,
    excluir_pet,
    buscar_detalhes_pet
)

def tela_perfil():
    usuario = usuario_atual()

    st.title("👤 Meu perfil")

    with st.form("editar_perfil"):
        nome = st.text_input("Nome", usuario.get("nome", ""))
        telefone = st.text_input("Telefone", usuario.get("telefone", ""))
        cidade = st.text_input("Cidade", usuario.get("cidade", ""))
        bio = st.text_area("Bio", usuario.get("bio", ""))

        salvar = st.form_submit_button("Salvar alterações")

    if salvar:
        atualizar_usuario(
            str(usuario["_id"]),
            {
                "nome": nome,
                "telefone": telefone,
                "cidade": cidade,
                "bio": bio
            }
        )

        st.success("Perfil atualizado.")
        st.rerun()

    st.divider()
    st.subheader("🐶 Meus pets")

    for pet in usuario.get("box_pets", []):
        foto = pet.get("foto", "").strip()

        if foto.startswith("http"):
            st.image(foto, use_container_width=True)
        else:
            st.warning("📷 Este pet ainda não possui foto válida.")

        st.write(f"**Nome:** {pet['nome']}")
        st.write(f"**Raça:** {pet['raca']}")

        if st.button(f"Excluir {pet['nome']}"):
            excluir_pet(str(usuario["_id"]), pet["id_pet"])
            st.warning("Pet excluído.")
            st.rerun()

    st.divider()
    st.subheader("Adicionar novo pet")

    with st.form("novo_pet"):
        nome_pet = st.text_input("Nome do pet")
        raca = st.text_input("Raça")
        idade = st.number_input("Idade", min_value=0, step=1)
        sexo = st.selectbox("Sexo", ["Macho", "Fêmea"])
        status_vacinal = st.selectbox("Status vacinal", ["Completo", "Incompleto"])
        documentacao = st.selectbox("Documentação", ["Em dia", "Pendente"])
        foto = st.text_input("Link da foto")

        adicionar = st.form_submit_button("Adicionar pet")

    if adicionar:
        pet = criar_pet(
            nome_pet,
            raca,
            idade,
            sexo,
            status_vacinal,
            documentacao,
            foto
        )

        adicionar_pet(str(usuario["_id"]), pet)
        st.success("Pet adicionado.")
        st.rerun()

    st.divider()
    
    st.subheader("🕒 Últimos pets visualizados")

    historico = listar_historico(str(usuario["_id"]))

    if historico:

        for id_pet in historico:

            resultado = buscar_detalhes_pet(id_pet)

            if resultado is None:
                continue

        pet = resultado["pet"]

        st.markdown("---")

        foto = pet.get("foto", "").strip()

        if foto.startswith("http"):
            st.image(foto, width=200)

        st.write(f"**🐶 Nome:** {pet['nome']}")
        st.write(f"**🐕 Raça:** {pet['raca']}")
        st.write(f"**🎂 Idade:** {pet['idade']} anos")
        st.write(f"**👤 Tutor:** {resultado['nome_tutor']}")
        st.write(f"**📍 Cidade:** {resultado['cidade']}")

    else:
        st.info("Você ainda não visualizou nenhum pet.")

    if st.button("Sair"):
        logout()

    if st.button("Excluir minha conta"):
        excluir_usuario(str(usuario["_id"]))
        st.session_state.usuario_logado = None
        st.warning("Conta excluída.")
        st.rerun()