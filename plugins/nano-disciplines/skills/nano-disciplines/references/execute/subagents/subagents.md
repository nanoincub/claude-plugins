# Subagent-Driven Execution

Motor de execução para features **Large** ou **Complex**: o controller (sessão principal) despacha 3 subagents por task — implementer, spec-reviewer, code-quality-reviewer — em vez de implementar inline.

> **Princípio:** o subagent **nunca** herda o histórico da sua sessão. Você constrói **exatamente** o contexto que ele precisa. Isolamento é o motivo dele existir.

Esta referência opera junto com [implement.md](../implement.md) (loop principal) e os 3 prompts ao lado.

---

## Quando usar

- Feature classificada como **Large** ou **Complex** no auto-sizing
- Tasks em `tasks.md` razoavelmente independentes (não tightly coupled)
- Você quer ficar na mesma sessão (sem handoff para parallel session)

**Não usar para:**
- Small/Medium — overhead de 3 dispatches por task não compensa
- Tasks com fortes dependências sequenciais entre código adjacente
- Quick fixes / bug fixes simples — usar fluxo inline de [implement.md](../implement.md)

---

## Fluxo (ordem é obrigatória)

```
1. Ler tasks.md uma vez, extrair TODAS as tasks com texto completo + contexto
2. Criar TodoWrite com todas as tasks

PARA CADA TASK:
   ┌─────────────────────────────────────────────────────┐
   │ Dispatch implementer (implementer-prompt.md)        │
   │   ↓                                                  │
   │ Implementer pergunta? → você responde, redespacha   │
   │   ↓                                                  │
   │ Implementer reporta DONE / DONE_WITH_CONCERNS /      │
   │   NEEDS_CONTEXT / BLOCKED                            │
   │   ↓                                                  │
   │ Dispatch spec reviewer (spec-reviewer-prompt.md)    │
   │   ↓                                                  │
   │ Spec ✅? → não: implementer corrige → re-review     │
   │   ↓ (só passa se ✅)                                 │
   │ Dispatch code quality reviewer                       │
   │   (code-quality-reviewer-prompt.md)                  │
   │   ↓                                                  │
   │ Quality ✅? → não: implementer corrige → re-review  │
   │   ↓                                                  │
   │ Marcar task complete no TodoWrite                    │
   └─────────────────────────────────────────────────────┘

APÓS TODAS AS TASKS:
   Dispatch final code reviewer para revisão da implementação inteira
   → seguir para fluxo de commit ([commit](nano-spec:commit/commit.md))
```

**Spec compliance ANTES de code quality. Sem exceção.**

Motivo: se o implementer construiu o errado ou deixou requisito de fora, revisar qualidade é desperdício — o código vai mudar de qualquer forma.

---

## Continuous Execution

**Não pause entre tasks para "should I continue?".** O dev pediu para executar o plano — execute. Os únicos motivos legítimos de parar:

- Status `BLOCKED` que você não consegue resolver
- Ambiguidade real que impede progresso
- Todas as tasks concluídas

Prompts de check-in e resumos de progresso entre tasks **desperdiçam o tempo do dev**.

---

## Model Selection

Use o modelo **menos potente** capaz de executar cada papel. Conserva custo e ganha velocidade.

| Tipo de task | Modelo |
|---|---|
| Mecânica: 1-2 arquivos, spec clara, função isolada | Mais barato/rápido (Haiku) |
| Integração: múltiplos arquivos, pattern matching, debugging | Standard (Sonnet) |
| Arquitetura, design, review de implementação completa | Mais capaz (Opus) |

Sinais de complexidade da task:
- 1-2 arquivos + spec completa → cheap
- Múltiplos arquivos + integração → standard
- Decisão de design ou entendimento amplo do codebase → mais capaz

A escolha é **por task**, não por sessão.

---

## Status do implementer — como reagir

O implementer reporta um de 4 estados. Cada um exige tratamento específico:

### `DONE`
Prosseguir para spec compliance review.

### `DONE_WITH_CONCERNS`
Completou o trabalho mas levantou dúvidas. Leia os concerns **antes** de prosseguir:
- Se sobre **correctness/scope** → endereçar antes de qualquer review
- Se **observação** (ex: "este arquivo está ficando grande") → registrar, seguir para review

### `NEEDS_CONTEXT`
Precisa de informação que não foi fornecida. Forneça o contexto faltante e re-despache (mesmo modelo).

### `BLOCKED`
Não consegue completar. Diagnostique:
1. **Problema de contexto** → forneça mais contexto, re-despache com mesmo modelo
2. **Precisa de mais raciocínio** → re-despache com modelo mais capaz
3. **Task grande demais** → quebrar em pedaços menores
4. **Plano está errado** → escalar para o dev

**Nunca** ignore um `BLOCKED` ou force o mesmo modelo a re-tentar sem mudar nada. Se o implementer disse que travou, algo precisa mudar.

---

## Os 3 prompts (templates)

| Prompt | Papel | Características-chave |
|---|---|---|
| [implementer-prompt.md](implementer-prompt.md) | Worker que faz a task | "Ask now" antes de começar · self-review em 4 dimensões · report estruturado com 4 status |
| [spec-reviewer-prompt.md](spec-reviewer-prompt.md) | Revisor: "construiu o que pediu?" | **"DO NOT TRUST THE REPORT"** — lê o código direto · procura missing / extra / misunderstandings |
| [code-quality-reviewer-prompt.md](code-quality-reviewer-prompt.md) | Revisor: "construiu **bem**?" | Wrapper sobre `code-reviewer-prompt.md` (review/) com checks adicionais de file responsibility |

**Como dispatch:** use `Agent tool` com `subagent_type: general-purpose` (ou outro se cabível), passando o texto completo do prompt + a task + contexto + (para reviewers) BASE_SHA/HEAD_SHA.

**Nunca** faça o subagent ler `tasks.md` ou outros arquivos do projeto para extrair sua própria task. Você (controller) já leu uma vez — passe o texto completo no prompt.

---

## Integração com nano-spec

| Hook nano-spec | Como aplicar |
|---|---|
| Naming por ID de requisito | Implementer DEVE nomear testes com `test_FEAT01_...`; spec reviewer DEVE verificar cobertura QUANDO/ENTÃO da spec.md |
| `.specs/features/[feature]/` | Contexto passado aos subagents inclui paths para spec.md, design.md, tasks.md, context.md (se existirem) |
| TDD interno | Implementer segue [tdd.md](../tdd/tdd.md) — Iron Law continua valendo dentro do subagent |
| Debug interno | Bug encontrado pelo implementer → seguir [debug.md](../systematic-debugging/debug.md), não chutar |
| Commit | Pós-tudo, o controller invoca skill [`nano-commit`](../nano-spec:nano-commit:SKILL.md) — não o subagent |

---

## Red Flags — STOP

Catálogo de erros operacionais. Se você se pegar fazendo qualquer um, pare:

- Começar implementação em `main`/`master`/`develop` sem consentimento explícito do dev
- Pular review (spec OU code quality)
- Avançar com issues não resolvidos
- Despachar múltiplos implementer subagents **em paralelo** (causa conflitos no working tree)
- Pedir para o subagent **ler** o `tasks.md` em vez de passar o texto completo
- Pular o scene-setting (subagent precisa entender onde a task se encaixa)
- Ignorar perguntas do subagent (responda antes de deixar prosseguir)
- Aceitar "close enough" no spec compliance (reviewer achou issues = não está pronto)
- Pular re-review depois de fixes
- Deixar o self-review do implementer substituir review real (precisa dos dois)
- **Começar code quality review antes de spec compliance estar ✅** (ordem errada)
- Avançar para a próxima task com review em aberto
- Tentar corrigir manualmente issues que o subagent não conseguiu (poluição de contexto — despache um fix subagent)

---

## Vantagens vs execução manual / inline

- Subagents seguem TDD naturalmente (prompt impõe)
- Contexto fresco por task — sem confusão entre tasks
- Subagent pode fazer perguntas **antes** de começar (não só depois de falhar)
- Self-review interno + 2 reviews externos catam issues cedo
- O controller (você) preserva contexto para coordenação
- Spec compliance impede over/under-build
- Code quality garante que o que foi construído é manutenível

**Custo:** mais dispatches (1 implementer + 2 reviewers por task), prep upfront para extrair tasks. Compensa porque issues são pegos cedo (mais barato que debugar depois).

---

## Quando uma review loop fica infinita

Se reviewer e implementer ficam em ping-pong por 3+ rodadas na mesma task:

1. Re-leia o feedback do reviewer com olhar fresco — está pedindo algo válido?
2. Se o desacordo é técnico real → escalar para o dev
3. Se o reviewer está sendo pedante (recommendations virando blockers) → ignore as "Recommendations" (são advisory) e foque só em "Issues"
4. Se o reviewer está confuso → forneça mais contexto no prompt (ex: paths certos, BASE_SHA correto)

Loop infinito também é um sinal — geralmente significa que a task estava mal especificada no `tasks.md`.
