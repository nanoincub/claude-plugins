# Session Handoff

## Pause Work

**Trigger:** "Pause work", "End session", "Create handoff"

**Purpose:** Checkpoint current state for resumption.

**Output:** `.specs/HANDOFF.md` (overwrites previous)

**Size target:** ~500 tokens

**Structure:**

```markdown
# Handoff

**Date:** [ISO timestamp]
**Feature:** [feature name]
**Task:** [task identifier] - [brief status]

## Completed ✓

- [Completed work item]
- [Completed work item]

## In Progress

- [Current work] ([percentage or status])
- Specific location: [file:line if applicable]

## Pending

- [Next immediate step]
- [Following step]

## Blockers

- [Blocker description] - [impact]

## Context

- Branch: [git branch if applicable]
- Uncommitted: [files with changes]
- Related decisions: [STATE.md references if applicable]
```

**Instructions:**

- Focus on actionable information for resumption
- Include specific file/line references where relevant
- Note uncommitted changes explicitly
- Reference related STATE.md entries if applicable

## Resume Work

**Trigger:** "Resume work", "Continue", "Load handoff"

**Process:**

1. Load HANDOFF.md
2. Load STATE.md for context
3. Carregar artefatos da feature em andamento conforme tipo de trabalho (ver tabela abaixo)
4. Summarize current position
5. Propose next action

### Quais arquivos carregar ao retomar (por tipo de trabalho)

| Trabalho pausado | Arquivos a carregar | Volta a qual fase do trilho |
|---|---|---|
| **Feature Large/Complex** com `tasks.md` | `spec.md` + `context.md` (se existe) + `design.md` (se existe) + `tasks.md` da feature | Próxima task `Pending` no `tasks.md`, ou task em `Implementing` se interrompida no meio |
| **Feature Medium** com tasks inline | `spec.md` + STATE.md (procurar última task registrada) | Próximo step do plano inline do Execute |
| **Quick Mode** em andamento | `.specs/quick/NNN-slug/TASK.md` (se foi criado) OU somente HANDOFF.md | Step do quick-mode em que parou — descrever → implementar → verificar → /simplify → testes → commit |
| **Bug fix via debug.md** | `spec.md` (se feature relacionada) + entrada do bug em STATE.md (B-[NNN] se registrado) | Fase atual do debug (Root Cause / Pattern / Hypothesis / Implementation) |
| **Refactor/melhoria sem feature formal** | STATE.md + git diff do trabalho não commitado | Continuar do diff atual |

### Quick Mode — formato compacto de handoff

Quick Mode não tem `tasks.md` formal. Quando o dev pausa um Quick Mode em andamento, criar HANDOFF.md compacto:

```markdown
# Handoff — Quick Mode

**Date:** YYYY-MM-DD HH:MM
**Quick task:** <descrição em 1 frase>
**Stage:** [describe | gitflow | implement | verify | /simplify | testes | docs | commit]

## Done
- [steps concluídos]

## Pending
- [próximo step exato]

## Context
- Branch: [git branch]
- Uncommitted: [arquivos com diff]
- Comando de verificação: [se aplicável]
```

Pode usar `.specs/quick/NNN-slug/TASK.md` em vez do HANDOFF.md global se o Quick Mode criou pasta própria.

### Response pattern

- "Resuming [feature OU quick task] at [fase OU step]"
- "Completed: [summary com refs concretas, ex: T1-T3 done, T4 in progress at file:line]"
- "Next: [próxima ação imediata, comando se aplicável]"
- "Continue with [specific step]?"

Se ao retomar detectar **mudança não trivial no repo** desde o pause (commits novos por outras pessoas, base atualizada), avisar antes de prosseguir: "Base mudou desde o pause — quer rebase / re-baseline?"
