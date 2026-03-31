# Nano-Spec — Plugin para Claude Code

Processo Spec-Driven da Nano Incub. Orquestra 8 fases de desenvolvimento com quality gates confirmativos.

```
SPECIFY → DESIGN → TASKS → EXECUTE → REVIEW → SECURITY → DOCS → COMMIT
```

## Instalacao

### Via Marketplace Nano Incub (recomendado)

Registre o marketplace (uma vez):

```bash
claude plugin marketplace add nanoincub/claude-plugins
```

Instale o nano-spec e o superpowers (dependencia):

```bash
claude plugin install superpowers@claude-plugins-official
claude plugin install nano-spec@nano-incub
```

> **Nota:** O superpowers e o motor do nano-spec — fornece TDD, debugging, worktrees, code review e outras ferramentas que o processo orquestra. O nano-spec funciona sem ele, mas com capacidades reduzidas.

### Via organizacao (automatico)

Se a organizacao ja sincronizou o marketplace `nanoincub/claude-plugins` com "Installed by default", o plugin e instalado automaticamente para todos os membros.

## Estrutura

```
nano-spec/
├── .claude-plugin/
│   └── plugin.json          # Metadados do plugin
├── hooks/
│   ├── hooks.json            # Configuracao de hooks (SessionStart)
│   ├── run-hook.cmd          # Wrapper cross-platform
│   └── session-start         # Hook que injeta contexto na sessao
├── skills/
│   └── nano-spec/
│       ├── SKILL.md          # Skill principal (orquestrador)
│       └── references/       # 21 references (fases, templates, comportamento)
└── README.md
```

## Versao

2.5.0 — Review/Security confirmativos, Commit ask-dev, sinais R1-R8 / S1-S11.
