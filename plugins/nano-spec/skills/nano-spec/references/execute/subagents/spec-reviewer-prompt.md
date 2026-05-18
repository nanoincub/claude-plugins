# Spec Compliance Reviewer — Prompt Template

> **Cabeçalho operacional (PT-BR):**
> Prompt do **PRIMEIRO reviewer** no two-stage review (per-task em Large/Complex). Pergunta: "o implementer construiu o que a spec pediu?"
> Template em **inglês** intencional. **Crítico:** o trecho `DO NOT TRUST THE REPORT` precisa ficar em EN — é o gatilho que faz o subagent ler o código direto em vez de confiar no report do implementer.
>
> **Quando despachar:** após implementer reportar `DONE`. **Antes** do code-quality-reviewer.
>
> **Ordem é não-negociável:** spec compliance → code quality. Inverter desperdiça revisão de qualidade em código que vai mudar.
>
> **Como despachar:** via Agent tool. Preencher `[FULL TEXT of task requirements]` (não passar só link) e `[From implementer's report]` (cole o report literal).
>
> **O que esperar de volta:** ✅ Spec compliant OU ❌ Issues found (lista com file:line).
>
> **Após recepção:** ❌ → implementer corrige → re-review. ✅ → despachar [code-quality-reviewer-prompt.md](code-quality-reviewer-prompt.md). Aplicar [receiving-feedback.md](../nano-disciplines:review/receiving-feedback.md).

---

Use this template when dispatching a spec compliance reviewer subagent.

**Purpose:** Verify implementer built what was requested (nothing more, nothing less)

```
Task tool (general-purpose):
  description: "Review spec compliance for Task N"
  prompt: |
    You are reviewing whether an implementation matches its specification.

    ## What Was Requested

    [FULL TEXT of task requirements]

    ## What Implementer Claims They Built

    [From implementer's report]

    ## CRITICAL: Do Not Trust the Report

    The implementer finished suspiciously quickly. Their report may be incomplete,
    inaccurate, or optimistic. You MUST verify everything independently.

    **DO NOT:**
    - Take their word for what they implemented
    - Trust their claims about completeness
    - Accept their interpretation of requirements

    **DO:**
    - Read the actual code they wrote
    - Compare actual implementation to requirements line by line
    - Check for missing pieces they claimed to implement
    - Look for extra features they didn't mention

    ## Your Job

    Read the implementation code and verify:

    **Missing requirements:**
    - Did they implement everything that was requested?
    - Are there requirements they skipped or missed?
    - Did they claim something works but didn't actually implement it?

    **Extra/unneeded work:**
    - Did they build things that weren't requested?
    - Did they over-engineer or add unnecessary features?
    - Did they add "nice to haves" that weren't in spec?

    **Misunderstandings:**
    - Did they interpret requirements differently than intended?
    - Did they solve the wrong problem?
    - Did they implement the right feature but wrong way?

    **Verify by reading code, not by trusting report.**

    Report:
    - ✅ Spec compliant (if everything matches after code inspection)
    - ❌ Issues found: [list specifically what's missing or extra, with file:line references]
```
