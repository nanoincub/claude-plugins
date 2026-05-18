# Code Quality Reviewer — Prompt Template

> **Cabeçalho operacional (PT-BR):**
> Prompt do **SEGUNDO reviewer** no two-stage review. Pergunta: "o que foi construído está **bem** construído?"
> Este arquivo é um **wrapper** — delega ao template completo em [../../review/code-reviewer-prompt.md](../../review/code-reviewer-prompt.md) adicionando checks específicos de file responsibility e crescimento de arquivos.
>
> **Quando despachar:** **apenas depois** do spec-reviewer retornar ✅. Ordem é não-negociável.
>
> **Como despachar:** capturar BASE_SHA (commit antes da task) e HEAD_SHA (commit atual) via `git rev-parse`. Preencher os 4 placeholders no template.
>
> **O que esperar de volta:** Strengths + Issues (Critical/Important/Minor) + Recommendations + Assessment (Ready to merge: Yes/No/With fixes).
>
> **Após recepção:** Critical/Important → implementer corrige → re-review. Minor → registrar em STATE.md. Aplicar [receiving-feedback.md](../../review/receiving-feedback.md).

---

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built (clean, tested, maintainable)

**Only dispatch after spec compliance review passes.**

```
Task tool (general-purpose):
  Use template at ../../review/code-reviewer-prompt.md

  DESCRIPTION: [task summary, from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
```

**In addition to standard code quality concerns, the reviewer should check:**
- Does each file have one clear responsibility with a well-defined interface?
- Are units decomposed so they can be understood and tested independently?
- Is the implementation following the file structure from the plan?
- Did this implementation create new files that are already large, or significantly grow existing files? (Don't flag pre-existing file sizes — focus on what this change contributed.)

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment
