---
name: nanoincub-spec-driven
description: >
  Processo Spec-Driven da Nano Incub. Orquestra fases: Specify → Design → Tasks →
  Execute → /simplify → Docs → Commit. Verificação executável por task. Auto-sizing por complexidade.
  Usa superpowers como motor quando instalado, funciona standalone quando não.
  Triggers: "nova feature", "implementar", "quick fix", "review", "commitar",
  "pause work", "resume work". Não use para design UI, docs isoladas, infra pura.
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 2.9.0
  based-on: tlc-spec-driven v2.0.0 by Felipe Rodrigues (github.com/felipfr)
---

# Nano Incub — Spec-Driven Development

Orquestrador leve. Gates obrigatórios. Zero cerimônia.

```
┌──────────┐   ┌──────────┐   ┌─────────┐   ┌─────────┐   ┌───────────┐   ┌──────┐   ┌────────┐
│ SPECIFY  │ → │  DESIGN  │ → │  TASKS  │ → │ EXECUTE │ → │ /SIMPLIFY │ → │ DOCS │ → │ COMMIT │
└──────────┘   └──────────┘   └─────────┘   └─────────┘   └───────────┘   └──────┘   └────────┘
   required      optional*      optional*     required       required       req M+     ask-dev
```

## Princípio: nanoincub = trilho, superpowers = motor

Este processo define O QUE fazer e EM QUE ORDEM. Quando `superpowers` está instalado,
delega O COMO para suas skills. Sem superpowers, funciona 100% standalone.

**Hierarquia:** nanoincub-spec-driven > using-superpowers > default system prompt.
O dispatcher do superpowers NÃO orquestra quando este processo está ativo.

## Auto-Sizing

| Escopo | Critério | Specify | Design | Tasks | Execute | Ciclo Pós-Execute |
|--------|----------|---------|--------|-------|---------|--------------------|
| **Small** | ≤3 files, 1 frase | **Quick mode** | — | — | Implement + verify | /simplify → commit |
| **Medium** | Feature clara, <10 tasks | Spec breve | Skip — inline | Skip — implícito | Implement + verify | /simplify → commit |
| **Large** | Multi-componente | Full spec + IDs | Arquitetura + componentes | Breakdown + deps | Implement + verify por task | /simplify → commit |
| **Complex** | Ambiguidade, domínio novo | Full spec + [discuss](references/discuss.md) | [Research](references/design.md) + arq. | Breakdown + paralelo | Implement + [UAT](references/validate.md) | /simplify → commit |

**Regras:**
- Specify e Execute são sempre obrigatórios
- /simplify é **obrigatório antes de qualquer commit** — roda sobre o diff acumulado de todas as tasks
- Suite completa de testes roda após /simplify, antes do commit
- Commit nunca é automático — sempre perguntar ao dev (ver [commit.md](references/commit.md))
- Docs é obrigatório para Medium+ ; no Quick Mode é checklist inline
- Design é pulado quando não há decisões arquiteturais
- Tasks é pulado quando há ≤3 passos óbvios
- Discuss é triggered *dentro* do Specify apenas quando o agente detecta áreas ambíguas que precisam de input do usuário (apenas Complex)
- UAT interativo é triggered *dentro* do Execute apenas para features user-facing com comportamento complexo (apenas Complex)
- Review e Security estão **desativados por padrão** — ativar via defaults opt-out se dev pedir (ver [review.md](references/review.md) e [security.md](references/security.md))

**Safety valve:** Se inline steps revelarem >5 steps → PARAR e criar tasks.md formal.

## Adaptação por Projeto (OBRIGATÓRIO)

Antes de iniciar qualquer fase, o agente DEVE carregar o contexto do projeto:

### 1. Detectar contexto do projeto

```
Ordem de leitura (parar quando encontrar):
1. CLAUDE.md (raiz do projeto ou monorepo)
2. AGENTS.md (se existir)
3. .specs/project/PROJECT.md (se existir)
```

### 2. Extrair convenções do projeto

Do CLAUDE.md e PROJECT.md, extrair e aplicar automaticamente:

| Convenção | Onde aplicar | Exemplo |
|-----------|-------------|---------|
| **Idioma do projeto** | Templates, mensagens, specs | PT-BR → specs em português |
| **Stack tecnológica** | Exemplos em templates (design, tasks) | PHP/Laravel → exemplos em PHP |
| **Scopes de commit** | Fase Commit | `api`, `painel-empresa`, etc. |
| **Comandos de teste** | Verificação no Execute | `docker exec ... php artisan test` |
| **Padrões de código** | coding-principles adaptados | camelCase, PascalCase, sufixos |
| **Regras de arquitetura** | Design, constraints | multi-tenancy, migrations centrais |
| **Containers/infra** | Comandos Artisan, migrations | Sempre via Docker |
| **Modelo de branching** | Commit (gitflow gate) | gitflow clássico, trunk-based, branches protegidas |

### 3. Regras de adaptação

- **Templates são esqueletos** — os exemplos dentro deles devem refletir a stack do projeto, não exemplos genéricos
- **Se o CLAUDE.md define modelo de branching** → usar esse modelo ao invés do gitflow clássico padrão
- **Se o CLAUDE.md define scopes de commit** → usar esses scopes, não inventar
- **Se o CLAUDE.md define comandos** (test, migrate, artisan) → usar esses comandos no Execute
- **Se o projeto tem .specs/codebase/** → carregar docs relevantes antes do Design
- **Se o projeto é monorepo** → identificar qual app é afetada e focar nela
- **Idioma**: usar o idioma do CLAUDE.md para toda comunicação e documentação gerada. Se CLAUDE.md está em português, specs, tasks, e mensagens devem ser em português.
- **Acentuação**: SEMPRE usar acentuação e caracteres especiais corretos do idioma detectado (ç, ã, é, ê, í, ó, ú, etc.). Nunca gerar texto sem acentos — "Especificação", não "Especificacao".

### 4. Cache de contexto

Na primeira invocação da sessão, extrair e manter em memória:

```
Projeto: [nome]
Stack: [linguagem/framework/versão]
Idioma: [PT-BR/EN/...]
Scopes de commit: [lista]
Branching: [gitflow clássico / trunk-based / custom]
Comando de teste: [comando]
Regras especiais: [lista resumida]
```

Exibir este resumo UMA VEZ no início da primeira fase. Não repetir.

### 4.1. Detectar Superpowers (OBRIGATÓRIO)

Na primeira invocação da sessão, verificar se `superpowers` está instalado:

```
Verificar se as skills estão disponíveis:
- superpowers:brainstorming
- superpowers:writing-plans
- superpowers:test-driven-development
- superpowers:systematic-debugging
- superpowers:verification-before-completion
```

**Se QUALQUER skill superpowers for encontrada** → `superpowers = true`.
Cachear resultado na sessão — não re-verificar.

Adicionar ao resumo de contexto:
```
Superpowers: [sim — skills disponíveis] ou [não — modo standalone]
```

**Quando `superpowers = true`:**
- Skills do superpowers são o **motor padrão** em cada fase (ver tabela "Integração Ativa")
- O dispatcher `using-superpowers` permanece DESATIVADO — nano-spec orquestra
- Dev pode desativar skills individuais via defaults opt-out ou CLAUDE.md

**Quando `superpowers = false`:**
- Fallback manual em cada fase (o processo funciona 100% standalone)
- Recomendar instalação UMA VEZ por sessão: `@superpowers` no marketplace

### 5. Gate: Project Init (OBRIGATÓRIO antes de qualquer feature)

Antes de iniciar qualquer feature, verificar se os artefatos de projeto existem:

```
Verificar:
1. .specs/project/PROJECT.md  — visão, goals, stack, scope
2. .specs/project/ROADMAP.md  — features e milestones
3. .specs/codebase/            — STACK.md, ARCHITECTURE.md, CONVENTIONS.md,
                                 STRUCTURE.md, TESTING.md, INTEGRATIONS.md, CONCERNS.md
```

- Se `.specs/project/` NÃO existe → rodar [project-init.md](references/project-init.md) + [roadmap.md](references/roadmap.md)
- Se `.specs/codebase/` NÃO existe → rodar [brownfield-mapping.md](references/brownfield-mapping.md) (mesmo em projetos novos com scaffold)
- Se ambos existem → carregar e continuar
- **NUNCA pular esta verificação.** CLAUDE.md NÃO substitui estes artefatos — são documentos com propósitos diferentes.
- Para projetos recém-scaffoldados, os docs de codebase serão breves mas ainda assim necessários para estabelecer a baseline.

**Após criar os artefatos**, adicionar uma seção `## Referência .specs/` no CLAUDE.md do projeto com um sumário que aponta para cada arquivo:

```markdown
## Referência .specs/

Documentação estruturada do projeto. Consultar antes de tomar decisões.

### Projeto
- `.specs/project/PROJECT.md` — Visão, goals, stack, scope
- `.specs/project/ROADMAP.md` — Features planejadas e milestones

### Codebase
- `.specs/codebase/STACK.md` — Stack tecnológica e dependências
- `.specs/codebase/ARCHITECTURE.md` — Padrões arquiteturais e fluxo de dados
- `.specs/codebase/CONVENTIONS.md` — Convenções de código e naming
- `.specs/codebase/STRUCTURE.md` — Estrutura de diretórios
- `.specs/codebase/TESTING.md` — Infraestrutura e padrões de teste
- `.specs/codebase/INTEGRATIONS.md` — Integrações externas
- `.specs/codebase/CONCERNS.md` — Tech debt, riscos e áreas frágeis

### Features
- `.specs/features/[feature]/spec.md` — Requisitos e critérios de aceite
- `.specs/features/[feature]/design.md` — Arquitetura e componentes
- `.specs/features/[feature]/tasks.md` — Tasks atômicas de implementação
```

Isto garante que qualquer agente que leia o CLAUDE.md saiba exatamente onde buscar cada tipo de informação.

## Gate: Gitflow — em TODOS os modos (incluindo Quick Mode)

Conforme [gitflow.md](references/gitflow.md). **Este gate NÃO é opcional.**

1. **Pré-specify (ou pré-describe no Quick Mode):** Se em branch protegida (`main`, `develop`, `master`), executar `git pull` para garantir que o trabalho parte da versão mais recente. Se o CLAUDE.md desativa gitflow, pular.
2. **Pré-execute (ou pré-implement no Quick Mode):** Sugerir criação da branch de trabalho (`feature/*`, `hotfix/*`, `release/*`) — neste ponto já se sabe o tipo de trabalho. Aguardar decisão do dev antes de implementar.
3. **Pré-commit (última chance):** Se steps 1-2 foram pulados, verificar branch antes de commitar. Última oportunidade de criar branch de trabalho.
4. **Pós-commit:** Perguntar ao dev sobre fechamento da branch — merge, PR, continuar trabalhando, ou manter.

**Quick Mode simplifica cerimônia de planejamento, não pula safety gates.** Ver seção "Gate: Gitflow" em [quick-mode.md](references/quick-mode.md).

## Defaults Opt-Out

No início de cada feature (Medium+), apresentar defaults e deixar dev ajustar.

**Com superpowers detectado:**
```
Escopo detectado: [Large]  |  Superpowers: ativo
Defaults: brainstorming → spec-reviewer → writing-plans → plan-reviewer →
          subagent-driven (two-stage review) → /simplify → verification → commit.
Opções para DESATIVAR: brainstorming, TDD, subagents, worktree.
Opções para ATIVAR: review extra, security.
Quer ajustar algo? (Enter para seguir com defaults)
```

**Sem superpowers:**
```
Escopo detectado: [Large]
Defaults: spec completa, tasks formais, execução sequencial,
          /simplify + suite de testes + commit.
Opções disponíveis: TDD, git worktree, subagent por task, review, security.
Quer ajustar algo? (Enter para seguir com defaults)
```

Uma pergunta, uma vez, com defaults sensatos. Se o dev configurar preferências
no CLAUDE.md do projeto, nunca mais perguntar.

## Workflows

**Projeto novo:**
1. Inicializar projeto → `.specs/project/` (PROJECT.md + ROADMAP.md)
2. Mapear codebase → `.specs/codebase/` (7 docs, mesmo com scaffold mínimo)
3. Para cada feature → Specify → (Design) → (Tasks) → Execute → /simplify → Suite de testes → Docs → Commit

**Codebase existente:**
1. Mapear codebase → `.specs/codebase/` (7 docs brownfield)
2. Inicializar projeto → PROJECT.md + ROADMAP.md
3. Para cada feature → mesmo fluxo adaptativo

**Quick mode:** Descrever → **Gitflow gate** → Implementar → Verificar → /simplify → Suite de testes → Docs (inline) → Commit

## Getting Started

```
Dev: "nova feature: login com Google"

Agente: Escopo Medium. Defaults: spec breve → execute → /simplify → suite de testes → commit.
        Opções: TDD, worktree, review, security. Ajustar? (Enter = defaults)

Dev: [Enter]

Agente: [Specify] Quem vai usar? Quais providers? Precisa de link com conta existente?

Dev: "Usuário final, só Google por enquanto, sim precisa linkar"

Agente: [gera spec.md com user stories + critérios de aceite]
        Spec ok? Posso implementar?

Dev: "sim"

Agente: [Execute] Implementando task 1...
        ✅ Implementado. Task toca lógica de auth → criando teste. Verde.

        Implementando task 2...
        ✅ Implementado. Verificação manual (config). OK.

        [/simplify] Analisando diff acumulado... 1 sugestão de reuse → corrigido.
        [Testes] Suite completa: 15/15 passando.
        [Docs] INTEGRATIONS.md atualizado (novo provider Google OAuth).

        Quer commitar?
Dev: "sim"

Agente: [Commit] feat(auth): add Google OAuth login — Refs: AUTH-01
```

## Project Structure

`.specs/` é a **fonte de verdade única** para todos os artefatos de planejamento.

```
.specs/
├── project/
│   ├── PROJECT.md      # Visão & objetivos
│   ├── ROADMAP.md      # Features & milestones
│   └── STATE.md        # Decisões, blockers, lições, deferred ideas
├── codebase/           # Brownfield (projetos existentes)
│   ├── STACK.md, ARCHITECTURE.md, CONVENTIONS.md
│   ├── STRUCTURE.md, TESTING.md, INTEGRATIONS.md
│   └── CONCERNS.md
├── features/[feature]/
│   ├── spec.md         # Requisitos com IDs rastreáveis
│   ├── context.md      # Decisões do usuário (inclui output de brainstorming)
│   ├── design.md       # Arquitetura & componentes
│   ├── tasks.md        # Tasks atômicas (inclui código de referência do writing-plans)
│   └── assets/         # Artefatos visuais (brainstorm HTML, diagramas exportados)
└── quick/NNN-slug/
    ├── TASK.md, SUMMARY.md
```

## Superpowers: Output para .specs/ (OBRIGATÓRIO)

Quando skills do superpowers gerarem artefatos de feature, **SEMPRE** salvar
dentro de `.specs/features/[feature]/` — **NUNCA** em `docs/superpowers/` ou `.superpowers/`.

| Skill superpowers | Output padrão (NÃO usar) | Output correto (.specs/) |
|---|---|---|
| `brainstorming` | `.superpowers/brainstorm/` | `.specs/features/[feature]/context.md` |
| `writing-plans` (plano) | `docs/superpowers/plans/` | `.specs/features/[feature]/tasks.md` |
| `writing-plans` (design) | `docs/superpowers/specs/` | `.specs/features/[feature]/design.md` |

**Regras de merge:**
- **brainstorming → context.md:** Decisões e escolhas vão para `context.md` no formato nano-spec. Artefatos HTML interativos vão para `assets/`.
- **writing-plans → tasks.md:** O plano vira `tasks.md` no formato TLC (What/Where/Depends/Done-when/Verify). Código inline vai como seção `**Código de referência**` dentro de cada task — marcado como referência, NÃO copy-paste.
- **writing-plans design → design.md:** Se `design.md` já existe, fundir — não sobrescrever.
- Se o arquivo `.specs/` **já existir**, ler antes de editar — nunca sobrescrever sem merge.

## Commands

**Projeto:**
| Trigger | Reference |
|---------|-----------|
| Inicializar projeto | [project-init.md](references/project-init.md) |
| Criar roadmap | [roadmap.md](references/roadmap.md) |
| Mapear codebase | [brownfield-mapping.md](references/brownfield-mapping.md) |
| Documentar riscos | [concerns.md](references/concerns.md) |
| Registrar decisão/blocker | [state-management.md](references/state-management.md) |
| Pausar/retomar trabalho | [session-handoff.md](references/session-handoff.md) |

**Feature:**
| Trigger | Reference |
|---------|-----------|
| Especificar feature | [specify.md](references/specify.md) |
| Discutir áreas cinzas | [discuss.md](references/discuss.md) |
| Projetar arquitetura | [design.md](references/design.md) |
| Quebrar em tasks | [tasks.md](references/tasks.md) |
| Implementar | [implement.md](references/implement.md) |
| Validar/UAT | [validate.md](references/validate.md) |
| Review de código | [review.md](references/review.md) |
| Auditoria de segurança | [security.md](references/security.md) |
| Atualizar docs do codebase | [docs-update.md](references/docs-update.md) |
| Commitar | [commit.md](references/commit.md) |
| Gitflow / branching | [gitflow.md](references/gitflow.md) |
| Quick fix | [quick-mode.md](references/quick-mode.md) |

## Comportamento do Agente

Ver [agent-behavior.md](references/agent-behavior.md). Resumo:
- Direto, sem cerimônia. Dev como senior.
- **Progress tracker obrigatório** — exibir fase atual e fases concluídas ao entrar em cada fase. Nunca omitir.
- Push-back quando spec vaga, scope creep, ou skip de gates.
- Flexibilizar quando dev pede, projeto legado, ou hotfix.

## Integração Ativa com Superpowers

Quando `superpowers = true` (detectado na seção 4.1), as skills são o **motor padrão** —
não opcionais. O agente DEVE invocá-las automaticamente. Se o dev quiser desativar,
faz via defaults opt-out ou CLAUDE.md.

| Fase | Superpowers (padrão quando detectado) | Fallback (standalone) |
|------|---------------------------------------|----------------------|
| **Specify** | **DEVE** invocar `brainstorming` → propor 2-3 abordagens → spec self-review via `spec-document-reviewer` → output para `context.md` + `spec.md` | Perguntas conversacionais |
| **Design** | **DEVE** usar `brainstorming` steps 5-8 → apresentar design incremental por seção → output para `design.md` | Research + design.md direto |
| **Tasks** | **DEVE** invocar `writing-plans` → tasks com TDD steps + código inline → plan self-review via `plan-document-reviewer` → output para `tasks.md` | Breakdown manual |
| **Execute** | **DEVE** usar `subagent-driven-development` (Large/Complex) com two-stage review (spec compliance → code quality) por task. `test-driven-development` para cada task com lógica. `systematic-debugging` quando encontrar bug. Baseline test antes de começar. | Ciclo implement → verify manual |
| **Execute (bug)** | **DEVE** invocar `systematic-debugging` → 4 fases (Root Cause → Pattern → Hypothesis → Fix) → failing test antes de corrigir | Fix ad-hoc |
| **/simplify** | /simplify sobre diff acumulado | (mesma skill) |
| **Review** | **DEVE** invocar `verification-before-completion` (Iron Law: evidência antes de claims) + `requesting-code-review` (subagent reviewer com BASE_SHA/HEAD_SHA) para Large/Complex | /simplify + self-check manual |
| **Docs** | Checklist contra `.specs/codebase/` — `brownfield-mapping` se docs muito defasados | Checklist manual |
| **Commit** | **DEVE** invocar `finishing-a-development-branch` → testes bloqueiam opções + 4 opções estruturadas + worktree cleanup | Conventional Commits + gitflow gate |

**Regras:**
- `DEVE` = invocação automática quando superpowers detectado. Não perguntar.
- Dev pode desativar qualquer skill via defaults opt-out — mas o padrão é ON.
- Skills são workers — o ciclo do nano-spec (Specify → Execute → /simplify → Commit) continua sendo o trilho.
- Todo output de skills vai para `.specs/` — NUNCA para `docs/superpowers/` ou `.superpowers/`.

### Rastreabilidade Spec → Testes → Commit

Quando superpowers está ativo, a rastreabilidade é reforçada:

1. **Spec → Tasks:** Após gerar `tasks.md`, o `plan-document-reviewer` DEVE verificar que TODOS os critérios QUANDO/ENTÃO da spec.md estão cobertos por pelo menos uma task.
2. **Spec → Testes:** Cada critério de aceite QUANDO/ENTÃO DEVE gerar um teste nomeado com o ID do requisito (ex: `test_AUTH01_invalid_email_returns_422`).
3. **Tasks → Commit:** Antes de commitar, `verification-before-completion` DEVE verificar que todos os requisitos mapeados na spec.md foram implementados e têm testes passando.
4. **Execute → STATE.md:** Quando `systematic-debugging` é invocado, lessons learned DEVEM ser registradas em STATE.md com contexto estruturado.

## Context Loading

**Base (~15k tokens):**
- PROJECT.md (se existir)
- ROADMAP.md (quando planejando/trabalhando em features)
- STATE.md (memória persistente)

**On-demand:**
- Codebase docs (quando trabalhando em projeto existente)
- CONCERNS.md (quando planejando features que tocam áreas frágeis)
- spec.md (quando trabalhando em feature específica)
- context.md (quando projetando ou implementando a partir de decisões)
- design.md (quando implementando a partir do design)
- tasks.md (quando executando tasks)

**Nunca carregar simultaneamente:**
- Múltiplas specs de features
- Múltiplos docs de arquitetura
- Documentos arquivados

**Target:** <40k tokens. Reserve 160k+ para trabalho.
**Monitoramento:** Exibir status quando >40k (ver [context-limits.md](references/context-limits.md))

## Knowledge Verification Chain

Ao pesquisar, projetar ou tomar decisões técnicas, seguir esta chain em ordem estrita:

```
Step 1: Codebase → código existente, convenções, padrões em uso
Step 2: Project docs → README, docs/, .specs/codebase/
Step 3: Context7 MCP → resolver library ID, consultar API/patterns atuais
Step 4: Web search → docs oficiais, fontes confiáveis
Step 5: Flag como incerto → "Não tenho certeza sobre X — meu raciocínio é Y, mas verifique"
```

**Regras:**
- Nunca pular para Step 5 se Steps 1-4 estão disponíveis
- Step 5 SEMPRE marcado como incerto — nunca apresentado como fato
- **NUNCA assumir ou fabricar.** Inventar APIs, patterns ou comportamentos que não existem causa falhas em cascata: design → tasks → implementação. Incerteza é sempre preferível a fabricação.

## Integrações com Skills de Terceiros

### Diagramas → mermaid-studio

Sempre que o workflow precisar criar ou atualizar diagramas, verificar se `mermaid-studio`
está instalado. Se sim, delegar. Se não, usar blocos mermaid inline e recomendar instalação
(uma vez por sessão).

### Exploração de código → codenavi

Sempre que o workflow precisar explorar código existente (brownfield mapping, análise de reuso,
identificação de padrões), verificar se `codenavi` está instalado. Se sim, delegar.
Se não, usar ferramentas built-in (ver [code-analysis.md](references/code-analysis.md))
e recomendar instalação (uma vez por sessão).

## Output Behavior

Após concluir tarefas leves (validação, state updates, session handoff), mencionar
naturalmente uma vez que tais tarefas funcionam bem com modelos mais rápidos/baratos.
Anotar em STATE.md em `Preferences` para não repetir.

Para tarefas pesadas (brownfield mapping, design complexo), notar brevemente os
requisitos de raciocínio antes de começar.

Ser conversacional, não robótico. Não interromper workflow — adicionar como nota
natural ao final. Pular se dev parece experiente ou já reconheceu a dica.

## Code Analysis

Ferramentas com graceful degradation. Ver [code-analysis.md](references/code-analysis.md).
