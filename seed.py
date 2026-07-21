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
        "bio": "A Luna é muito brincalhona e adora fazer novas amizades para passeios no parque.",
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
        "bio": "O Thor é cheio de energia e procura um companheiro para brincar e correr todos os dias.",
        "pet": criar_pet(
            "Thor",
            "Bulldog Francês",
            4,
            "Macho",
            "https://images.pexels.com/photos/33501591/pexels-photo-33501591.jpeg"
        )
    },
    {
        "nome": "Marina Alves",
        "email": "marina@email.com",
        "bio": "A Mel é muito dócil. Estamos procurando novas amizades e, quem sabe, um futuro companheiro.",
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
            "bio": item["bio"],
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
            "bio": "O Bob adora aventuras e está procurando novos amigos para brincar e passear.",
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
            "bio": "A Nina é muito carinhosa e sociável. Procuramos um pet para amizade e muita diversão.",
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
            "bio": item["bio"],
            "box_pets": [item["pet"]]
        })

    print("Banco populado com sucesso!")
    print("Login principal:")
    print("E-mail: yago@email.com")
    print("Senha: 123")

if __name__ == "__main__":
    popular_banco()