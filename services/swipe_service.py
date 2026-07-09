from datetime import datetime
from db import swipes
from services.match_service import criar_match_se_reciproco

def usuario_ja_avaliou(id_usuario, id_pet):
    return swipes.find_one({
        "id_usuario": str(id_usuario),
        "id_pet": id_pet
    })

def registrar_swipe(usuario_logado, pet_avaliado, tipo_swipe):
    swipes.insert_one({
        "id_usuario": str(usuario_logado["_id"]),
        "id_pet": pet_avaliado["id_pet"],
        "tipo_swipe": tipo_swipe,
        "timestamp": datetime.now()
    })

    if tipo_swipe == "like":
        return criar_match_se_reciproco(usuario_logado, pet_avaliado)

    return False

def buscar_curtidas_recebidas(meu_pet):
    return list(swipes.find({
        "id_pet": meu_pet["id_pet"],
        "tipo_swipe": "like"
    }))