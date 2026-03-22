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
| `DATABASE_URL` | Conexão SQLAlchemy | `postgresql+psycopg://firecrust:firecrust@localhost:5432/firecrust` |
| `JWT_SECRET_KEY` | Chave do token | `change-me` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token | `720` |

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
