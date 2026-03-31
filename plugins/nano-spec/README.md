# Nano-Spec — Plugin para Claude Code

Processo Spec-Driven da Nano Incub. Orquestra 8 fases de desenvolvimento com quality gates confirmativos.

```
┌──────────┐   ┌──────────┐   ┌─────────┐   ┌─────────┐   ┌────────┐   ┌──────────┐   ┌──────┐   ┌────────┐
│ SPECIFY  │ → │  DESIGN  │ → │  TASKS  │ → │ EXECUTE │ → │ REVIEW │ → │ SECURITY │ → │ DOCS │ → │ COMMIT │
└──────────┘   └──────────┘   └─────────┘   └─────────┘   └────────┘   └──────────┘   └──────┘   └────────┘
   required      optional*      optional*     required    confirmative  confirmative    req M+     ask-dev
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
| **Small** | ≤3 arquivos, 1 frase | Quick Mode | Confirmativo (sinais → ask → commit) |
| **Medium** | Feature clara, <10 tasks | Specify → Execute → ask commit | Confirmativo |
| **Large** | Multi-componente | Todas as 8 fases | Confirmativo por task |
| **Complex** | Ambiguidade, domínio novo | Todas + Discuss + Research | Confirmativo por task |

## Quality Gates

- **Specify + Execute** — sempre obrigatórios
- **Review + Security** — obrigatórios antes de qualquer commit
- **Commit** — nunca automático, sempre pergunta ao dev

### Sistema de Sinais

Durante a execução, o processo detecta padrões no código que disparam perguntas:

**Review (R1-R8):** Lógica condicional, mutação de estado, chamadas API, controle de fluxo, estruturas de dados, mudanças estruturais, alto volume, testes.

**Security (S1-S11):** Input de usuário, autenticação, autorização, dados sensíveis, criptografia, APIs externas, queries de banco, rendering dinâmico, configuração de segurança, keywords, novas dependências.

## Integração com Superpowers

O nano-spec é o **trilho** (o que fazer e em que ordem), o superpowers é o **motor** (como fazer):

| Fase | Sem Superpowers | Com Superpowers |
|------|-----------------|-----------------|
| Specify | Q&A conversacional | + brainstorming → context.md |
| Design | Pesquisa manual | + brainstorming steps 5-8 |
| Tasks | Breakdown manual | + writing-plans → tasks.md |
| Execute | Code + verify | + TDD, worktrees, subagents, debug |
| Review | /review + /simplify | + verification-before-completion |
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

2.5.0 — Review/Security confirmativos, Commit ask-dev, sinais R1-R8 / S1-S11.

Baseado em [tlc-spec-driven](https://github.com/felipfr) v2.0.0 por Felipe Rodrigues. Licença CC-BY-4.0.
