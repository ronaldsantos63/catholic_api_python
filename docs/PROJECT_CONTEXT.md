# Contexto do Projeto

## Objetivo

O Catholic API Python expõe uma API simples para obter a liturgia diária católica em português. A fonte atual é o site da Canção Nova, consultado via chamada AJAX de calendário e depois por scraping da página de liturgia retornada.

## Público

- Aplicativos ou sites que precisam exibir a liturgia diária.
- Desenvolvedores que precisam manter a extração de dados litúrgicos.
- Agentes de IA trabalhando no repositório.

## Fonte externa

O projeto depende da estrutura HTML e dos endpoints públicos de `https://liturgia.cancaonova.com`. Essa estrutura pode mudar sem aviso. Mudanças no scraper devem ser feitas com cuidado, preferencialmente com fixtures de HTML.

## Não objetivos atuais

- Não há autenticação.
- Não há banco de dados.
- Não há cache persistente.
- Não há OpenAPI/Swagger versionado.
- Não há suíte extensa de testes automatizados; existe uma suíte mínima em `tests/`.

## Contrato principal

`GET /liturgy` deve continuar aceitando o header opcional `period` no formato `dd/mm/yyyy` e retornar JSON com `date_string`, `date`, `color`, `entry_title` e `readings`.
