---
name: nano-disciplines
description: >
  Disciplinas técnicas universais da Nano Incub — TDD (Iron Law), systematic debugging,
  verification before completion, code review (5 eixos), subagent dispatch, parallel dispatch,
  receiving feedback, security review, validation, code analysis, coding principles.
  Reutilizáveis por qualquer plugin ou processo. Não é orquestrador — é caixa de ferramentas.
  Triggers: "aplicar TDD", "rodar debug sistemático", "review desse PR", "verificar antes
  de marcar como pronto", "code review", "Iron Law", "subagent review".
  Não use para: orquestração de processo (use nano-spec), commits/gitflow (use nano-commit),
  artefatos de spec (use nano-spec).
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 1.0.0
---

# Nano Disciplines — Caixa de Ferramentas Técnicas

**Goal**: Fornecer as disciplinas técnicas universais adotadas pela Nano Incub em formato reutilizável. Cada disciplina é independente, invocável por qualquer plugin ou diretamente.

Esta skill **não orquestra processo**. Quando chamada, o agente carrega a disciplina específica solicitada e aplica suas regras. Para processo orquestrado de Spec-Driven Development, ver `nano-spec`.

---

## Índice de Disciplinas

| Categoria | Referência | Quando aplicar |
|---|---|---|
| **Verification** | [verification.md](references/verification.md) | Iron Law — antes de qualquer claim "feito/passou/funciona". Evidência fresh nesta mensagem |
| **TDD** | [execute/tdd/tdd.md](references/execute/tdd/tdd.md) | Tasks com lógica de negócio, mutação de estado, API, fluxo condicional. RED→GREEN→REFACTOR |
| **TDD — anti-patterns** | [execute/tdd/testing-anti-patterns.md](references/execute/tdd/testing-anti-patterns.md) | Antes de escrever mocks ou testes async — 5 anti-padrões com Gate Functions |
| **Debug** | [execute/systematic-debugging/debug.md](references/execute/systematic-debugging/debug.md) | Bug encontrado. 4 fases (Root Cause → Pattern → Hypothesis → Fix) + Fase 4.5 (defense-in-depth) |
| **Debug — defense-in-depth** | [execute/systematic-debugging/defense-in-depth.md](references/execute/systematic-debugging/defense-in-depth.md) | Após fix, prevenir reincidência |
| **Debug — root cause tracing** | [execute/systematic-debugging/root-cause-tracing.md](references/execute/systematic-debugging/root-cause-tracing.md) | Cadeia causal além do sintoma imediato |
| **Subagents** | [execute/subagents/subagents.md](references/execute/subagents/subagents.md) | Large/Complex — fresh subagent per task + two-stage review (spec compliance → code quality) |
| **Parallel dispatch** | [execute/subagents/parallel-dispatch.md](references/execute/subagents/parallel-dispatch.md) | Tasks `[P]` independentes — múltiplos subagents em paralelo. Inclui Protocolo Dois-Eixos |
| **Implementer prompt** | [execute/subagents/implementer-prompt.md](references/execute/subagents/implementer-prompt.md) | Template do subagent implementador |
| **Code quality reviewer** | [execute/subagents/code-quality-reviewer-prompt.md](references/execute/subagents/code-quality-reviewer-prompt.md) | Template do subagent revisor de qualidade |
| **Code analysis** | [execute/code-analysis.md](references/execute/code-analysis.md) | Análise de código existente — graceful degradation |
| **Coding principles** | [execute/coding-principles.md](references/execute/coding-principles.md) | Princípios aplicados antes do `/simplify` — simplicidade, escopo, intent |
| **Code review** | [review/code-review.md](references/review/code-review.md) | Review de PR/diff — 5 eixos (Correctness, Performance, Maintainability, Security, Testing) |
| **Code reviewer prompt** | [review/code-reviewer-prompt.md](references/review/code-reviewer-prompt.md) | Template do subagent revisor de código |
| **Receiving feedback** | [review/receiving-feedback.md](references/review/receiving-feedback.md) | Recebendo feedback de review — zero performative agreement, verificar antes de implementar |
| **Security review** | [review/security.md](references/review/security.md) | Auditoria de segurança — OWASP, secrets, injection, authZ |
| **Validate (UAT)** | [review/validate.md](references/review/validate.md) | Validação contra critérios de aceite — User Acceptance Testing |
| **Docs update** | [docs/docs-update.md](references/docs/docs-update.md) | Sincronizar `.specs/codebase/` após mudança arquitetural ou de convenção |

---

## Convenção de referência cross-plugin

Quando outra skill (ex: `nano-spec`, `nano-commit`) precisa referenciar uma disciplina desta plugin, usar a notação:

```
[disciplina](nano-disciplines:<caminho-em-references>)
```

Exemplos:
- `nano-disciplines:verification.md`
- `nano-disciplines:execute/tdd/tdd.md`
- `nano-disciplines:review/code-review.md`

A skill consumidora resolve o caminho real ao instalar/invocar.

---

## Quando NÃO usar

- Você precisa de **orquestração de processo** (specify → design → tasks → execute → commit) → use `nano-spec`
- Você precisa de **fluxo de commit/branch/PR** → use `nano-commit`
- Você precisa de **artefatos de spec** (`spec.md`, `design.md`, `tasks.md`) → use `nano-spec`

Nano-disciplines é **caixa de ferramentas**. Para o *método* que usa essas ferramentas em sequência, instale `nano-spec` por cima.

---

## Versão

**1.0.0** — Extração das 10 disciplinas técnicas que estavam internalizadas em `nano-spec` 4.0.0. Disponibilizadas como plugin standalone para reuso fora do contexto Spec-Driven. `nano-spec` 5.0.0 passa a depender deste plugin via HARD BLOCK.

Disciplinas adaptadas do [superpowers](https://github.com/obra/superpowers) por Jesse Vincent (Anthropic), conforme estavam internalizadas no `nano-spec` 4.0.0. Mantém integralmente as adaptações Nano (PT-BR, naming por ID de requisito em testes, two-stage review por task, Protocolo Dois-Eixos).

Licença CC-BY-4.0.
