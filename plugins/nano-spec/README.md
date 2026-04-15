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

> **Nota:** O superpowers é o motor do nano-spec — fornece TDD, debugging, worktrees, code review e outras ferramentas que o processo orquestra. O nano-spec funciona sem ele, mas com capacidades reduzidas.

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

O nano-spec é o **trilho** (o que fazer e em que ordem), o superpowers é o **motor** (como fazer):

| Fase | Sem Superpowers | Com Superpowers |
|------|-----------------|-----------------|
| Specify | Q&A conversacional | + brainstorming → context.md |
| Design | Pesquisa manual | + brainstorming steps 5-8 |
| Tasks | Breakdown manual | + writing-plans → tasks.md |
| Execute | Code + verify (teste) | + TDD, worktrees, subagents, debug |
| /simplify | /simplify sobre diff acumulado | (mesma skill) |
| Commit | Conventional Commits | + finishing-a-development-branch |

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

2.9.0-beta.2 — Feat: gitflow reescrito para git-flow-next (Tower) — CLI atômica com detecção automática e instalação multiplataforma.

Baseado em [tlc-spec-driven](https://github.com/felipfr) v2.0.0 por Felipe Rodrigues. Licença CC-BY-4.0.
