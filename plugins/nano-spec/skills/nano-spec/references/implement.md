# Execute

**Goal**: Implement ONE task at a time. Surgical changes. Verify. Repeat.

This is where code gets written. Every task follows the same cycle: plan → implement → verify. Verification is built into every task, not a separate phase.

⚠️ **NÃO commitar nesta fase.** O commit acontece na Fase 7 (Commit) após Review e Security.

---

## MANDATORY: Before Starting Any Implementation

**Verificar branch (gitflow):** Se em branch protegida, sugerir criação da branch de trabalho apropriada (`feature/*`, `hotfix/*`, `release/*`) conforme [gitflow.md](gitflow.md). Neste ponto o tipo de trabalho já é conhecido.

**Read [coding-principles.md](coding-principles.md) and state:**

1. **Assumptions** - What am I assuming? Any uncertainty?
2. **Files to touch** - List ONLY files this task requires
3. **Success criteria** - How will I verify this works?

⚠️ **Do not proceed without stating these explicitly.**

---

## Process

### 0. List Atomic Steps (MANDATORY when Tasks phase was skipped)

If there is no `tasks.md` for this feature, you MUST list atomic steps before writing any code. This is non-negotiable — it prevents the agent from losing focus and doing too many things at once.

```
## Execution Plan

1. [Step] → files: [list] → verify: [how] → commit: [message]
2. [Step] → files: [list] → verify: [how] → commit: [message]
3. [Step] → files: [list] → verify: [how] → commit: [message]
```

**Each step must be:**

- ONE deliverable (one component, one function, one endpoint, one file change)
- Independently verifiable (can prove it works before moving on)
- Independently committable (gets its own atomic git commit)

If listing steps reveals >5 steps or complex dependencies, STOP and create a formal `tasks.md` instead. The Tasks phase was wrongly skipped.

### 1. Pick Task

From tasks.md (if exists) or from the execution plan above. User specifies ("implement T3") or suggest next available.

### 2. Verify Dependencies

If tasks.md exists, check dependencies. If using inline plan, follow the order listed.

❌ If blocked: "T3 depends on T2 which isn't done. Should I do T2 first?"

### 3. State Implementation Plan

Before writing code:

```
Files: [list]
Approach: [brief description]
Success: [how to verify]
```

### 4. Implement

- Follow "What" and "Where" exactly
- Reference "Reuses" for patterns
- Apply [coding-principles.md](coding-principles.md):
  - Simplest code that works
  - Touch ONLY listed files
  - No scope creep

### 5. Verify "Done When"

Check all criteria before marking done.

### 6. Verify (teste executável)

Após implementar, avaliar se a task precisa de teste automatizado:

- **Precisa de teste:** task toca lógica de negócio, mutação de estado, API, ou fluxo condicional → criar teste que prove o comportamento, rodar, verde = segue
- **Não precisa:** task é apenas config, docs, rename, ou similar → verificação manual suficiente
- Rodar apenas os testes do módulo/arquivo afetado pela task (não a suite completa)
- A suite completa de testes roda uma vez só, após todas as tasks, antes do commit

### 7. Self-Check

Ask: "Would senior engineer flag this as overcomplicated?"

- Yes → Simplify before continuing
- No → Proceed to next task

### 8. Scope Guardrail

During implementation, you will notice things that could be improved, refactored, or added. **Do not act on them.** Instead:

- If it's a bug: note it in STATE.md as a blocker or use quick mode
- If it's an improvement: note it in STATE.md under "Deferred Ideas" or "Lessons Learned"
- If it's related to the current task: only include it if it's in the "Done when" criteria

**The heuristic:** "Is this in my task definition?" If no, don't touch it.

### 9. Update Task Status

Mark task complete in tasks.md. Update requirement traceability in spec.md if requirement IDs are used.

Após completar todas as tasks (ou a task atual no Quick Mode), rodar `/simplify` sobre o diff acumulado → pedir ao dev para rodar a suite completa de testes → **perguntar ao dev se quer commitar** ([commit.md](commit.md)).

---

## Se superpowers instalado

Ferramentas opcionais disponíveis durante Execute (configuradas via defaults opt-out no início da feature):

| Ferramenta | Quando usar | Skill |
|-----------|-------------|-------|
| **TDD** | Dev optou por TDD nos defaults | `superpowers:test-driven-development` — RED→GREEN→REFACTOR por task |
| **Git worktree** | Dev optou por isolamento | `superpowers:using-git-worktrees` — setup antes da primeira task |
| **Subagent por task** | Escopo Large/Complex com tasks independentes | `superpowers:subagent-driven-development` — inclui 2-stage review por task |
| **Debug estruturado** | Bug encontrado durante implementação | `superpowers:systematic-debugging` — investigate → analyze → hypothesis → fix |
| **Tasks paralelas** | Tasks independentes entre si | `superpowers:dispatching-parallel-agents` |
| **Validate/UAT** | Feature user-facing Complex | Invoke [validate.md](validate.md) — UAT interativo com relatório |

**Regra:** Essas ferramentas são workers. O ciclo do Execute (pick → implement → verify) continua sendo o trilho.

---

## Execution Template

```markdown
## Implementing T[X]: [Task Title]

**Reading**: task definition from tasks.md
**Dependencies**: [All done? ✅ | Blocked by: TY]

### Pre-Implementation (MANDATORY)

- **Assumptions**: [state explicitly]
- **Files to touch**: [list ONLY these]
- **Success criteria**: [how to verify]

### Implementation

[Do the work]

### Verification

- [x] Done when criterion 1
- [x] Done when criterion 2
- [x] No unnecessary changes made
- [x] Matches existing patterns
- [x] Teste criado e passando (se aplicável)
- [x] Testes do módulo afetado passando

**Status**: ✅ Complete | ❌ Blocked | ⚠️ Partial
```

---

## Tips

- **One task at a time** — Focus prevents errors
- **Tools matter** — Wrong MCP = wrong approach
- **Reuses save tokens** — Copy patterns, don't reinvent
- **Verify all criteria** — antes de marcar como concluído
- **Stay surgical** — Touch only what's necessary
- **Não commitar aqui** — após todas as tasks: /simplify → dev roda suite completa → commit
- **Never "while I'm here"** — Scope creep during implementation is the #1 quality killer
- **Learn from mistakes** — If something goes wrong, add a Lesson Learned to STATE.md
