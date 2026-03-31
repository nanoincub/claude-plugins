# Nano-Spec — Plugin para Claude Code

Processo Spec-Driven da Nano Incub. Orquestra 8 fases de desenvolvimento com quality gates obrigatórios.

```
SPECIFY → DESIGN → TASKS → EXECUTE → REVIEW → SECURITY → DOCS → COMMIT
```

## Instalacao

### Via Claude Code (recomendado)

```bash
claude plugins add rafaelyanagui/nano-spec
```

### Via ZIP (organizacao)

1. Descompactar o ZIP
2. Copiar a pasta para `~/.claude/plugins/cache/nano-spec/nano-spec/2.5.0/`
3. Adicionar em `~/.claude/plugins/installed_plugins.json`:

```json
"nano-spec@nano-spec": [
  {
    "scope": "user",
    "installPath": "~/.claude/plugins/cache/nano-spec/nano-spec/2.5.0",
    "version": "2.5.0",
    "installedAt": "2026-03-31T00:00:00.000Z",
    "lastUpdated": "2026-03-31T00:00:00.000Z"
  }
]
```

4. Habilitar em `~/.claude/settings.json`:

```json
"enabledPlugins": {
  "nano-spec@nano-spec": true
}
```

5. Reiniciar o Claude Code.

## Estrutura

```
plugin/
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
