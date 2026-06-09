# Desenvolvimento

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Rodar localmente

```bash
export FLASK_ENV=development
flask --app app run --debug
```

ou:

```bash
python app.py
```

## Variáveis de ambiente

| Variável | Descrição |
| --- | --- |
| `BASE_URL` | Troca a fonte externa, útil para fixtures, proxy ou ambiente de teste. |
| `FLASK_ENV` | Em `development`, usa logs em stdout com nível `DEBUG`; em outros ambientes, grava em `app.log`. |
| `REQUEST_TIMEOUT` | Timeout das chamadas HTTP externas. |
| `CATHOLIC_API_KEY` | Quando definido, exige `X-API-Key` nos endpoints da API. |
| `RATE_LIMIT_ENABLED` | Liga/desliga rate limit em memória. |
| `RATE_LIMIT_REQUESTS` | Limite de requisições por IP. |
| `RATE_LIMIT_WINDOW_SECONDS` | Janela do rate limit. |
| `MAX_CONTENT_LENGTH` | Tamanho máximo do payload. |
| `SECURITY_HSTS_ENABLED` | Adiciona HSTS em ambientes HTTPS. |

## Convenções

- Mantenha a API pequena e explícita.
- Não adicione dependências sem necessidade clara.
- Preserve o formato `period = dd/mm/yyyy` enquanto não houver versionamento de API.
- Para mudanças no scraper, prefira fixtures/mocks a chamadas reais em testes.
- Para logs, evite registrar tokens, cookies de usuários ou dados pessoais.

## Verificação mínima

```bash
PYTHONPYCACHEPREFIX=/private/tmp/catholic-api-pycache python3 -m compileall app.py adapter extractor middleware passenger_wsgi.py
python -m unittest
npx --yes pyright
```

## Antes de abrir PR

1. Rode a verificação mínima.
2. Se alterou contrato HTTP, atualize `docs/API.md`.
3. Se alterou scraping, documente a premissa em `docs/ARCHITECTURE.md`.
4. Se alterou fluxo para agentes, atualize `AGENTS.md` e `docs/AI_AGENTS.md`.
