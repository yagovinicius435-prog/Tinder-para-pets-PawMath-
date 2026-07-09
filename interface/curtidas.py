import streamlit as st
from bson import ObjectId

from db import usuarios, matches
from interface.utils import usuario_atual
from services.swipe_service import buscar_curtidas_recebidas, registrar_swipe


def tela_curtidas():
    usuario = usuario_atual()

    st.title("❤️ Quem curtiu meu pet")

    if "match_novo" in st.session_state:
        dados_match = st.session_state["match_novo"]

        st.success(
            f"🎉 Parabéns! Deu Match entre {dados_match['meu_pet']} e {dados_match['outro_pet']}!"
        )

        st.info("Agora vocês podem conversar na aba Matches.")

        if st.button("Ir para meus matches"):
            del st.session_state["match_novo"]
            st.session_state.pagina_atual = "💬 Matches"
            st.rerun()

        st.divider()

    if not usuario or not usuario.get("box_pets"):
        st.warning("Você precisa ter um pet cadastrado.")
        return

    meu_pet = usuario["box_pets"][0]

    curtidas = buscar_curtidas_recebidas(meu_pet)

    if not curtidas:
        st.info(f"Ninguém curtiu {meu_pet['nome']} ainda.")
        return

    encontrou_perfil = False

    for curtida in curtidas:
        tutor = usuarios.find_one({
            "_id": ObjectId(curtida["id_usuario"])
        })

        if not tutor or not tutor.get("box_pets"):
            continue

        if str(tutor["_id"]) == str(usuario["_id"]):
            continue

        pet_tutor = tutor["box_pets"][0]

        match_existente = matches.find_one({
            "$or": [
                {"id_pet1": meu_pet["id_pet"], "id_pet2": pet_tutor["id_pet"]},
                {"id_pet1": pet_tutor["id_pet"], "id_pet2": meu_pet["id_pet"]}
            ]
        })

        if match_existente:
            continue

        encontrou_perfil = True

        st.divider()

        foto = pet_tutor.get("foto", "").strip()

        if foto.startswith("http"):
            st.image(foto, use_container_width=True)
        else:
            st.warning("📷 Foto não disponível.")

        st.markdown(f"## 🐶 {pet_tutor['nome']}")
        st.write(f"**Raça:** {pet_tutor['raca']}")
        st.write(f"**Idade:** {pet_tutor['idade']} anos")
        st.write(f"**Sexo:** {pet_tutor['sexo']}")
        st.write(f"**Tutor:** {tutor['nome']}")
        st.write(f"**Cidade:** {tutor['cidade']}")
        st.write(f"**Bio do tutor:** {tutor.get('bio', '')}")

        st.info(f"{pet_tutor['nome']} curtiu o {meu_pet['nome']} ❤️")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"❌ Ignorar {pet_tutor['nome']}", key=f"ignorar_{pet_tutor['id_pet']}"):
                st.warning("Perfil ignorado.")
                st.rerun()

        with col2:
            if st.button(f"❤️ Curtir de volta {pet_tutor['nome']}", key=f"curtir_{pet_tutor['id_pet']}"):
                deu_match = registrar_swipe(usuario, pet_tutor, "like")

                if deu_match:
                    st.session_state["match_novo"] = {
                        "meu_pet": meu_pet["nome"],
                        "outro_pet": pet_tutor["nome"]
                    }

                st.rerun()

    if not encontrou_perfil:
        st.info("Todas as curtidas recebidas já viraram match.")