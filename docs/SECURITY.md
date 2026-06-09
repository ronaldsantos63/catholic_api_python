# Segurança e Privacidade

## Superfície Atual

- API pública sem autenticação.
- Scraping de site externo.
- Logging de headers de requisição.
- Página de privacidade estática.

## Riscos

- O header `period` não é validado formalmente antes de ser usado para montar query params.
- Chamadas `requests` não definem timeout.
- Logs de headers podem registrar dados sensíveis se clientes enviarem tokens ou cookies por engano.
- O parser consome HTML externo; mudanças na fonte podem gerar exceções.

## Regras para Mudanças

- Valide entradas antes de usá-las em chamadas externas.
- Use timeouts em novas chamadas de rede.
- Não registre segredos, tokens, cookies de usuário ou dados pessoais.
- Ao mudar `templates/privacy.html`, preserve a clareza sobre coleta de dados e analytics.
- Ao adicionar dependências, verifique necessidade, manutenção e superfície de ataque.

## Revisão Recomendada

Ao revisar PRs, trate como alta prioridade:

- Vazamento de dados em logs.
- Novos endpoints sem validação.
- Mudanças que expõem HTML externo sem sanitização.
- Dependências novas sem justificativa.
- Alterações no contrato de `/liturgy` sem documentação.

