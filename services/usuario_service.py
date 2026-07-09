from bson import ObjectId
from db import usuarios, swipes, matches

def criar_usuario(dados):
    return usuarios.insert_one(dados)

def buscar_usuario_por_email(email):
    return usuarios.find_one({"email": email})

def login(email, senha):
    return usuarios.find_one({"email": email, "senha": senha})

def buscar_usuario_por_id(id_usuario):
    return usuarios.find_one({"_id": ObjectId(id_usuario)})

def atualizar_usuario(id_usuario, dados):
    return usuarios.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$set": dados}
    )

def excluir_usuario(id_usuario):
    usuario = buscar_usuario_por_id(id_usuario)

    if usuario:
        for pet in usuario.get("box_pets", []):
            swipes.delete_many({"id_pet": pet["id_pet"]})
            matches.delete_many({
                "$or": [
                    {"id_pet1": pet["id_pet"]},
                    {"id_pet2": pet["id_pet"]}
                ]
            })

    swipes.delete_many({"id_usuario": id_usuario})
    matches.delete_many({
        "$or": [
            {"id_usuario1": id_usuario},
            {"id_usuario2": id_usuario}
        ]
    })

    return usuarios.delete_one({"_id": ObjectId(id_usuario)})