import streamlit as st
from services.usuario_service import buscar_usuario_por_id

def iniciar_sessao():
    if "usuario_logado" not in st.session_state:
        st.session_state.usuario_logado = None

def usuario_atual():
    if not st.session_state.usuario_logado:
        return None

    return buscar_usuario_por_id(st.session_state.usuario_logado)

def logout():
    st.session_state.usuario_logado = None
    st.rerun()

def card_pet(tutor, pet):
    foto = pet.get("foto", "").strip()

    if foto.startswith("http"):
        st.image(foto, use_container_width=True)
    else:
        st.warning("📷 Este pet ainda não possui foto válida.")

    st.markdown(f"## 🐶 {pet.get('nome', 'Pet sem nome')}")
    st.write(f"**Raça:** {pet.get('raca', 'Não informado')}")
    st.write(f"**Idade:** {pet.get('idade', 'Não informado')} anos")
    st.write(f"**Sexo:** {pet.get('sexo', 'Não informado')}")
    st.write(f"**Vacinação:** {pet.get('status_vacinal', 'Não informado')}")
    st.write(f"**Tutor:** {tutor.get('nome', 'Tutor não informado')}")
    st.write(f"**Cidade:** {tutor.get('cidade', 'Não informado')}")
    st.write(f"**Bio:** {tutor.get('bio', '')}")