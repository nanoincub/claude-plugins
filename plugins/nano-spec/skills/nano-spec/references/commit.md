# Commit

**Goal**: Criar commits atômicos, rastreáveis e no formato padronizado.

**Fase final confirmativa** — sempre perguntar ao dev antes de iniciar o fluxo de commit.

---

## Processo

### 0. Validação de branch (gitflow)

Antes de qualquer commit, verificar a branch atual conforme [gitflow.md](gitflow.md). Se em branch protegida, sugerir criação de feature/hotfix branch. Sugestão, não bloqueio — dev tem a palavra final.

### 1. Perguntar ao dev

Após concluir o Execute (ou série de ajustes), perguntar:

    Implementação concluída. Quer commitar?
      Arquivos modificados: [lista]
      Commit sugerido: <type>(<scope>): <description>

- Se **sim** → Docs → Commit
- Se **não** → fim. Mudanças ficam no working tree. Dev decide quando retomar.

### 2. Gates pré-commit (após confirmação)

- [ ] /simplify passou sobre diff acumulado (obrigatório)
- [ ] Dev rodou suite completa de testes (obrigatório — ver nota abaixo)
- [ ] Docs atualizado — ver [docs-update.md](docs-update.md)
- [ ] Todos os "Done when" da task estão verificados
- [ ] Rastreabilidade verificada (ver nota abaixo)

**Integração ativa com superpowers:** Quando superpowers estiver detectado, invocar `superpowers:verification-before-completion` como gate obrigatório. Os testes DEVEM passar antes de oferecer opções de commit — se falharem, BLOQUEAR o fluxo de commit (não apenas pedir ao dev, mas impedir o avanço até que passem).

**Suite de testes (sem superpowers):** O agente NÃO roda a suite completa — pede ao dev para rodar, informando o comando. Motivo: evitar gasto de tokens desnecessário em output de centenas de testes. O agente fornece o comando e aguarda confirmação do dev.

**Rastreabilidade:** Antes de commitar, verificar que todos os IDs de requisito ([FEAT]-XX) da spec.md mapeados para esta task estão com status "Verified" na tabela de rastreabilidade. Se algum está "Pending" ou "Implementing", ALERTAR o dev com a lista de IDs pendentes e perguntar se deseja prosseguir mesmo assim.

**Nota:** /simplify deve ter rodado após o Execute. Se já rodou e não houve ajustes depois, não rodar novamente.

### 3. Criar commit atômico

Cada task recebe seu próprio commit. Nunca agrupar múltiplas tasks em um commit.

**Formato ([Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)):**

```
<type>(<scope>): <description>

[optional body]

Refs: [FEAT]-XX
```

### 4. Types

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

### 5. Regras da description

- Imperativo: "add", não "added" ou "adds"
- Minúscula no início
- Sem ponto final
- Complete a frase: "If applied, this commit will _[your description]_"

### 6. Scope

Feature name ou área do módulo, lowercase.

**IMPORTANTE:** Se o CLAUDE.md do projeto define scopes válidos, usar APENAS esses scopes.
Se não define, usar o nome da feature ou área do módulo.

Exemplos genéricos: `auth`, `cart`, `api`, `settings`

### 7. Refs (rastreabilidade)

Quando a task tem ID rastreável (ex: AUTH-01), adicionar no footer:

```
feat(auth): add email validation to login form

Refs: AUTH-01
```

Para quick tasks sem ID, omitir o Refs.

### 8. Breaking changes

Append `!` após type/scope E adicionar footer `BREAKING CHANGE:`:

```
feat(api)!: change authentication endpoint response format

BREAKING CHANGE: login endpoint now returns JWT in body instead of cookie

Refs: AUTH-05
```

---

## Exemplos

```
feat(auth): add email validation to login form

Refs: AUTH-01
```

```
fix(cart): prevent negative quantity on item decrement

Refs: CART-03
```

```
refactor(api): extract token refresh logic into service

Move token refresh from inline handler to dedicated AuthTokenService
for reuse across multiple endpoints.

Refs: AUTH-02
```

Quick task (sem Refs):

```
fix(auth): prevent 401 on token refresh
```

---

## Regras

- **Um commit por task** — clean git history, bisect e rollback possíveis
- **Description referencia o que FOI FEITO**, não o que foi planejado
- **Apenas arquivos da task** — nunca incluir mudanças "while I'm here"
- **Testes junto** — se testes são parte da task, incluir no mesmo commit

---

## Após o commit

Atualizar `.specs/project/STATE.md` com o registro da task (ver [state-management.md](state-management.md)).

Se usando tasks.md, marcar a task como completa e atualizar rastreabilidade em spec.md.

---

## Fechamento de Branch (gitflow)

Após commitar, se o trabalho foi feito em uma branch criada pelo gitflow (`feature/*`, `hotfix/*`, `release/*`), verificar se superpowers está disponível.

### Com superpowers (integração ativa)

DEVE invocar `superpowers:finishing-a-development-branch` — verifica testes, apresenta 4 opções (merge/PR/manter/discard), exige confirmação tipada para discard, e cuida do worktree cleanup automaticamente.

### Sem superpowers (fluxo manual)

Quando superpowers NÃO estiver disponível, apresentar as opções manualmente:

```
Commit feito na branch [branch]. Como quer prosseguir?

  1. Merge local (review + git flow finish — recomendado para features médias/grandes)
  2. Criar PR (push + abrir pull request para review externo)
  3. Continuar trabalhando nesta branch (mais commits pendentes)
  4. Discard (descartar branch — requer confirmação: digitar "discard")
```

**Branch destino** conforme [gitflow.md](gitflow.md):
- `feature/*` → `develop`
- `hotfix/*` → `main` + `develop`
- `release/*` → `main` + `develop`

**Regras:**
- Sempre perguntar — nunca fazer merge ou push automaticamente
- **Opção 1:** rodar review do diff da branch contra a branch destino, depois `git flow finish`. Recomendado para features médias/grandes
- **Opção 2:** push da branch e criar pull request via `gh pr create`
- **Opção 4:** exigir que o dev digite "discard" para confirmar — protege contra descarte acidental
- Se houver mais tasks pendentes na mesma feature, opção 3 é a natural
- Se git worktree foi usado, informar o dev para fazer cleanup manual do worktree após merge ou discard

### Alerta de desvio de escopo

Ao commitar, o agente DEVE verificar se o trabalho é coerente com o propósito da branch atual. Se detectar desvio, alertar:

```
⚠️ Você está na branch feature/login, mas este commit toca [área diferente].
Isso deveria estar em uma branch separada?

  → Criar nova branch para este trabalho (recomendado)
  → Commitar aqui mesmo (minha branch, minha decisão)
```

**Sinais de desvio:**
- Commit com scope diferente do scope da branch (ex: branch `feature/login`, commit toca `sms` ou `infra`)
- Arquivos modificados fora do domínio da feature (ex: branch de feature tocando configs de deploy)
- Tipo de trabalho incompatível (ex: branch `feature/*` com trabalho de `hotfix`)

**Regras:**
- Alertar uma vez por desvio detectado — não insistir se o dev optar por continuar
- Se o dev pedir para criar nova branch, stashar mudanças atuais, criar a branch correta, e aplicar

---

## Tips

- **Commit é a última fase** — se chegou aqui, o código já passou por /simplify e dev confirmou testes
- **Mensagem conta a história** — quem ler o git log deve entender o que e por que
- **Atomic = reversível** — cada commit pode ser revertido independentemente
