---
name: nano-commit
description: >
  Fluxo completo de commit da Nano Incub — git-flow-next como HARD BLOCK,
  gitflow clássico (feature/hotfix/release com semver), Conventional Commits,
  gates obrigatórios (/simplify + suite de testes + rastreabilidade),
  detecção de desvio de escopo e 4 opções de fechamento de branch (merge/PR/
  continuar/discard com confirmação). Invocação direta sem precisar carregar
  o orquestrador nano-spec inteiro.
  Triggers: "commitar", "fazer commit", "criar commit", "criar branch",
  "criar PR", "abrir PR", "finalizar branch", "fechar feature", "gitflow",
  "merge feature", "merge branch", "fechar branch", "git flow". Não use para
  inicializar projeto, especificar feature, ou implementar código.
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 1.3.0
---

# Nano Commit — Gitflow + Conventional Commits

**Goal**: Padronizar branching e commits da Nano Incub via [git-flow-next](https://github.com/gittower/git-flow-next). Gates obrigatórios. Configurável por projeto via CLAUDE.md.

---

## Gate: Detecção e Instalação (HARD BLOCK)

Na primeira interação com gitflow na sessão, executar:

```bash
git flow version
```

- **Se output contém "git-flow-next"** → cachear `gitflow = true`, prosseguir
- **Se comando falha ou indica outra implementação** → **BLOQUEAR TODO O PROCESSO**

Quando bloqueado, exibir:

```
⛔ git-flow-next NÃO está instalado. Este é um requisito obrigatório.

Instale antes de continuar:
  macOS:    brew install gittower/tap/git-flow-next
  Linux:    brew install gittower/tap/git-flow-next
  Windows:  winget install GitTower.GitFlowNext
  Manual:   https://github.com/gittower/git-flow-next/releases

Após instalar, diga "pronto" para continuar.
```

**Regras:**
- NÃO prosseguir para nenhuma fase
- NÃO oferecer alternativa com git puro — git-flow-next é obrigatório
- Aguardar dev confirmar instalação, re-verificar com `git flow version`
- Não re-verificar a cada gate após sucesso — cachear na sessão
- **Única exceção:** CLAUDE.md contém `Sem gitflow` ou `trunk-based`

### Inicialização do repositório

Se o repositório ainda não foi inicializado:

```bash
git flow init --defaults    # branch naming padrão (main/develop/feature/release/hotfix)
git flow init               # interativo — permite customizar nomes
```

---

## Detectar Configuração do Projeto

Ler CLAUDE.md e extrair:

| Configuração | Efeito |
|--------------|--------|
| `## Branching` ou `## Git Flow` | Usar modelo definido pelo projeto |
| `Branch principal: master` | Tratar `master` como equivalente a `main` |
| `Branches protegidas: [lista]` | Usar lista do projeto ao invés do padrão |
| `Sem gitflow` / `trunk-based` | Desativar validação de branch |
| `Prefixo de branch: [padrão]` | Usar padrão do projeto para naming |
| `Scopes de commit: [lista]` | Usar APENAS esses scopes nos commits |
| `Comandos de teste: [comando]` | Usar este comando ao pedir suite ao dev |

Se CLAUDE.md não menciona branching → gitflow clássico (Vincent Driessen) como default.

---

## Modelo de Branches

| Branch | Origem | Destino | Propósito |
|--------|--------|---------|-----------|
| `main` (ou `master` em legados) | — | — | Código em produção. Apenas merges de `release/*` e `hotfix/*`. **Protegida.** |
| `develop` | `main` | — | Integração de features. Base para novas features. **Protegida.** |
| `feature/*` | `develop` | `develop` | Desenvolvimento de features |
| `release/*` | `develop` | `main` + `develop` | Preparação de release |
| `hotfix/*` | `main` | `main` + `develop` | Correção urgente em produção |
| `support/*` | `main` (tag) | — | Manutenção de versões anteriores (raro) |

### Naming

```
feature/<scope>-<slug>
release/<version>
hotfix/<version>
support/<version>
```

- **scope** (feature): mesmo scope do commit (ex: `auth`, `cart`, `api`)
- **slug** (feature): descrição curta em kebab-case
- **version**: semver (ex: `1.2.0`, `1.0.1`)

Exemplos: `feature/auth-google-login`, `release/2.1.0`, `hotfix/1.0.1`.

**Nota — release/hotfix:** nome da branch vira tag no `finish`. Por isso `<tipo>/<version>` em semver.

**Se CLAUDE.md define convenção diferente, usar a do projeto.**

---

## Fluxo Completo

### Pré-specify: atualizar branch base

Se em branch protegida, executar:

```bash
git pull --ff-only
```

### Pré-execute (Step 0): Baseline Test Gate

**Antes** de criar a branch de trabalho, rodar a suite completa de testes na base atualizada (`develop` para feature/bugfix/release, `main` para hotfix). Fluxo detalhado em [../nano-spec/references/baseline-test-gate.md](../nano-spec/references/baseline-test-gate.md).

- **Verde** → seguir para criação da branch.
- **Vermelho** → exibir alerta de máxima importância (formato em `baseline-test-gate.md`) com 2 opções:
  - **[1] PARAR** (fortemente recomendado): corrigir baseline antes — git blame nos testes para identificar autor.
  - **[2] OVERRIDE**: prosseguir registrando snapshot em `.specs/project/STATE.md` (testes falhando, SHA da base, responsável, plano). Sem registro → processo BLOQUEIA. Override aqui NÃO dispensa o gate pré-commit final.

Agente NÃO roda os testes diretamente — pede ao dev e aguarda confirmação do resultado (evita gasto de tokens em output).

### Pré-execute: criar branch de trabalho

Após Specify (e Design/Tasks se aplicável), tipo já é conhecido. Sugerir:

```
Você está na branch [branch]. Gitflow recomenda criar uma branch de trabalho.

Sugestão (sempre prefixado por `git checkout <base> && git pull --ff-only`):

  Feature/refactor (base: develop):
    git checkout develop && git pull --ff-only && \
    git flow feature start <scope>-<slug>

  Bugfix não-urgente (base: develop):
    git checkout develop && git pull --ff-only && \
    git flow bugfix start <scope>-<slug>

  Hotfix urgente (base: main — nome vira tag semver):
    git checkout main && git pull --ff-only && \
    git flow hotfix start <version>

  Release (base: develop — nome vira tag semver):
    git checkout develop && git pull --ff-only && \
    git flow release start <version>

Quer que eu crie a branch? (informe o nome ou aceite a sugestão)
Ou prefere trabalhar direto aqui? Em projetos com mais de um dev,
commitar direto em [branch] pode causar conflitos e sobrescrever trabalho de colegas.
```

**Regras:**
- Sempre sugerir, nunca bloquear — dev tem palavra final
- Se dev confirmar trabalho na branch protegida, seguir sem insistir
- Sugestão de nome deve usar o scope da feature/fix atual
- Sempre `git checkout <base> && git pull --ff-only` ANTES do `git flow <type> start`. Não usar `--fetch` (não substitui o pull)

### Pré-commit (Step 0): validação de branch

Se o gate de início foi pulado ou dev escolheu ficar na branch protegida, verificar branch novamente antes de commitar. Última chance de criar branch de trabalho. Sugestão, não bloqueio.

### Step 1: perguntar ao dev

Após concluir Execute (ou série de ajustes):

```
Implementação concluída. Quer commitar?
  Arquivos modificados: [lista]
  Commit sugerido: <type>(<scope>): <description>
```

- **Sim** → seguir
- **Não** → fim. Mudanças ficam no working tree.

### Step 2: gates pré-commit (ordem obrigatória)

1. [ ] `/simplify` passou sobre diff acumulado (obrigatório — roda **primeiro**, refatora o diff)
2. [ ] Dev rodou suite completa de testes **após** o /simplify (obrigatório — valida o diff já refatorado; ver nota)
3. [ ] Docs atualizado — ver `docs-update.md` no orquestrador
4. [ ] Todos os "Done when" da task verificados
5. [ ] Rastreabilidade verificada (ver nota)
6. [ ] **Baseline overrides reconciliados** — se há entrada ativa em STATE.md (`## Baseline overrides ativos`), suite verde aqui significa que as falhas foram resolvidas: mover entrada para `## Baseline overrides resolvidos` com data. Se a suite ainda mostra alguma das falhas originais → BLOQUEAR commit e exibir: "Override aceito em <data> ainda não foi resolvido. Resolva antes de fechar a branch."

> **Ordem fixa /simplify → testes:** se a suite rodou **antes** do /simplify, NÃO conta. Pedir nova rodada após a refatoração — qualquer regressão introduzida pelo /simplify só é capturada se os testes rodarem depois.

**Gate Iron Law (obrigatório):** aplicar [verification.md](nano-disciplines:verification.md) como gate bloqueante. Testes DEVEM passar (com evidência fresca, **nesta mensagem**) antes de oferecer opções de commit — se falharam ou se a verificação não foi rodada nesta interação, BLOQUEAR o fluxo (não apenas pedir ao dev, mas impedir o avanço).

**Suite de testes:** agente NÃO roda — pede ao dev e aguarda confirmação (evita gasto de tokens em output de centenas de testes). A confirmação do dev é o que dispara a Iron Law (ver [verification.md > Suite de testes](nano-disciplines:verification.md#suite-de-testes--política-do-nano-spec)).

**Rastreabilidade:** verificar que todos os IDs de requisito (`[FEAT]-XX`) da spec.md mapeados para esta task estão com status "Verified" na tabela de rastreabilidade. Se algum está "Pending" ou "Implementing", ALERTAR o dev com a lista de IDs pendentes e perguntar se deseja prosseguir.

### Step 3: detectar desvio de escopo

Antes de gerar a mensagem, verificar se o trabalho é coerente com o propósito da branch:

**Sinais de desvio:**
- Scope do commit ≠ scope da branch (ex: branch `feature/login`, commit toca `sms`)
- Arquivos modificados fora do domínio da feature (ex: branch de feature tocando configs de deploy)
- Tipo de trabalho incompatível (ex: branch `feature/*` com trabalho de `hotfix`)

Se detectado:

```
⚠️ Você está na branch feature/login, mas este commit toca [área diferente].
Isso deveria estar em uma branch separada?

  → Criar nova branch para este trabalho (recomendado)
  → Commitar aqui mesmo (minha branch, minha decisão)
```

**Alertar uma vez por desvio — não insistir.** Se dev pedir nova branch, stashar mudanças, criar a branch correta e aplicar.

### Step 4: criar commit atômico

**Um commit por task.** Nunca agrupar múltiplas tasks num commit.

**Formato (Conventional Commits 1.0.0):**

```
<type>(<scope>): <description>

[optional body]

Refs: [FEAT]-XX
```

---

## Types

| Type       | Quando usar                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | Nova feature ou capacidade                              |
| `fix`      | Correção de bug                                         |
| `refactor` | Mudança de código que não corrige bug nem adiciona feature |
| `docs`     | Apenas documentação                                     |
| `test`     | Adicionando ou corrigindo testes                        |
| `style`    | Formatação, semicolons, etc. (sem mudança de código)    |
| `perf`     | Melhoria de performance                                 |
| `build`    | Sistema de build ou dependências externas               |
| `ci`       | Arquivos e scripts de CI                                |
| `chore`    | Tarefas de manutenção que não modificam src ou test     |

---

## Regras da Description

- Imperativo: "add", não "added" ou "adds"
- Minúscula no início
- Sem ponto final
- Idioma do projeto (PT-BR para projetos da Nano, salvo override no CLAUDE.md)
- Complete a frase: "If applied, this commit will _[your description]_"

## Scope

Feature name ou área do módulo, lowercase.

- Se CLAUDE.md define scopes válidos → usar APENAS esses
- Se não define → nome da feature ou área do módulo

Exemplos genéricos: `auth`, `cart`, `api`, `settings`.

## Refs (rastreabilidade)

Quando a task tem ID rastreável (ex: `AUTH-01`), adicionar no footer:

```
feat(auth): add email validation to login form

Refs: AUTH-01
```

Quick tasks sem ID → omitir Refs.

## Breaking changes

Append `!` após type/scope **E** adicionar footer `BREAKING CHANGE:`:

```
feat(api)!: change authentication endpoint response format

BREAKING CHANGE: login endpoint now returns JWT in body instead of cookie

Refs: AUTH-05
```

## Regras gerais

- Um commit por task — clean git history, bisect e rollback possíveis
- Description referencia o que FOI FEITO, não o que foi planejado
- Apenas arquivos da task — nunca incluir mudanças "while I'm here"
- Testes junto — se testes são parte da task, incluir no mesmo commit

---

## Comandos git-flow-next

git-flow-next orquestra a sequência correta (merge, tag, cleanup). O agente DEVE usar estes comandos — não improvisar com git manual.

> **⚠️ Duas regras invariantes:**
> 1. **Sempre `git checkout <base> && git pull --ff-only` antes de `git flow <type> start`** — o `--fetch` do git-flow-next não fast-forwarda a base local; ver Anti-patterns.
> 2. **Sempre `--no-ff` inline no `finish`** — git-flow-next faz fast-forward por padrão, o que apaga a bolha de merge.

### Feature

```bash
# Atualizar base local + criar branch
git checkout develop && git pull --ff-only
git flow feature start <scope>-<slug>

# Sincronizar com develop durante o trabalho
git flow update

# Publicar no remote
git flow publish

# Finalizar — merge --no-ff para develop + delete branch
git flow finish --no-ff
```

### Bugfix

Mesmo fluxo de feature — diferença é semântica (separar correção de bug de nova capacidade no histórico). Branch parte de `develop`, merge volta para `develop`.

```bash
# Atualizar base local + criar branch
git checkout develop && git pull --ff-only
git flow bugfix start <scope>-<slug>

# Trabalhar (commits normais)

# Finalizar — merge --no-ff para develop + delete branch
git flow finish --no-ff
```

### Release

```bash
# Atualizar base local + criar branch
git checkout develop && git pull --ff-only
git flow release start <version>

# Preparar (bump version, docs, fixes menores)

# Finalizar — merge --no-ff para main + tag + merge --no-ff para develop + delete branch
git flow finish --no-ff
```

### Hotfix

```bash
# Atualizar base local (main) + criar branch — nome da branch vira a tag (semver)
git checkout main && git pull --ff-only
git flow hotfix start <version>     # ex: 1.0.1

# Corrigir (commits normais)

# Finalizar — merge --no-ff para main + tag + merge --no-ff para develop + delete branch
git flow finish --no-ff
```

**Se existe `release/*` ativa durante hotfix:** merge na release ao invés de develop (git-flow-next gerencia automaticamente).

### Shorthands (auto-detect branch type)

Preferir sempre que o agente já está na branch correta:

| Comando | O que faz |
|---------|-----------|
| `git flow finish` | Finaliza a branch atual (merge + tag + cleanup) |
| `git flow publish` | Push da branch atual para o remote |
| `git flow update` | Sync da branch atual com a branch pai |
| `git flow delete` | Remove a branch atual |
| `git flow rename <nome>` | Renomeia a branch atual |

### Flags úteis

```bash
git flow feature finish --no-ff       # força merge commit (preserva bolha) — SEMPRE usar
git flow feature finish --keep        # não deleta a branch após merge
git flow release finish --no-tag      # finaliza sem criar tag
git flow hotfix finish --push         # push automático após finish
```

Flags podem ser combinadas: `git flow feature finish --no-ff --push`.

### Anti-patterns conhecidos

**`git flow <type> start --fetch` em vez de `pull`:** `--fetch` atualiza `origin/develop` mas não fast-forwarda a base local — a branch nasce stale. Sintoma: `git log feature/foo..origin/develop` mostra commits logo após o `start`. Correção: rebase contra a base atualizada.

### Regras de Merge

- **Sempre passar `--no-ff` inline** no `git flow <tipo> finish`
- **Tag em release e hotfix:** nome da branch vira nome da tag. Para tag diferente, passar `--tagname <tag>`.
- Agente orienta mas NÃO executa `git flow finish` em branches protegidas sem confirmação do dev
- Branch local é deletada automaticamente pelo `git flow finish` (usar `--keep` para preservar)

---

## Pós-Commit: Fechamento de Branch

Após commitar em `feature/*`, `bugfix/*`, `hotfix/*` ou `release/*`, conduzir o fechamento estruturado: verificar testes → apresentar 4 opções → executar escolha do dev.

### Step 1 — Iron Law (gate obrigatório)

Aplicar [verification.md](nano-disciplines:verification.md) — confirmar **com evidência fresca nesta mensagem** que a suite de testes passa. Se não foi verificado nesta interação, BLOQUEAR o fluxo e voltar ao gate de pre-commit.

> Se os testes falharam, **não** apresentar as 4 opções. Reportar falhas e parar até serem corrigidas.

### Step 2 — Branch destino (por tipo)

| Tipo de branch | Destino |
|---|---|
| `feature/*` / `bugfix/*` | `develop` |
| `hotfix/*` | `main` + `develop` |
| `release/*` | `main` + `develop` |

### Step 3 — Apresentar 4 opções (texto exato)

```
Implementação concluída. O que fazer?

1. Merge local em <destino> (git flow finish --no-ff)
2. Push e criar Pull Request
3. Manter a branch como está (cuido depois)
4. Descartar este trabalho

Qual opção?
```

Sem explicação extra. **Sempre perguntar** — nunca executar merge/push automaticamente.

### Step 4 — Executar escolha

#### Opção 1 — Merge local

1. Review do diff da branch contra o destino (mostrar ao dev antes de mergear)
2. Executar:
   ```bash
   git flow <tipo> finish --no-ff <nome>
   ```
   `--no-ff` é **sempre inline**. Preserva a bolha de merge mesmo em fast-forward.
3. Branch local é deletada automaticamente pelo `git flow finish` (passar `--keep` se quiser preservar)
4. Para `hotfix/release` com tag: nome da branch vira nome da tag por default; usar `--tagname <tag>` para customizar

#### Opção 2 — Push + PR

```bash
git push -u origin <feature-branch>

gh pr create --title "<title>" --body "$(cat <<'EOF'
## Sumário
- <bullet do que mudou>
- <bullet do que mudou>

## Test Plan
- [ ] <passo de verificação>
- [ ] <passo de verificação>

Refs: [FEAT]-XX (se aplicável)
EOF
)"
```

A branch fica viva para iterações do PR — **não** deletar.

#### Opção 3 — Manter

Reportar: `Mantendo branch <nome>. Sem ação de merge/push.` Fim.

#### Opção 4 — Descartar

**Exigir confirmação tipada antes de qualquer ação destrutiva:**

```
Isto vai apagar PERMANENTEMENTE:
- Branch <nome>
- Commits: <lista de SHAs>

Digite 'discard' para confirmar.
```

Esperar a string exata `discard`. Qualquer outra resposta cancela a operação.

Se confirmado:
```bash
git checkout <destino>
git branch -D <feature-branch>
```

### Quick Reference

| Opção | Merge | Push | Keep branch | Delete branch |
|---|---|---|---|---|
| 1. Merge local | ✅ via `git flow finish --no-ff` | — | — | ✅ automático |
| 2. Push + PR | — | ✅ | ✅ (para iterar PR) | — |
| 3. Manter | — | — | ✅ | — |
| 4. Descartar | — | — | — | ✅ force (após `discard` tipado) |

### Red Flags

- Apresentar opções **sem** ter verificado testes nesta mensagem (Iron Law)
- Pular `--no-ff` no `git flow finish` (perde bolha de merge)
- Fazer merge ou push **automaticamente** sem perguntar ao dev
- Descartar branch sem confirmação tipada `discard`
- Deletar a branch antes do merge ter sido confirmado bem-sucedido
- `git push --force` em branch protegida sem pedido explícito do dev
- Fazer perguntas open-ended ("o que fazer agora?") em vez das 4 opções estruturadas

### Common Mistakes

| Erro | Correção |
|---|---|
| Pular verificação de testes antes das opções | Iron Law primeiro, sempre |
| Aceitar `Discard` / `DESCARTAR` / variações | Exigir a string exata `discard` (lowercase) |
| Esquecer `--no-ff` em fast-forward merge | Sempre passar inline |
| Cleanup de branch antes do merge concluído | Merge primeiro, depois delete |
| Criar PR sem test plan no body | Template tem `## Test Plan` obrigatório |

---

## Pós-Commit: Atualizar STATE.md

Atualizar `.specs/project/STATE.md` com o registro da task (ver `state-management.md` no orquestrador).

Se usando `tasks.md`, marcar a task como completa e atualizar rastreabilidade em `spec.md`.

---

## Integração com nano-spec

| Fase do orquestrador | Comportamento desta skill |
|---------------------|--------------------------|
| **Pré-specify** | `git pull` se em branch protegida |
| **Pré-execute** | `git checkout <base> && git pull --ff-only && git flow <tipo> start` — base atualizada via pull explícito |
| **Commit** | Esta skill é invocada — gates + commit + fechamento |
| **Pós-commit** | Fechamento estruturado (4 opções: merge/PR/manter/discard) — ver seção "Pós-Commit: Fechamento de Branch" desta skill |

Quando invocada **diretamente** (sem o orquestrador `nano-spec` rodando — ex: dev pediu "commitar" sem ter entrado no fluxo de spec), aplicar o fluxo completo do HARD BLOCK ao fechamento de branch.

---

## Referência Avançada

Para cenários complexos (conflitos no finish, configuração avançada, hooks, filters), consultar Context7: `/gittower/git-flow-next`.

---

## Quando NÃO aplicar

- Projeto solo sem releases formais → trunk-based pode ser melhor
- CLAUDE.md explicitamente desativa gitflow
- Dev pede para ignorar → respeitar sem insistir
- Hotfix urgente onde o dev decide commitar direto na main

