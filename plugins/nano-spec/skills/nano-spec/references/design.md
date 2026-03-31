# Design

**Goal**: Define HOW to build it. Architecture, components, what to reuse.

**Skip this phase when:** The change is straightforward — no architectural decisions, no new patterns, no component interactions to plan. For simple features, design happens inline during Execute.

## Process

### 1. Load Context

Read `.specs/features/[feature]/spec.md` before designing. If `.specs/features/[feature]/context.md` exists, load it too — it contains implementation decisions that constrain the design (layout choices, behavior preferences, interaction patterns). Decisions marked as "Agent's Discretion" are yours to decide.

### 1.5. Research (Optional but Recommended)

If the feature involves unfamiliar technology, patterns, or integrations, research before designing. Document findings briefly in the design doc or as inline notes. This prevents incorrect assumptions from propagating into tasks.

Follow the **Knowledge Verification Chain** (see SKILL.md) in strict order:

```
Codebase → Project docs → Context7 MCP → Web search → Flag as uncertain
```

**CRITICAL: NEVER assume or fabricate information.** If you cannot find an answer through the chain, explicitly say "I don't know" or "I couldn't find documentation for this". Inventing an API, a pattern, or a behavior that doesn't exist is far worse than admitting uncertainty. Wrong assumptions propagate through design → tasks → implementation and cause cascading failures.

Good triggers for research: new libraries, unfamiliar APIs, performance-sensitive features, security-sensitive features, patterns you haven't used in this codebase before.

### 2. Define Architecture

Overview of how components interact. Use mermaid diagrams when helpful. Before creating any diagrams, check if the `mermaid-studio` skill is available (see Skill Integrations in SKILL.md).

### 3. Identify Code Reuse

**CRITICAL**: What existing code can we leverage? This saves tokens and reduces errors.

If `.specs/codebase/CONCERNS.md` exists, check it before designing. Any component flagged as fragile, carrying tech debt, or having test coverage gaps requires extra care in the design — document how the design mitigates those concerns.

### 4. Define Components and Interfaces

Each component: Purpose, Location, Interfaces, Dependencies, What it reuses.

### 5. Define Data Models

If the feature involves data, define models before implementation.

---

## Template: `.specs/features/[feature]/design.md`

**IMPORTANTE:** Este template é um esqueleto stack-agnostic. O agente DEVE:
- Escrever no **idioma do projeto** (detectado do CLAUDE.md)
- Usar **paths reais** do projeto (não `src/path/to/file`)
- Exemplos de código e interfaces na **linguagem do projeto**
- Modelos de dados no **formato do projeto** (Eloquent model, migration, etc.)

````markdown
# [Feature] — Design

**Spec**: `.specs/features/[feature]/spec.md`
**Status**: Draft | Approved

---

## Visão Geral da Arquitetura

[Descrição breve da abordagem arquitetural]

```mermaid
graph TD
    A[Ação do Usuário] --> B[Componente A]
    B --> C[Camada de Serviço]
    C --> D[Banco de Dados]
    B --> E[Componente B]
```
````

---

## Análise de Reuso

### Componentes Existentes

| Componente           | Localização                  | Como Usar                 |
| -------------------- | ---------------------------- | ------------------------- |
| [Componente]         | `app/[app]/path/to/file`     | [Estender/Importar/Ref]   |
| [Utilitário]         | `app/[app]/path/to/file`     | [Como ajuda]              |

### Pontos de Integração

| Sistema        | Método de Integração                    |
| -------------- | --------------------------------------- |
| [API existente]| [Como a feature se conecta]             |
| [Banco]        | [Como os dados se conectam]             |

---

## Componentes

### [Nome do Componente]

- **Propósito**: [O que faz — uma frase]
- **Localização**: `app/[app]/path/to/component`
- **Interface pública**:
  - `nomeMetodo(param): retorno` — [descrição]
- **Dependências**: [O que precisa para funcionar]
- **Reusa**: [Código existente que aproveita]

---

## Modelos de Dados (se aplicável)

[Descrever usando o formato da stack do projeto. Exemplos por stack:]

**Para projetos Laravel:**
```
Tabela: nome_tabela
- id (bigint, PK)
- campo1 (varchar)
- campo2 (integer)
- created_at, updated_at (timestamps)

Relacionamentos: belongsTo(OutroModel), hasMany(RelatedModel)
```

**Para projetos TypeScript:**
```typescript
interface NomeModel {
  id: string
  campo1: string
  campo2: number
}
```

**Para outros:** usar formato nativo da stack detectada.

---

## Tratamento de Erros

| Cenário        | Tratamento    | Impacto no Usuário |
| -------------- | ------------- | ------------------ |
| [Cenário 1]    | [Como tratar] | [O que o user vê]  |

---

## Decisões Técnicas (apenas não-óbvias)

| Decisão           | Escolha         | Justificativa |
| ----------------- | --------------- | ------------- |
| [O que decidimos] | [O que escolhemos] | [Por quê]  |

---

## Tips

- **Load context first** — If context.md exists, decisions there are locked
- **Research when uncertain** — 5 minutes of research prevents hours of rework
- **Reuse is king** — Every component should reference existing patterns
- **Interfaces first** — Define contracts before implementation
- **Keep it visual** — Diagrams save 1000 words (check mermaid-studio skill in Skill Integrations)
- **Small components** — If component does 3+ things, split it
- **Check CONCERNS.md** — If it exists, flag fragile areas the design must address
- **Confirm before Tasks** — User approves design before breaking into tasks
