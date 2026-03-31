# Arquitetura

**Padrão:** Marketplace monorepo com plugins modulares

## Estrutura de Alto Nível

```
claude-plugins/                    # Marketplace (repositório raiz)
├── .claude-plugin/
│   └── marketplace.json           # Registro central de plugins
└── plugins/
    └── [plugin-name]/             # Plugin independente
        ├── .claude-plugin/
        │   └── plugin.json        # Metadados do plugin
        ├── skills/                # Skills (prompts estruturados)
        │   └── [skill-name]/
        │       ├── SKILL.md       # Definição principal
        │       └── references/    # Guias de referência
        └── hooks/                 # Hooks de eventos (opcional)
            ├── hooks.json         # Configuração de eventos
            └── [script]           # Scripts de hook
```

## Padrões Identificados

### Marketplace → Plugin → Skill (hierarquia de 3 níveis)

**Localização:** Raiz do repositório
**Propósito:** Organizar plugins independentes sob um registro central
**Implementação:** `marketplace.json` aponta para diretórios em `plugins/`, cada um com seu `plugin.json`

### Skill com References (documentação modular)

**Localização:** `plugins/[plugin]/skills/[skill]/`
**Propósito:** Separar o orquestrador principal (SKILL.md) de guias detalhados por fase
**Implementação:** SKILL.md referencia `references/*.md` via links relativos, carregados sob demanda

### Hook de Contexto Leve (lazy loading)

**Localização:** `plugins/[plugin]/hooks/`
**Propósito:** Injetar contexto mínimo (~5KB) no SessionStart, carregando a skill completa (~370 linhas + 21 references) apenas quando necessário
**Implementação:** `session-start` gera JSON com `additionalContext` contendo regras essenciais e triggers de ativação

### Polyglot Wrapper (cross-platform)

**Localização:** `hooks/run-hook.cmd`
**Propósito:** Executar hooks bash tanto em Unix quanto Windows
**Implementação:** Arquivo que é simultaneamente batch script (Windows) e bash script (Unix), usando `CMDBLOCK` como delimitador

## Fluxo de Dados

### Instalação e Distribuição

```
GitHub repo → claude plugin marketplace add → registro local
           → organização sync → instalação automática para equipe
```

### Execução em Sessão

```
SessionStart hook → injeta contexto leve (regras + triggers)
                  → dev pede tarefa → trigger detectado
                  → Skill tool carrega SKILL.md completo
                  → SKILL.md referencia references/*.md conforme fase
```

## Organização de Código

**Abordagem:** Por plugin (cada plugin é autocontido)

**Fronteiras de módulo:**
- Marketplace (raiz): apenas registro e documentação geral
- Plugin: autocontido com metadados, skills e hooks próprios
- Skill: SKILL.md como orquestrador + references como guias de fase
