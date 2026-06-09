# Arquitetura de Documentação para Agentes de IA

## Fonte Canônica

`AGENTS.md` é a fonte canônica de instruções para agentes neste repositório. Arquivos específicos de ferramentas devem apontar para ele ou repetir apenas o mínimo necessário.

## Arquivos Criados

| Ferramenta | Arquivo | Função |
| --- | --- | --- |
| LLM doc index | `llms.txt` | Mapa curto para agentes encontrarem a documentação principal. |
| Agentes compatíveis com AGENTS.md, Codex, Copilot agent, Windsurf/Devin e outros | `AGENTS.md` | Instruções canônicas do projeto. |
| Claude Code | `CLAUDE.md` | Importa `AGENTS.md` e adiciona notas específicas do Claude. |
| Claude Code rules | `.claude/rules/python-api.md` | Regra path-scoped para código Python. |
| Gemini CLI | `GEMINI.md` | Instruções específicas do Gemini. |
| Gemini CLI config | `.gemini/settings.json` | Configura carregamento de `AGENTS.md` e `GEMINI.md`. |
| GitHub Copilot | `.github/copilot-instructions.md` | Instruções repository-wide. |
| GitHub Copilot path-specific | `.github/instructions/*.instructions.md` | Instruções por tipo de arquivo. |
| Cursor | `.cursor/rules/catholic-api.mdc` | Regra always-on em formato MDC. |
| Devin/Windsurf Cascade | `.devin/rules/catholic-api.md` | Regra workspace preferred. |
| Windsurf legado | `.windsurf/rules/catholic-api.md` | Fallback para instalações antigas. |
| Review agents | `REVIEW.md` | Diretrizes específicas para revisão de PR. |
| Codex/Copilot skills | `.agents/skills/*/SKILL.md` | Workflows reutilizáveis repo-scoped para Codex e GitHub Copilot agent. |
| Claude Code skills | `.claude/skills/*/SKILL.md` | Workflows reutilizáveis de projeto para Claude Code. |
| Gemini CLI skills | `.gemini/skills/*/SKILL.md` | Workflows reutilizáveis de workspace para Gemini CLI. |

## Princípios

- Mantenha `AGENTS.md` curto, concreto e acionável.
- Coloque explicações longas em `docs/`.
- Use skills para procedimentos recorrentes ou frágeis.
- Evite duplicação extensa entre arquivos de agentes.
- Quando uma skill mudar, mantenha os espelhos em `.agents/skills`, `.claude/skills` e `.gemini/skills` alinhados.
- Não crie cópias em `.github/skills` enquanto `.agents/skills` atender Copilot; isso evita skills duplicadas no mesmo agente.
- Quando uma ferramenta aceitar import, prefira importar `AGENTS.md`.
- Quando uma ferramenta não aceitar import confiável, inclua resumo curto e direcione para `AGENTS.md`.

## Quando Atualizar

- Mudou rota, schema ou erro HTTP: atualize `docs/API.md`, `README.md` e `AGENTS.md`.
- Mudou scraper ou premissas da fonte externa: atualize `docs/ARCHITECTURE.md` e a skill `liturgy-scraper-maintenance`.
- Mudou setup, comando ou deploy: atualize `README.md`, `docs/DEVELOPMENT.md`, `docs/OPERATIONS.md` e `AGENTS.md`.
- Mudou política para agentes: atualize este arquivo, `AGENTS.md`, `REVIEW.md` quando aplicável e wrappers específicos.
