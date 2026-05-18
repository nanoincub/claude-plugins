# Nano-Spec — Guia Passo a Passo

> Processo Spec-Driven da Nano Incub para Claude Code.
> Este guia te leva do zero ao primeiro commit, com cada etapa explicada.

---

## Sumário

- [Parte 1 — Entender em 1 minuto](#parte-1--entender-em-1-minuto)
- [Parte 2 — Pré-requisitos (instalar antes de usar)](#parte-2--pré-requisitos-instalar-antes-de-usar)
- [Parte 3 — Primeira vez no projeto](#parte-3--primeira-vez-no-projeto)
- [Parte 4 — Fluxo de uma feature, passo a passo](#parte-4--fluxo-de-uma-feature-passo-a-passo)
- [Parte 5 — Os 4 tamanhos de tarefa](#parte-5--os-4-tamanhos-de-tarefa)
- [Parte 6 — Os gates inegociáveis](#parte-6--os-gates-inegociáveis)
- [Parte 7 — Exemplos prontos](#parte-7--exemplos-prontos)
- [Parte 8 — Personalizar pelo CLAUDE.md](#parte-8--personalizar-pelo-claudemd)
- [Parte 9 — Disciplinas internas](#parte-9--disciplinas-internas)
- [Parte 10 — Estrutura `.specs/`](#parte-10--estrutura-specs)
- [Parte 11 — Troubleshooting](#parte-11--troubleshooting)
- [Glossário](#glossário)

---

## Parte 1 — Entender em 1 minuto

**Nano-Spec é um trilho.** Você descreve o que quer; o agente conduz por um caminho com paradas obrigatórias até o commit:

```
SPECIFY → DESIGN → TASKS → EXECUTE → /simplify → DOCS → COMMIT
required  opcional  opcional required  obrigatório  M+    pergunta
```

Três regras que nunca mudam:

1. **`/simplify`** roda antes de qualquer commit.
2. **Suite de testes** roda depois e precisa passar.
3. **Commit nunca é automático** — o agente sempre pergunta.

Tudo o mais (Design, Tasks, etc.) é pulado conforme o tamanho da tarefa.

**Hierarquia de instruções** (em caso de conflito):

```
1. CLAUDE.md / instruções diretas do dev   ← maior prioridade
2. Nano-spec (este processo)
3. Disciplinas internas (TDD, debug, verification, subagents — em references/)
4. System prompt padrão                    ← menor prioridade
```

---

## Parte 2 — Pré-requisitos (instalar antes de usar)

Desde a versão **4.0.0**, o nano-spec é **standalone** — as disciplinas técnicas (TDD, debug, verification, code review, subagents, parallel dispatch) estão internalizadas. Não há dependência de plugins externos.

O único pré-requisito de ferramenta externa é o `git-flow-next`.

### git-flow-next (gerenciamento de branches)

```bash
# macOS / Linux
brew install gittower/tap/git-flow-next

# Windows
winget install GitTower.GitFlowNext
```

Para **desativar** gitflow num projeto específico, no `CLAUDE.md`:

```markdown
## Branching
Sem gitflow
```

---

## Parte 3 — Primeira vez no projeto

Antes da primeira feature, o agente prepara duas coisas. Isso acontece **uma vez por projeto**.

### Passo 1 — Project Init

Se `.specs/project/` não existir, o agente cria:

- `PROJECT.md` — visão, goals, stack, escopo
- `ROADMAP.md` — features planejadas e milestones

**Você dispara dizendo**: "inicializar projeto" — ou simplesmente pedindo qualquer feature. Se faltar, o agente faz primeiro.

### Passo 2 — Brownfield Mapping

Se `.specs/codebase/` não existir, o agente mapeia o código atual em 7 documentos:

| Arquivo | O que documenta |
|---------|-----------------|
| `STACK.md` | Tecnologias e dependências |
| `ARCHITECTURE.md` | Padrões e fluxo de dados |
| `CONVENTIONS.md` | Naming e estilo |
| `STRUCTURE.md` | Organização de diretórios |
| `TESTING.md` | Infraestrutura de testes |
| `INTEGRATIONS.md` | APIs externas e serviços |
| `CONCERNS.md` | Tech debt, riscos, áreas frágeis |

> **Greenfield (projeto novo)**: os 7 docs nascem curtos e crescem com o projeto.
> **Brownfield (projeto existente)**: os 7 docs nascem ricos, baseados no código real.

Pronto. O projeto está preparado. A partir daqui, é só feature em feature.

---

## Parte 4 — Fluxo de uma feature, passo a passo

Quando você diz **"implementar X"**, **"nova feature: X"**, **"fix bug: X"** ou similar, o agente inicia o fluxo abaixo.

### Passo 0 — SessionStart (automático)

Ao abrir a sessão, o plugin injeta ~3 KB no contexto: hierarquia, auto-sizing resumido, gates e triggers. **Não** carrega o processo inteiro — só ensina o agente quando deve carregar.

Faz um HARD BLOCK na primeira interação git: **git-flow-next instalado?** Se não, o processo para (a menos que `CLAUDE.md` defina "Sem gitflow").

### Passo 1 — Detecção de contexto (automático, ~3s)

O agente lê (na ordem, parando no primeiro que achar):

1. `CLAUDE.md` na raiz
2. `AGENTS.md`
3. `.specs/project/PROJECT.md`

Mostra **uma vez** na sessão um resumo curto: idioma, stack, scopes de commit, comando de teste.

### Passo 2 — Auto-sizing (automático)

O agente classifica a tarefa em **Small / Medium / Large / Complex** e te diz qual fluxo vai seguir. (Ver [Parte 5](#parte-5--os-4-tamanhos-de-tarefa).)

### Passo 3 — Specify

Cria a pasta `.specs/features/YYYY-MM-DD-[feature]/` (prefixo de data **obrigatório** — usa a data corrente + slug em kebab-case derivado do título; ex: `2026-05-12-google-login`) e produz `spec.md` com:

> **Tem features antigas sem prefixo de data?** Na primeira sessão após o upgrade para 3.0.1, o agente detecta automaticamente e oferece migração. Você pode rodar manualmente: `bash plugins/nano-spec/scripts/migrate-feature-dates.sh --dry-run` (preview) ou `--yes` (aplicar). O script usa a data do **primeiro commit do `spec.md`** via `git log`.

- User stories
- Critérios de aceite com **IDs rastreáveis** (`FEAT-01`, `FEAT-02`, …)
- Cada critério em formato **QUANDO / ENTÃO**
- Constraints (performance, segurança, compatibilidade)
- **Out of scope** explícito

**Disciplinas aplicadas** (em `references/specify/`):
- 🧠 **discovery** — explora intenção do usuário, requisitos e design antes de implementar; propõe 2-3 abordagens com tradeoffs; perguntas one-at-a-time; HARD-GATE: sem código antes da spec aprovada.
- 📝 **`spec-document-reviewer-prompt.md`** — subagent revisor para Large/Complex que audita a spec procurando ambiguidades, critérios não testáveis e gaps.

> **Gate de saída**: você confirma "spec ok".
> **Quick Mode (Small)**: vira só uma frase descrevendo o que vai ser feito.

### Passo 4 — Discuss *(só em Complex, dentro do Specify)*

Se houver ambiguidade real, o agente faz **perguntas estruturadas** para você responder antes de fechar a spec. Não é conversa fiada — é lista numerada de decisões pendentes.

### Passo 5 — Design *(opcional)*

Produz `design.md`:

- Arquitetura proposta
- Componentes e responsabilidades
- Decisões com **tradeoffs**
- Diagramas (mermaid inline)

**Disciplina aplicada** (em `references/design/`):
- 🧠 **discovery arquitetural** — aprofunda design incremental, levantando alternativas arquiteturais e seus tradeoffs. Apresentação por seção com aprovação do dev entre seções.

**Pula quando** não há decisão arquitetural a tomar.

### Passo 6 — Tasks *(opcional)*

Produz `tasks.md` no formato **TLC**. Cada task tem:

- **What** — o que mudar
- **Where** — em quais arquivos
- **Depends** — dependências (ou —)
- **Done when** — critério objetivo de pronto
- **Verify** — como provar (teste, comando, observação)

**Disciplinas aplicadas** (em `references/tasks/`):
- 📋 **TDD inline** — converte spec em plano executável; quebra em tasks atômicas com TDD steps explícitos. Premissa "zero context, questionable taste" + No Placeholders.
- 🔍 **`plan-document-reviewer-prompt.md`** — subagent revisor para Large/Complex que audita o plano checando atomicidade, dependências corretas e critérios verificáveis.

**Pula quando** há ≤3 passos óbvios.

### Passo 7 — Execute

Para cada task:

1. Implementar a mudança
2. Avaliar se precisa de teste (lógica nova → sim; config/copy → não)
3. Rodar testes do módulo afetado
4. Atualizar rastreabilidade na `spec.md` (`Pending → Implementing → Verified`)

**Disciplinas aplicadas** (em `references/execute/`):
- 🧪 **`tdd/tdd.md`** — Iron Law "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST". Ciclo Red → Verify Red → Green → Verify Green → Refactor.
- 🤖 **`subagents/subagents.md`** — 3 subagents per task (implementer → spec compliance review → code quality review) para Large/Complex. Continuous execution entre tasks.
- 🤖 **`subagents/parallel-dispatch.md`** — múltiplos subagents em paralelo para tasks independentes, com check de conflitos pós-retorno.
- 🐛 **`systematic-debugging/debug.md`** — Iron Law "NO FIXES WITHOUT ROOT CAUSE FIRST" + 4 fases (Root Cause → Pattern → Hypothesis → Fix) + Fase 4.5 (questionar arquitetura após 3 fixes falharem).

### Passo 8 — `/simplify` *(gate obrigatório)*

O agente roda **uma vez** sobre o diff acumulado de todas as tasks, procurando:

- Duplicação que podia reusar código existente
- Abstração prematura
- Complexidade desnecessária
- Funções/variáveis não utilizadas

Se sugere ajustes, aplica e re-roda.

### Passo 9 — Suite completa de testes *(gate obrigatório)*

O agente **não roda os testes diretamente** — informa o comando e aguarda você confirmar o resultado. Isso evita encher o contexto com output de centenas de testes.

O comando vem do `CLAUDE.md` ou é inferido da stack.

**Disciplina aplicada** (em `nano-disciplines:verification`):
- ✅ **Iron Law** — "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE". Exige evidência (output do teste, **nesta mensagem**) antes de declarar pronto; bloqueia avanço se falhar.

> Se algum teste falha → **bloqueia o commit**. Sem exceção.

### Passo 10 — Docs *(obrigatório em Medium+)*

Atualizar `.specs/codebase/` com o que mudou:

- Nova dependência → `STACK.md` + `INTEGRATIONS.md`
- Mudou padrão arquitetural → `ARCHITECTURE.md`
- Nova convenção → `CONVENTIONS.md`
- Risco/tech debt → `CONCERNS.md`

**Quick Mode**: checklist inline, sem arquivos novos.

### Passo 11 — Commit

Delegado para a skill **`nano-spec:nano-commit`**, que executa em ordem:

1. **HARD BLOCK** do `git-flow-next` (instalado, ou processo bloqueado)
2. Validação de branch (sugere `git flow feature/hotfix/release start` se você está em branch protegida)
3. Pergunta explícita: "quer commitar? Arquivos: […]. Sugestão: `<type>(<scope>): <description>`"
4. Recapitulação dos gates: `/simplify` ✓, testes ✓, docs ✓, rastreabilidade ✓
5. Detecção de desvio de escopo (commit em branch errada?)
6. Commit atômico em **Conventional Commits 1.0.0**
7. Pós-commit: 4 opções — `merge local · PR · continuar · discard (com confirmação tipada)`

**Disciplinas aplicadas (Large+)**:
- 👀 **`nano-disciplines:code-review`** + **`code-reviewer-prompt.md`** — subagent revisor (5 eixos) do diff (BASE_SHA → HEAD_SHA) antes de fechar. Pre-commit Large/Complex: Protocolo Dois-Eixos em paralelo (Standards + Spec).
- 🎯 **`nano-commit` (seção "Pós-Commit: Fechamento de Branch")** — 4 opções estruturadas de encerramento (merge local / PR / continuar / discard com confirmação tipada).

---

## Parte 5 — Os 4 tamanhos de tarefa

O agente classifica automaticamente. Você pode forçar dizendo "trate como Quick Mode" ou "vamos no fluxo completo".

| Escopo | Quando | Specify | Design | Tasks | Execute | Pós |
|--------|--------|---------|--------|-------|---------|-----|
| **Small** | ≤3 arquivos, 1 frase | Quick mode | — | — | Direto | `/simplify` → commit |
| **Medium** | Feature clara, <10 tasks | Spec breve | Inline | Implícito | Por task | `/simplify` → commit |
| **Large** | Multi-componente | Full spec + IDs | Arquitetura | Breakdown + deps | Por task | `/simplify` → commit |
| **Complex** | Ambiguidade, domínio novo | Full + Discuss | Research + arquitetura | Breakdown + paralelo | Por task + UAT | `/simplify` → commit |

**Regras rápidas**:

- **Specify** e **Execute** são sempre obrigatórios (em Small viram "descrever" + "implementar").
- **Design** pula quando não há decisão arquitetural.
- **Tasks** pula quando há ≤3 passos óbvios.
- **Discuss** dispara dentro de Specify só em Complex.
- **UAT** dispara dentro de Execute só em Complex, para features user-facing.

**Safety valve**: se durante a execução surgirem mais de 5 passos não previstos, o agente **para** e gera um `tasks.md` formal. Auto-sizing é estimativa, não compromisso.

---

## Parte 6 — Os gates inegociáveis

Resumo de onde o processo bloqueia ou exige confirmação:

| Gate | Quando | O que faz | Pode pular? |
|------|--------|-----------|-------------|
| **Project Init** | Sem `.specs/project/` | Cria PROJECT + ROADMAP | Não |
| **Brownfield Mapping** | Sem `.specs/codebase/` | Cria 7 docs | Não |
| **git-flow-next (HARD BLOCK)** | Primeira interação gitflow da sessão | Bloqueia se não instalado | Só via `CLAUDE.md → "Sem gitflow"` |
| **Branch gitflow** | Antes de Specify/Execute/Commit | Sugere `git flow start` se em branch protegida | Sim, você confirma |
| **`/simplify`** | Antes do commit | Roda no diff acumulado | Não |
| **Testes** | Após `/simplify` | Suite completa precisa passar | Não |
| **Docs** | Antes do commit (Medium+) | `.specs/codebase/` atualizado | Não em Medium+ |
| **Commit ask** | Após gates | "Quer commitar?" | — |
| **Branch closing** | Após commit | 4 opções (merge/PR/continuar/discard) | — |

---

## Parte 7 — Exemplos prontos

### Exemplo A — Quick fix

```
Você:  quick fix — corrigir texto do botão de salvar

Agente:
  [Auto-sizing] Small · Quick Mode
  [Gitflow] Você está em main — sugiro `git flow hotfix start <versão>`
Você:  sim
  [Implementação] Aplicado
  [/simplify] OK
  [Testes] Rodar `<comando do CLAUDE.md>`?
Você:  passou
  [Commit] fix(ui): ajusta texto do botão de salvar
  [Pós-commit] 1. Merge local · 2. PR · 3. Continuar · 4. Discard
```

### Exemplo B — Feature média

```
Você:  implementar autenticação via provedor externo

Agente:
  [Contexto] <stack> · <idioma> · Scopes: <…>
  [Auto-sizing] Medium
  [Specify via brainstorming] 2 abordagens propostas…
Você:  abordagem 1
  → spec.md com AUTH-01..AUTH-04
  [Execute] AUTH-01 implementada com teste · …
  [/simplify] 1 reuso aplicado
  [Testes] Comando: <…> · 42/42 verde
  [Docs] INTEGRATIONS.md atualizado
  [Commit] feat(auth): adiciona autenticação via provedor externo
           Refs: AUTH-01, AUTH-02, AUTH-03, AUTH-04
```

### Exemplo C — Bug em produção

```
Você:  fix bug — usuários recebem 401 ao renovar sessão

Agente:
  [Auto-sizing] Medium · bug em fluxo crítico
  [Systematic Debugging — 4 fases]
    Root Cause: serviço não trata token expirado
    Pattern: erro silencioso em catch genérico
    Hypothesis: middleware responde antes do refresh
    Fix: ordem de middlewares + teste de regressão
  [Failing test] criado
  [Implementação] Fix aplicado · teste verde
  [/simplify] OK
  [Testes] 42/42 verde
  [Commit] fix(auth): corrige ordem de middlewares no refresh
```

---

## Parte 8 — Personalizar pelo CLAUDE.md

O agente lê o `CLAUDE.md` do projeto na primeira fase da sessão e adapta tudo.

| Convenção no CLAUDE.md | Onde aplica |
|------------------------|-------------|
| Idioma | Specs, mensagens, commits |
| Stack | Exemplos em templates |
| Scopes de commit | Fase Commit (lista controlada vs livre) |
| Comandos de teste | Verificação no Execute |
| Padrões de código | Princípios aplicados no `/simplify` |
| Regras de arquitetura | Design, constraints |
| Containers/infra | Comandos de execução |
| Modelo de branching | Commit (gate gitflow) |

**Exemplo de scopes customizados** no `CLAUDE.md`:

```markdown
## Scopes de commit
- `api`, `painel`, `admin`, `infra`, `docs`
```

**Atualizou o CLAUDE.md no meio da sessão?** Peça: *"recarregue o contexto do projeto"*.

---

## Parte 9 — Disciplinas internas

Desde a versão **4.0.0** o nano-spec é **standalone**: as 10 disciplinas técnicas que originalmente vinham do plugin `superpowers` foram **internalizadas** em `references/`. Sem dependência de plugins externos.

O nano-spec aplica essas disciplinas **automaticamente** em cada fase:

| Fase | Disciplina aplicada |
|---|---|
| Specify | `specify/specify.md` — discovery (2-3 abordagens) + `spec-document-reviewer-prompt.md` para Large/Complex |
| Design | `design/design.md` — apresentação incremental por seção |
| Tasks | `tasks/tasks.md` — premissa "zero context" + No Placeholders + TDD inline + `plan-document-reviewer-prompt.md` |
| Execute (qualquer) | `nano-disciplines:tdd` — Iron Law TDD em tasks com lógica |
| Execute (Large+) | `nano-disciplines:skills/nano-disciplines/references/subagents/subagents.md` — 3 subagents per task (two-stage review) |
| Execute (tasks `[P]`) | `nano-disciplines:skills/nano-disciplines/references/subagents/parallel-dispatch.md` — múltiplos subagents em paralelo |
| Execute (bug) | `nano-disciplines:debug` — 4 fases + Fase 4.5 |
| Commit gate | `nano-disciplines:verification` — Iron Law "evidência fresh antes de claim" |
| Code review (Large+) | `nano-disciplines:code-review` + `code-reviewer-prompt.md`; pre-commit Large/Complex: Protocolo Dois-Eixos |
| Recepção de feedback | `nano-disciplines:skills/code-review/references/receiving-feedback.md` — zero performative agreement |
| Branch closing | `nano-commit` seção "Pós-Commit: Fechamento de Branch" |

**Output sempre em `.specs/`** — todas as disciplinas escrevem artefatos de feature em `.specs/features/YYYY-MM-DD-[feature]/`. Nunca espalhar em outros diretórios.

> **Histórico:** Versões 3.x do nano-spec dependiam do plugin `superpowers` (HARD BLOCK no SessionStart). A 4.0.0 internalizou tudo. As disciplinas internas têm paridade funcional com as originais — em alguns pontos são mais rigorosas (vertical-slice em tasks, naming por ID de requisito em testes, Protocolo Dois-Eixos em review, `git flow --no-ff` inline em branch closing).

---

## Parte 10 — Estrutura `.specs/`

```
.specs/
├── project/
│   ├── PROJECT.md          # Visão, goals, stack, escopo
│   ├── ROADMAP.md          # Features e milestones
│   └── STATE.md            # Decisões, blockers, lições
│
├── codebase/               # Brownfield (sempre presente)
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── STRUCTURE.md
│   ├── TESTING.md
│   ├── INTEGRATIONS.md
│   └── CONCERNS.md
│
├── features/YYYY-MM-DD-[feature]/   # Prefixo de data OBRIGATÓRIO
│   │                                 # ex: 2026-05-12-google-login/
│   ├── spec.md             # Requisitos com IDs rastreáveis
│   ├── context.md          # Decisões + brainstorming
│   ├── design.md           # Arquitetura
│   ├── tasks.md            # Tasks (formato TLC)
│   └── assets/             # Diagramas
│
└── quick/NNN-slug/         # Quick fixes
    ├── TASK.md
    └── SUMMARY.md
```

`.specs/` é **fonte de verdade única** para artefatos de planejamento. Não duplicar em `docs/` ou outros lugares.

---

## Parte 11 — Troubleshooting

### "Por que o nano-spec não ativou?"

- Use um trigger reconhecido: *"implementar X"*, *"nova feature: X"*, *"quick fix: X"*, *"commitar"*, *"fix bug"*, *"refactor"*.
- SessionStart hook pode ter falhado — reinicie a sessão.
- Cheque `claude plugin list` — o `nano-spec` está ativo?

### "git-flow-next não está instalado, processo bloqueado"

É intencional. Veja [Parte 2](#parte-2--pré-requisitos-instalar-antes-de-usar). Para desativar gitflow num projeto, `CLAUDE.md → "Sem gitflow"`.

### "O agente não respeita meu CLAUDE.md"

Ele lê uma vez por sessão. Atualizou agora? Peça: *"recarregue o contexto do projeto"*.

### "Quero pular um gate"

- `/simplify` + testes + Project Init são **hard blocks** — não dá.
- Gitflow: desative via `CLAUDE.md`.
- Specify/Design/Tasks: peça **Quick Mode** explicitamente.
- Commit: você pode dizer *"commitar mesmo assim"* — o agente cede, mas avisa.

### "Vejo referências a superpowers no projeto"

Versões anteriores (3.x) do nano-spec dependiam do plugin externo `superpowers`. Desde a 4.0.0 tudo está internalizado em `references/`. Se você está vendo menções a `superpowers:X` em outros lugares, são resíduos — o agente deve usar os arquivos internos correspondentes.

---

## Glossário

| Termo | Significado |
|-------|-------------|
| **Spec-Driven** | Especificar antes de implementar |
| **Orquestrador** | A skill `nano-spec:nano-spec` que coordena fases |
| **Skill filha** | Skill autônoma do plugin (ex: `nano-spec:nano-commit`) |
| **Reference** | Arquivo `.md` em `skills/nano-spec/references/`, carregado on-demand |
| **Trilho** | Processo (o que / em que ordem) |
| **Disciplinas internas** | Métodos técnicos (TDD, debug, verification, subagents, etc.) internalizados em `references/` |
| **Gate** | Ponto onde o processo bloqueia ou exige confirmação |
| **HARD BLOCK** | Gate que para tudo até resolver |
| **Auto-Sizing** | Detecção automática do escopo (Small/Medium/Large/Complex) |
| **Quick Mode** | Fluxo abreviado para Small (≤3 arquivos, 1 frase) |
| **Brownfield** | Projeto existente com código já escrito |
| **Greenfield** | Projeto novo, do zero |
| **Conventional Commits** | Formato `<type>(<scope>): <description>` |
| **Rastreabilidade** | IDs `FEAT-XX` ligam spec → tasks → testes → commits |
| **`/simplify`** | Skill que revisa o diff por reuso, qualidade, eficiência |
| **UAT** | User Acceptance Testing — validação interativa em Complex |

---

## Próximos passos

- [Diagrama do fluxo](./fluxo-nano-spec.excalidraw) — abrir no Excalidraw
- [SKILL.md do orquestrador](../skills/nano-spec/SKILL.md) — fonte canônica
- [SKILL.md do nano-commit](../skills/nano-commit/SKILL.md) — fluxo de commit/gitflow
- [References](../skills/nano-spec/references/) — guias de cada fase

---

**Versão deste guia**: aplica a nano-spec 4.0+.
**Licença**: CC-BY-4.0.
**Baseado em**: [tlc-spec-driven](https://github.com/felipfr) v2.0.0 por Felipe Rodrigues.
