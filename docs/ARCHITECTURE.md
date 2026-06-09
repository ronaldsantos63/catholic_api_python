# Arquitetura

## Visão Geral

O projeto é uma aplicação Flask pequena, organizada em camadas simples:

1. `app.py` recebe a requisição HTTP.
2. `DailyLurgy.get()` lê e valida o header `period`.
3. `ExtractorService.daily_liturgy_markdown(period)` resolve a URL da liturgia e faz scraping.
4. `Utils` normaliza datas, query params, HTML e Markdown.
5. Flask retorna o dicionário como JSON.

## Fluxo de `GET /liturgy`

```text
Cliente
  -> Flask route /liturgy
  -> DailyLurgy.get()
  -> Config()
  -> ExtractorService.daily_liturgy_markdown(period)
  -> POST /wp-admin/admin-ajax.php na Canção Nova
  -> extrai href da data solicitada
  -> GET na página da liturgia
  -> BeautifulSoup parseia cabeçalho e leituras
  -> MarkdownConverter converte blocos litúrgicos
  -> jsonify(...)
```

## Componentes

### `app.py`

- Cria `Flask` e `flask_restful.Api`.
- Configura logging por ambiente.
- Registra `ExceptionLoggingMiddleware`.
- Define rotas `/`, `/privacy` e recurso REST `/liturgy`.

### `extractor/config.py`

- Define `BASE_URL`, com override por variável de ambiente.
- Mantém cookies e headers esperados pela chamada AJAX da Canção Nova.

### `extractor/extractor_service.py`

- `__get_liturgy_url(period)`: monta payload AJAX e procura o link da data.
- `__parse_response(period)`: baixa a página final da liturgia.
- `__parse_header_scrapy(soup)`: extrai data, cor litúrgica e título.
- `daily_liturgy_markdown(period)`: retorna leituras em Markdown.
- `daily_liturgy(period)`: parser alternativo/legado com estrutura detalhada por leitura.

### `extractor/utils.py`

- Conversão de `BeautifulSoup` para Markdown.
- Normalização de datas e meses em português.
- Conversão de `period` para query params.
- Limpeza simples de HTML.

### `middleware/ExceptionLoggingMiddleware.py`

- Captura exceções não tratadas na aplicação WSGI.
- Registra headers sanitizados e retorna JSON genérico com status 500.

### `adapter/logging_adapter.py`

- Prefixa mensagens de log com `RemoteAddr`.

### `passenger_wsgi.py`

- Entry point para hospedagem Passenger.

## Pontos Frágeis

- O scraper assume IDs como `liturgia-1`, `liturgia-2`, `liturgia-3`, `liturgia-4` e classes como `cor-liturgica` e `entry-title`.
- `__get_liturgy_url` assume que o HTML AJAX contém um link cujo `href` inclui `sDia`, `sMes` e `sAno`.
- Alguns trechos usam índices fixos de parágrafos; qualquer mudança no HTML de origem pode quebrar o parser.
- O formato do header `period` é validado como data real em `dd/mm/yyyy`.
