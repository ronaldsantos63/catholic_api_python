# Segurança e Privacidade

## Superfície Atual

- API pública sem autenticação.
- Scraping de site externo.
- Logging de headers de requisição sanitizados.
- Página de privacidade estática.

## Riscos

- API key é opcional para preservar compatibilidade; ambientes públicos devem definir `CATHOLIC_API_KEY`.
- Rate limit em memória é por processo e não substitui proteção de borda em produção.
- O parser consome HTML externo; mudanças na fonte podem gerar exceções.

## Controles Atuais

- O header `period` é validado como data real em `dd/mm/yyyy`.
- Chamadas `requests` usam timeout configurável por `REQUEST_TIMEOUT`.
- Headers sensíveis são mascarados antes de ir para logs.
- Rate limit em memória reduz abuso simples por IP.
- `CATHOLIC_API_KEY` permite exigir chave de API sem quebrar clientes quando não configurada.

## Regras para Mudanças

- Preserve a validação de entradas antes de chamadas externas.
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
