---
name: nano-resumo-dia
description: Extrai timeline de trabalho dos históricos de sessão do Claude Code. Use quando o usuário pedir "timeline", "resumo do dia", "o que fiz ontem", "o que fiz hoje", "histórico de trabalho", "work summary", "sessões do dia", "meu trabalho de ontem". Não use para análise de código ou git log.
license: CC-BY-4.0
metadata:
  author: Rafael Yanagui
  version: 1.0.0
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

### 3. Apresentar o resultado

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
