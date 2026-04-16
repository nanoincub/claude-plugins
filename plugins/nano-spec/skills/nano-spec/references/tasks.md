# Tasks

**Goal**: Break into GRANULAR, ATOMIC tasks. Clear dependencies. Right tools. Parallel execution plan.

**Skip this phase when:** There are ≤3 obvious steps. In that case, tasks are implicit — go straight to Execute and list them inline in your implementation plan.

## Why Granular Tasks?

| Vague Task (BAD) | Granular Tasks (GOOD)             |
| ---------------- | --------------------------------- |
| "Create form"    | T1: Create email input component  |
|                  | T2: Add email validation function |
|                  | T3: Create submit button          |
|                  | T4: Add form state management     |
|                  | T5: Connect form to API           |
| "Implement auth" | T1: Create login form             |
|                  | T2: Create register form          |
|                  | T3: Add token storage utility     |
|                  | T4: Create auth API service       |
|                  | T5: Add route protection          |

**Benefits of granular:**

- **Agents don't err** - Single focus, no ambiguity
- **Easy to test** - Each task = one verifiable outcome
- **Parallelizable** - Independent tasks run simultaneously
- **Errors isolated** - One failure doesn't block everything

**Rule**: One task = ONE of these:

- One component
- One function
- One API endpoint
- One file change

---

## Process

### Geração via superpowers (quando disponível)

Quando `superpowers` estiver instalado, o agente **DEVE** invocar `superpowers:writing-plans` para gerar as tasks antes de qualquer breakdown manual.

**Por quê:** o `writing-plans` assume um engineer com zero contexto do projeto — cada step inclui código real inline, segue TDD rigoroso (write failing test → run → implement → run → commit), e executa self-review automático ao final.

**Fluxo:**

1. Invocar `superpowers:writing-plans` passando como input a spec (`spec.md`) e o design (`design.md`) da feature
2. O output gerado vai para `.specs/features/[feature]/tasks.md`
3. Seguir com o Plan Self-Review (seção abaixo) antes de aprovar

**Se superpowers NÃO estiver disponível:** usar o breakdown manual descrito nas seções seguintes.

---

### 1. Review Design

Read `.specs/features/[feature]/design.md` before creating tasks.

### 2. Break Into Atomic Tasks

**Task = ONE deliverable**. Examples:

- ✅ "Create UserService interface" (one file, one concept)
- ❌ "Implement user management" (too vague, multiple files)

### 3. Define Dependencies

What MUST be done before this task can start?

### 4. Create Execution Plan

Group tasks into phases. Identify what can run in parallel.

### 5. ASK About MCPs and Skills

**CRITICAL**: Before execution, ask the user:

> "For each task, which tools should I use?"
>
> **Available MCPs**: [list from project or user]
> **Available Skills**: [list from project or user]

---

## Template: `.specs/features/[feature]/tasks.md`

```markdown
# [Feature] Tasks

**Design**: `.specs/features/[feature]/design.md`
**Status**: Draft | Approved | In Progress | Done

---

## Execution Plan

### Phase 1: Foundation (Sequential)

Tasks that must be done first, in order.
```

T1 → T2 → T3

```

### Phase 2: Core Implementation (Parallel OK)
After foundation, these can run in parallel.

```

     ┌→ T4 ─┐

T3 ──┼→ T5 ─┼──→ T8
└→ T6 ─┘
T7 ──────→

```

### Phase 3: Integration (Sequential)
Bringing it all together.

```

T8 → T9

---

## Task Breakdown

### T1: [Create X Interface]

**What**: [One sentence: exact deliverable]
**Where**: `src/path/to/file.ts`
**Depends on**: None
**Reuses**: `src/existing/BaseInterface.ts`
**Requirement**: [FEAT]-01 _(ID rastreável da spec.md — OBRIGATÓRIO)_
**Verify**: `npm test -- --grep "X Interface"` → espera "✓ all methods defined"

**Tools**:

- MCP: `filesystem` (or NONE)
- Skill: NONE

**Steps** (quando superpowers ativo — cada step com checkbox para tracking):

- [ ] Criar arquivo `src/path/to/file.ts` com interface base
- [ ] Escrever teste que falha validando métodos da interface (TDD red)
- [ ] Executar teste — confirmar falha esperada
- [ ] Implementar interface completa conforme design
- [ ] Executar teste — confirmar que passa (TDD green)
- [ ] Commit: `feat([scope]): create X interface`

> **Nota:** steps de teste DEVEM referenciar o critério QUANDO/ENTÃO da spec correspondente.
> Ex.: spec [FEAT]-01 diz "QUANDO usuário submete form ENTÃO valida email" → teste deve cobrir esse cenário.

**Done when**:

- [ ] Interface defined with all methods from design
- [ ] Types exported correctly
- [ ] No TypeScript errors

---

### T2: [Implement Y Service] [P]

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts`
**Depends on**: T1
**Reuses**: `src/services/BaseService.ts` patterns

**Tools**:

- MCP: `filesystem`, `context7`
- Skill: NONE

**Done when**:

- [ ] Implements interface from T1
- [ ] Handles error cases from design
- [ ] Unit test passes

---

### T3: [Create Z Component] [P]

**What**: [Exact deliverable]
**Where**: `src/components/ZComponent.tsx`
**Depends on**: T1
**Reuses**: `src/components/BaseComponent.tsx`

**Tools**:

- MCP: `filesystem`
- Skill: NONE

**Done when**:

- [ ] Component renders correctly
- [ ] Handles props from interface
- [ ] Follows existing component patterns

---

### T4: [Add A Feature to Y]

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts` (modify)
**Depends on**: T2, T3
**Reuses**: Existing service patterns

**Tools**:

- MCP: `filesystem`, `github`
- Skill: `api-design`

**Done when**:

- [ ] Feature works per acceptance criteria
- [ ] Integration test passes

**Commit**: `feat([scope]): [description]`

---

## Parallel Execution Map

Visual representation of what can run simultaneously:

```

Phase 1 (Sequential):
  T1 ──→ T2 ──→ T3

Phase 2 (Parallel):
  T3 complete, then:
    ├── T4 [P]
    ├── T5 [P]  } Can run simultaneously
    └── T6 [P]

Phase 3 (Sequential):
  T4, T5, T6 complete, then:
    T7 ──→ T8

```

---

## Task Granularity Check

Before approving tasks, verify they are granular enough:

| Task                            | Scope         | Status       |
| ------------------------------- | ------------- | ------------ |
| T1: Create email input          | 1 component   | ✅ Granular  |
| T2: Add validation function     | 1 function    | ✅ Granular  |
| T3: Create form with all fields | 5+ components | ❌ Split it! |
| T4: Connect to API              | 1 function    | ✅ Granular  |

**Granularity check**:

- ✅ 1 component / 1 function / 1 endpoint = Good
- ⚠️ 2-3 related things in same file = OK if cohesive
- ❌ Multiple components or files = MUST split

---

## Tips

- **[P] = Parallel OK** — Mark tasks that can run simultaneously
- **Reuses = Token saver** — Always reference existing code
- **Tools per task** — MCPs and Skills prevent wrong approaches
- **Dependencies are gates** — Clear what blocks what
- **Done when = Testable** — If you can't verify it, rewrite it
- **Requirement ID = Traceable** — Every task traces back to a spec requirement
- **One commit per task** — Plan the commit message format in advance

---

## Task Verification Standards

Every task MUST include:

**Done when checklist:**

- Specific, testable outcomes
- Pass/fail criteria
- Test execution commands

**Verify section:**

- Commands to prove functionality
- Expected outputs
- Success indicators

**Structure:**

```markdown
### T1: [Task name]

**What:** [Deliverable]
**Where:** [File path]

**Done when:**

- [ ] [Specific outcome]
- [ ] [Specific outcome]
- [ ] Tests pass: [command]

**Verify:**
[Command to prove it works]
[Expected output/behavior]
```

**Quality check:**

- Can task be verified without human judgment?
- Is success criteria binary (pass/fail)?
- Can verification be automated?

---

### Plan Self-Review (obrigatório quando superpowers ativo)

Após gerar `tasks.md`, o agente **DEVE** executar self-review antes de considerar o plano aprovado:

1. **Spec coverage**: cada requisito (`[FEAT]-XX`) da `spec.md` tem pelo menos uma task associada? Listar requisitos órfãos se houver.
2. **Placeholder scan**: buscar "TBD", "TODO", "...", ou steps sem código real inline. Nenhum placeholder é aceitável no plano final.
3. **Type consistency**: nomes de funções, métodos, interfaces e tipos são consistentes entre todas as tasks? (ex.: se T1 cria `UserService`, T3 não pode referenciar `UsersService`).

**Para features Large/Complex:** despachar subagent via **Agent tool** com o prompt template de `plan-document-reviewer` do superpowers (localizado em `skills/writing-plans/plan-document-reviewer-prompt.md`). Passar os paths de `tasks.md` e `spec.md` como input. O reviewer valida: completude, alinhamento com spec, decomposição e buildability.

**Se superpowers NÃO estiver disponível:** executar self-review manual contra os mesmos três critérios acima.

---

### Execution Handoff

Após `tasks.md` aprovado (self-review concluído sem pendências), oferecer ao desenvolvedor:

> **Como deseja executar?**
>
> 1. **Subagent-Driven** _(recomendado)_ — fresh subagent por task + two-stage review (code review + verification). Melhor isolamento de contexto e qualidade.
> 2. **Execução Inline** — mesmo contexto, sequencial. Mais rápido para features pequenas.

**Se superpowers NÃO estiver disponível:** execução inline é o único caminho — não oferecer opção de subagent.
