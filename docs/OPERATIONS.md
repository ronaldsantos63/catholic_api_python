# Operação

## Deploy

O arquivo `passenger_wsgi.py` expõe `application` para ambientes que usam Passenger:

```python
from app import app as application
```

Em outros ambientes WSGI, a aplicação Flask principal está em `app:app`.

## Logging

- Em `FLASK_ENV=development`, logs vão para `StreamHandler`.
- Fora de `development`, logs usam `RotatingFileHandler` em `app.log`, com `maxBytes=10000` e `backupCount=3`.
- O `HostLoggerAdapter` prefixa logs com o IP remoto.
- `@app.before_request` registra método, path e headers sanitizados.
- Headers sensíveis como `Authorization`, `Cookie` e `X-API-Key` são mascarados.
- A API aplica rate limit em memória por IP quando `RATE_LIMIT_ENABLED=true`.
- `CATHOLIC_API_KEY`, quando definido, exige header `X-API-Key` nos endpoints da API.

## Dependência Externa

O scraper depende de:

- `POST {BASE_URL}/wp-admin/admin-ajax.php`
- Cookies e headers definidos em `Config`
- Estrutura HTML da página de liturgia

Se a fonte externa mudar, sintomas esperados:

- `a_tag` não encontrado ao resolver a URL da liturgia.
- IDs `liturgia-*` ausentes.
- Campos de cabeçalho litúrgico ausentes.
- Erros 404 retornados por `/liturgy`.

## Recomendações

- Manter timeout nas chamadas `requests`.
- Manter validação de `period` antes de chamar a fonte externa.
- Considerar cache por data para reduzir chamadas externas.
- Adicionar healthcheck que não dependa da Canção Nova.
- Manter mascaramento de headers sensíveis em produção.
