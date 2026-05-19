# Tasks

**Goal**: Break into GRANULAR, ATOMIC tasks. Clear dependencies. Right tools. Parallel execution plan.

**Skip this phase when:** There are ≤3 obvious steps. In that case, tasks are implicit — go straight to Execute and list them inline in your implementation plan.

## Premissa de escrita

Escreva o `tasks.md` assumindo que **o executor tem zero contexto do codebase e gosto questionável**. Isso significa:

- **Código real inline em cada step** — não "implemente a função X", mas o corpo da função no markdown.
- **Comandos exatos com output esperado** — não "rode os testes", mas `pytest path/test.py::name -v` → `PASS`.
- **Paths de arquivo completos** — não "no service de usuário", mas `src/services/user_service.py:123-145`.

Se um engenheiro precisa **interpretar** o que está escrito para executar, o plano falhou.

## No Placeholders (plan failures)

Os padrões abaixo são **falhas de plano** — nunca apareçam no `tasks.md` final:

- `TBD`, `TODO`, `implement later`, `fill in details`
- `Add appropriate error handling` / `add validation` / `handle edge cases` (sem detalhar quais erros, quais validações)
- `Write tests for the above` (sem o código real dos testes)
- `Similar to Task N` (repita o código — o executor pode ler tasks fora de ordem)
- Steps que descrevem **o que** fazer sem mostrar **como** (code blocks são obrigatórios em steps de código)
- Referências a tipos, funções ou métodos não definidos em nenhuma task

Se o self-review encontrar qualquer um desses, **corrigir inline antes de avançar**.

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

## Modos de breakdown

A geração de tasks tem **dois modos**. O agente escolhe baseado no escopo:

| Modo | Quando usar | Granularidade |
|------|-------------|---------------|
| **Horizontal (default)** | Small/Medium, ou Large/Complex single-component | 1 task = 1 componente / função / arquivo |
| **Vertical-slice (tracer bullets)** | Large/Complex multi-camada (schema + API + UI) | 1 task = 1 fatia end-to-end através de todas as camadas |

Em features multi-camada, o modo vertical-slice produz incrementos demoáveis isoladamente — cada slice "atravessa" o sistema inteiro. Útil quando há risco de integração ou quando o dev quer ver valor entregue continuamente.

Adaptado de `to-issues` (matpocock-skills). Diferença: no Nano, slices viram tasks no `tasks.md` local — não publicamos automaticamente em issue tracker externo (publicação no ClickUp fica opcional via skill `ticket`).

### Vertical-slice + TDD inline (duas camadas)

Vertical-slice define a **fronteira** de cada task (end-to-end através de camadas); a "Premissa de escrita" + "No Placeholders" no topo deste arquivo definem o **interior** de cada task (TDD step-by-step com código inline). Não são incompatíveis — são camadas diferentes:

1. Primeiro desenhar slices (HITL/AFK + dependências + acceptance criteria)
2. Depois, para cada slice aprovado, expandir os steps TDD internos com código real inline (premissa "zero context, questionable taste")
3. Resultado em `tasks.md`: cada task é um slice com steps TDD inline

Quando vertical-slice está ativo, a expansão de steps TDD aplica-se **dentro de cada slice**, não para gerar o breakdown inteiro de uma vez.

### Regras de vertical slice

- Cada slice entrega um caminho **estreito mas COMPLETO** por todas as camadas (schema, API, UI, testes)
- Slice concluído é **demoável ou verificável isoladamente**
- Preferir muitos slices finos sobre poucos grossos
- Cada slice é **HITL** (human-in-the-loop) ou **AFK** (autônomo)
  - **HITL** — exige decisão arquitetural, revisão de design, ou aprovação do dev
  - **AFK** — pode ser implementado e mergeado sem interação

Preferir AFK quando possível.

### Fluxo do modo vertical-slice

1. Ler `spec.md` e `design.md`
2. Desenhar slices (numerados, com tipo HITL/AFK e dependências)
3. Apresentar breakdown ao dev como lista numerada com:
   - **Título** curto e descritivo
   - **Tipo** (HITL/AFK)
   - **Blocked by** (refs a outros slices)
   - **User stories cobertas** (refs a `[FEAT]-XX` da spec)
4. Quiz ao dev:
   - A granularidade está certa? (grosso/fino demais)
   - As dependências estão corretas?
   - Algum slice deve ser unido ou dividido?
   - Marcação HITL/AFK está correta?
5. Iterar até aprovação
6. Gravar slices como tasks em `tasks.md` na ordem de dependência (blockers primeiro)

### Template de task em modo vertical-slice

```markdown
### T1: [Slice — verbo + objeto end-to-end]

**Tipo**: AFK | HITL
**O que entrega**: [Descrição concisa do comportamento end-to-end. NÃO listar camada-por-camada.]
**Camadas tocadas**: [schema, API, UI, testes — quais entram no slice]
**Depends on**: None | T0
**Refs**: `[FEAT]-01, [FEAT]-02` _(IDs rastreáveis da spec.md — OBRIGATÓRIO)_

**Critérios de aceite**:
- [ ] [Critério 1 — demoável]
- [ ] [Critério 2 — demoável]
- [ ] [Critério 3 — demoável]

**Verify**: [Comando ou cenário manual que prova o slice]
```

Evitar paths de arquivo específicos e snippets de código no campo "O que entrega" — eles ficam stale rápido. Exceção: se um protótipo (ver [discuss.md](../meta/discuss.md)) produziu um snippet que codifica uma decisão de forma mais precisa que prosa (state machine, schema, type shape), inlinar e marcar como vindo de protótipo.

---

## Process

### 1. Load Context (OBRIGATÓRIO)

Antes de quebrar em tasks, carregar nesta ordem:

1. `.specs/features/YYYY-MM-DD-[feature]/spec.md` — requisitos + IDs `[FEAT]-XX`
2. `.specs/features/YYYY-MM-DD-[feature]/context.md` — **OBRIGATÓRIO se existir** — decisões aprovadas no discovery (abordagem escolhida, trade-offs, restrições) são constraints; tasks não devem contradizer
3. `.specs/features/YYYY-MM-DD-[feature]/design.md` — arquitetura aprovada (se a fase Design rodou)

Se `context.md` registra decisão que conflita com o design proposto, escalar ao dev antes de gerar tasks. Não inventar reconciliação silenciosa.

### 1.5. Load Test Coverage Matrix

Ler `.specs/codebase/TESTING.md` (se existir) antes de criar tasks. A Matriz de Cobertura de Testes
e a Avaliação de Paralelismo orientam duas decisões críticas:

**Testes co-localizados:** toda task que cria ou modifica uma camada de código com tipo de teste exigido
DEVE incluir a escrita/atualização desses testes na mesma task. Testes NÃO são tasks separadas.

| Task cria...                                  | Done When deve incluir...                          |
| --------------------------------------------- | -------------------------------------------------- |
| Camada com exigência "unit"                   | Unit test escrito + gate quick passa               |
| Camada com exigência "e2e"                    | E2E test escrito + gate full passa                 |
| Camada com exigência "integration"            | Integration test escrito + gate full passa         |
| Camada com exigência "none"                   | Gate check no nível apropriado                     |

**Flags de paralelismo:** cruzar com a Avaliação de Paralelismo ao marcar tasks `[P]`:

- Se o tipo de teste exigido da task está marcado "Parallel-Safe: Não" → remover flag `[P]`
- Se o tipo de teste exigido da task está marcado "Parallel-Safe: Sim" → `[P]` é permitido
- Se a task não tem testes → `[P]` depende apenas de dependências de código

Se `TESTING.md` não existir (projeto greenfield), perguntar ao dev quais tipos de teste e comandos
o projeto usará antes de criar tasks.

### 2. Break Into Atomic Tasks

**Task = ONE deliverable**. Examples:

- ✅ "Create UserService interface" (one file, one concept)
- ❌ "Implement user management" (too vague, multiple files)

### 3. Define Dependencies

What MUST be done before this task can start?

### 4. Create Execution Plan

Group tasks into phases. Identify what can run in parallel.

### 5. Validate Before Presenting (OBRIGATÓRIO)

Antes de apresentar as tasks ao dev, rodar TODOS os três pre-approval checks. Não são opcionais — são gates. Se qualquer check falhar, reestruturar as tasks e re-rodar até passarem.

**Check 1: Task Granularity** — verificar que cada task é atômica (ver seção Task Granularity Check).

**Check 2: Diagram-Definition Cross-Check** — verificar que o diagrama de execução bate com o campo `Depends on` de cada task (ver seção Diagram-Definition Cross-Check). Construir a tabela cross-check e incluí-la no output.

**Check 3: Test Co-location Validation** — verificar que o campo `Tests` de cada task bate com a matriz de cobertura do `TESTING.md` (ver seção Test Co-location Validation). Construir a tabela de validação e incluí-la no output.

**Apresentar ambas as tabelas junto com as tasks** para o dev ver os resultados da validação. Qualquer ❌ significa que VOCÊ deve reestruturar antes de apresentar — não mostrar tasks falhando ao dev pedindo aprovação.

### 6. ASK About MCPs and Skills

**CRITICAL**: Before execution, ask the user:

> "For each task, which tools should I use?"
>
> **Available MCPs**: [list from project or user]
> **Available Skills**: [list from project or user]

---

## Template: `.specs/features/YYYY-MM-DD-[feature]/tasks.md`

```markdown
# [Feature] Tasks

**Design**: `.specs/features/YYYY-MM-DD-[feature]/design.md`
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
**Refs**: `[FEAT]-01` _(IDs rastreáveis da spec.md — OBRIGATÓRIO; múltiplos separados por vírgula)_
**Verify**: `npm test -- --grep "X Interface"` → espera "✓ all methods defined"

**Tools**:

- MCP: `filesystem` (or NONE)
- Skill: NONE

**Steps** (cada step com checkbox para tracking):

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

**Tests**: [unit/e2e/integration/none — vindo da coverage matrix]
**Gate**: [quick/full/build — vindo dos gate check commands]

---

### T2: [Implement Y Service] [P]

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts`
**Depends on**: T1
**Reuses**: `src/services/BaseService.ts` patterns
**Refs**: `[FEAT]-02, [FEAT]-03`

**Tools**:

- MCP: `filesystem`, `context7`
- Skill: NONE

**Done when**:

- [ ] Implements interface from T1
- [ ] Handles error cases from design
- [ ] Gate check passa: `[comando quick gate vindo do TESTING.md]`
- [ ] Test count: [N] tests passam (sem deleções silenciosas)

**Tests**: unit
**Gate**: quick

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
- [ ] Gate check passa: `[comando quick gate vindo do TESTING.md]`
- [ ] Test count: [N] tests passam (sem deleções silenciosas)

**Tests**: unit
**Gate**: quick

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
- [ ] Gate check passa: `[comando full gate vindo do TESTING.md]`
- [ ] Test count: [N] tests passam (sem deleções silenciosas)

**Tests**: integration
**Gate**: full

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

**Constraint de paralelismo:** uma task marcada `[P]` precisa ter TODAS estas condições:

- Nenhuma dependência pendente
- Tipo de teste exigido é parallel-safe (segundo Avaliação de Paralelismo do `TESTING.md`)
- Sem estado mutável compartilhado com outras tasks `[P]` na mesma fase

Se os testes da task NÃO são parallel-safe, ela DEVE rodar sequencial mesmo que o código de implementação não tenha dependências. A execução dos testes é o gargalo.

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

## Diagram-Definition Cross-Check

Antes de aprovar as tasks, verificar que o diagrama de execução é consistente com as definições das tasks. Esses são artefatos independentes que podem divergir — o diagrama é desenhado para clareza visual, enquanto o corpo das tasks é escrito para precisão. Os dois precisam concordar.

Para cada task, conferir:

| Task | Depends On (corpo da task) | Diagrama mostra              | Status                |
| ---- | -------------------------- | ---------------------------- | --------------------- |
| T[N] | [deps do corpo]            | [deps das setas do diagrama] | ✅ Match ou ❌ Mismatch |

**Regras:**

- Todo `Depends on` no corpo da task precisa ter seta correspondente no diagrama.
- Toda seta no diagrama precisa corresponder a um `Depends on` no corpo da task alvo.
- Tasks mostradas como paralelas (`[P]`) no diagrama não podem depender umas das outras.
- Se uma task depende de outra na mesma fase paralela, elas NÃO são paralelas — corrigir o diagrama ou remover a flag `[P]`.

---

## Test Co-location Validation

Antes de aprovar as tasks, verificar que o campo `Tests` de TODA task é consistente com a Matriz de Cobertura de Testes do `TESTING.md`. Este é um gate hard — tasks que falham aqui DEVEM ser corrigidas.

Para cada task, conferir: a task cria ou modifica uma camada de código que tem tipo de teste exigido na matriz de cobertura? Se sim, o campo `Tests` da task DEVE bater.

| Task           | Camada criada/modificada       | Matriz exige | Task diz             | Status                  |
| -------------- | ------------------------------ | ------------ | -------------------- | ----------------------- |
| T[N]: [nome]   | [camada da matriz]             | [tipo]       | [campo Tests da task]| ✅ OK ou ❌ VIOLATION  |

**Regras:**

- "Testado em outra task" NÃO é justificativa válida para `Tests: none`. Isso é test deferral — exatamente o anti-pattern que esta validação previne.
- `Tests: none` só é válido quando a matriz de cobertura diz "none" para aquela camada de código.
- Se a task cria MÚLTIPLAS camadas (ex: service + controller), usar o tipo de teste MAIS ALTO exigido por qualquer uma delas.
- Qualquer ❌ VIOLATION → reestruturar a task para incluir os testes exigidos antes de prosseguir.

**Resolvendo dependências de compilação:**

Quando uma task cria código que só pode ser testado depois que uma task posterior completa (ex: um controller que precisa de wiring de módulo antes que seus testes e2e rodem), NÃO adiar os testes para uma task separada. Em vez disso, reestruturar:

1. **Merge forward:** mover os testes da task não-testável para a task mais cedo onde eles passam a ser executáveis (ex: a task de wiring inclui wiring + testes e2e para o controller que ela habilita).
2. **Merge backward:** absorver a dependência bloqueante na task atual para que ela se torne self-testable (ex: a task de controller inclui seu próprio registro de módulo).

Escolher a opção que mantém as tasks atômicas e coesas. O objetivo: nenhuma task produz código não-verificado. Se o código não pode ser testado na task que o cria, as fronteiras da task estão erradas.

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

- Outcomes específicos, testáveis
- Critérios pass/fail
- Comando de teste específico vindo da tabela Gate Check Commands
- Pass count esperado (previne deleção silenciosa de testes)

**Verify section:**

- Commands to prove functionality
- Expected outputs
- Success indicators

**Structure:**

```markdown
### T1: [Task name]

**What:** [Deliverable]
**Where:** [File path]
**Tests**: [unit/e2e/integration/none]
**Gate**: [quick/full/build]

**Done when:**

- [ ] [Specific outcome]
- [ ] [Specific outcome]
- [ ] Gate check passa: `[comando vindo dos Gate Check Commands]`
- [ ] Test count: [N] tests passam (sem deleções silenciosas)

**Verify:**
[Command to prove it works]
[Expected output/behavior]
```

**Quality check:**

- Can task be verified without human judgment?
- Is success criteria binary (pass/fail)?
- Can verification be automated?

---

### Plan Self-Review (obrigatório)

Após gerar `tasks.md`, o agente **DEVE** executar self-review antes de considerar o plano aprovado:

1. **Spec coverage**: cada requisito (`[FEAT]-XX`) da `spec.md` tem pelo menos uma task associada? Listar requisitos órfãos se houver.
2. **Placeholder scan**: buscar "TBD", "TODO", "...", ou steps sem código real inline. Nenhum placeholder é aceitável no plano final.
3. **Type consistency**: nomes de funções, métodos, interfaces e tipos são consistentes entre todas as tasks? (ex.: se T1 cria `UserService`, T3 não pode referenciar `UsersService`).

**Para features Large/Complex:** despachar subagent via **Agent tool** usando o prompt template em [`plan-document-reviewer-prompt.md`](plan-document-reviewer-prompt.md). Passar os paths de `tasks.md` e `spec.md` como input. O reviewer valida: completude, alinhamento com spec, decomposição e buildability.

**Para features Small/Medium:** executar self-review manual contra os três critérios acima.

---

### Execution Handoff

Após `tasks.md` aprovado (self-review concluído sem pendências), oferecer ao desenvolvedor:

> **Como deseja executar?**
>
> 1. **Subagent-Driven** _(recomendado para Large/Complex)_ — fresh subagent por task + two-stage review (spec compliance → code quality). Melhor isolamento de contexto e qualidade. Ver [`nano-disciplines:skills/nano-disciplines/references/subagents/subagents.md`](nano-disciplines:skills/nano-disciplines/references/subagents/subagents.md).
> 2. **Execução Inline** — mesmo contexto, sequencial. Mais rápido para features pequenas. Ver [`../execute/implement.md`](../execute/implement.md).
