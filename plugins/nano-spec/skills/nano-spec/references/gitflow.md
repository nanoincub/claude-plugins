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

## Início de Trabalho (dois momentos)

O gitflow atua em dois momentos ao iniciar trabalho novo:

### Branches protegidas

- `main`
- `develop`
- `master` (alias de main em projetos legados)

### Pré-specify: atualizar branch base

Se em branch protegida, executar:

```bash
git pull origin <branch-atual>
```

Garante que o trabalho parte da versão mais recente. Neste ponto ainda não se sabe o tipo de branch a criar.

### Pré-execute: criar branch de trabalho

Após Specify (e Design/Tasks se aplicável), o tipo de trabalho já é conhecido. Sugerir criação da branch:

```
⚠️ Você está na branch [branch]. Gitflow recomenda criar uma branch de trabalho.

Sugestão:
  → git checkout -b feature/<scope>-<slug>  (para features/refactors)
  → git checkout -b hotfix/<scope>-<slug>   (para correção urgente)
  → git checkout -b release/<version>       (para preparação de release)

Quer que eu crie a branch? (informe o nome ou aceite a sugestão)
Ou prefere trabalhar direto aqui? ⚠️ Em projetos com mais de um dev,
commitar direto em [branch] pode causar conflitos e sobrescrever trabalho de colegas.
```

**Ao criar a branch, executar exatamente:**

```bash
git checkout -b <tipo>/<nome> <branch-base>
```

Onde `<branch-base>` é `develop` para features e `main` para hotfixes. Ver seção "Comandos Exatos por Fluxo" para sequências completas.

**Regras:**
- Sempre sugerir, nunca bloquear — o dev tem a palavra final
- Se o dev confirmar que quer trabalhar na branch protegida, seguir sem insistir
- A sugestão de nome deve usar o scope da feature/fix atual

### Branches válidas para trabalho direto

- `feature/*`, `hotfix/*`, `release/*`, `support/*` — já isoladas, seguir normalmente
- Qualquer branch personalizada que não seja protegida

---

## Validação de Branch (Gate pré-commit)

Se o gate de início de trabalho foi pulado ou o dev escolheu ficar na branch protegida, o agente verifica novamente antes do commit conforme [commit.md](commit.md) Step 0. Última chance de criar branch antes de commitar.

---

## Comandos Exatos por Fluxo

Sequências completas para cada tipo de branch. O agente DEVE usar estes comandos — não improvisar.

### Feature

```bash
# Criar
git checkout develop
git pull origin develop
git checkout -b feature/<scope>-<slug>

# Trabalhar (commits normais)

# Finalizar (após confirmação do dev)
git checkout develop
git pull origin develop
git merge --no-ff feature/<scope>-<slug>
git branch -d feature/<scope>-<slug>
git push origin develop
```

### Release

```bash
# Criar
git checkout develop
git pull origin develop
git checkout -b release/<version>

# Preparar (bump version, docs, fixes menores)

# Finalizar
git checkout main
git pull origin main
git merge --no-ff release/<version>
git tag -a v<version> -m "Release <version>"
git checkout develop
git merge --no-ff release/<version>
git branch -d release/<version>
git push origin main
git push origin develop
git push --tags
```

### Hotfix

```bash
# Criar
git checkout main
git pull origin main
git checkout -b hotfix/<scope>-<slug>

# Corrigir (commits normais)

# Finalizar
git checkout main
git merge --no-ff hotfix/<scope>-<slug>
git tag -a v<version> -m "Hotfix <version>"
git checkout develop
git merge --no-ff hotfix/<scope>-<slug>
git branch -d hotfix/<scope>-<slug>
git push origin main
git push origin develop
git push --tags
```

**Se existe `release/*` ativa durante hotfix:** merge na release ao invés de develop.

---

## Regras de Merge

- Sempre `--no-ff` em todos os merges — preserva histórico como grupo
- Sempre `git pull` antes de merge — evita conflitos por branch desatualizada
- O agente orienta mas NÃO executa merges em branches protegidas sem confirmação do dev
- Deletar branch local após merge bem-sucedido

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
| **Pré-specify** | `git pull` se em branch protegida, para partir da versão mais recente |
| **Pré-execute** | Sugerir criação de branch de trabalho — tipo já conhecido. Se worktree ativado, branch já está isolada |
| **Commit** | Gate pré-commit: última verificação de branch (Step 0 em [commit.md](commit.md)) |
| **Pós-commit** | 4 opções: review + merge, merge direto, continuar trabalhando, manter. Alerta de desvio de escopo da branch |
| **Finishing branch** | Se superpowers/worktree, `finishing-a-development-branch` com cleanup adicional |

---

## Quando NÃO aplicar

- Projeto solo sem releases formais (trunk-based pode ser melhor)
- CLAUDE.md explicitamente desativa gitflow
- Dev pede para ignorar — respeitar sem insistir
- Hotfix urgente onde o dev decide commitar direto na main

