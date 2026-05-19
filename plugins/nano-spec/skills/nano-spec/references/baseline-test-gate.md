# Baseline Test Gate

Gate obrigatório que roda **antes** de criar qualquer branch de trabalho (`feature/*`, `bugfix/*`, `hotfix/*`, `release/*`). Garante que a base está verde — assim falhas pré-existentes não viram bloqueio seu no commit final.

## Quando dispara

Em TODOS os modos (Full, Medium, Quick), logo após o `git pull` da base e **antes** de `git flow <tipo> start`.

Mapa base → tipo de trabalho:

| Tipo de trabalho | Branch base |
|------------------|-------------|
| feature/bugfix   | `develop`   |
| hotfix           | `main`      |
| release          | `develop`   |

Se CLAUDE.md define modelo de branching diferente (trunk-based, etc.) → adaptar a base; o gate continua valendo sobre a base configurada.

## Fluxo

```
1. git checkout <base> && git pull --ff-only
2. Rodar suite completa de testes (comando do CLAUDE.md ou inferido da stack)
3. Avaliar resultado:
   - Verde → seguir para criação da branch de trabalho
   - Vermelho → exibir alerta + 2 opções
```

## Comando de teste

Vem, em ordem:

1. CLAUDE.md → seção de comandos de teste
2. `.specs/codebase/TESTING.md` → comando padrão
3. Inferência da stack (ex: `npm test`, `php artisan test`, `pytest`, `go test ./...`)
4. Se nada inferível → PERGUNTAR ao dev: "Qual o comando para rodar a suite completa nesta base?"

Agente NÃO roda os testes diretamente — pede ao dev e aguarda confirmação do resultado. Motivo: evita gasto de tokens em output de centenas de testes. [verification.md](nano-disciplines:verification) (Iron Law) valida a confirmação.

## Resultado VERMELHO — alerta padrão

Exibir EXATAMENTE este alerta (ou equivalente no idioma do projeto):

```
⚠️  BASELINE QUEBRADA — atenção máxima

A base `<branch>` tem testes falhando ANTES da sua feature começar.

Falhas relatadas:
  - <test_id_1>
  - <test_id_2>
  ...

Esses testes NÃO são responsabilidade desta feature, mas o gate
pré-commit final exige suite completamente verde. Se você seguir,
vai precisar lidar com essas falhas ANTES de fechar a branch
(corrigir, ou rebasar quando alguém corrigir na base).

Opções:

  [1] PARAR — corrigir a baseline primeiro (FORTEMENTE RECOMENDADO)
      → Identifique quem introduziu as falhas (git blame nos testes)
      → Avise a pessoa — geralmente quem fez tem domínio e conserta rápido
      → Depois retome esta feature

  [2] OVERRIDE — seguir mesmo assim, registrando em STATE.md
      → Use APENAS se: (a) sabe que outra pessoa vai consertar,
        (b) o conserto é independente do seu trabalho, ou
        (c) você mesmo vai consertar como parte deste trabalho
      → Aviso: o gate pré-commit final VAI cobrar suite verde.
        Override aqui não dispensa o gate lá.

Qual opção? [1/2]
```

## Override — registro obrigatório em STATE.md

Se dev escolhe [2], registrar em `.specs/project/STATE.md` (criar a seção se não existir) **antes** de criar a branch de trabalho:

```markdown
## Baseline overrides ativos

### <YYYY-MM-DD> — feature `<nome-da-feature>` iniciada com baseline vermelha

- **Base:** `<branch>` no commit `<sha-curto>`
- **Testes falhando no momento do start:**
  - `<test_id_1>`
  - `<test_id_2>`
- **Responsável pelo conserto:** <nome ou "a definir">
- **Plano:** <"aguardar conserto na base" | "vou consertar nesta feature" | "rebasar quando consertado">
- **Risco aceito:** o gate pré-commit final vai exigir suite verde
```

Regras do registro:
- **Snapshot fiel** — copiar a lista exata de testes falhando, não resumir
- **SHA curto da base** — para rastrear se a base mudou desde
- **Responsável** — sempre tentar preencher; se desconhecido, "a definir" e prosseguir
- **Não apagar overrides após resolver** — mover para seção `## Baseline overrides resolvidos` com data de resolução

## Lembretes em sessões subsequentes

Ao detectar override ativo no STATE.md, agente DEVE alertar UMA VEZ por sessão no início do trabalho:

```
ℹ️  Esta feature foi iniciada com baseline vermelha em <data>.
    Testes ainda relevantes: <lista atualizada via re-run mental ou re-execução>
    Responsável: <nome>
    O gate pré-commit final vai cobrar suite verde.
```

## Pré-commit final — interação com este gate

No gate pré-commit (em `nano-commit`):

1. Suite completa precisa estar verde — sem exceção.
2. Se override ativo no STATE.md:
   - Verificar se as falhas originais foram resolvidas (base atualizada + rebase ou merge).
   - Se SIM → atualizar STATE.md movendo override para "resolvidos".
   - Se NÃO → BLOQUEAR commit, exibir: "Override foi aceito no início, mas a baseline ainda está vermelha. Resolva antes de fechar a branch."

## Casos especiais

### CLAUDE.md desativa testes automatizados

Se o projeto declara explicitamente que não tem suite ou que testes são manuais → **gate vira soft**: avisar uma vez por sessão e seguir. Registrar em STATE.md a primeira vez.

### Suite muito lenta

Se dev declara no CLAUDE.md `Suite lenta — rodar apenas em pré-commit` → o gate ainda dispara, mas aceita a confirmação do dev como evidência. Override mais frequente é esperado neste caso.

### Falha intermitente (flaky)

Não tratar como verde. Pedir ao dev re-rodar; se permanece falhando → tratar como vermelha. Flaky tests viram entry em CONCERNS.md, não escape do gate.

## Por que esse gate existe

Sem ele, o ciclo é:
1. Dev começa feature em base potencialmente vermelha (não sabe)
2. Implementa, refatora, /simplify
3. Gate pré-commit final: suite vermelha
4. Dev descobre que falhas não são dele
5. Bloqueio: ou corrige falha alheia (sem domínio, lento), ou abandona PR, ou espera

Com ele:
- Falha é descoberta antes do trabalho começar
- Devolve para quem tem domínio
- Override consciente vira rastro auditável em STATE.md
