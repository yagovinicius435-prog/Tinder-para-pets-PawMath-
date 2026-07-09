import streamlit as st

from interface.utils import iniciar_sessao, usuario_atual
from interface.inicio import tela_inicio
from interface.cadastro import tela_cadastro
from interface.explorar import tela_explorar
from interface.curtidas import tela_curtidas
from interface.matches import tela_matches
from interface.perfil import tela_perfil

st.set_page_config(
    page_title="PawMatch",
    page_icon="🐾",
    layout="centered"
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fff6f0 0%, #ffe0e6 100%);
    }

    div.stButton > button {
        border-radius: 25px;
        height: 3em;
        font-weight: bold;
        width: 100%;
        border: none;
    }

    img {
        border-radius: 25px;
        max-height: 420px;
        object-fit: cover;
    }

    section[data-testid="stSidebar"] {
        background-color: #fff0f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

iniciar_sessao()
usuario = usuario_atual()

if usuario:
    st.sidebar.title("🐾 PawMatch")
    st.sidebar.write(f"Olá, **{usuario['nome']}**")

    opcoes_menu = [
        "🔎 Explorar",
        "❤️ Curtidas",
        "💬 Matches",
        "👤 Perfil"
    ]

    if "pagina_atual" not in st.session_state:
        st.session_state.pagina_atual = "🔎 Explorar"

    pagina = st.sidebar.radio(
        "Navegação",
        opcoes_menu,
        index=opcoes_menu.index(st.session_state.pagina_atual)
    )

    st.session_state.pagina_atual = pagina

    if pagina == "🔎 Explorar":
        tela_explorar()

    elif pagina == "❤️ Curtidas":
        tela_curtidas()

    elif pagina == "💬 Matches":
        tela_matches()

    elif pagina == "👤 Perfil":
        tela_perfil()

else:
    aba_login, aba_cadastro = st.tabs(["Entrar", "Criar conta"])

    with aba_login:
        tela_inicio()

    with aba_cadastro:
        tela_cadastro()
#C:\Users\Lenovo\AppData\Local\Python\pythoncore-3.14-64\python.exe -m streamlit run app.py