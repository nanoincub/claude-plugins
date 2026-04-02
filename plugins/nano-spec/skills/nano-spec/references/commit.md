# Commit

**Goal**: Criar commits atômicos, rastreáveis e no formato padronizado.

**Fase final confirmativa** — sempre perguntar ao dev antes de iniciar o fluxo de commit.

---

## Processo

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

**Suite de testes:** O agente NÃO roda a suite completa — pede ao dev para rodar, informando o comando. Motivo: evitar gasto de tokens desnecessário em output de centenas de testes. O agente fornece o comando e aguarda confirmação do dev.

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

## Se git worktree foi usado

Quando `superpowers:using-git-worktrees` foi usado no Execute, após commitar invocar
`superpowers:finishing-a-development-branch` que apresenta 4 opções:

1. Merge local para branch base
2. Push + criar PR
3. Manter branch como está
4. Descartar trabalho

Se worktree NÃO foi usado → apenas commit (e push se dev solicitar).

---

## Tips

- **Commit é a última fase** — se chegou aqui, o código já passou por /simplify e dev confirmou testes
- **Mensagem conta a história** — quem ler o git log deve entender o que e por que
- **Atomic = reversível** — cada commit pode ser revertido independentemente
