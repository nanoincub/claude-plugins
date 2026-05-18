---
name: nanoincub-spec-driven
description: >
  Processo Spec-Driven da Nano Incub. Orquestra fases: Specify → Design → Tasks →
  Execute → /simplify → Docs → Commit. Verificação executável por task. Auto-sizing por complexidade.
  Standalone — disciplinas técnicas (TDD, debug, verification, code review, subagents) internalizadas.
  Triggers: "nova feature", "implementar", "quick fix", "review", "commitar",
  "pause work", "resume work". Não use para design UI, docs isoladas, infra pura.
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 4.0.0
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

## Princípio: trilho + disciplinas internas

Este processo define **O QUE fazer e EM QUE ORDEM** (o trilho: Specify → Design → Tasks → Execute → /simplify → Docs → Commit) e também **O COMO** (as disciplinas técnicas: TDD, debugging, verification, code review, subagents, parallel dispatch). Tudo internalizado em `references/`, sem dependências de plugins externos.

**Disciplinas técnicas** (workers invocados pelas fases):
- [execute/tdd/](references/execute/tdd/tdd.md) — TDD com Iron Law
- [execute/systematic-debugging/](references/execute/systematic-debugging/debug.md) — debug em 4 fases
- [execute/subagents/](references/execute/subagents/subagents.md) — fresh subagent per task + two-stage review
- [execute/subagents/parallel-dispatch.md](references/execute/subagents/parallel-dispatch.md) — múltiplos subagents em paralelo
- [meta/verification.md](references/meta/verification.md) — Iron Law "evidência antes de claim"
- [review/code-review.md](references/review/code-review.md) — code reviewer subagent (5 eixos) + Protocolo Dois-Eixos
- [review/receiving-feedback.md](references/review/receiving-feedback.md) — protocolo de recepção (zero performative agreement)

## Auto-Sizing

| Escopo | Critério | Specify | Design | Tasks | Execute | Ciclo Pós-Execute |
|--------|----------|---------|--------|-------|---------|--------------------|
| **Small** | ≤3 files, 1 frase | **Quick mode** | — | — | Implement + verify | /simplify → commit |
| **Medium** | Feature clara, <10 tasks | Spec breve | Skip — inline | Skip — implícito | Implement + verify | /simplify → commit |
| **Large** | Multi-componente | Full spec + IDs | Arquitetura + componentes | Breakdown + deps | Implement + verify por task | /simplify → commit |
| **Complex** | Ambiguidade, domínio novo | Full spec + [discuss](references/meta/discuss.md) | [Research](references/design/design.md) + arq. | Breakdown + paralelo | Implement + [UAT](references/review/validate.md) | /simplify → commit |

**Regras:**
- Specify e Execute são sempre obrigatórios
- /simplify é **obrigatório antes de qualquer commit** — roda sobre o diff acumulado de todas as tasks
- Suite completa de testes roda após /simplify, antes do commit
- Commit nunca é automático — sempre perguntar ao dev (invocar skill [`nano-spec:nano-commit`](../nano-commit/SKILL.md))
- Docs é obrigatório para Medium+ ; no Quick Mode é checklist inline
- Design é pulado quando não há decisões arquiteturais
- Tasks é pulado quando há ≤3 passos óbvios
- Discuss é triggered *dentro* do Specify apenas quando o agente detecta áreas ambíguas que precisam de input do usuário (apenas Complex)
- UAT interativo é triggered *dentro* do Execute apenas para features user-facing com comportamento complexo (apenas Complex)
- Review e Security estão **desativados por padrão** — ativar via defaults opt-out se dev pedir (ver [review.md](references/review/review.md) e [security.md](references/review/security.md))

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

### 5. Gate: Project Init (OBRIGATÓRIO antes de qualquer feature)

Antes de iniciar qualquer feature, verificar se os artefatos de projeto existem:

```
Verificar:
1. .specs/project/PROJECT.md  — visão, goals, stack, scope
2. .specs/project/ROADMAP.md  — features e milestones
3. .specs/codebase/            — STACK.md, ARCHITECTURE.md, CONVENTIONS.md,
                                 STRUCTURE.md, TESTING.md, INTEGRATIONS.md, CONCERNS.md
```

- Se `.specs/project/` NÃO existe → rodar [project-init.md](references/init/project-init.md) + [roadmap.md](references/init/roadmap.md)
- Se `.specs/codebase/` NÃO existe → rodar [brownfield-mapping.md](references/init/brownfield-mapping.md) (mesmo em projetos novos com scaffold)
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
- `.specs/features/YYYY-MM-DD-[feature]/spec.md` — Requisitos e critérios de aceite
- `.specs/features/YYYY-MM-DD-[feature]/design.md` — Arquitetura e componentes
- `.specs/features/YYYY-MM-DD-[feature]/tasks.md` — Tasks atômicas de implementação

### Decisões (opcional, criado lazy pelo grill)
- `.specs/decisions/NNNN-titulo.md` — ADRs (Architecture Decision Records) — criadas via [grill.md](references/meta/grill.md) quando hard-to-reverse + surprising + trade-off real
```

Isto garante que qualquer agente que leia o CLAUDE.md saiba exatamente onde buscar cada tipo de informação.

## Gate: Gitflow — em TODOS os modos (incluindo Quick Mode)

Fluxo completo na skill [`nano-spec:nano-commit`](../nano-commit/SKILL.md). **Este gate NÃO é opcional.**

**Pré-requisito (HARD BLOCK):** Na primeira interação com gitflow na sessão, executar `git flow version`. Se git-flow-next NÃO está instalado → **BLOQUEAR TODO O PROCESSO** até o dev instalar. Sem exceções, sem fallback para git puro. Única exceção: CLAUDE.md define `Sem gitflow` ou `trunk-based`.

1. **Pré-specify (ou pré-describe no Quick Mode):** Se em branch protegida (`main`, `develop`, `master`), executar `git pull` para garantir que o trabalho parte da versão mais recente. Se o CLAUDE.md desativa gitflow, pular.
2. **Pré-execute (ou pré-implement no Quick Mode):** Sugerir criação da branch de trabalho (`feature/*`, `hotfix/*`, `release/*`) — neste ponto já se sabe o tipo de trabalho. Aguardar decisão do dev antes de implementar.
3. **Pré-commit (última chance):** Se steps 1-2 foram pulados, verificar branch antes de commitar. Última oportunidade de criar branch de trabalho.
4. **Pós-commit:** Perguntar ao dev sobre fechamento da branch — merge, PR, continuar trabalhando, ou manter.

**Quick Mode simplifica cerimônia de planejamento, não pula safety gates.** Ver seção "Gate: Gitflow" em [quick-mode.md](references/quick-mode/quick-mode.md).

## Defaults Opt-Out

No início de cada feature (Medium+), apresentar defaults e deixar dev ajustar:

```
Escopo detectado: [Large]
Defaults: discovery + spec-reviewer → tasks + plan-reviewer →
          subagent-driven (two-stage review) → /simplify → verification → commit.
Opções para DESATIVAR: discovery extenso, TDD, subagents.
Opções para ATIVAR: code review extra, security.
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
        Opções: TDD, review, security. Ajustar? (Enter = defaults)

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
├── features/YYYY-MM-DD-[feature]/    # Prefixo de data OBRIGATÓRIO (ex: 2026-05-12-google-login)
│   ├── spec.md         # Requisitos com IDs rastreáveis
│   ├── context.md      # Decisões do usuário (inclui output de brainstorming)
│   ├── design.md       # Arquitetura & componentes
│   ├── tasks.md        # Tasks atômicas (inclui código de referência do writing-plans)
│   └── assets/         # Artefatos visuais (brainstorm HTML, diagramas exportados)
└── quick/NNN-slug/
    ├── TASK.md, SUMMARY.md
```

## Naming da pasta de feature (OBRIGATÓRIO)

Toda pasta em `.specs/features/` **DEVE** seguir o padrão `YYYY-MM-DD-[feature]`, onde:

- `YYYY-MM-DD` = data de criação da feature (data atual quando a fase Specify rodar)
- `[feature]` = slug em kebab-case derivado do título/intenção

**Exemplos válidos:**
- `.specs/features/2026-05-12-google-login/`
- `.specs/features/2026-05-12-payment-checkout/`
- `.specs/features/2026-05-13-fix-token-refresh/`

**Razão:** garante ordenação cronológica natural no filesystem e preserva histórico mesmo após renames.

**Quando criar:** no início da fase Specify, antes de escrever `spec.md`. Use a data corrente (não a data de início da sessão se diferente).

**Quando NÃO renomear:** depois de criada, a pasta mantém a data original mesmo que a feature seja revisada em outro dia.

### Migração de pastas legadas (pré-3.0.1)

Na detecção de contexto da sessão, **o agente DEVE** rodar:

```bash
find .specs/features -mindepth 1 -maxdepth 1 -type d \
  ! -regex '.*/[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-.*' 2>/dev/null
```

Se retornar 1+ pastas, oferecer **uma vez por sessão** (não a cada feature):

```
Detectei N pasta(s) em .specs/features/ sem prefixo de data (padrão pré-3.0.1):
  - <pasta1>
  - <pasta2>

Quer renomear para o padrão YYYY-MM-DD-[feature]? A data vem do primeiro commit
do spec.md (ou do filesystem, se a pasta nunca foi commitada).

[s] sim, renomear todas    [d] dry-run primeiro    [n] não, deixar como está
```

Resposta do dev:
- **s** → rodar `bash <PLUGIN_ROOT>/scripts/migrate-feature-dates.sh --yes`
- **d** → rodar `bash <PLUGIN_ROOT>/scripts/migrate-feature-dates.sh --dry-run` e perguntar de novo
- **n** → não tocar; lembrar do `STATE.md` que a migração foi recusada (não perguntar de novo na mesma sessão)

O script usa `git mv` quando possível (preserva histórico) e cai para `mv` simples fora de repo git.

## Output: tudo em .specs/ (OBRIGATÓRIO)

Artefatos de feature **SEMPRE** vão para `.specs/features/YYYY-MM-DD-[feature]/`:

| Artefato | Origem | Destino |
|---|---|---|
| Decisões + abordagem aprovada do discovery | Specify | `.specs/features/YYYY-MM-DD-[feature]/context.md` |
| Requisitos com IDs `[FEAT]-XX` | Specify | `.specs/features/YYYY-MM-DD-[feature]/spec.md` |
| Arquitetura + componentes | Design | `.specs/features/YYYY-MM-DD-[feature]/design.md` |
| Tasks atômicas (TDD inline) | Tasks | `.specs/features/YYYY-MM-DD-[feature]/tasks.md` |
| Artefatos visuais (mockups, diagramas exportados) | Discovery / Design | `.specs/features/YYYY-MM-DD-[feature]/assets/` |

**Regras de merge:**
- **context.md:** Decisões e trade-offs do discovery. Artefatos HTML interativos vão para `assets/`.
- **tasks.md (formato Nano):** Tasks no formato What/Where/Depends/Done-when/Verify. Código inline vai como seção `**Código de referência**` dentro de cada task — marcado como referência, NÃO copy-paste.
- **design.md:** Se já existe, fundir — não sobrescrever.
- Se o arquivo `.specs/` **já existir**, ler antes de editar — nunca sobrescrever sem merge.

## Commands

**Projeto:**
| Trigger | Reference |
|---------|-----------|
| Inicializar projeto | [project-init.md](references/init/project-init.md) |
| Criar roadmap | [roadmap.md](references/init/roadmap.md) |
| Mapear codebase | [brownfield-mapping.md](references/init/brownfield-mapping.md) |
| Documentar riscos | [concerns.md](references/init/concerns.md) |
| Registrar decisão/blocker | [state-management.md](references/meta/state-management.md) |
| Pausar/retomar trabalho | [session-handoff.md](references/meta/session-handoff.md) |

**Feature:**
| Trigger | Reference |
|---------|-----------|
| Especificar feature | [specify.md](references/specify/specify.md) |
| Discutir áreas cinzas | [discuss.md](references/meta/discuss.md) |
| Stress-test de spec / glossário | [grill.md](references/meta/grill.md) |
| Projetar arquitetura | [design.md](references/design/design.md) |
| Quebrar em tasks (horizontal ou vertical-slice) | [tasks.md](references/tasks/tasks.md) |
| Implementar | [implement.md](references/execute/implement.md) |
| Validar/UAT | [validate.md](references/review/validate.md) |
| Review de código | [review.md](references/review/review.md) |
| Auditoria de segurança | [security.md](references/review/security.md) |
| Atualizar docs do codebase | [docs-update.md](references/docs/docs-update.md) |
| Commitar | skill [`nano-spec:nano-commit`](../nano-commit/SKILL.md) |
| Gitflow / branching | skill [`nano-spec:nano-commit`](../nano-commit/SKILL.md) |
| Quick fix | [quick-mode.md](references/quick-mode/quick-mode.md) |

## Comportamento do Agente

Ver [agent-behavior.md](references/meta/agent-behavior.md). Resumo:
- Direto, sem cerimônia. Dev como senior.
- **Progress tracker obrigatório** — exibir fase atual e fases concluídas ao entrar em cada fase. Nunca omitir.
- Push-back quando spec vaga, scope creep, ou skip de gates.
- Flexibilizar quando dev pede, projeto legado, ou hotfix.

## Disciplinas por fase

Cada fase aplica disciplinas internas **automaticamente**. Dev pode desativar via defaults opt-out ou CLAUDE.md.

| Fase | Disciplina aplicada |
|---|---|
| **Specify** | [specify/specify.md](references/specify/specify.md) — discovery (2-3 abordagens, perguntas one-at-a-time) → spec self-review (5 critérios) → [spec-document-reviewer](references/specify/spec-document-reviewer-prompt.md) para Large/Complex → outputs em `context.md` + `spec.md` |
| **Design** | [design/design.md](references/design/design.md) — apresentar design incremental por seção com aprovação do dev → output para `design.md` |
| **Tasks** | [tasks/tasks.md](references/tasks/tasks.md) — premissa "zero context" + No Placeholders + TDD steps inline → plan self-review → [plan-document-reviewer](references/tasks/plan-document-reviewer-prompt.md) para Large/Complex → output para `tasks.md` |
| **Execute** | [execute/implement.md](references/execute/implement.md) com [tdd.md](references/execute/tdd/tdd.md) para tasks com lógica, [debug.md](references/execute/systematic-debugging/debug.md) quando encontrar bug, [subagents.md](references/execute/subagents/subagents.md) (two-stage review) para Large/Complex. Baseline test antes de começar. Sem worktree — trabalho na branch. |
| **Execute (bug)** | [debug.md](references/execute/systematic-debugging/debug.md) → Iron Law + 4 fases (Root Cause → Pattern → Hypothesis → Fix) → failing test antes de corrigir |
| **/simplify** | /simplify sobre diff acumulado (skill própria) |
| **Review** | [verification.md](references/meta/verification.md) (Iron Law: evidência antes de claims) + [code-review.md](references/review/code-review.md) (subagent reviewer com BASE_SHA/HEAD_SHA) ou Protocolo Dois-Eixos para Large/Complex pre-commit |
| **Docs** | Checklist contra `.specs/codebase/` — [brownfield-mapping](references/init/brownfield-mapping.md) se docs muito defasados |
| **Commit** | Skill `nano-spec:nano-commit` aplica [verification.md](references/meta/verification.md) (Iron Law) + fechamento estruturado (4 opções: merge/PR/manter/discard) → testes bloqueiam opções |

**Regras:**
- Aplicação automática — não perguntar antes de cada disciplina.
- Dev pode desativar via defaults opt-out, mas o padrão é ON.
- Disciplinas são workers — o ciclo do nano-spec (Specify → Execute → /simplify → Commit) é o trilho.
- Todo output vai para `.specs/`.

### Rastreabilidade Spec → Testes → Commit

A rastreabilidade é reforçada em 4 pontos do trilho:

1. **Spec → Tasks:** Após gerar `tasks.md`, o [plan-document-reviewer](references/tasks/plan-document-reviewer-prompt.md) DEVE verificar que TODOS os critérios QUANDO/ENTÃO da spec.md estão cobertos por pelo menos uma task.
2. **Spec → Testes:** Cada critério de aceite QUANDO/ENTÃO DEVE gerar um teste nomeado com o ID do requisito (ex: `test_AUTH01_invalid_email_returns_422`).
3. **Tasks → Commit:** Antes de commitar, aplicar [verification.md](references/meta/verification.md) (Iron Law) para verificar que todos os requisitos mapeados na spec.md foram implementados e têm testes passando.
4. **Execute → STATE.md:** Quando [debug.md](references/execute/systematic-debugging/debug.md) é acionado (bug encontrado), lessons learned DEVEM ser registradas em STATE.md com contexto estruturado.

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
**Monitoramento:** Exibir status quando >40k (ver [context-limits.md](references/meta/context-limits.md))

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
Se não, usar ferramentas built-in (ver [code-analysis.md](references/execute/code-analysis.md))
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

Ferramentas com graceful degradation. Ver [code-analysis.md](references/execute/code-analysis.md).
