# Execute

**Goal**: Implement ONE task at a time. Surgical changes. Verify. Repeat.

This is where code gets written. Every task follows the same cycle: plan → implement → verify. Verification is built into every task, not a separate phase.

⚠️ **NÃO commitar nesta fase.** O commit acontece na Fase 7 (Commit) após Review e Security.

---

## MANDATORY: Before Starting Any Implementation

### Baseline Test Gate (entry gate)

**ANTES de criar qualquer branch de trabalho** (`feature/*`, `bugfix/*`, `hotfix/*`, `release/*`), rodar a suite completa de testes na base atualizada (`develop` para feature/bugfix, `main` para hotfix).

```
SE suite passa (GREEN):
    → prosseguir para criação da branch e início da implementação

SE suite falha (RED):
    → ⚠️ ALERTA P0 ao dev:

    "Baseline RED detectado em <branch base>.
     N teste(s) falhando ANTES da minha implementação.
     Implementar sobre base quebrada esconde minha contribuição
     dentro das falhas pré-existentes.

     Opções:
       [1] STOP — corrigir baseline primeiro (RECOMENDADO)
       [2] OVERRIDE — prosseguir mesmo assim
            ↳ requer entrada em .specs/project/STATE.md com:
              - Lista de testes falhando (nome + erro)
              - SHA da base no momento do override
              - Responsável pela decisão
              - Plano e prazo para resolver o baseline
            ↳ NÃO exime do gate final pre-commit"
```

A entrada no STATE.md é estruturada (template):

```markdown
## Override Baseline Test Gate — YYYY-MM-DD

- **Base branch:** develop
- **Base SHA:** abc1234
- **Snapshot de falhas:**
  - test_foo_bar (TypeError: ...)
  - test_baz_qux (AssertionError: ...)
- **Responsável:** @dev
- **Razão do override:** hotfix urgente / decisão consciente de fazer paralelo / etc.
- **Plano para resolver baseline:** [quando + quem + como]
```

**Override aqui NÃO exime** o gate final pre-commit (`/simplify` + testes verdes). Se você overrideu o baseline RED, ao chegar no commit os testes precisam estar todos passando — incluindo os que falhavam antes. Caso contrário o commit é bloqueado.

> Fluxo detalhado com template de alerta, registro estruturado em STATE.md, casos especiais (CLAUDE.md sem testes, suite lenta, flaky) e reconciliação pré-commit: [../baseline-test-gate.md](../baseline-test-gate.md).

### Verificar branch (gitflow)

Se em branch protegida, sugerir criação da branch de trabalho apropriada (`feature/*`, `hotfix/*`, `release/*`) conforme [gitflow.md](../commit/gitflow.md). Neste ponto o tipo de trabalho já é conhecido.

### Load context (OBRIGATÓRIO)

Antes de implementar qualquer task, carregar nesta ordem:

1. `.specs/features/YYYY-MM-DD-[feature]/spec.md` — requisitos + IDs `[FEAT]-XX` para naming dos testes
2. `.specs/features/YYYY-MM-DD-[feature]/context.md` — **OBRIGATÓRIO se existir** — decisões aprovadas no discovery são constraints, não reoptar
3. `.specs/features/YYYY-MM-DD-[feature]/design.md` — arquitetura aprovada (se existir)
4. `.specs/features/YYYY-MM-DD-[feature]/tasks.md` — task específica + dependências + Done When

Se `context.md` registra uma decisão que parece incorreta agora, **escalar ao dev** com proposta de revisão. Nunca ignorar silenciosamente.

⚠️ **Pular esta carga = implementar contra constraint aprovado = retrabalho garantido.**

### Read [coding-principles.md](coding-principles.md) and state:

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

> Lembrete: as decisões em `context.md` carregadas no início desta seção são constraints. Não reoptar durante a implementação.

### 5. Verify "Done When"

Check all criteria before marking done.

### 6. Verify (teste executável)

Após implementar, avaliar se a task precisa de teste automatizado:

- **Precisa de teste:** task toca lógica de negócio, mutação de estado, API, ou fluxo condicional → rodar [ciclo TDD completo](tdd/tdd.md) (RED → Verify RED → GREEN → Verify GREEN → REFACTOR)
- **Não precisa:** task é apenas config, docs, rename, ou similar → verificação manual suficiente
- Rodar apenas os testes do módulo/arquivo afetado pela task (não a suite completa)
- A suite completa de testes roda uma vez só, após todas as tasks, antes do commit

**Iron Law (de [tdd.md](tdd/tdd.md)):**

> `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`

Escreveu código antes do teste? Delete e recomece. Não guarde "como referência". Para racionalizações comuns, ver tabela em [tdd.md](tdd/tdd.md#tabela-de-racionalizações). Para red flags que disparam "start over", ver [tdd.md](tdd/tdd.md#red-flags--stop-and-start-over).

**Naming dos testes:** os testes DEVEM referenciar critérios de aceite da spec. Não é "criar teste que prove o comportamento" genérico — é criar teste **nomeado com ID do requisito** que prove o critério QUANDO/ENTÃO específico (ex: `test_PAY03_expired_card_returns_declined`). Cada critério testável da spec deve ter pelo menos um teste correspondente com rastreabilidade explícita.

**Se a task envolve mocks:** ler [testing-anti-patterns.md](tdd/testing-anti-patterns.md) antes — 5 anti-padrões com Gate Functions para evitar testar mock em vez de comportamento real.

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

Após completar todas as tasks (ou a task atual no Quick Mode), rodar `/simplify` sobre o diff acumulado → pedir ao dev para rodar a suite completa de testes → **perguntar ao dev se quer commitar** ([commit.md](../commit/commit.md)).

---

## Roteamento de disciplinas (árvore de decisão)

Antes de implementar cada task, o agente DEVE decidir quais disciplinas aplicar usando esta árvore:

```
Task = bug fix?
├─ SIM → debug.md (4 fases obrigatórias antes de qualquer fix)
│        └─ Failing test reproduzindo o bug → tdd.md ciclo completo
└─ NÃO → segue abaixo

Tipo da task?
├─ Config / docs / rename / format → SEM TDD; verificação manual; pular para step 7 (Self-Check)
├─ Lógica de negócio / mutação de estado / API / fluxo condicional → tdd.md (RED → Verify RED → GREEN → Verify GREEN → REFACTOR)
└─ Mocks envolvidos? → ler testing-anti-patterns.md ANTES de escrever os mocks

Escopo da feature?
├─ Small / Medium → execução INLINE nesta sessão (você implementa direto)
├─ Large / Complex → subagents.md (3 subagents per task: implementer → spec compliance → code quality)
└─ Tasks marcadas [P] em tasks.md sem dependências cruzadas → parallel-dispatch.md
        └─ ANTES de despachar: verificar que os agents editariam ARQUIVOS DIFERENTES
        └─ DEPOIS do retorno: verification 4 passos (conflict check obrigatório)

Bug encontrado DURANTE implementação de outra task?
└─ STOP da task atual → debug.md → registrar em STATE.md → retomar task original
```

**Sinais de alerta** (mudam a disciplina escolhida):

| Sinal | Mude para |
|---|---|
| 3+ fixes consecutivos falharam | `debug.md` Fase 4.5 — questionar arquitetura, escalar ao dev |
| Subagent retorna BLOCKED | Diagnosticar: contexto faltando? modelo subdimensionado? task grande demais? plano errado? |
| Loop infinito reviewer ↔ implementer (3+ rodadas) | Re-ler feedback; pode ser task mal especificada no `tasks.md` |
| Mock setup > 50% do teste | Code está acoplado demais — usar dependency injection ([testing-anti-patterns.md](tdd/testing-anti-patterns.md) #3) |

---

## Disciplinas técnicas (referência rápida)

O Execute aplica estas disciplinas **automaticamente** conforme decidido pela árvore acima:

| Disciplina | Quando | Regra |
|---|---|---|
| **Baseline test** | Antes de qualquer task | Rodar suite de testes → se falham, reportar ao dev e aguardar |
| [tdd.md](tdd/tdd.md) (ciclo TDD interno) | Tasks com lógica | RED → Verify RED → GREEN → Verify GREEN → REFACTOR. Testes nomeados com ID do requisito (ex: `test_AUTH01_...`). Config/docs/rename → verificação manual |
| [debug.md](systematic-debugging/debug.md) (4 fases) | Bug encontrado | Iron Law: NO FIXES WITHOUT ROOT CAUSE FIRST. Phase 1 → 2 → 3 → 4. Após 3 fixes falharem (Phase 4.5) → escalar ao dev, questionar arquitetura |
| [subagents.md](subagents/subagents.md) (3 subagents por task) | Large/Complex | Implementer → **Spec Compliance Review → Code Quality Review** por task. Ordem obrigatória. Continuous execution entre tasks. |
| [parallel-dispatch.md](subagents/parallel-dispatch.md) | Tasks independentes (`[P]` em tasks.md, sem dependências cruzadas) | 1 agent por domínio disjunto. Após retorno: verification 4 passos (incluindo check de conflitos) + suite completa |
| [code-review.md](nano-disciplines:review/code-review.md) | Após todas as tasks (Large/Complex) | Code-reviewer subagent para revisão da implementação completa. Para pre-commit: Protocolo Dois-Eixos (ver [review.md](../review/review.md)) |

**Regra:** Essas disciplinas são workers. O ciclo do Execute (pick → implement → verify) continua sendo o trilho.

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
