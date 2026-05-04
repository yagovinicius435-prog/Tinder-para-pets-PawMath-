# 🐾 PawMatch

> Tinder para pets — conectando animais para reprodução responsável.

---

## 📌 Tema do Projeto

**PawMatch** é uma plataforma mobile-first que conecta donos de animais de estimação que buscam parceiros reprodutivos para seus pets. Inspirado na mecânica de swipe do Tinder, o app permite que tutores criem perfis detalhados de seus animais e encontrem matches compatíveis por raça, localização e saúde.

---

## ⭐ Funcionalidade que mais entrega valor

### Match por compatibilidade entre pets

O coração do PawMatch é o **sistema de match inteligente**: o dono cria o perfil do seu pet (raça, idade, sexo, localização, status vacinal e documentação) e o app exibe cards de pets compatíveis para avaliar com swipe.

Quando dois donos curtem mutuamente o pet do outro, ocorre um **match** — e um canal de mensagens é aberto entre os tutores para combinar os detalhes da reprodução.

**Por que essa funcionalidade é a mais valiosa:**
- Elimina a busca manual em grupos de redes sociais e classifieds
- Garante compatibilidade básica antes do contato (raça, sexo, localização)
- Cria um canal de comunicação seguro e rastreável entre donos
- Reduz riscos ao exigir comprovação de vacinas no cadastro

---

## 🗃️ Banco de Dados

O projeto utiliza **MongoDB** (NoSQL orientado a documentos) como banco de dados principal.

### Justificativa da escolha NoSQL

| Critério | Motivo |
|---|---|
| Esquema flexível | Cada espécie/raça pode ter atributos diferentes (ex: gatos têm pelagem, cães têm porte) |
| Consultas geoespaciais | MongoDB suporta índices `2dsphere` nativamente para busca por proximidade |
| Escalabilidade horizontal | Volume de fotos e perfis cresce rapidamente |
| Documentos aninhados | Perfil do pet, fotos e documentos ficam em um único documento |

### Principais coleções

```
users          → dados do dono (auth, contato, localização)
pets           → perfil completo do animal
swipes         → registro de curtidas/passes (para detectar match)
matches        → pares que se curtiram mutuamente
messages       → histórico de chat entre donos após match
```

### Exemplo de documento — coleção `pets`

```json
{
  "_id": "ObjectId(...)",
  "owner_id": "ObjectId(...)",
  "name": "Thor",
  "species": "dog",
  "breed": "Golden Retriever",
  "sex": "male",
  "age_months": 24,
  "vaccinated": true,
  "pedigree": true,
  "location": {
    "type": "Point",
    "coordinates": [-48.1879, -18.6486]
  },
  "city": "Araguari, MG",
  "photos": ["https://storage/.../thor1.jpg"],
  "description": "Brincalhão e saudável. Buscamos fêmea da mesma raça.",
  "created_at": "2026-05-02T10:00:00Z"
}
```

---

## 🚀 Funcionalidades previstas

- [x] Cadastro de perfil do pet com fotos
- [x] Swipe de curtir / passar / super like
- [x] Match automático ao haver curtida mútua
- [x] Chat entre donos após o match
- [ ] Verificação de carteira de vacinação (upload de documento)
- [ ] Filtros avançados (raça, porte, distância, pedigree)
- [ ] Notificações push de novos matches
- [ ] Avaliação de donos após reprodução

---

## 🛠️ Stack tecnológica (proposta)

| Camada | Tecnologia |
|---|---|
| Frontend | React Native |
| Backend | Node.js + Express |
| Banco de dados | MongoDB Atlas |
| Armazenamento de fotos | AWS S3 / Cloudflare R2 |
| Autenticação | Firebase Auth |
| Geolocalização | MongoDB 2dsphere + Google Maps API |

---

## 👥 Equipe

| Nome | Função |
|---|---|
| — | A definir |

---

## 📄 Licença

MIT License — consulte o arquivo `LICENSE` para mais detalhes.
