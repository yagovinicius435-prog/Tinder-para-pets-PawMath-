from uuid import uuid4
from bson import ObjectId
from db import usuarios, swipes, matches

def criar_pet(nome, raca, idade, sexo, status_vacinal, documentacao, foto):
    return {
        "id_pet": str(uuid4()),
        "nome": nome,
        "raca": raca,
        "idade": idade,
        "sexo": sexo,
        "status_vacinal": status_vacinal,
        "documentacao": documentacao,
        "foto": foto
    }

def adicionar_pet(id_usuario, pet):
    return usuarios.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$push": {"box_pets": pet}}
    )

def excluir_pet(id_usuario, id_pet):
    usuarios.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$pull": {"box_pets": {"id_pet": id_pet}}}
    )

    swipes.delete_many({"id_pet": id_pet})
    matches.delete_many({
        "$or": [
            {"id_pet1": id_pet},
            {"id_pet2": id_pet}
        ]
    })

def buscar_pet_por_id(id_pet):
    usuario = usuarios.find_one({"box_pets.id_pet": id_pet})

    if not usuario:
        return None, None

    for pet in usuario.get("box_pets", []):
        if pet["id_pet"] == id_pet:
            return usuario, pet

    return None, None

def listar_pets_para_explorar(usuario_logado):

    pipeline = [
        {
            "$match": {
                "_id": {
                    "$ne": usuario_logado["_id"]
                }
            }
        },
        {
            "$unwind": "$box_pets"
        },
        {
            "$project": {
                "_id": 0,
                "id_usuario": "$_id",
                "nome_tutor": "$nome",
                "cidade": 1,
                "bio": "$bio",
                "nome": "$box_pets.nome",
                "id_pet": "$box_pets.id_pet",
                "raca": "$box_pets.raca",
                "idade": "$box_pets.idade",
                "sexo": "$box_pets.sexo",
                "status_vacinal": "$box_pets.status_vacinal",
                "documentacao": "$box_pets.documentacao",
                "foto": "$box_pets.foto"
            }
        },
        {
            "$sample": {
                "size": 20
            }
        }
    ]

    return list(usuarios.aggregate(pipeline))

def buscar_detalhes_pet(id_pet):

    pipeline = [
        {
            "$unwind": "$box_pets"
        },
        {
            "$match": {
                "box_pets.id_pet": id_pet
            }
        },
        {
            "$project": {
                "_id": 0,
                "nome_tutor": "$nome",
                "cidade": "$cidade",
                "pet": "$box_pets"
            }
        }
    ]

    resultado = list(usuarios.aggregate(pipeline))

    if resultado:
        return resultado[0]

    return None