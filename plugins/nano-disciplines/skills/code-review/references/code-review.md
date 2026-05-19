# Code Review — guia operacional

Quando e como pedir review de código no nano-spec. O nano-spec tem **dois mecanismos** complementares:

| Mecanismo | Onde mora | Quando usar |
|---|---|---|
| **Protocolo Dois-Eixos** | [review.md > Dois-Eixos](review.md#protocolo-dois-eixos-largecomplex-pré-commit) | Pre-commit Large/Complex — review **especializado** em paralelo (Standards + Spec). Substitui o code reviewer geral nesse slot. |
| **Code Reviewer (geral)** | [code-reviewer-prompt.md](code-reviewer-prompt.md) | Todos os outros casos: post-commit antes de merge, "review me" standalone, code-quality-reviewer dos subagents per-task, e features Medium quando dev pede explicitamente |

> **Princípio:** Review early, review often. O reviewer recebe **contexto isolado** (apenas o range git BASE..HEAD), nunca o histórico da sessão.

---

## Quando pedir review

**Obrigatório:**
- Após cada task no [fluxo subagent-driven](../execute/subagents/subagents.md) (code-quality-reviewer per-task)
- Antes de merge para `main` / `develop`
- Após implementar feature major

**Opcional mas valioso:**
- Quando travado (perspectiva fresca)
- Antes de refactor grande (baseline check)
- Após corrigir bug complexo

---

## Code Reviewer (template completo)

### Pattern de dispatch

```bash
# Pre-merge ou ad-hoc:
BASE_SHA=$(git merge-base HEAD main)      # ou: origin/main, develop
HEAD_SHA=$(git rev-parse HEAD)

# Per-task (subagents):
BASE_SHA=<commit antes da task>
HEAD_SHA=<commit final da task>
```

`git merge-base` é preferível a `HEAD~1` porque cobre branches com múltiplos commits.

### Dispatch

Despachar subagent com o template em [`code-reviewer-prompt.md`](code-reviewer-prompt.md), preenchendo:

- `{DESCRIPTION}` — resumo curto do que foi construído
- `{PLAN_OR_REQUIREMENTS}` — o que deveria fazer (path da spec/tasks, ou texto direto)
- `{BASE_SHA}` / `{HEAD_SHA}` — range git

O reviewer roda `git diff` por conta própria — você passa **apenas** o range, não os arquivos.

### O reviewer avalia 5 eixos

| Eixo | Foco |
|---|---|
| Plan alignment | Implementação match plano? Desvios justificados? Tudo presente? |
| Code quality | Separation of concerns, error handling, type safety, DRY sem premature abstraction, edge cases |
| Architecture | Design decisions, scalability/performance, security, integração |
| Testing | Tests verify real behavior (não mock), edge cases, integration, all passing |
| Production readiness | Migration strategy, backward compat, docs, no obvious bugs |

### Output esperado (formato fixo)

```markdown
### Strengths
[O que está bem feito. Específico.]

### Issues

#### Critical (Must Fix)
[Bugs, security, data loss, broken functionality]

#### Important (Should Fix)
[Architecture, missing features, error handling, test gaps]

#### Minor (Nice to Have)
[Style, optimization, doc polish]

Por issue: file:line + what + why + how (se não óbvio)

### Recommendations
[Melhorias para futuro]

### Assessment
**Ready to merge?** Yes | No | With fixes
**Reasoning:** [1-2 frases técnicas]
```

**Severidade calibrada:** "Not everything is Critical." Marcar nitpicks como Critical é red flag — solapa a confiança no resto do report.

---

## Action plan pós-review

| Severidade | Ação |
|---|---|
| **Critical** | Corrigir **imediatamente** — bloqueia tudo |
| **Important** | Corrigir antes de prosseguir / mergear |
| **Minor** | Anotar em STATE.md ("Deferred Ideas") para depois |
| **Recommendations** | Advisory — não bloqueiam, mas vale considerar |

**Se reviewer estiver errado:**

Não implemente cegamente. Push back **com raciocínio técnico**:
- Mostre código/testes que provam que funciona
- Cite a spec que contradiz o feedback
- Peça clarificação se ambíguo

Ver [receiving-feedback.md](receiving-feedback.md) para o protocolo completo de recepção (6 passos READ→UNDERSTAND→VERIFY→EVALUATE→RESPOND→IMPLEMENT + forbidden responses + push back patterns).

---

## Quando NÃO usar code reviewer (use Dois-Eixos)

Pre-commit em features **Large** ou **Complex** com spec formal e `CONVENTIONS.md` populado → o Protocolo Dois-Eixos é mais rigoroso porque:

- Particiona em 2 subagents paralelos especializados (Standards + Spec) em vez de 1 reviewer monolítico
- Cada eixo cita regra textualmente (CONVENTIONS) ou ID de requisito (`[FEAT]-XX`) — sem severidade subjetiva
- Roda em paralelo via [parallel-dispatch.md](../execute/subagents/parallel-dispatch.md)
- Dev decide endereçar/pular/discutir (preserva agência) em vez de Yes/No/With fixes

**Mas:** Dois-Eixos **não cobre** architecture / production readiness / testing depth — para esses, complementar com code reviewer ou bater como observações no commit.

---

## Red Flags

- Skipar review porque "é simples"
- Ignorar issues Critical
- Avançar com Important não resolvido
- Argumentar com feedback técnico válido (defensiva)
- Aceitar review onde o agent disse "looks good" sem evidência específica
- Reviewer que marca nitpick como Critical
- Reviewer sem verdict claro no final

---

## Limites

| Tool | Max re-runs | Após limite |
|---|---|---|
| Code review (geral ou Dois-Eixos) | 3 | Escalar para dev com lista de issues |

Loop infinito de review → ping-pong com o implementer é sinal de:
- Task mal especificada no `tasks.md`, ou
- Reviewer está sendo pedante (filtrar para só "Issues", ignorar "Recommendations"), ou
- Desacordo técnico real → escalar para dev
