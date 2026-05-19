# nano-commit

Fluxo completo de commit da Nano Incub. Standalone — invocável sem nano-spec.

## Instalação

```bash
claude plugin install nano-commit@nano-incub
```

## O que tem

| Componente | Função |
|---|---|
| **git-flow-next HARD BLOCK** | Verifica instalação obrigatória antes de qualquer fluxo de branch |
| **Gitflow clássico** | `feature/*`, `hotfix/*`, `release/*` com semver |
| **Conventional Commits** | Mensagens padronizadas (`tipo(escopo): descrição`) |
| **Gates pré-commit obrigatórios** | `/simplify` → suite de testes → rastreabilidade `Refs:` → commit |
| **4 opções de fechamento de branch** | merge / PR / continuar / discard (com confirmação) |
| **Detecção de scope drift** | Alerta quando o diff foge do escopo declarado |

## Como usar

### Standalone (sem nano-spec)

Triggers diretos: `"commitar"`, `"fazer commit"`, `"criar branch"`, `"criar PR"`, `"abrir PR"`, `"finalizar branch"`, `"fechar feature"`, `"gitflow"`, `"merge feature"`, `"merge branch"`, `"fechar branch"`, `"git flow"`.

```
Dev: "commitar"
Agente: [invoca skill nano-commit:nano-commit] → roda gates → propõe mensagem → confirma com dev
```

### Integrado ao nano-spec

`nano-spec` 6.0.0+ depende deste plugin via HARD BLOCK e invoca a skill na fase **Commit** do trilho Spec-Driven (Specify → Design → Tasks → Execute → /simplify → Commit).

### Refs cross-plugin

Outros plugins referenciam esta skill via:

```
nano-commit:nano-commit
nano-commit:skills/nano-commit/SKILL.md
```

## Pré-requisitos

- **git-flow-next** instalado localmente (HARD BLOCK próprio). Sem fallback para git puro.
- Repositório com modelo de branching gitflow clássico — ou CLAUDE.md declarando `trunk-based` / `Sem gitflow` para desativar.

## Estrutura

```
plugins/nano-commit/
├── .claude-plugin/plugin.json
├── README.md
└── skills/nano-commit/
    └── SKILL.md
```

## Versão

**1.4.0** — Promovido a plugin standalone, extraído do `nano-spec` 5.0.0 → 6.0.0 (BREAKING split). Conteúdo da skill inalterado em relação a 1.3.0; bump minor pela mudança de empacotamento (sub-skill → plugin top-level).

**1.3.0** — Última versão interna ao `nano-spec`.
