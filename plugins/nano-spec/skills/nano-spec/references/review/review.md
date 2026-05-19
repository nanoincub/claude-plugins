# Review (opt-in)

**Desativado por padrão.** Ativar via defaults opt-out no início da feature ou quando o dev pedir explicitamente.

**Goal**: Garantir que o código está correto, limpo e eficiente.

**Nota:** A qualidade de código é garantida por /simplify (obrigatório) + verificação executável por task. Esta fase adicional é recomendada para projetos críticos ou quando o dev preferir uma camada extra de revisão.

## Sinais de Review (baseados no diff)

O agente avalia o diff real após cada ajuste. Se ALGUM sinal é detectado, avisa o dev.

| # | Sinal | Descrição |
|---|-------|-----------|
| R1 | Lógica condicional/loops | Conditionals, loops, switch, ternários com lógica de negócio |
| R2 | Mutação de estado | State, variáveis de instância, stores, databases |
| R3 | Chamadas de API | Fetch, axios, HTTP calls, query builders |
| R4 | Controle de fluxo | Routing, middleware, error handling, redirects, guards |
| R5 | Estrutura de dados | Models, schemas, migrations, interfaces de API, DTOs |
| R6 | Mudança estrutural | Reorganização de módulos, imports, dependências entre arquivos |
| R7 | Volume com lógica | >5 arquivos com código (não docs/config) |
| R8 | Testes | Testes novos ou modificados |

**Sinais servem para perguntas antecipadas** — quando review está ativado, se detectados durante ajustes, o agente pergunta se quer rodar review agora.

## Fluxo Confirmativo

1. Após cada ajuste, o agente avalia o diff contra os sinais R1-R8
2. Se sinal detectado → avisar o dev: "Detectei [sinal]. Quer rodar review agora ou deixar pro commit?"
3. Se dev diz "agora" → rodar /review imediatamente
4. Se dev diz "depois" → anotar sinal como pendente
5. Antes do commit → rodar /review sobre diff acumulado (se review ativado)

**Regra:** Não interromper para todo sinal trivial. Agrupar sinais relacionados e avisar uma vez.
**Escape hatch:** Na dúvida entre rodar ou skipar → RODAR.

---

## Fluxo

**Ordem pre-commit canônica (sempre):** `/simplify` → suite completa de testes (Iron Law) → commit.

**Quando Review e/ou Code reviewer subagent estão ativados** (opt-in via defaults ou pedido do dev), eles entram **antes** do `/simplify` — corrigir bugs/lógica antes do refactor evita re-trabalho no simplify.

```
Execute concluído
    │
    ▼
[OPT-IN] /review (bugs, lógica, edge cases)   ← skill built-in do Claude Code
    │
    ├── Critical/Important → Corrigir → /review novamente (max 3x)
    ├── Suggestions → Registrar em STATE.md → Continuar
    └── Limpo → Continuar
    │
    ▼
[OPT-IN, Large/Complex] Code reviewer subagent
    └── Despachar via code-review.md (template em code-reviewer-prompt.md) com BASE_SHA e HEAD_SHA
    └── Para pre-commit Large/Complex: usar Protocolo Dois-Eixos (mais abaixo) NO LUGAR deste step
    │
    ▼
1. /simplify (reuse, quality, efficiency)   ← OBRIGATÓRIO
    │
    ├── Issues → Corrigir → /simplify novamente (max 3x)
    └── Limpo → Avançar
    │
    ▼
2. Suite completa de testes + Iron Law verification   ← OBRIGATÓRIO
    └── Aplicar nano-disciplines:verification
        └── Evidência FRESH antes de qualquer claim de "pronto"
        └── Testes DEVEM passar — Iron Law bloqueia commit se falharem
    │
    ▼
Commit (skill nano-commit aplica gates próprios)
```

**Por que essa ordem:** `/simplify` antes dos testes valida que o refactor não introduziu regressões (testes correm sobre o diff já simplificado). Inverter (testes → simplify) deixa janela para regressões silenciosas — o simplify altera código e ninguém valida depois.

---

## Como invocar

O `/review` e `/simplify` são skills nativas do Claude Code (não são MCPs externos).
Para executá-los, o agente deve usar o **Skill tool**:

```
Skill tool: skill: "simplify"
```

Se `/review` não estiver disponível como skill, o agente DEVE fazer a revisão manualmente:
1. Ler todos os arquivos modificados
2. Analisar contra os critérios abaixo
3. Reportar findings no mesmo formato

**Nunca pular esta fase por não encontrar o comando.** A revisão manual é o fallback.

---

## Processo

### 1. Executar `/review` (ou revisão manual)

Analisa bugs, edge cases, convenções, performance, testes.

| Severidade | Ação |
|------------|------|
| **Critical/Important** | Corrigir. Re-executar `/review`. |
| **Suggestion** | Registrar em STATE.md (Deferred Ideas). Continuar. |
| **Limpo** | Avançar para `/simplify`. |

### 2. Executar `/simplify`

Analisa reuse, quality, efficiency em paralelo.

- Issues → Corrigir → Re-executar `/simplify`
- Limpo → Avançar para Security

### 3. Verificação Formal (obrigatório)

**Iron Law: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"**

O agente DEVE aplicar a [Gate Function da Iron Law](nano-disciplines:verification#gate-function-5-passos-obrigatórios). Resumo dos 5 passos:

1. **IDENTIFY** — Que comando prova o claim?
2. **RUN** — Executar o comando FULL, fresh, **nesta mensagem**
3. **READ** — Output completo, exit code, contar falhas
4. **VERIFY** — Output confirma o claim?
5. **ONLY THEN** — Fazer a claim COM evidência

Ver [verification.md](nano-disciplines:verification) para a referência completa: tabela de Common Failures, Red Flags de linguagem, prevenção de racionalizações, e patterns por tipo de claim (tests / regression / build / requirements / agent delegation).

**Red flags que PARAM o agente** (resumo — ver lista completa em [verification.md > Red Flags](nano-disciplines:verification#red-flags--palavras-proibidas-até-verificar)):
- Usar "should", "probably", "seems to" em claims de completude
- Expressar satisfação antes de verificar ("Great!", "Done!", "Pronto!")
- Referenciar output de execuções anteriores como prova

### 3.1. Code Review por Subagente (obrigatório para Large/Complex)

Quando escopo é Large/Complex, o agente DEVE despachar um subagent code-reviewer fresh que avalia o código sem contexto da sessão, trazendo perspectiva independente. Template em [code-reviewer-prompt.md](nano-disciplines:skills/code-review/references/code-reviewer-prompt.md), guia operacional em [code-review.md](nano-disciplines:code-review).

**Para pre-commit Large/Complex:** usar o **Protocolo Dois-Eixos** mais abaixo NO LUGAR deste step. Os dois eixos especializados (Standards + Spec) cobrem o mesmo terreno com mais rigor.

Parâmetros obrigatórios:
- **BASE_SHA** — commit base antes das mudanças
- **HEAD_SHA** — commit head com as mudanças

O reviewer analisa o diff isoladamente, sem acesso ao histórico de conversa — isso garante avaliação imparcial. O agente principal DEVE verificar os achados do reviewer conforme seção 4 abaixo.

### 4. Verificação de achados de subagentes

> **Regra de ouro:** Se o agente principal não fez `Read` da linha de código citada, o achado **NÃO** entra no relatório. Nenhuma exceção.

Quando subagentes (Agent tool) ou skills externas retornam findings de review, o agente principal **DEVE** verificar cada um antes de reportar ou corrigir:

- [ ] `Read` do arquivo e linha exata — o código existe como descrito?
- [ ] `git diff` — o issue foi introduzido nesta branch ou é pré-existente?
- [ ] Contexto de framework — o framework já mitiga? (escape de templates, CSRF automático, ORM com prepared statements)
- [ ] Contexto de domínio — é decisão intencional? Na dúvida, perguntar ao dev

**Prompts para subagentes de review** devem instruir: "Retorne conteúdo de arquivos e observações factuais. NÃO classifique severidade nem recomende correções."

**Gate de aprovação:** Após verificação, apresentar achados verificados ao dev com evidência (arquivo, linha, código real, motivo). O dev é o juiz final — decide se o achado é realmente um issue e como corrigir. O agente **NÃO** implementa correções sem aprovação.

**Separação no relatório:**
- **Issues introduzidos pela branch** — escopo do review, ação requerida
- **Observações pré-existentes** (opcional) — seção separada, fora do escopo da branch

Ver [agent-behavior.md](../meta/agent-behavior.md) para regras gerais de confiabilidade e padrões de falso positivo.

### 5. Recepção de Feedback

**Triggers automáticos** — aplicar [receiving-feedback.md](nano-disciplines:skills/code-review/references/receiving-feedback.md) sempre que UM dos eventos abaixo ocorrer:

| Evento | Trigger |
|---|---|
| Subagent revisor retornou (spec-reviewer, code-quality-reviewer, code-reviewer geral, plan-document-reviewer, spec-document-reviewer) | Antes de tocar em qualquer fix sugerido |
| Dev dá feedback inline na sessão sobre código que você acabou de escrever | Antes de aplicar a mudança pedida |
| Comentário em PR no GitHub respondido por você | Antes de redigir a resposta ou aplicar fix |
| Protocolo Dois-Eixos retornou achados (Standards/Spec) | Antes de endereçar |

**Protocolo de 6 passos:** READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT.

**Não-negociáveis:**
- NUNCA implementar feedback cegamente — verificar tecnicamente primeiro
- Push back com raciocínio técnico se o feedback estiver errado
- Zero performative agreement ("você está totalmente certo!", "great point!", "thanks for catching that!")
- Itens unclear → STOP, perguntar antes de implementar QUALQUER item

Se você se pegar prestes a escrever "Thanks" ou variação: apague. Estado a correção em vez disso.

---

## Protocolo Dois-Eixos (Large/Complex pré-commit)

Code review pré-commit particionado em dois subagents paralelos (Standards + Spec). **Substitui** o code reviewer geral da seção 3.1 em features Large/Complex.

**Doc dedicado:** [dois-eixos.md](dois-eixos.md) — princípio, quando ativar, fluxo completo, prompts dos 2 agents, formato de relatório, como reconciliar discordâncias.

**Resumo:**

| Eixo | O que verifica | Fonte |
|---|---|---|
| **Standards** | Código segue convenções do repo? | `.specs/codebase/CONVENTIONS.md`, `CLAUDE.md` |
| **Spec** | Código implementa fielmente o que foi pedido? | `spec.md` (acceptance criteria + `[FEAT]-XX`), `tasks.md` |

Quando ativar: **Complex** sempre, **Large** default, Medium/Small/Quick skip (usar [code-review.md](nano-disciplines:code-review) se o dev pedir review).

---

## Limites

| Tool | Max re-runs | Após limite |
|------|-------------|-------------|
| /review | 3 | Escalar para dev com lista de issues |
| /simplify | 3 | Escalar para dev |

---

## Quick Mode

No Quick Mode (≤3 files): /review só executa quando ativado e dev confirma. /simplify continua obrigatório (conforme quick-mode.md).

---

## Feature-Level Validation & UAT (opcional)

**Quando rodar:** após todas as tasks de uma feature (ou priority group) concluídas, antes de declarar a feature "pronta". É a verificação macro que complementa as verificações por-task feitas durante Execute.

**Interactive UAT é disparado quando:** a feature tem comportamento complexo voltado ao usuário onde julgamento humano importa (fluxos de UI, padrões de interação, design visual). Para trabalho backend-only ou infraestrutura, checks automatizados bastam.

**Triggers de validação explícita:** "validate", "verify work", "UAT", "test with me", "walk me through it".

### 1. Check Completed Tasks

Percorrer `tasks.md`:

- [ ] Todas as tasks marcadas como done?
- [ ] Alguma blocked ou partial?

### 2. Verify Acceptance Criteria

Para cada user story em `spec.md`:

```markdown
### P1: [Story Title]

**Acceptance Criteria**:

1. WHEN [X] THEN [Y] → [PASS/FAIL]
2. WHEN [X] THEN [Y] → [PASS/FAIL]
```

### 3. Run Build-Level Gate Check (OBRIGATÓRIO)

Rodar o gate check de nível Build do `TESTING.md`. NÃO é opcional.

Se `TESTING.md` não existir (greenfield), usar o comando de gate combinado com o dev na fase Tasks.

1. Rodar: `[comando build gate do TESTING.md, ou o comando combinado no planejamento]`
2. Exit code não-zero = STOP. Não prosseguir para Code Quality Check.
3. Registrar resultados:
   - Total test count: [N]
   - Passed: [N]
   - Failed: [lista]
   - Skipped: [lista — cada skip precisa ser justificado]

**Test Integrity Check:**

- Comparar test count atual contra o count antes da feature ser implementada
- Se test count DIMINUIU: investigar por quê. Testes só devem ser deletados com justificativa explícita.
- Se assertions foram enfraquecidas (menos específicas que antes): marcar como potencial regressão.

### 4. Interactive UAT (se feature user-facing)

Para cada deliverable testável, apresentar um teste por vez:

```
Test [N]: [Test Name]

Expected: [O que deve acontecer — específico e observável]

→ Funcionou? Descreva o que você vê.
```

Aguardar resposta do dev:

| Dev diz                            | Interpretar como          |
| ---------------------------------- | ------------------------- |
| "sim", "pass", "funciona", "next"  | ✅ Pass                  |
| "skip", "não consigo testar", "n/a"| ⏭️ Skip                  |
| Qualquer outra coisa               | ❌ Issue — registrar verbatim |

**Severity inference (nunca perguntar severidade ao dev):**

| Descrição do dev contém                          | Severidade inferida |
| ------------------------------------------------ | ------------------- |
| crash, error, exception, fails, broken, quebrou  | Blocker             |
| doesn't work, wrong, missing, can't, errado      | Major               |
| slow, weird, off, minor, small, lento            | Minor               |
| color, font, spacing, alignment, visual, cor     | Cosmetic            |
| (não claro)                                      | Major (default)     |

### 5. Generate Fix Plans (se issues encontrados)

Para cada issue encontrado durante UAT:

1. **Diagnose** — analisar o codebase para achar a root cause
2. **Create fix task** — escrever definição de task com:
   - What: o fix específico
   - Where: paths de arquivo
   - Verify: como provar que o fix funciona
   - Done when: critérios de aceitação do fix
3. **Present fix plan** — mostrar todas as fix tasks ao dev para aprovação

Fix tasks seguem o mesmo formato de tasks regulares e podem ser executadas via fase implement.

**Guardrail:** máximo 3 iterações diagnósticas por issue. Se a root cause não for encontrada após 3 tentativas, marcar para investigação humana.

### 6. Validation Report

Template:

```markdown
# [Feature] Validation

**Date**: [YYYY-MM-DD]
**Spec**: `.specs/features/YYYY-MM-DD-[feature]/spec.md`

---

## Task Completion

| Task | Status     | Notes   |
| ---- | ---------- | ------- |
| T1   | ✅ Done    | -       |

## User Story Validation

### P1: [Story Title]

| Criterion     | Result  |
| ------------- | ------- |
| WHEN X THEN Y | ✅ PASS |

**Status**: ✅ P1 Complete

## Interactive UAT Results (se realizado)

| #   | Test        | Result   | Details                                              |
| --- | ----------- | -------- | ---------------------------------------------------- |
| 1   | [Test name] | ✅ Pass  | -                                                    |
| 2   | [Test name] | ❌ Issue | [resposta verbatim do dev] — Severidade: [inferida] |

## Tests

- **Gate command**: [comando completo]
- **Result**: [X] passed, [Y] failed, [Z] skipped
- **Test count antes da feature**: [N]
- **Test count depois da feature**: [M]
- **Delta**: [+(M - N) novos tests]
- **Skipped tests**: [lista com justificativa para cada]
- **Failures**: [lista com detalhes]

## Fix Plans (se issues encontrados)

### Fix 1: [Descrição do issue]

- **Root cause**: [o que está realmente errado]
- **Fix task**: [definição de task]
- **Priority**: [Blocker/Major/Minor/Cosmetic]

## Requirement Traceability Update

Atualizar status dos requisitos em `spec.md`:

| Requirement | Previous Status | New Status   |
| ----------- | --------------- | ------------ |
| [FEAT]-01   | Implementing    | ✅ Verified  |
| [FEAT]-02   | Implementing    | ❌ Needs Fix |

## Summary

**Overall**: ✅ Ready | ⚠️ Issues | ❌ Not Ready

**What works**: [lista]
**Issues found**: [Issue 1: como corrigir]
**Next steps**: [ação]
```

---

## Tips

- Review é opt-in — ativar via defaults ou quando dev pedir
- Foque em Critical/Important primeiro
- Suggestions são para o futuro — anote em STATE.md
- Re-review após correção — correções podem introduzir problemas
