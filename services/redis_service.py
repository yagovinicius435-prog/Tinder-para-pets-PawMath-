from redis_db import redis_client

# Salva um pet visualizado
def adicionar_pet_visualizado(id_usuario, id_pet):
    chave = f"historico:{id_usuario}"

    redis_client.lpush(chave, id_pet)

    # Mantém apenas os 10 últimos pets
    redis_client.ltrim(chave, 0, 9)


# Lista o histórico
def listar_historico(id_usuario):
    chave = f"historico:{id_usuario}"
    return redis_client.lrange(chave, 0, -1)

# Conta visualizações únicas de um pet
def registrar_visualizacao(id_pet, id_usuario):
    chave = f"visualizacoes:{id_pet}"

    redis_client.pfadd(chave, id_usuario)


# Retorna quantidade aproximada de usuários únicos
def total_visualizacoes(id_pet):
    chave = f"visualizacoes:{id_pet}"

    return redis_client.pfcount(chave)