# Gitflow

**Goal**: Padronizar o modelo de branching da equipe usando gitflow clássico (Vincent Driessen), garantindo que commits aconteçam na branch correta e que o time siga um fluxo previsível.

**Configurável por projeto** — se o CLAUDE.md define um modelo de branching diferente, respeitar.

---

## Modelo de Branches

| Branch | Origem | Destino | Propósito |
|--------|--------|---------|-----------|
| `main` | — | — | Código em produção. Apenas merges de `release/*` e `hotfix/*` |
| `develop` | `main` | — | Integração de features. Base para novas features |
| `feature/*` | `develop` | `develop` | Desenvolvimento de features |
| `release/*` | `develop` | `main` + `develop` | Preparação de release (bumps, docs, fixes menores) |
| `hotfix/*` | `main` | `main` + `develop` | Correção urgente em produção |
| `support/*` | `main` (tag) | — | Manutenção de versões anteriores (raro) |

---

## Naming de Branches

```
feature/<scope>-<slug>
release/<version>
hotfix/<scope>-<slug>
support/<version>
```

- **scope**: o mesmo scope do commit (ex: `auth`, `cart`, `api`)
- **slug**: descrição curta em kebab-case
- **version**: semver (ex: `1.2.0`)

Exemplos:
- `feature/auth-google-login`
- `release/2.1.0`
- `hotfix/cart-negative-quantity`

**IMPORTANTE:** Se o CLAUDE.md do projeto define convenção de naming diferente, usar a do projeto.

---

## Validação de Branch (Gate pré-commit)

Antes de commitar, o agente DEVE verificar a branch atual:

### Branches protegidas (NÃO commitar diretamente)

- `main`
- `develop`
- `master` (alias de main em projetos legados)

### Ação quando em branch protegida

Se o dev está em `main`, `develop` ou `master`:

```
⚠️ Você está na branch [branch]. Gitflow recomenda não commitar diretamente aqui.

Sugestão: criar uma branch antes de commitar.
  → feature/<scope>-<slug>  (para features/refactors)
  → hotfix/<scope>-<slug>   (para correção urgente)

Quer que eu crie a branch? (informe o nome ou aceite a sugestão)
Ou prefere commitar aqui mesmo? (seu projeto, sua decisão)
```

**Regras:**
- Sempre sugerir, nunca bloquear — o dev tem a palavra final
- Se o dev confirmar que quer commitar na branch protegida, seguir sem insistir
- A sugestão de nome deve usar o scope da feature/fix atual

### Branches válidas para commit direto

- `feature/*` — desenvolvimento normal
- `hotfix/*` — correção urgente
- `release/*` — preparação de release
- `support/*` — manutenção de versão
- Qualquer branch personalizada que não seja protegida

---

## Orientação de Merge

Quando o dev perguntar sobre merge ou quando o fluxo envolver integração:

- **Feature → develop**: sempre `--no-ff` para preservar histórico como grupo. Deletar branch após merge.
- **Release → main + develop**: merge na main, criar tag `v<version>`, merge de volta na develop. Deletar branch.
- **Hotfix → main + develop**: merge na main, criar tag, merge na develop. Se existe `release/*` ativa, merge na release ao invés de develop.

**Regras:**
- Sempre `--no-ff` em todos os merges
- O agente orienta mas NÃO executa merges em branches protegidas sem confirmação do dev

---

## Configuração por Projeto

O agente detecta e respeita configurações do CLAUDE.md:

| Configuração no CLAUDE.md | Efeito |
|---------------------------|--------|
| `## Branching` ou `## Git Flow` | Usar modelo definido pelo projeto |
| `Branch principal: master` | Tratar `master` como equivalente a `main` |
| `Branches protegidas: [lista]` | Usar lista do projeto ao invés do padrão |
| `Sem gitflow` / `trunk-based` | Desativar validação de branch |
| `Prefixo de branch: [padrão]` | Usar padrão do projeto para naming |

Se o CLAUDE.md não menciona branching → usar gitflow clássico como default.

---

## Integração com o Fluxo nano-spec

| Fase | Comportamento com gitflow |
|------|--------------------------|
| **Execute** | Se worktree ativado, branch já está isolada — gitflow não interfere |
| **Commit** | Validação de branch como Step 0 (ver [commit.md](commit.md)) |
| **Finishing branch** | Se superpowers instalado, `finishing-a-development-branch` apresenta opções de merge |

---

## Quando NÃO aplicar

- Projeto solo sem releases formais (trunk-based pode ser melhor)
- CLAUDE.md explicitamente desativa gitflow
- Dev pede para ignorar — respeitar sem insistir
- Hotfix urgente onde o dev decide commitar direto na main

