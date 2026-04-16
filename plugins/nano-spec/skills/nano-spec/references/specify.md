# Specify

**Goal**: Capture WHAT to build with testable, traceable requirements.

If the feature has ambiguous gray areas (multiple valid approaches for user-facing behavior), the agent will automatically trigger the [discuss gray areas](discuss.md) process within this phase. For clear, well-defined features, it goes straight to the next phase.

## Process

### 1. Clarify Requirements

You are a thinking partner, not an interviewer. Start open — let the user dump their mental model. Follow the energy: whatever they emphasize, dig into that.

Ask conversationally (not as a checklist):

- "What problem are you solving?"
- "Who is the user and what's their pain?"
- "What does success look like?"

If needed:

- "What are the constraints (time, tech, resources)?"
- "What is explicitly out of scope?"

**Challenge vagueness.** Never accept fuzzy answers. "Good" means what? "Users" means who? "Simple" means how? Make the abstract concrete: "Walk me through using this." "What does that actually look like?"

**Know when to stop.** When you understand what they're building, why, who it's for, and what done looks like — offer to proceed.

#### Integração com superpowers (quando detectado)

Quando o plugin **superpowers** estiver instalado, o agente **DEVE** invocar `superpowers:brainstorming` para conduzir o Specify. O brainstorming:

- Explora contexto e faz perguntas **uma a uma**
- Propõe **2-3 abordagens** com trade-offs claros
- Apresenta o design **por seções** com aprovação incremental do dev

Output do brainstorming vai para `.specs/features/[feature]/context.md`.

Se superpowers **não** estiver detectado, usar o fluxo de perguntas conversacionais existente acima (fallback).

### 2. Capture User Stories with Priorities

**P1 = MVP** (must ship), **P2** (should have), **P3** (nice to have)

Each story MUST be **independently testable** - you can implement and demo just that story.

> **Nota (superpowers ativo):** Quando o brainstorming propôs 2-3 abordagens, as user stories devem refletir **apenas a abordagem APROVADA** pelo dev, não todas as abordagens exploradas.

### 3. Write Acceptance Criteria

Use **WHEN/THEN/SHALL** format - it's precise and testable:

- WHEN [event/action] THEN [system] SHALL [response/behavior]

---

## Template: `.specs/features/[feature]/spec.md`

**IMPORTANTE:** Este template é um esqueleto. O agente DEVE:
- Escrever no **idioma do projeto** (detectado do CLAUDE.md)
- Adaptar exemplos à **stack do projeto** (detectada do CLAUDE.md/PROJECT.md)
- Usar **scopes e convenções** do projeto nos IDs e referências

```markdown
# [Feature Name] — Especificação

## Problema

[Descrever o problema em 2-3 frases. Que dor resolve? Por que agora?]

## Objetivos

- [ ] [Objetivo primário com resultado mensurável]
- [ ] [Objetivo secundário com resultado mensurável]

## Fora do Escopo

Excluído explicitamente. Documentado para prevenir scope creep.

| Item        | Motivo         |
| ----------- | -------------- |
| [Feature X] | [Por que excluído] |

---

## User Stories

### P1: [Título] ⭐ MVP

**User Story**: Como [papel], quero [capacidade] para que [benefício].

**Por que P1**: [Por que é crítico para MVP]

**Critérios de Aceite**:

1. QUANDO [ação/evento] ENTÃO o sistema DEVE [comportamento esperado]
2. QUANDO [ação/evento] ENTÃO o sistema DEVE [comportamento esperado]
3. QUANDO [caso limite] ENTÃO o sistema DEVE [tratamento gracioso]

**Teste Independente**: [Como verificar — ex: "Executar [comando do projeto] e confirmar [resultado]"]

---

### P2: [Título]

**User Story**: Como [papel], quero [capacidade] para que [benefício].

**Por que P2**: [Por que não é MVP mas importante]

**Critérios de Aceite**:

1. QUANDO [evento] ENTÃO o sistema DEVE [comportamento]

**Teste Independente**: [Como verificar]

---

### P3: [Título]

**User Story**: Como [papel], quero [capacidade] para que [benefício].

**Por que P3**: [Por que é nice-to-have]

**Critérios de Aceite**:

1. QUANDO [evento] ENTÃO o sistema DEVE [comportamento]

---

## Casos Limite

- QUANDO [condição de fronteira] ENTÃO o sistema DEVE [comportamento]
- QUANDO [cenário de erro] ENTÃO o sistema DEVE [tratamento gracioso]
- QUANDO [input inesperado] ENTÃO o sistema DEVE [resposta de validação]

---

## Rastreabilidade de Requisitos

Cada requisito recebe um ID único para rastreamento entre design, tasks e validação.

| ID Requisito   | Story       | Fase   | Status  |
| -------------- | ----------- | ------ | ------- |
| [FEAT]-01      | P1: [Story] | Design | Pending |
| [FEAT]-02      | P1: [Story] | Design | Pending |
| [FEAT]-03      | P2: [Story] | -      | Pending |

**Formato do ID:** `[CATEGORIA]-[NÚMERO]` (ex: `AUTH-01`, `COLAB-03`, `NOTIF-02`)

**Valores de status:** Pending → In Design → In Tasks → Implementing → Verified

**Cobertura:** X total, Y mapeados em tasks, Z sem mapeamento ⚠️

---

## Critérios de Sucesso

Como sabemos que a feature está pronta:

- [ ] [Resultado mensurável]
- [ ] [Resultado mensurável]

---

## Notas Técnicas (opcional, quando relevante)

Incluir quando a feature tem constraints técnicas que o time de design/tasks precisa saber:

- **Auth existente**: [framework/lib atual que deve ser preservada]
- **Multi-tenancy**: [como a feature interage com o modelo multi-tenant]
- **Banco de dados**: [tipo de banco, ORM, constraints]
- **Lib sugerida**: [biblioteca ou abordagem técnica preferida]
- **Migrations**: [onde vivem as migrations, tabelas afetadas]
- **UI**: [framework de UI, componentes afetados]
- **Scopes afetados**: [quais scopes de commit serão tocados]
```

---

### Spec Self-Review (obrigatório quando superpowers ativo)

Quando o plugin **superpowers** estiver detectado, após gerar `spec.md`, o agente **DEVE** realizar spec self-review com os seguintes critérios:

1. **Placeholder scan** — buscar "TBD", "TODO", seções vazias ou incompletas
2. **Consistência interna** — seções se contradizem entre si?
3. **Scope check** — spec está focada o suficiente para gerar um plano executável?
4. **Ambiguity check** — algum requisito é interpretável de 2 formas diferentes?
5. **YAGNI** — há features ou requisitos não solicitados pelo dev?

Corrigir problemas encontrados **inline** na própria spec. Sem ciclo de re-review.

Para escopo **Large/Complex**: despachar subagent via **Agent tool** com o prompt template de `spec-document-reviewer` do superpowers (localizado em `skills/brainstorming/spec-document-reviewer-prompt.md`). Passar o path do `spec.md` como input. O reviewer valida: completude, consistência, clareza, escopo e YAGNI.

Se superpowers **não** estiver detectado: o agente faz self-review manual contra os mesmos 5 critérios acima.

---

## Tips

- **P1 = Vertical Slice** — feature completa e demo-ável, não só backend ou frontend
- **QUANDO/ENTÃO é código** — se não dá pra escrever como teste, reescrever
- **IDs de requisito são obrigatórios** — toda story mapeia para IDs rastreáveis
- **Casos limite importam** — o que quebra? O que é vazio? O que é enorme?
- **Fora do Escopo previne creep** — se não está aqui, não é construído
- **Confirmar antes de Discuss** — usuário aprova spec antes de avançar
- **Decomposição** — Se o pedido descreve múltiplos subsistemas independentes, decompor em sub-projetos antes de especificar. Cada sub-projeto tem seu próprio ciclo spec→plan→execute.
- **Acentuação correta** — SEMPRE usar acentuação e caracteres especiais do idioma do projeto (ç, ã, é, etc.). Nunca gerar texto sem acentos.
