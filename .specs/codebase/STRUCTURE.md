# Estrutura do Projeto

**Raiz:** `claude-plugins/`

## Árvore de Diretórios

```
claude-plugins/
├── .claude/
│   └── settings.local.json        # Permissões locais do Claude Code
├── .claude-plugin/
│   └── marketplace.json           # Registro central do marketplace
├── .specs/                        # Documentação estruturada (nano-spec)
│   ├── project/                   # Visão, roadmap, estado
│   └── codebase/                  # Mapeamento do codebase
├── plugins/
│   └── nano-spec/                 # Plugin principal
│       ├── .claude-plugin/
│       │   └── plugin.json        # Metadados do plugin
│       ├── hooks/
│       │   ├── hooks.json         # Config de hooks (SessionStart)
│       │   ├── run-hook.cmd       # Wrapper cross-platform
│       │   └── session-start      # Script de injeção de contexto
│       ├── skills/
│       │   └── nano-spec/
│       │       ├── SKILL.md       # Orquestrador principal (~370 linhas)
│       │       └── references/    # 21 guias de referência
│       │           ├── agent-behavior.md
│       │           ├── brownfield-mapping.md
│       │           ├── code-analysis.md
│       │           ├── coding-principles.md
│       │           ├── commit.md
│       │           ├── concerns.md
│       │           ├── context-limits.md
│       │           ├── design.md
│       │           ├── discuss.md
│       │           ├── docs-update.md
│       │           ├── implement.md
│       │           ├── project-init.md
│       │           ├── quick-mode.md
│       │           ├── review.md
│       │           ├── roadmap.md
│       │           ├── security.md
│       │           ├── session-handoff.md
│       │           ├── specify.md
│       │           ├── state-management.md
│       │           ├── tasks.md
│       │           └── validate.md
│       └── README.md
└── README.md                      # Documentação do marketplace
```

## Organização por Módulo

### Marketplace (raiz)

**Propósito:** Registro e distribuição de plugins
**Localização:** `.claude-plugin/marketplace.json`, `README.md`
**Arquivos-chave:** `marketplace.json` (registro de plugins)

### Plugin nano-spec

**Propósito:** Processo spec-driven de 8 fases para desenvolvimento com IA
**Localização:** `plugins/nano-spec/`
**Arquivos-chave:**
- `skills/nano-spec/SKILL.md` — orquestrador principal
- `hooks/session-start` — injeção de contexto no SessionStart
- `hooks/run-hook.cmd` — wrapper cross-platform

### References (guias de fase)

**Propósito:** Documentação detalhada de cada fase e aspecto do processo
**Localização:** `plugins/nano-spec/skills/nano-spec/references/`
**Organização por tema:**
- **Projeto:** project-init, roadmap, brownfield-mapping, concerns, state-management, session-handoff
- **Feature:** specify, design, tasks, implement, validate
- **Quality gates:** review, security
- **Finalização:** docs-update, commit
- **Suporte:** discuss, quick-mode, coding-principles, code-analysis, agent-behavior, context-limits

## Diretórios Especiais

**`.specs/`:** Documentação estruturada gerada pelo nano-spec. Fonte de verdade para artefatos de planejamento.

**`.claude/`:** Configurações locais do Claude Code (permissões, settings).

**`.claude-plugin/`:** Metadados reconhecidos pelo sistema de plugins do Claude Code.
