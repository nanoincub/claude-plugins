# Gitflow

**Goal**: Padronizar o modelo de branching da equipe usando gitflow clássico (Vincent Driessen), garantindo que commits aconteçam na branch correta e que o time siga um fluxo previsível.

**Ferramenta**: [git-flow-next](https://github.com/gittower/git-flow-next) (Tower) — reimplementação moderna em Go, drop-in replacement do nvie/gitflow. **Obrigatória.**

**Configurável por projeto** — se o CLAUDE.md define um modelo de branching diferente, respeitar.

---

## Gate: Detecção e Instalação (HARD BLOCK)

O agente DEVE executar esta verificação **uma vez por sessão** (na primeira interação com gitflow):

```bash
git flow version
```

- **Se output contém "git-flow-next"** → cachear `gitflow = true`, prosseguir normalmente
- **Se comando falha ou indica outra implementação** → **BLOQUEAR TODO O PROCESSO**

**Quando bloqueado**, o agente DEVE:
1. Exibir mensagem de bloqueio clara:
```
⛔ git-flow-next NÃO está instalado. Este é um requisito obrigatório.

Instale antes de continuar:
  macOS:    brew install gittower/tap/git-flow-next
  Linux:    brew install gittower/tap/git-flow-next
  Windows:  winget install GitTower.GitFlowNext
  Manual:   https://github.com/gittower/git-flow-next/releases

Após instalar, diga "pronto" para continuar.
```
2. **NÃO prosseguir** para nenhuma fase (Specify, Execute, Commit — NENHUMA)
3. **NÃO oferecer alternativa** com git puro — git-flow-next é obrigatório
4. **Aguardar** o dev confirmar que instalou, e então re-verificar com `git flow version`

**Única exceção:** Se o CLAUDE.md do projeto contém `Sem gitflow` ou `trunk-based`, pular este gate.

**Não re-verificar** a cada gate após sucesso — cachear o resultado na sessão.

### Inicialização do repositório

Se o repositório ainda não foi inicializado com git-flow, executar:

```bash
git flow init --defaults    # aceita branch naming padrão (main/develop/feature/release/hotfix)
git flow init               # interativo — permite customizar nomes
```

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
hotfix/<version>
support/<version>
```

- **scope** (feature): o mesmo scope do commit (ex: `auth`, `cart`, `api`)
- **slug** (feature): descrição curta em kebab-case
- **version**: semver (ex: `1.2.0`, `1.0.1`)

Exemplos:
- `feature/auth-google-login`
- `release/2.1.0`
- `hotfix/1.0.1`

**Nota — release e hotfix:** O git-flow-next usa o nome da branch como tag por padrão no `finish`. Por isso ambas seguem `<tipo>/<version>` em semver — a descrição do fix vai na mensagem do commit, NÃO no nome da branch. Se o nome da branch não for semver, a tag gerada também não será (ex: `hotfix/cart-negative-quantity` produz tag `cart-negative-quantity`). Para tag diferente do nome da branch, passar `--tagname <tag>` no finish.

**IMPORTANTE:** Se o CLAUDE.md do projeto define convenção de naming diferente, usar a do projeto.

---

## Início de Trabalho (dois momentos)

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

> **Nota:** `git pull` é o único comando git manual no fluxo — git-flow-next não tem comando de sync para branches protegidas.

### Pré-execute: criar branch de trabalho

Após Specify (e Design/Tasks se aplicável), o tipo de trabalho já é conhecido. Sugerir criação da branch:

```
Você está na branch [branch]. Gitflow recomenda criar uma branch de trabalho.

Sugestão:
  → git flow feature start <scope>-<slug>   (para features/refactors)
  → git flow hotfix start <version>         (para correção urgente, ex: 1.0.1 — nome vira a tag)
  → git flow release start <version>        (para preparação de release — nome vira a tag)

Quer que eu crie a branch? (informe o nome ou aceite a sugestão)
Ou prefere trabalhar direto aqui? Em projetos com mais de um dev,
commitar direto em [branch] pode causar conflitos e sobrescrever trabalho de colegas.
```

**Regras:**
- Sempre sugerir, nunca bloquear — o dev tem a palavra final
- Se o dev confirmar que quer trabalhar na branch protegida, seguir sem insistir
- A sugestão de nome deve usar o scope da feature/fix atual
- Usar `--fetch` para garantir que a branch parte da versão remota mais recente

### Branches válidas para trabalho direto

- `feature/*`, `hotfix/*`, `release/*`, `support/*` — já isoladas, seguir normalmente
- Qualquer branch personalizada que não seja protegida

---

## Validação de Branch (Gate pré-commit)

Se o gate de início de trabalho foi pulado ou o dev escolheu ficar na branch protegida, o agente verifica novamente antes do commit conforme [commit.md](commit.md) Step 0. Última chance de criar branch antes de commitar.

---

## Comandos

O git-flow-next orquestra a sequência correta (merge, tag, cleanup). O agente DEVE usar estes comandos — não improvisar com git manual.

> **⚠️ Importante:** diferente do gitflow clássico (AVH), o **git-flow-next NÃO aplica `--no-ff` por padrão** — quando possível ele faz fast-forward, o que apaga a "bolha" de merge da feature no histórico. Para preservar o histórico visual do gitflow, **sempre passar `--no-ff` inline** no `finish`.

### Feature

```bash
# Criar (a partir de develop)
git flow feature start <scope>-<slug>

# Sincronizar com develop durante o trabalho
git flow update

# Publicar no remote
git flow publish

# Finalizar — merge --no-ff para develop + delete branch
git flow finish --no-ff
```

### Release

```bash
# Criar (a partir de develop)
git flow release start <version>

# Preparar (bump version, docs, fixes menores)

# Finalizar — merge --no-ff para main + tag + merge --no-ff para develop + delete branch
git flow finish --no-ff
```

### Hotfix

```bash
# Criar (a partir de main) — nome da branch vira a tag (semver)
git flow hotfix start <version>     # ex: 1.0.1

# Corrigir (commits normais)

# Finalizar — merge --no-ff para main + tag + merge --no-ff para develop + delete branch
git flow finish --no-ff
```

**Se existe `release/*` ativa durante hotfix:** merge na release ao invés de develop (git-flow-next gerencia isso automaticamente).

### Shorthands (auto-detect branch type)

Comandos que detectam automaticamente o tipo da branch atual — **preferir sempre que o agente já está na branch correta**:

| Comando | O que faz |
|---------|-----------|
| `git flow finish` | Finaliza a branch atual (merge + tag + cleanup) |
| `git flow publish` | Push da branch atual para o remote |
| `git flow update` | Sync da branch atual com a branch pai |
| `git flow delete` | Remove a branch atual |
| `git flow rename <nome>` | Renomeia a branch atual |

### Flags úteis

```bash
git flow feature finish --no-ff       # força merge commit (preserva bolha no histórico) — SEMPRE usar
git flow feature finish --keep        # não deleta a branch após merge
git flow release finish --no-tag      # finaliza sem criar tag
git flow hotfix finish --push         # push automático após finish
git flow feature start --fetch        # fetch do remote antes de criar
```

Flags podem ser combinadas: `git flow feature finish --no-ff --push`.

### Tornar `--no-ff` permanente (opcional)

Se o dev prefere não lembrar da flag, configurar por repositório:

```bash
git config gitflow.feature.finish.no-ff true
git config gitflow.release.finish.no-ff true
git config gitflow.hotfix.finish.no-ff true
```

O agente **continua passando `--no-ff` inline** mesmo com a config setada — é idempotente e deixa a intenção explícita no histórico de comandos.

---

## Regras de Merge

- **Sempre passar `--no-ff` inline** no `git flow <tipo> finish` — git-flow-next faz fast-forward por padrão e apaga a bolha da feature no histórico
- **Tag em release e hotfix:** o git-flow-next usa o nome da branch como nome da tag por padrão. Por isso ambas seguem `<tipo>/<version>` (ex: `release/2.1.0`, `hotfix/1.0.1`). Se precisar de tag diferente do nome da branch, passar `--tagname <tag>` no `finish`.
- O agente orienta mas NÃO executa `git flow finish` em branches protegidas sem confirmação do dev
- Branch local é deletada automaticamente pelo `git flow finish` (usar `--keep` para preservar)

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
| **Pré-execute** | `git flow <tipo> start` — tipo já conhecido |
| **Commit** | Gate pré-commit: última verificação de branch (Step 0 em [commit.md](commit.md)) |
| **Pós-commit** | 4 opções: review + `git flow finish`, `git flow finish` direto, continuar trabalhando, manter |
| **Finishing branch** | Se superpowers detectado, `finishing-a-development-branch` |

---

## Referência Avançada

Para cenários complexos (conflitos no finish, configuração avançada, hooks, filters), consultar Context7: `/gittower/git-flow-next`.

---

## Quando NÃO aplicar

- Projeto solo sem releases formais (trunk-based pode ser melhor)
- CLAUDE.md explicitamente desativa gitflow
- Dev pede para ignorar — respeitar sem insistir
- Hotfix urgente onde o dev decide commitar direto na main
