# Documentação

Este diretório concentra o contexto durável do projeto. Use estes arquivos como fonte para humanos e agentes de IA.

## Mapa

- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md): objetivo, domínio, premissas e não objetivos.
- [ARCHITECTURE.md](ARCHITECTURE.md): componentes, fluxo de requisição e dependências internas.
- [API.md](API.md): contrato HTTP, headers, respostas e erros.
- [DEVELOPMENT.md](DEVELOPMENT.md): setup local, comandos e fluxo de desenvolvimento.
- [TESTING.md](TESTING.md): validação existente e testes recomendados.
- [OPERATIONS.md](OPERATIONS.md): deploy WSGI/Passenger, logs e dependência externa.
- [SECURITY.md](SECURITY.md): riscos, privacidade e cuidados para mudanças.
- [AI_AGENTS.md](AI_AGENTS.md): arquitetura de instruções para agentes e arquivos específicos.

## Regra de manutenção

Ao mudar comportamento público, atualize `README.md`, `docs/API.md` e `AGENTS.md`. Ao mudar arquitetura interna, atualize `docs/ARCHITECTURE.md` e as skills relevantes em `.agents/skills/`.

