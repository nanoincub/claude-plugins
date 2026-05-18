# Nano Incub — Claude Code Plugins

Marketplace interno de plugins da Nano Incub para [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview).

Centraliza plugins que automatizam e padronizam fluxos de desenvolvimento com IA, fornecendo processos estruturados, quality gates e integração com ferramentas existentes.

## Plugins Disponíveis

| Plugin | Descrição | Versão |
|--------|-----------|--------|
| [**nano-spec**](plugins/nano-spec/) | Processo Spec-Driven — orquestrador puro (Specify → Design → Tasks → Execute → /simplify → Commit). Requer `nano-disciplines` + `nano-commit`. | 6.0.0 |
| [**nano-disciplines**](plugins/nano-disciplines/) | Disciplinas técnicas universais: TDD, debug, verification, code review, subagents, parallel dispatch, security, validate, docs-update, context-limits. Reutilizável fora do Spec-Driven. | 1.2.0 |
| [**nano-commit**](plugins/nano-commit/) | Fluxo de commit (gitflow + Conventional Commits + 4 opções de fechamento). Standalone, invocável sem nano-spec. | 1.4.0 |
| [**nano-resumo-dia**](plugins/nano-resumo-dia/) | Timeline de trabalho dos históricos de sessão do Claude Code | 1.0.0 |

## Instalação

### Pré-requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) instalado e configurado

> **HARD BLOCK:** desde a 6.0.0, o nano-spec depende de DOIS plugins via HARD BLOCK — `nano-disciplines` (caixa de ferramentas universal) e `nano-commit` (fluxo de commit/gitflow). Sem um dos dois, o orquestrador bloqueia. Instale os três.

### Via terminal (recomendado)

Registre o marketplace (uma vez):

```bash
claude plugin marketplace add nanoincub/claude-plugins
```

Instale os plugins (ordem: dependências primeiro, depois o orquestrador):

```bash
claude plugin install nano-disciplines@nano-incub
claude plugin install nano-commit@nano-incub
claude plugin install nano-spec@nano-incub
```

### Via organização (automático)

1. Claude Code → **Organização** → **Plugins** → **Adicionar plugins** → **Sincronizar do GitHub**
2. Selecione o repositório `nanoincub/claude-plugins`
3. Ative sincronização automática
4. Altere acesso para **"Installed by default"**

Após sincronizar, o plugin é instalado automaticamente para todos os membros.

## Uso Rápido

Após instalar, basta pedir qualquer tarefa de desenvolvimento. O nano-spec ativa automaticamente:

```
Dev: "nova feature: login com Google"

Agent: Medium scope. Defaults: spec breve → execute → /simplify → suite de testes → commit.
       Opções: TDD, worktree, review, security. Ajustar? (Enter = defaults)

Dev: [Enter]

Agent: [Specify] Quem vai usar? Quais providers?
Dev: "Usuário final, só Google, precisa linkar com conta existente"

Agent: [Spec gerada] Spec ok? Posso implementar?
Dev: "sim"

Agent: [Execute] Implementando task 1... ✅ Teste criado e passando.
       Implementando task 2... ✅ Verificação manual OK.
       [/simplify] Diff acumulado analisado. 1 sugestão de reuse → corrigido.
       [Testes] Suite completa: 15/15 passando.
       [Docs] Atualizado.
       Quer commitar?
Dev: "sim"

Agent: [Commit] feat(auth): add Google OAuth login
```

**Triggers:** `"nova feature"`, `"implementar"`, `"quick fix"`, `"review"`, `"commitar"`, `"fix bug"`, `"refactor"`

## Arquitetura

```
claude-plugins/
├── .claude-plugin/
│   └── marketplace.json      # Registro de plugins
├── plugins/
│   └── nano-spec/            # Plugin principal
│       ├── .claude-plugin/
│       │   └── plugin.json   # Metadados
│       ├── hooks/            # SessionStart hook
│       ├── skills/
│       │   └── nano-spec/
│       │       ├── SKILL.md  # Orquestrador (~370 linhas)
│       │       └── references/  # 21 guias de fase
│       └── README.md
├── .specs/                   # Documentação estruturada
├── CLAUDE.md                 # Convenções do projeto
└── README.md
```

## Adicionando Novos Plugins

1. Crie em `plugins/nome-do-plugin/`:

```
plugins/nome-do-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── nome-da-skill/
│       └── SKILL.md
└── hooks/ (opcional)
```

2. Registre em `.claude-plugin/marketplace.json`:

```json
{
  "name": "nome-do-plugin",
  "description": "Descrição do plugin",
  "category": "development",
  "source": "./plugins/nome-do-plugin",
  "homepage": "https://github.com/nanoincub/nome-do-plugin"
}
```

3. Push — sincronização automática distribui para a organização.

## Licença

CC-BY-4.0 — baseado em [tlc-spec-driven](https://github.com/felipfr) v2.0.0 por Felipe Rodrigues.
