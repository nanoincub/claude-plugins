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
| **Hooks de gitflow** | `hooks/gitflow/` — abrem o PR no GitHub a cada `git flow publish` e avisam quando tag/back-merge ficaram só locais |
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

## Hooks de gitflow (GitHub)

```bash
plugins/nano-commit/hooks/gitflow/install.sh /caminho/do/repo
```

Copia os hooks para `.githooks/` do repositório alvo (versionável) e aponta
`gitflow.path.hooks` para lá.

| Hook | O que faz |
|---|---|
| `post-flow-<tipo>-publish` | abre o PR com `gh` na base correta (`develop` para feature/bugfix, `main` para release/hotfix), já com o aviso de não deletar a branch e o comando do `finish` |
| `post-flow-<tipo>-finish` | confere tag e branches base contra o remote e avisa o que ficou por publicar |

Saem em silêncio quando o remote não é GitHub, quando falta `gh` ou quando já há
PR aberto — nunca fazem o comando de gitflow falhar. Overrides: `NANO_PR_TITLE`,
`NANO_PR_DRAFT=1`, `NANO_PR_SKIP=1`.

## Pré-requisitos

- **git-flow-next ≥ 1.2.0** instalado localmente (HARD BLOCK próprio). Sem fallback para git puro. A 1.2.0 é o piso porque abaixo dela o `finish` não tem `--push` e um cleanup remoto falho trava todo `finish` seguinte do repositório.
- **gh** autenticado, para os hooks de PR (opcional — sem ele o fluxo segue manual).
- Repositório com modelo de branching gitflow clássico — ou CLAUDE.md declarando `trunk-based` / `Sem gitflow` para desativar.

## Estrutura

```
plugins/nano-commit/
├── .claude-plugin/plugin.json
├── README.md
├── hooks/gitflow/
│   ├── install.sh
│   ├── nano-pr-create
│   ├── nano-finish-check
│   ├── post-flow-{feature,bugfix,release,hotfix}-publish
│   └── post-flow-{feature,bugfix,release,hotfix}-finish
└── skills/nano-commit/
    └── SKILL.md
```

## Versão

**1.6.0** — Correções no fechamento por PR no GitHub, validadas em sandbox: o `finish` passa a exigir tipo e nome (sem eles o comando opera na branch atual e falha depois do checkout na base) e `--push` (sem ele a tag e o back-merge ficam só na máquina do dev). Piso de versão do git-flow-next (≥ 1.2.0) no HARD BLOCK. `main` deixa de precisar ficar desprotegida neste fluxo. Novos hooks de gitflow em `hooks/gitflow/`: abrem o PR no `publish` e avisam o que ficou por publicar no `finish`.

**1.5.0** — Fechamento por PR bifurcado por plataforma. No GitHub o PR não substitui o `git flow finish`: o fluxo é `publish` → PR → `finish`, e o `finish` roda depois do merge para criar a tag e fazer o back-merge em `develop`. No GitLab nada muda — segue push + Merge Request. Inclui os pré-requisitos de configuração do repositório no GitHub (`delete_branch_on_merge` desligado, squash/rebase desligados) e a ressalva sobre back-merge com `develop` protegida.

**1.4.0** — Promovido a plugin standalone, extraído do `nano-spec` 5.0.0 → 6.0.0 (BREAKING split). Conteúdo da skill inalterado em relação a 1.3.0; bump minor pela mudança de empacotamento (sub-skill → plugin top-level).

**1.3.0** — Última versão interna ao `nano-spec`.
