import streamlit as st
from interface.utils import usuario_atual
from services.match_service import listar_matches_usuario, desfazer_match
from services.pet_service import buscar_pet_por_id
from services.chat_service import enviar_mensagem

def tela_matches():
    usuario = usuario_atual()

    st.title("💬 Meus Matches")

    meus_matches = listar_matches_usuario(str(usuario["_id"]))

    if not meus_matches:
        st.info("Você ainda não tem matches.")
        return

    for match in meus_matches:
        if match["id_usuario1"] == str(usuario["_id"]):
            outro_pet_id = match["id_pet2"]
        else:
            outro_pet_id = match["id_pet1"]

        tutor, pet = buscar_pet_por_id(outro_pet_id)

        if not tutor or not pet:
            continue

        st.divider()

        st.markdown(f"## 🐾 Match com {pet['nome']}")
        st.write(f"**Tutor:** {tutor['nome']}")
        st.write(f"**Cidade:** {tutor['cidade']}")

        foto = pet.get("foto", "").strip()

        if foto.startswith("http"):
            st.image(foto, use_container_width=True)
        else:
            st.warning("📷 Foto não disponível.")

        with st.expander("💬 Abrir conversa"):
            mensagens = match.get("chat_completo", [])

            if not mensagens:
                st.info("Comece a conversa para marcar um encontro dos pets.")

            for msg in mensagens:
                remetente = "Você" if msg["id_usuario_remetente"] == str(usuario["_id"]) else tutor["nome"]
                st.write(f"**{remetente}:** {msg['conteudo']}")

            nova_msg = st.text_input(
                "Digite sua mensagem",
                key=f"msg_{match['_id']}"
            )

            if st.button("Enviar mensagem", key=f"enviar_{match['_id']}"):
                if nova_msg.strip():
                    enviar_mensagem(match, str(usuario["_id"]), nova_msg)
                    st.rerun()

        if st.button(f"🗑️ Excluir match com {pet['nome']}", key=f"delete_{match['_id']}"):
            desfazer_match(match["_id"])
            st.warning("Match excluído.")
            st.rerun()