---
name: nano-resumo-dia
description: Extrai timeline de trabalho dos históricos de sessão do Claude Code, cruzando com eventos do Google Calendar para enriquecer a análise. Use quando o usuário pedir "timeline", "resumo do dia", "o que fiz ontem", "o que fiz hoje", "histórico de trabalho", "work summary", "sessões do dia", "meu trabalho de ontem". Não use para análise de código ou git log.
license: CC-BY-4.0
metadata:
  author: Rafael Yanagui
  version: 1.1.0
---

# Work Timeline

Extrai uma timeline de trabalho a partir dos históricos de sessão do Claude Code, formatada como tabela Markdown com horário BRT.

## Colunas

| Coluna | Fonte |
|--------|-------|
| Horário (BRT) | Primeiro timestamp da sessão convertido UTC-3 |
| Projeto | Diretório do projeto (readable) |
| Branch | Campo `gitBranch` das entries |
| Descrição | Primeira mensagem do usuário (limpa, até 80 chars) |
| Duração | Diferença entre primeiro e último timestamp da sessão no dia |
| Msgs | Total de mensagens (user + assistant) |
| Session ID | ID completo da sessão (UUID, compatível com `claude --resume`) |

## Instruções

### 1. Determinar a data

- Sem data explícita: usar **ontem**
- "hoje": usar data atual
- Data específica: usar a data informada (formato YYYY-MM-DD)

### 2. Executar o script

O script está em `scripts/timeline.py` relativo ao diretório base desta skill.
Use o "Base directory for this skill" informado pelo sistema para construir o caminho absoluto.

```bash
python3 <base-directory>/scripts/timeline.py [YYYY-MM-DD]
```

Para saída JSON (útil para processamento adicional):
```bash
python3 <base-directory>/scripts/timeline.py [YYYY-MM-DD] --json
```

### 3. Consultar Google Calendar (enriquecimento)

Em paralelo à execução do script, consulte o MCP do Google Calendar para obter os eventos do dia-alvo. Isso ajuda a entender o contexto: reuniões, blocos de foco, compromissos que expliquem gaps entre sessões.

Passos:

1. Carregar a tool via ToolSearch:
   ```
   ToolSearch query="select:mcp__claude_ai_Google_Calendar__list_events"
   ```
2. Chamar `mcp__claude_ai_Google_Calendar__list_events` com a janela do dia-alvo (00:00 a 23:59 BRT, convertido para UTC ou usando timezone `America/Sao_Paulo`). Se não houver `calendarId` específico pedido, usar o primário.
3. Se a autenticação não estiver completa, opcionalmente chamar `mcp__claude_ai_Google_Calendar__list_calendars` antes; se falhar com erro de auth, **siga sem o calendário** e avise no final ("Calendar indisponível — timeline mostrada sem cruzamento de eventos").

Use os eventos para:

- **Cruzar com sessões**: indicar quando uma sessão começou logo após uma reunião, ou quando há um gap explicado por um evento.
- **Compor o resumo por projeto**: se um evento "Reunião X com cliente Y" coincide com sessões no projeto Y, incorporar no resumo (ex: "Pós-reunião com cliente Y: ajustes no cadastro").
- **Apresentar uma seção extra "Agenda do dia"** com os eventos (horário BRT, título, participantes resumidos) antes do resumo por projeto. Omita eventos all-day irrelevantes (aniversários, feriados) salvo se forem o único conteúdo.

Não fabrique correspondências: se o evento não tem relação clara com nenhuma sessão, apenas liste-o em "Agenda do dia".

### 4. Apresentar o resultado

A saída do script contém duas tabelas:
1. **Timeline detalhada** — mostrar exatamente como o script gera (não alterar)
2. **Resumo por projeto** — a coluna "Resumo" vem com `{RESUMO}` placeholder. Você DEVE substituir cada `{RESUMO}` por um resumo curto (max 60 chars) escrito por você, baseado nos dados do comentário HTML `<!-- DADOS PARA GERAR RESUMO -->` no final da saída. O resumo deve ser em português, conciso, descrevendo O QUE foi feito (ex: "Bug fix no cadastro de autorizações", "Documentação do projeto com nano-spec"). Não copiar a descrição — sintetizar.

Remova os comentários HTML antes de apresentar ao usuário.

Se o usuário pedir exportação ou formato diferente, use a flag `--json` e reformate conforme necessário.

## Exemplos

### Exemplo 1: "o que fiz ontem?"

```bash
python3 <base-directory>/scripts/timeline.py
```

Resultado: tabela com todas as sessões de ontem.

### Exemplo 2: "timeline de 2026-04-02"

```bash
python3 <base-directory>/scripts/timeline.py 2026-04-02
```

### Exemplo 3: "o que fiz hoje?"

Calcular a data de hoje e passar como argumento:

```bash
python3 <base-directory>/scripts/timeline.py 2026-04-07
```
