# Catholic API Python

API Flask para consultar a liturgia diária católica a partir da Canção Nova e retornar os dados em JSON, com leituras convertidas para Markdown.

## Recursos

- `GET /liturgy`: retorna data litúrgica, cor, título da celebração e leituras do dia.
- Header opcional `period`: data no formato `dd/mm/yyyy`; se omitido, usa a data atual do servidor.
- `GET /privacy`: página HTML com termos de privacidade do aplicativo.
- `GET /`: resposta simples de saúde/identificação da API.

## Requisitos

- Python 3.9 ou superior.
- Dependências em `requirements.txt`.
- Acesso de rede para `https://liturgia.cancaonova.com`, usado como fonte externa.

## Instalação local

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Execução

```bash
export FLASK_ENV=development
flask --app app run --debug
```

Alternativa:

```bash
python app.py
```

## Exemplos

Liturgia da data atual:

```bash
curl http://127.0.0.1:5000/liturgy
```

Liturgia de uma data específica:

```bash
curl -H "period: 23/05/2024" http://127.0.0.1:5000/liturgy
```

Resposta resumida:

```json
{
  "date_string": {
    "day": "23",
    "month": "Mai",
    "year": "2024"
  },
  "date": "23/05/2024",
  "color": "Verde",
  "entry_title": "7a Semana do Tempo Comum",
  "readings": {
    "first_reading": "...",
    "psalm": "...",
    "second_reading": "...",
    "gospel": "..."
  }
}
```

## Configuração

| Variável | Padrão | Uso |
| --- | --- | --- |
| `BASE_URL` | `https://liturgia.cancaonova.com` | Fonte externa usada pelo scraper. |
| `FLASK_ENV` | não definido | Em `development`, logs vão para stdout com nível `DEBUG`; fora disso, usa `app.log`. |

## Arquitetura

- `app.py`: aplicação Flask, rotas, logging e registro do middleware.
- `extractor/extractor_service.py`: busca a URL da liturgia e extrai os dados do HTML.
- `extractor/config.py`: URL base, cookies e headers usados na chamada AJAX.
- `extractor/utils.py`: funções utilitárias de data, limpeza de HTML e Markdown.
- `middleware/ExceptionLoggingMiddleware.py`: captura exceções não tratadas e retorna JSON 500.
- `adapter/logging_adapter.py`: adiciona `remote_addr` aos logs.
- `passenger_wsgi.py`: entrypoint WSGI para hospedagem com Passenger.

Mais detalhes em [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Validação

Não há suíte de testes versionada neste momento. A verificação mínima de sintaxe usada no projeto é:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/catholic-api-pycache python3 -m compileall app.py adapter extractor middleware passenger_wsgi.py
```

Ao alterar scraping, prefira testes com HTML fixture ou mocks de `requests` para evitar depender da disponibilidade da Canção Nova.

## Documentação para agentes de IA

Este repositório inclui arquivos específicos para agentes:

- `AGENTS.md`: fonte canônica de instruções para agentes de código.
- `llms.txt`: índice curto para ferramentas e agentes que procuram um mapa LLM-friendly.
- `CLAUDE.md`: entrada do Claude Code, importando `AGENTS.md`.
- `GEMINI.md` e `.gemini/settings.json`: contexto para Gemini CLI.
- `.github/copilot-instructions.md` e `.github/instructions/*.instructions.md`: GitHub Copilot.
- `.cursor/rules/*.mdc`: Cursor.
- `.devin/rules/*.md` e `.windsurf/rules/*.md`: Devin/Windsurf Cascade.
- `REVIEW.md`: diretrizes específicas para agentes de revisão de PR.
- `.agents/skills/*/SKILL.md`: skills repo-scoped compartilhadas por Codex e GitHub Copilot agent.
- `.claude/skills/*/SKILL.md`: skills de projeto para Claude Code.
- `.gemini/skills/*/SKILL.md`: skills de workspace para Gemini CLI.

Veja [docs/AI_AGENTS.md](docs/AI_AGENTS.md).
