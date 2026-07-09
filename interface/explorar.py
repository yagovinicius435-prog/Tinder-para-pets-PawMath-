import streamlit as st
from interface.utils import usuario_atual, card_pet
from services.pet_service import listar_pets_para_explorar
from services.swipe_service import usuario_ja_avaliou, registrar_swipe

def tela_explorar():
    usuario = usuario_atual()

    st.title("🔎 Explorar pets")

    if not usuario.get("box_pets"):
        st.warning("Cadastre um pet primeiro.")
        return

    pets = listar_pets_para_explorar(usuario)

    pets_disponiveis = []

    for tutor, pet in pets:
        if not usuario_ja_avaliou(str(usuario["_id"]), pet["id_pet"]):
            pets_disponiveis.append((tutor, pet))

    if not pets_disponiveis:
        st.info("Você já avaliou todos os pets disponíveis.")
        return

    tutor, pet = pets_disponiveis[0]

    card_pet(tutor, pet)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❌ Rejeitar"):
            registrar_swipe(usuario, pet, "dislike")
            st.rerun()

    with col2:
        if st.button("❤️ Curtir"):
            deu_match = registrar_swipe(usuario, pet, "like")

            if deu_match:
                st.balloons()
                st.success("🎉 Deu Match!")

            st.rerun()