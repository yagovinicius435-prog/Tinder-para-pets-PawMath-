import redis

redis_client = redis.Redis(
    host="communicative-orchid-proven-59300.db.redis.io",
    port= 17936,
    username="default",
    password="PacAnMbW2gAHj0afTXHCc8o2yb68QfOn",
    decode_responses=True
)

print(redis_client.ping())

# Registra uma visualização única de um pet
def registrar_visualizacao(id_pet, id_usuario):

    chave = f"visualizacoes:{id_pet}"

    redis_client.pfadd(chave, id_usuario)


# Retorna a quantidade aproximada de usuários únicos
def total_visualizacoes(id_pet):

    chave = f"visualizacoes:{id_pet}"

    return redis_client.pfcount(chave)