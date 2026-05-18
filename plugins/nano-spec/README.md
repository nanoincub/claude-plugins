# Nano-Spec — Plugin para Claude Code

Processo Spec-Driven da Nano Incub. Orquestra fases de desenvolvimento com verificação executável por task e /simplify obrigatório. **Standalone — zero dependências de plugins externos** desde a versão 4.0.0.

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

Instale o nano-spec:

```bash
claude plugin install nano-spec@nano-incub
```

> **Standalone:** o nano-spec **não depende mais** de plugins externos desde a versão 4.0.0. Todas as disciplinas técnicas (TDD, debug, verification, code review, subagents, parallel dispatch) estão internalizadas nas references.

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
| Execute | `execute/implement.md` + `execute/tdd/` (Iron Law) + `execute/systematic-debugging/` (4 fases) |
| Execute (Large/Complex) | `execute/subagents/` (3 subagents per task: implementer → spec compliance → code quality) |
| /simplify | (skill própria do Claude Code) |
| Review | `meta/verification.md` (Iron Law) + `review/code-review.md` ou Protocolo Dois-Eixos |
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

**4.0.0 (BREAKING)** — Standalone total: as 10 disciplinas que viviam no plugin `superpowers` (brainstorming, writing-plans, TDD, systematic-debugging, subagent-driven-development, verification-before-completion, requesting-code-review, receiving-code-review, finishing-a-development-branch, dispatching-parallel-agents) foram **internalizadas** em `references/`. HARD BLOCK do superpowers removido do hook e do SKILL.md. Zero dependências de plugins externos. Bump major sinaliza fim da dependência obrigatória. Preserva integralmente as correções da 3.2.0 (Baseline Test Gate + fix `--fetch` no `nano-commit`). nano-commit 1.2.0 → 1.3.0 (Gate Iron Law via `verification.md` interno + Pós-Commit Fechamento de Branch inline — 4 opções).

3.2.0 — Feat: Baseline Test Gate antes de criar branch de trabalho (roda suite na base; vermelho → PARAR ou OVERRIDE com registro em STATE.md). Ordem pré-commit fixa `/simplify → testes → commit` tornada explícita em tabelas e diagramas. Fix `--fetch`: substituído por `git checkout <base> && git pull --ff-only` antes de `git flow <type> start` (o `--fetch` do git-flow-next não fast-forwarda a base local). nano-commit 1.0.1 → 1.2.0.

3.1.0 — Feat: integração de 3 skills do matpocock adaptadas ao padrão Nano — `grill.md` (stress-test de spec contra `CONVENTIONS.md` + ADRs em `.specs/decisions/`), modo vertical-slice em `tasks.md` (tracer bullets HITL/AFK), e protocolo dois-eixos em `review.md` (Standards + Spec via sub-agentes paralelos pré-commit).

3.0.1 — Convenção: pasta de feature em `.specs/features/` passa a exigir prefixo de data `YYYY-MM-DD-[feature]`.

3.0.0 (BREAKING) — Superpowers vira obrigatório (revertido na 4.0.0).

2.11.0 — Feat: extrai fluxo de gitflow + commit para skill autônoma `nano-spec:nano-commit`.

Baseado em [tlc-spec-driven](https://github.com/felipfr) v2.0.0 por Felipe Rodrigues. Licença CC-BY-4.0.
