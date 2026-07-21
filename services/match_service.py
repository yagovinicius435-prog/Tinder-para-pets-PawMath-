from datetime import datetime
from bson import ObjectId
from db import swipes, matches
from services.pet_service import buscar_pet_por_id


def criar_match_se_reciproco(usuario_logado, pet_curtido):
    meu_pet = usuario_logado["box_pets"][0]

    tutor_curtido, _ = buscar_pet_por_id(pet_curtido["id_pet"])

    if not tutor_curtido:
        return False

    swipe_reciproco = swipes.find_one({
        "id_usuario": str(tutor_curtido["_id"]),
        "id_pet": meu_pet["id_pet"],
        "tipo_swipe": "like"
    })

    if not swipe_reciproco:
        return False

    match_existente = matches.find_one({
        "$or": [
            {
                "id_pet1": meu_pet["id_pet"],
                "id_pet2": pet_curtido["id_pet"]
            },
            {
                "id_pet1": pet_curtido["id_pet"],
                "id_pet2": meu_pet["id_pet"]
            }
        ]
    })

    if match_existente:
        return True

    matches.insert_one({
        "id_usuario1": str(usuario_logado["_id"]),
        "id_usuario2": str(tutor_curtido["_id"]),
        "id_pet1": meu_pet["id_pet"],
        "id_pet2": pet_curtido["id_pet"],
        "data_match": datetime.now(),
        "chat_completo": []
    })

    return True


def listar_matches_usuario(id_usuario):

    pipeline = [

        {
            "$match": {
                "$or": [
                    {"id_usuario1": str(id_usuario)},
                    {"id_usuario2": str(id_usuario)}
                ]
            }
        },

        {
            "$set": {
                "usuario_lookup": {
                    "$cond": [
                        {"$eq": ["$id_usuario1", str(id_usuario)]},
                        {"$toObjectId": "$id_usuario2"},
                        {"$toObjectId": "$id_usuario1"}
                    ]
                }
            }
        },

        {
            "$lookup": {
                "from": "usuários",
                "localField": "usuario_lookup",
                "foreignField": "_id",
                "as": "tutor"
            }
        },

        {
            "$unwind": {
                "path": "$tutor",
                "preserveNullAndEmptyArrays": True
            }
        },

        {
            "$project": {
                "_id": 1,
                "id_usuario1": 1,
                "id_usuario2": 1,
                "id_pet1": 1,
                "id_pet2": 1,
                "data_match": 1,
                "chat_completo": 1,
                "nome_tutor": "$tutor.nome",
                "cidade": "$tutor.cidade",
                "bio": "$tutor.bio"
            }
        },

        {
            "$sort": {
                "data_match": -1
            }
        }

    ]

    return list(matches.aggregate(pipeline))


def desfazer_match(id_match):
    return matches.delete_one({"_id": id_match})