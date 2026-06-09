# Instruções para Agentes

## Projeto

Este repositório é uma API Flask em Python para retornar a liturgia diária católica em JSON, extraída da Canção Nova e convertida parcialmente para Markdown.

Leia também:

- `README.md` para setup e visão geral.
- `docs/ARCHITECTURE.md` para fluxo interno.
- `docs/API.md` para contrato HTTP.
- `docs/SECURITY.md` antes de mexer em logs, entrada de usuário ou rede.
- `REVIEW.md` para diretrizes específicas de revisão de PR.

## Comandos

Setup local:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Rodar API:

```bash
export FLASK_ENV=development
flask --app app run --debug
```

Verificação mínima:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/catholic-api-pycache python3 -m compileall app.py adapter extractor middleware passenger_wsgi.py
python -m unittest
```

## Contrato da API

- Preserve `GET /liturgy`.
- O header opcional `period` usa `dd/mm/yyyy`.
- Se `period` for omitido, a data atual do servidor é usada.
- A resposta deve manter `date_string`, `date`, `color`, `entry_title` e `readings`.
- Mudanças de schema devem ser aditivas ou documentadas em `docs/API.md`.

## Arquitetura

- Rotas e logging ficam em `app.py`.
- Scraping e parsing ficam em `extractor/extractor_service.py`.
- Configuração de fonte externa fica em `extractor/config.py`.
- Utilitários puros ficam em `extractor/utils.py`.
- Middleware WSGI fica em `middleware/`.
- Não misture scraping, rota Flask e formatação de resposta em uma função nova se puder manter as camadas atuais.

## Estilo

- Siga o estilo Python existente.
- Prefira mudanças pequenas e localizadas.
- Não adicione dependências sem justificativa clara.
- Não reestruture o projeto inteiro para resolver uma tarefa pontual.
- Mantenha nomes públicos e rotas estáveis.

## Scraping

- A fonte externa pode mudar sem aviso.
- Ao alterar parsing, use mocks ou fixtures de HTML quando criar testes.
- Não faça testes automatizados dependerem da Canção Nova ao vivo por padrão.
- Considere IDs e classes do HTML externo como contrato frágil.

## Segurança

- Valide entradas novas.
- Use timeout em novas chamadas de rede.
- Não expanda logging de headers, cookies ou tokens.
- Antes de mexer em privacidade ou analytics, leia `docs/SECURITY.md` e `templates/privacy.html`.

## Documentação

- Atualize `README.md` e `docs/` quando mudar comportamento.
- Atualize este arquivo quando mudar comandos, contrato, arquitetura ou expectativas de agente.
- Atualize `REVIEW.md` quando mudar critérios de revisão ou riscos críticos.
- Mantenha arquivos específicos de ferramentas alinhados com este arquivo.

## Skills Disponíveis

- `catholic-api-maintenance`: use para mudanças em Flask, rotas, middleware, logging, WSGI, dependências ou contrato HTTP.
- `liturgy-scraper-maintenance`: use para mudanças no scraping, parsing da Canção Nova, conversão Markdown ou utilitários de data/HTML.
- `agent-docs-maintenance`: use para mudanças em `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Copilot, Cursor, Devin/Windsurf ou skills.

As skills estão espelhadas em `.agents/skills`, `.claude/skills` e `.gemini/skills` para cobrir Codex, GitHub Copilot agent, Claude Code e Gemini CLI.

## Review Guidelines

- Trate regressões no contrato de `/liturgy` como prioridade alta.
- Trate vazamento de dados em logs como prioridade alta.
- Verifique se mudanças no scraper documentam novas premissas.
- Verifique se alterações de dependências são necessárias e versionadas.
