# Fire Crust Back End

Backend em Python com FastAPI e PostgreSQL para o site de pedidos da pizzaria Fire Crust.

## O que está incluído

- Tenant único para a própria Fire Crust.
- Cadastro e login de clientes com JWT.
- Catálogo de pizzas, bebidas e adicionais.
- Criação e consulta dos pedidos do próprio cliente.
- Resumo da jornada do cliente com pedidos abertos e valor gasto.
- Configuração pronta para PostgreSQL em produção.
- Carregamento de variáveis com `python-dotenv` a partir do arquivo `.env`.
- Seed de itens iniciais de cardápio para PostgreSQL (`db/seed_menu_items.sql`).
- Testes automatizados usando SQLite em memória.

## Rodando localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
uvicorn app.main:app --reload
```

A aplicação sobe em `http://127.0.0.1:8000`.

## Variáveis de ambiente

A aplicação chama `load_dotenv()` na inicialização e depois monta as settings com Pydantic.

| Variável | Descrição | Padrão |
| --- | --- | --- |
| `APP_NAME` | Nome da API | `Fire Crust SaaS API` |
| `DATABASE_URL` | Conexão SQLAlchemy | `postgresql+psycopg://firecrust:firecrust@localhost:5433/firecrust` |
| `JWT_SECRET_KEY` | Chave do token | `change-me` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token | `720` |

## Seed de itens no PostgreSQL

Se você iniciar via Docker Compose em um volume novo, o Postgres executa automaticamente o script:

- `db/seed_menu_items.sql`

Comando:

```bash
docker compose up -d
```

Se o banco já existir e você quiser aplicar manualmente:

```bash
docker compose exec db psql -U firecrust -d firecrust -f /docker-entrypoint-initdb.d/01_seed_menu_items.sql
```

## Endpoints principais

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/menu-items`
- `POST /api/v1/menu-items`
- `GET /api/v1/orders`
- `POST /api/v1/orders`
- `GET /api/v1/dashboard/summary`

## Modelo da aplicação

A API foi simplificada para uma única pizzaria:

- o `User` representa o cliente final;
- o cardápio é compartilhado por toda a Fire Crust;
- cada cliente enxerga apenas os próprios pedidos;
- não existe mais identificação de restaurante ou multi-tenant.
