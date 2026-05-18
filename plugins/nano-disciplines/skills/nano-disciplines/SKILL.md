---
name: nano-disciplines
description: >
  Índice + internals da caixa de ferramentas técnicas da Nano Incub. As 4 disciplinas
  user-facing principais (tdd, debug, verification, code-review) são skills promovidas
  no mesmo plugin — invoque-as diretamente. Este umbrella hospeda os internals
  (subagent dispatch, parallel dispatch, code analysis, coding principles, validate/UAT,
  docs-update) que são chamados POR outras skills, não pelo dev diretamente.
  Triggers: "ver disciplinas nano", "índice de disciplinas", "lista das skills nano-disciplines",
  "qual disciplina aplicar". Para invocação direta de TDD/debug/verification/code-review,
  use as skills promovidas (tdd, debug, verification, code-review).
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 1.1.0
---

# Nano Disciplines — Caixa de Ferramentas

Disciplinas técnicas universais da Nano Incub. Não orquestra processo — é toolbox.

## Skills promovidas (invocação direta)

As 4 disciplinas mais usadas estão como **skills separadas** no mesmo plugin:

| Skill | Quando invocar | Triggers principais |
|---|---|---|
| [`nano-disciplines:tdd`](../tdd/SKILL.md) | Task com lógica — escrever teste antes do código | "aplicar TDD", "test-driven", "RED-GREEN-REFACTOR" |
| [`nano-disciplines:debug`](../debug/SKILL.md) | Bug encontrado — 4 fases + defense-in-depth | "debug isso", "bug", "root cause", "por que quebrou" |
| [`nano-disciplines:verification`](../verification/SKILL.md) | Antes de qualquer claim "feito/passou" — Iron Law | "verificar", "iron law", "antes de marcar pronto" |
| [`nano-disciplines:code-review`](../code-review/SKILL.md) | Review de PR/diff — 5 eixos + security + receiving-feedback | "code review", "revise PR", "audite segurança" |

## Internals (referências consumidas por outras skills)

Estas disciplinas não têm skill promovida — são invocadas POR outras skills (geralmente `nano-spec` ou as 4 acima):

| Referência | Usado por | Propósito |
|---|---|---|
| [subagents/subagents.md](references/subagents/subagents.md) | `nano-spec` Execute Large/Complex | Fresh subagent per task + two-stage review (spec compliance → code quality) |
| [subagents/parallel-dispatch.md](references/subagents/parallel-dispatch.md) | `nano-spec` Execute (tasks `[P]`) + Protocolo Dois-Eixos | Múltiplos subagents em paralelo + verificação de conflitos |
| [subagents/implementer-prompt.md](references/subagents/implementer-prompt.md) | `subagents.md` | Template do subagent implementador |
| [subagents/code-quality-reviewer-prompt.md](references/subagents/code-quality-reviewer-prompt.md) | `subagents.md`, `code-review` | Template do subagent revisor de qualidade (wrapper de `code-reviewer-prompt`) |
| [code-analysis.md](references/code-analysis.md) | `/simplify`, `nano-spec` Execute | Análise de código existente — graceful degradation |
| [coding-principles.md](references/coding-principles.md) | `/simplify`, `nano-spec` Execute | Princípios pré-`/simplify` — simplicidade, escopo, intent |
| [validate.md](references/validate.md) | `nano-spec` Review (Complex), UAT | Validação contra critérios de aceite — User Acceptance Testing |
| [docs-update.md](references/docs-update.md) | `nano-spec` Docs phase | Sincronizar `.specs/codebase/` após mudança arquitetural |

## Convenção de referência cross-plugin

Quando outra skill referencia conteúdo deste plugin:

- **Invocar skill promovida**: `nano-disciplines:tdd`, `nano-disciplines:debug`, `nano-disciplines:verification`, `nano-disciplines:code-review`
- **Arquivo específico em skill promovida**: `nano-disciplines:skills/tdd/references/testing-anti-patterns.md`
- **Internal do umbrella**: `nano-disciplines:skills/nano-disciplines/references/subagents/subagents.md`

## Quando NÃO usar este plugin

- Orquestração de processo Spec-Driven → use `nano-spec`
- Commits / branches / PRs → use `nano-spec:nano-commit`
- Artefatos de spec (`spec.md`, `design.md`, `tasks.md`) → use `nano-spec`

## Versão

**1.1.0** — Split em 4 skills promovidas (tdd, debug, verification, code-review) + umbrella com internals. Estrutura anterior (1.0.0) era 1 skill umbrella com todas as 20 references — substituída pela hierarquia atual para tornar as disciplinas user-facing mais assertivas no índice global.

1.0.0 — Extração inicial das disciplinas internalizadas no `nano-spec` 4.0.0.

Disciplinas adaptadas do [superpowers](https://github.com/obra/superpowers) por Jesse Vincent (Anthropic). Licença CC-BY-4.0.
