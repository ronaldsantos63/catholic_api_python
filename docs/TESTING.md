# Testes

## Estado Atual

Há uma suíte mínima em `tests/` usando `unittest` e `Flask.test_client()`.

A validação mínima atual é compilação de sintaxe:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/catholic-api-pycache python3 -m compileall app.py adapter extractor middleware passenger_wsgi.py
python -m unittest
```

## Testes Recomendados

### Unitários para `Utils`

- `parse_day` com dia de um e dois dígitos.
- `parse_month` para todos os meses abreviados usados pela fonte.
- `map_period_to_query_params` com `dd/mm/yyyy`.
- `clean_html` com tags, comentários, `&nbsp;` e espaços duplicados.

### Unitários para `ExtractorService`

Use mocks de `requests.post` e `requests.get`.

- Quando `period` é omitido, deve usar a data atual.
- Quando o AJAX retorna link da data, deve chamar a página da liturgia.
- Quando `liturgia-1..4` existem, deve preencher as leituras correspondentes.
- Quando uma leitura não existe, não deve quebrar.

### Integração Flask

Use `app.test_client()`.

- `GET /` retorna 200.
- `GET /privacy` retorna 200.
- `GET /liturgy` retorna 200 com mocks do scraper.
- Falha do scraper retorna 404 no recurso.

## Evite

- Testes que dependem da Canção Nova ao vivo por padrão.
- Fixtures grandes sem necessidade.
- Snapshot de HTML inteiro quando um fragmento representativo basta.
