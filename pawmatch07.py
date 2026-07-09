from uuid import uuid4
from datetime import datetime
from db import usuarios, swipes, matches

def criar_pet(nome, raca, idade, sexo, foto):
    return {
        "id_pet": str(uuid4()),
        "nome": nome,
        "raca": raca,
        "idade": idade,
        "sexo": sexo,
        "status_vacinal": "Completo",
        "documentacao": "Em dia",
        "foto": foto
    }

def popular_banco():
    usuarios.delete_many({})
    swipes.delete_many({})
    matches.delete_many({})

    # Seu usuário principal
    meu_pet = criar_pet(
        "Patch",
        "Golden Retriever",
        3,
        "Macho",
        "https://images.unsplash.com/photo-1552053831-71594a27632d"
    )

    meu_usuario = {
        "nome": "Yago Vinicius",
        "email": "yago@email.com",
        "senha": "123",
        "telefone": "34999999999",
        "cidade": "Uberlândia",
        "bio": "Tutor do Patch. Procurando amizades para meu pet.",
        "box_pets": [meu_pet]
    }

    resultado_meu_usuario = usuarios.insert_one(meu_usuario)
    meu_id = str(resultado_meu_usuario.inserted_id)

    # Usuários que já curtiram o Patch
    usuarios_que_me_curtiram = [
        {
            "nome": "Ana Souza",
            "email": "ana@email.com",
            "pet": criar_pet(
                "Luna",
                "Shih-tzu",
                2,
                "Fêmea",
                "https://images.unsplash.com/photo-1587300003388-59208cc962cb"
            )
        },
        {
            "nome": "Carlos Lima",
            "email": "carlos@email.com",
            "pet": criar_pet(
                "Thor",
                "Bulldog Francês",
                4,
                "Macho",
                "https://images.unsplash.com/photo-1583511655826-05700442b31b"
            )
        },
        {
            "nome": "Marina Alves",
            "email": "marina@email.com",
            "pet": criar_pet(
                "Mel",
                "Poodle",
                3,
                "Fêmea",
                "https://images.unsplash.com/photo-1517423440428-a5a00ad493e8"
            )
        }
    ]

    for item in usuarios_que_me_curtiram:
        tutor = {
            "nome": item["nome"],
            "email": item["email"],
            "senha": "123",
            "telefone": "34988888888",
            "cidade": "Uberlândia",
            "bio": "Esse tutor já curtiu o Patch.",
            "box_pets": [item["pet"]]
        }

        resultado_tutor = usuarios.insert_one(tutor)
        id_tutor = str(resultado_tutor.inserted_id)

        # Aqui acontece a curtida deles no seu pet
        swipes.insert_one({
            "id_usuario": id_tutor,
            "id_pet": meu_pet["id_pet"],
            "tipo_swipe": "like",
            "timestamp": datetime.now()
        })

    # Usuários normais para aparecer na aba Explorar
    usuarios_explorar = [
        {
            "nome": "Rafael Dias",
            "email": "rafael@email.com",
            "pet": criar_pet(
                "Bob",
                "Beagle",
                5,
                "Macho",
                "https://images.unsplash.com/photo-1505628346881-b72b27e84530"
            )
        },
        {
            "nome": "Bianca Rocha",
            "email": "bianca@email.com",
            "pet": criar_pet(
                "Nina",
                "Spitz Alemão",
                2,
                "Fêmea",
                "https://images.unsplash.com/photo-1596492784531-6e6eb5ea9993"
            )
        }
    ]

    for item in usuarios_explorar:
        usuarios.insert_one({
            "nome": item["nome"],
            "email": item["email"],
            "senha": "123",
            "telefone": "34977777777",
            "cidade": "Uberlândia",
            "bio": "Perfil disponível para você avaliar na aba Explorar.",
            "box_pets": [item["pet"]]
        })

    print("Banco populado com sucesso!")
    print("Login principal:")
    print("E-mail: yago@email.com")
    print("Senha: 123")

if __name__ == "__main__":
    popular_banco()