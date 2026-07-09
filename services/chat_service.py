from datetime import datetime
from uuid import uuid4
from db import matches

def enviar_mensagem(match, id_usuario_remetente, conteudo):
    mensagem = {
        "id_mensagem": str(uuid4()),
        "id_match": str(match["_id"]),
        "id_usuario_remetente": str(id_usuario_remetente),
        "conteudo": conteudo,
        "timestamp": datetime.now()
    }

    return matches.update_one(
        {"_id": match["_id"]},
        {"$push": {"chat_completo": mensagem}}
    )