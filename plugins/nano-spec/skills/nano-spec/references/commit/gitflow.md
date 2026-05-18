# Gitflow

> **Fluxo completo vive em [`nano-spec:nano-commit`](../../../nano-commit/SKILL.md).**
> Este arquivo lista os HARD BLOCKs e regras críticas de gitflow para quem navega pelos references.

## HARD BLOCK: `git-flow-next` instalado

Na primeira interação git da sessão, executar `git flow version`. Se não estiver instalado → **BLOQUEAR TODO O PROCESSO** até o dev instalar.

**Sem exceções, sem fallback para git puro.** Única exceção: `CLAUDE.md` do projeto define `## Branching: Sem gitflow` ou `trunk-based`.

```bash
# macOS / Linux
brew install gittower/tap/git-flow-next

# Windows
winget install GitTower.GitFlowNext
```

## Regras de branching

| Tipo de branch | Base | Destino do merge | Tag automática |
|---|---|---|---|
| `feature/<slug>` | `develop` | `develop` | — |
| `bugfix/<slug>` | `develop` | `develop` | — |
| `hotfix/<version>` | `main` | `main` + `develop` | ✅ (nome da branch vira tag) |
| `release/<version>` | `develop` | `main` + `develop` | ✅ (nome da branch vira tag) |
| `support/<version>` | `main` (tag específica) | — | — |

**Naming semver para hotfix/release:** `hotfix/1.2.1`, `release/1.3.0`. Descrição vai na mensagem do commit, NÃO no nome da branch.

## Comandos canônicos

```bash
# Iniciar (sempre com --fetch para partir do remote atualizado)
git flow feature start --fetch <slug>
git flow hotfix start --fetch <version>
git flow release start --fetch <version>

# Finalizar (sempre com --no-ff inline — preserva bolha de merge)
git flow feature finish --no-ff <slug>
git flow hotfix finish --no-ff <version>
git flow release finish --no-ff <version>

# Tag diferente do nome da branch
git flow hotfix finish --no-ff --tagname <tag> <version>
```

## Gates de gitflow no trilho

| Momento | Gate |
|---|---|
| **Pré-specify** (ou pré-describe no Quick Mode) | Se em branch protegida (`main`/`develop`/`master`): `git pull` para garantir base atualizada |
| **Pré-execute** | Sugerir criação da branch de trabalho — tipo já conhecido neste ponto |
| **Pré-commit** | Última chance: verificar branch antes de commitar (sugestão, não bloqueio) |
| **Pós-commit** | Apresentar 4 opções: merge local / PR / manter / discard (com confirmação tipada `discard`) |

## Detalhes operacionais

Comandos exatos, tratamento de cada cenário (release com tag custom, discard com confirmação dupla, etc.), e integração com o orquestrador estão em [`nano-commit/SKILL.md`](../../../nano-commit/SKILL.md).
