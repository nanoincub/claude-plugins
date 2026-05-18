# Commit

> **Fluxo completo vive em [`nano-commit`](nano-commit:skills/nano-commit/SKILL.md).**
> Este arquivo lista os HARD BLOCKs e gates críticos para quem navega pelos references sem carregar a skill `nano-commit`.

## Quando o orquestrador entra aqui

- Orquestrador `nano-spec` invoca `Skill('nano-commit')` na fase Commit
- Invocação standalone: dev diz "commitar", "criar PR", "fechar branch", etc. — a skill é auto-disparada via description

## HARD BLOCKs (não-negociáveis)

| HARD BLOCK | Onde dispara | Como desativar |
|---|---|---|
| **`git-flow-next` instalado** | Primeira interação git da sessão | `CLAUDE.md` define `## Branching` → `Sem gitflow` ou `trunk-based` |
| **Iron Law: testes passando** | Antes de oferecer opções de commit | Não desativável — ver [verification.md](nano-disciplines:verification) |
| **`/simplify` rodou no diff acumulado** | Antes do commit | Não desativável |
| **Confirmação tipada `discard`** | Antes de descartar branch (opção 4) | Não desativável — proteção contra perda de trabalho |

## Ordem pre-commit (fixa)

```
/simplify (refactor)
    ↓
Suite completa de testes (Iron Law verification)
    ↓
Commit (sempre pergunta ao dev primeiro)
    ↓
Pós-commit: 4 opções de fechamento (merge / PR / manter / discard)
```

**Inverter `/simplify` ↔ testes** deixa janela para regressões silenciosas — `/simplify` altera código e ninguém revalida.

## Conventional Commits

`<type>(<scope>): <description>` — types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, `build`, `ci`.

Scopes vêm do `CLAUDE.md` do projeto. Mensagem em PT-BR (ou idioma definido pelo projeto).

**Rastreabilidade:** se a feature tem IDs `[FEAT]-XX`, incluir `Refs: [FEAT]-01, [FEAT]-02` no rodapé.

## Detalhes operacionais

Tudo abaixo está em [`nano-commit`](nano-commit:skills/nano-commit/SKILL.md):

- Validação de branch antes do commit
- Detecção de desvio de escopo
- Comandos exatos por tipo de branch (`feature/`, `hotfix/`, `release/`)
- Template de PR body com Test Plan obrigatório
- Atualização de STATE.md pós-commit
