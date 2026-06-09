# API

## Base

Em desenvolvimento local, use:

```text
http://127.0.0.1:5000
```

## `GET /`

Retorna uma página HTML simples:

```html
<h1>Catholic Api</h1>
```

## `GET /privacy`

Retorna `templates/privacy.html`, com termos de privacidade do aplicativo Catholic Daily Liturgy.

## `GET /liturgy`

Retorna a liturgia diária.

### Headers

| Header | Obrigatório | Formato | Descrição |
| --- | --- | --- | --- |
| `period` | não | `dd/mm/yyyy` | Data da liturgia. Se ausente, usa a data atual do servidor. |

### Exemplo

```bash
curl -H "period: 23/05/2024" http://127.0.0.1:5000/liturgy
```

### Resposta 200

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

### Campos

- `date_string.day`: dia como aparece no HTML.
- `date_string.month`: mês abreviado em português.
- `date_string.year`: ano.
- `date`: data normalizada como `dd/mm/yyyy`.
- `color`: cor litúrgica.
- `entry_title`: título da celebração.
- `readings.first_reading`: primeira leitura em Markdown, quando existir.
- `readings.psalm`: salmo em Markdown, quando existir.
- `readings.second_reading`: segunda leitura em Markdown, quando existir.
- `readings.gospel`: evangelho em Markdown, quando existir.

### Erros

Quando o scraper não consegue montar a resposta, `DailyLurgy.get()` retorna:

```json
{
  "error": "No liturgy found for the period: 23/05/2024"
}
```

com status `404`.

Exceções não tratadas pelo middleware retornam:

```json
{
  "error": "Internal Server Error",
  "message": "..."
}
```

com status `500`.

## Compatibilidade

Preserve o nome dos campos públicos ao alterar o scraper. Se for necessário adicionar campos, prefira mudança aditiva e documente aqui.

