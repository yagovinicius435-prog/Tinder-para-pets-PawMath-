import streamlit as st
from pymongo import MongoClient


@st.cache_resource
def conectar_mongo():
    client = MongoClient(st.secrets["MONGO_URI"])
    return client[st.secrets["DB_NAME"]]


db = conectar_mongo()

usuarios = db["usuários"]
swipes = db["curtida_deslize"]
matches = db["partidas"]