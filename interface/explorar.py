import streamlit as st
from interface.utils import usuario_atual, card_pet
from services.pet_service import listar_pets_para_explorar
from services.swipe_service import usuario_ja_avaliou, registrar_swipe
from services.redis_service import (
    adicionar_pet_visualizado,
    registrar_visualizacao,
    total_visualizacoes
)

def tela_explorar():
    usuario = usuario_atual()

    st.title("🔎 Explorar pets")

    if not usuario.get("box_pets"):
        st.warning("Cadastre um pet primeiro.")
        return

    pets = listar_pets_para_explorar(usuario)

    pets_disponiveis = [
        pet for pet in pets
        if not usuario_ja_avaliou(str(usuario["_id"]), pet["id_pet"])
    ]

    if not pets_disponiveis:
        st.info("Você já avaliou todos os pets disponíveis.")
        return

    # Índice do pet exibido
    if "indice_pet" not in st.session_state:
        st.session_state.indice_pet = 0

    # Garante que o índice nunca saia do intervalo
    if st.session_state.indice_pet >= len(pets_disponiveis):
        st.session_state.indice_pet = len(pets_disponiveis) - 1

    if st.session_state.indice_pet < 0:
        st.session_state.indice_pet = 0

    pet = pets_disponiveis[st.session_state.indice_pet]

    adicionar_pet_visualizado(str(usuario["_id"]), pet["id_pet"])
    registrar_visualizacao(pet["id_pet"], str(usuario["_id"]))

    tutor = {
        "nome": pet["nome_tutor"],
        "cidade": pet["cidade"],
        "bio": pet["bio"]
    }

    card_pet(tutor, pet)

    visualizacoes = total_visualizacoes(pet["id_pet"])

    st.caption(
        f"👀 Visualizado por aproximadamente {visualizacoes} usuário(s) diferente(s)"
    )

    st.write(
        f"Pet {st.session_state.indice_pet + 1} de {len(pets_disponiveis)}"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("⬅️ Anterior"):
            if st.session_state.indice_pet > 0:
                st.session_state.indice_pet -= 1
                st.rerun()

    with col2:
        if st.button("❌ Rejeitar"):
            registrar_swipe(usuario, pet, "dislike")

            if st.session_state.indice_pet >= len(pets_disponiveis) - 1:
                st.session_state.indice_pet = max(0, len(pets_disponiveis) - 2)

            st.rerun()

    with col3:
        if st.button("❤️ Curtir"):
            deu_match = registrar_swipe(usuario, pet, "like")

            if deu_match:
                st.balloons()
                st.success("🎉 Deu Match!")

            if st.session_state.indice_pet >= len(pets_disponiveis) - 1:
                st.session_state.indice_pet = max(0, len(pets_disponiveis) - 2)

            st.rerun()

    with col4:
        if st.button("➡️ Próximo"):
            if st.session_state.indice_pet < len(pets_disponiveis) - 1:
                st.session_state.indice_pet += 1
                st.rerun()