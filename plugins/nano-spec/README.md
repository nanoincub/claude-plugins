# Nano-Spec — Plugin para Claude Code

Processo Spec-Driven da Nano Incub. Orquestra fases de desenvolvimento com verificação executável por task e /simplify obrigatório.

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

Instale o nano-spec e o superpowers (dependência):

```bash
claude plugin install superpowers@claude-plugins-official
claude plugin install nano-spec@nano-incub
```

> **Nota:** O superpowers é **obrigatório** desde a versão 3.0 do nano-spec. Fornece TDD, debugging, code review, brainstorming, writing-plans e outras ferramentas que o processo orquestra. O nano-spec faz HARD BLOCK no SessionStart se superpowers não estiver instalado.

### Via organização (automático)

Se a organização já sincronizou o marketplace `nanoincub/claude-plugins` com "Installed by default", o plugin é instalado automaticamente para todos os membros.

## Auto-Sizing

O processo adapta a complexidade automaticamente:

| Escopo | Critério | Fases | Pós-Execute |
|--------|----------|-------|-------------|
| **Small** | ≤3 arquivos, 1 frase | Quick Mode | /simplify → commit |
| **Medium** | Feature clara, <10 tasks | Specify → Execute → /simplify → commit | /simplify → commit |
| **Large** | Multi-componente | Todas as fases | /simplify → commit |
| **Complex** | Ambiguidade, domínio novo | Todas + Discuss + Research | /simplify → commit |

## Quality Gates

- **Specify + Execute** — sempre obrigatórios
- **Verificação por task** — após cada task, avaliar se precisa de teste e rodar testes do módulo afetado
- **/simplify + suite completa** — obrigatórios antes de qualquer commit
- **Review + Security** — opt-in (ativar via defaults ou quando dev pedir)
- **Commit** — nunca automático, sempre pergunta ao dev

## Integração com Superpowers

O nano-spec é o **trilho** (o que fazer e em que ordem), o superpowers é o **motor** obrigatório (como fazer):

| Fase | Skill do superpowers invocada |
|------|-------------------------------|
| Specify | brainstorming → context.md + spec-document-reviewer |
| Design | brainstorming steps 5-8 (design incremental) |
| Tasks | writing-plans → tasks.md + plan-document-reviewer |
| Execute | TDD, subagents, systematic-debugging |
| /simplify | (skill própria do Claude Code) |
| Commit | verification-before-completion + finishing-a-development-branch |

## Estrutura

```
nano-spec/
├── .claude-plugin/
│   └── plugin.json              # Metadados do plugin
├── hooks/
│   ├── hooks.json               # Configuração de hooks (SessionStart)
│   ├── run-hook.cmd             # Wrapper cross-platform (bash + batch)
│   └── session-start            # Hook de injeção de contexto (~5KB)
├── skills/
│   └── nano-spec/
│       ├── SKILL.md             # Orquestrador principal (~370 linhas)
│       └── references/          # 21 guias de referência
│           ├── project-init.md      # Inicialização de projeto
│           ├── roadmap.md           # Criação de roadmap
│           ├── brownfield-mapping.md # Mapeamento de codebase
│           ├── specify.md           # Especificação de features
│           ├── design.md            # Projeto de arquitetura
│           ├── tasks.md             # Breakdown em tasks
│           ├── implement.md         # Implementação (Execute)
│           ├── validate.md          # Validação/UAT
│           ├── review.md            # Review de código
│           ├── security.md          # Auditoria de segurança
│           ├── docs-update.md       # Atualização de docs
│           ├── commit.md            # Commit com gates
│           ├── gitflow.md           # Gitflow e validação de branch
│           ├── quick-mode.md        # Quick fixes
│           ├── discuss.md           # Discussão de áreas cinzas
│           ├── concerns.md          # Documentação de riscos
│           ├── state-management.md  # Gestão de estado/decisões
│           ├── session-handoff.md   # Pausar/retomar trabalho
│           ├── coding-principles.md # Princípios de código
│           ├── code-analysis.md     # Ferramentas de análise
│           ├── agent-behavior.md    # Comportamento do agente
│           └── context-limits.md    # Gestão de contexto
└── README.md
```

## Como Funciona

1. **SessionStart:** Hook injeta contexto leve (~5KB) com regras essenciais e triggers
2. **Trigger:** Dev pede tarefa de desenvolvimento → nano-spec ativa automaticamente
3. **Auto-sizing:** Detecta complexidade e seleciona fases adequadas
4. **Execução:** Percorre fases, detecta sinais, pergunta ao dev sobre gates
5. **Output:** Artefatos em `.specs/`, código implementado, commit com Conventional Commits

## Versão

3.1.0 — Feat: integração de 3 skills do matpocock adaptadas ao padrão Nano — `grill.md` (stress-test de spec contra `CONVENTIONS.md` + ADRs em `.specs/decisions/`), modo vertical-slice em `tasks.md` (tracer bullets HITL/AFK), e protocolo dois-eixos em `review.md` (Standards + Spec via sub-agentes paralelos pré-commit, substitui `requesting-code-review` em Large/Complex).

3.0.1 — Convenção: pasta de feature em `.specs/features/` passa a exigir prefixo de data `YYYY-MM-DD-[feature]` (ex: `2026-05-12-google-login/`). Garante ordenação cronológica e preserva histórico após renames. Atualizado em SKILL.md, references, GUIA.md e CLAUDE.md. Inclui script `scripts/migrate-feature-dates.sh` para migrar pastas legadas (data vem do primeiro commit do `spec.md` via `git log`).

3.0.0 (BREAKING) — Superpowers vira **obrigatório**: HARD BLOCK no SessionStart, remoção de todos os fallbacks "standalone" em references, SKILL.md, hook e docs. Sem superpowers, nano-spec não roda. Bump major sinaliza incompatibilidade com sessões que dependiam do modo standalone.

2.11.1 — Fix: `--fetch` como default em todos os `git flow <tipo> start` na skill `nano-commit` (feature, bugfix, hotfix, release). Garante que branches partem da base remota atualizada, evitando criação a partir de develop/main stale. Adicionado bloco Bugfix.

2.11.0 — Feat: extrai fluxo de gitflow + commit para skill autônoma `nano-spec:nano-commit`, invocável standalone sem carregar o orquestrador. References `gitflow.md` e `commit.md` viram pointers para compatibilidade.

2.10.4 — Fix: naming de hotfix usa semver (`hotfix/<version>`) — git-flow-next usa o nome da branch como tag por padrão.

2.10.3 — Docs: `git flow finish --no-ff` inline (git-flow-next não aplica `--no-ff` por padrão, ao contrário do gitflow clássico).

2.10.2 — Fix: git-flow-next como hard block obrigatório, remove worktree, integração ativa com superpowers.

Baseado em [tlc-spec-driven](https://github.com/felipfr) v2.0.0 por Felipe Rodrigues. Licença CC-BY-4.0.
