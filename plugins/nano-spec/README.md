# Nano-Spec — Plugin para Claude Code

Processo Spec-Driven da Nano Incub. Orquestra fases de desenvolvimento com verificação executável por task e /simplify obrigatório. **Requer `nano-disciplines` + `nano-commit`** (HARD BLOCKs) — disciplinas técnicas em `nano-disciplines` (desde 5.0.0) e fluxo de commit/gitflow em `nano-commit` (desde 6.0.0).

```
┌──────────┐   ┌──────────┐   ┌─────────┐   ┌─────────┐   ┌───────────┐   ┌──────┐   ┌────────┐
│ SPECIFY  │ → │  DESIGN  │ → │  TASKS  │ → │ EXECUTE │ → │ /SIMPLIFY │ → │ DOCS │ → │ COMMIT │
└──────────┘   └──────────┘   └─────────┘   └─────────┘   └───────────┘   └──────┘   └────────┘
   required      optional*      optional*     required       required       req M+     ask-dev
```

## Instalação

### Via Marketplace Nano Incub (recomendado)

Registre o marketplace (uma vez):

```bash
claude plugin marketplace add nanoincub/claude-plugins
```

Instale o nano-spec e as duas dependências obrigatórias:

```bash
claude plugin install nano-disciplines@nano-incub
claude plugin install nano-commit@nano-incub
claude plugin install nano-spec@nano-incub
```

> **HARD BLOCK:** desde a versão 6.0.0, o nano-spec **exige** dois plugins via HARD BLOCK: `nano-disciplines` (disciplinas técnicas universais — TDD, debug, verification, code review, subagents, security, validate, etc.) e `nano-commit` (fluxo de gitflow + Conventional Commits + 4 opções de fechamento). Sem qualquer um dos dois, o processo bloqueia na entrada.

### Via organização (automático)

Se a organização já sincronizou o marketplace `nanoincub/claude-plugins` com "Installed by default", o plugin é instalado automaticamente para todos os membros.

## Auto-Sizing

O processo adapta a complexidade automaticamente:

| Escopo | Critério | Fases | Pós-Execute |
|--------|----------|-------|-------------|
| **Small** | ≤3 arquivos, 1 frase | Quick Mode | /simplify → tests → commit |
| **Medium** | Feature clara, <10 tasks | Specify → Execute → /simplify → commit | /simplify → tests → commit |
| **Large** | Multi-componente | Todas as fases | /simplify → tests → commit |
| **Complex** | Ambiguidade, domínio novo | Todas + Discuss + Research | /simplify → tests → commit |

## Quality Gates

- **Specify + Execute** — sempre obrigatórios
- **Verificação por task** — após cada task, avaliar se precisa de teste e rodar testes do módulo afetado
- **Iron Law (verification)** — evidência fresh antes de qualquer claim de "pronto"
- **/simplify + suite completa** — obrigatórios antes de qualquer commit (ordem: simplify FIRST, depois testes)
- **Review + Security** — opt-in (ativar via defaults ou quando dev pedir)
- **Commit** — nunca automático, sempre pergunta ao dev

## Disciplinas Internas

O nano-spec é **trilho + disciplinas**. Cada fase aciona disciplinas internas (todas em `references/`):

| Fase | Disciplina aplicada |
|---|---|
| Specify | `specify/specify.md` — discovery (2-3 abordagens) + `spec-document-reviewer-prompt.md` |
| Design | `design/design.md` — apresentação incremental por seção |
| Tasks | `tasks/tasks.md` — premissa "zero context" + No Placeholders + TDD inline + `plan-document-reviewer-prompt.md` |
| Execute | `execute/implement.md` + `nano-disciplines:tdd` (Iron Law) + `nano-disciplines:debug` (4 fases) |
| Execute (Large/Complex) | `execute/subagents/` (3 subagents per task: implementer → spec compliance → code quality) |
| /simplify | (skill própria do Claude Code) |
| Review | `nano-disciplines:verification` (Iron Law) + `nano-disciplines:code-review` ou Protocolo Dois-Eixos |
| Commit | Skill `nano-commit` (gitflow + verification + 4 opções de fechamento) |

## Estrutura

```
nano-spec/
├── .claude-plugin/plugin.json
├── hooks/
│   ├── hooks.json
│   ├── run-hook.cmd
│   └── session-start                   # contexto leve no SessionStart
├── skills/
│   ├── nano-spec/
│   │   ├── SKILL.md                    # orquestrador principal
│   │   └── references/                 # disciplinas + guias por fase
│   │       ├── init/                   # project-init, roadmap, brownfield-mapping, concerns
│   │       ├── specify/                # specify + spec-reviewer prompt
│   │       ├── design/
│   │       ├── tasks/                  # tasks + plan-reviewer prompt
│   │       ├── execute/                # implement + tdd/ + systematic-debugging/ + subagents/
│   │       ├── review/                 # review + Dois-Eixos + code-reviewer + receiving-feedback
│   │       ├── commit/                 # commit, gitflow (pointers para nano-commit)
│   │       ├── docs/                   # docs-update
│   │       ├── quick-mode/
│   │       └── meta/                   # verification, agent-behavior, grill, discuss, state-mgmt
│   └── nano-commit/SKILL.md            # skill standalone para commit + gitflow
└── README.md
```

## Como Funciona

1. **SessionStart:** Hook injeta contexto leve com regras essenciais e triggers
2. **Trigger:** Dev pede tarefa de desenvolvimento → nano-spec ativa automaticamente
3. **Auto-sizing:** Detecta complexidade e seleciona fases adequadas
4. **Execução:** Percorre fases, aplica disciplinas internas automaticamente
5. **Output:** Artefatos em `.specs/features/YYYY-MM-DD-[feature]/`, código implementado, commit com Conventional Commits

## Versão

**6.0.1** — Hook `SessionStart` agora detecta os 4 plugins nano-* (nano-spec, nano-commit, nano-disciplines, nano-resumo-dia) e injeta no contexto da sessão um bloco de status visual com ✅/❌ por plugin, exibido como primeira coisa da primeira resposta do assistente. Facilita diagnóstico imediato de dependências faltantes sem precisar rodar `claude plugin list`.

**6.0.0 (BREAKING)** — Conclui a pureza arquitetural Spec-Driven iniciada na 5.0.0. Remove de nano-spec os 2 itens que não eram canonicamente SDD: a skill `nano-commit` (delivery — gitflow/Conventional Commits/PR) foi **extraída** para o plugin standalone `nano-commit` (v1.4.0), e `meta/context-limits.md` (regra de tamanho de arquivo — universal) **moveu** para `nano-disciplines` (v1.2.0). nano-spec passa a depender de DOIS plugins via HARD BLOCK: `nano-disciplines >= 1.2.0` e `nano-commit >= 1.4.0`. Refs migradas: `nano-spec:nano-commit:*` → `nano-commit:*`; `references/meta/context-limits.md` → `nano-disciplines:skills/nano-disciplines/references/context-limits.md`. Stub legado `references/commit/gitflow.md` removido (conteúdo já vive na SKILL.md do nano-commit). Para upgrade: instalar os 3 plugins via marketplace; refs hard-coded a `nano-spec:nano-commit` em código de terceiros precisam ser migradas para `nano-commit:`.

**5.0.0 (BREAKING)** — Split arquitetural: as disciplinas técnicas internalizadas na 4.0.0 (verification, TDD, systematic-debugging, subagents, parallel-dispatch, code-review, receiving-feedback, security, validate, docs-update, code-analysis, coding-principles) foram **extraídas** para o plugin `nano-disciplines`. nano-spec volta a ser o que é: orquestrador puro de Spec-Driven Development. Disciplinas são consumidas via convenção `nano-disciplines:<path>`. HARD BLOCK em `nano-disciplines` no hook session-start e no SKILL.md. Motivação: preservar a identidade Spec-Driven (forma do processo) separada das ferramentas técnicas (disciplinas universais reutilizáveis fora do contexto Spec-Driven). Fica em nano-spec: `specify/`, `design/`, `tasks/`, `init/`, `quick-mode/`, `commit/`, `baseline-test-gate.md`, `execute/implement.md`, `meta/{agent-behavior,context-limits,discuss,grill,session-handoff,state-management}.md`, `review/{dois-eixos,review}.md`, e os reviewer prompts para spec/plan/tasks.

**4.0.0 (BREAKING)** — Standalone total: as 10 disciplinas que viviam no plugin `superpowers` foram **internalizadas** em `references/`. HARD BLOCK do superpowers removido. Zero dependências de plugins externos. Bump major sinaliza fim da dependência obrigatória. Preserva integralmente as correções da 3.2.0 (Baseline Test Gate + fix `--fetch` no `nano-commit`). nano-commit 1.2.0 → 1.3.0 (Gate Iron Law via `verification.md` + Pós-Commit Fechamento de Branch inline). *Internalização revertida na 5.0.0 via split em `nano-disciplines`.*

3.2.0 — Feat: Baseline Test Gate antes de criar branch de trabalho (roda suite na base; vermelho → PARAR ou OVERRIDE com registro em STATE.md). Ordem pré-commit fixa `/simplify → testes → commit` tornada explícita em tabelas e diagramas. Fix `--fetch`: substituído por `git checkout <base> && git pull --ff-only` antes de `git flow <type> start` (o `--fetch` do git-flow-next não fast-forwarda a base local). nano-commit 1.0.1 → 1.2.0.

3.1.0 — Feat: integração de 3 skills do matpocock adaptadas ao padrão Nano — `grill.md` (stress-test de spec contra `CONVENTIONS.md` + ADRs em `.specs/decisions/`), modo vertical-slice em `tasks.md` (tracer bullets HITL/AFK), e protocolo dois-eixos em `review.md` (Standards + Spec via sub-agentes paralelos pré-commit).

3.0.1 — Convenção: pasta de feature em `.specs/features/` passa a exigir prefixo de data `YYYY-MM-DD-[feature]`.

3.0.0 (BREAKING) — Superpowers vira obrigatório (revertido na 4.0.0).

2.11.0 — Feat: extrai fluxo de gitflow + commit para skill autônoma `nano-commit`.

Baseado em [tlc-spec-driven](https://github.com/felipfr) v2.0.0 por Felipe Rodrigues. Licença CC-BY-4.0.
