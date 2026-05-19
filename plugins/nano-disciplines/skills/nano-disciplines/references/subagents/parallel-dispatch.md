# Parallel Dispatch

Padrão de dispatch para **2+ problemas independentes** — um subagent por domínio, rodando simultaneamente. Variante "fan-out" do dispatch single descrito em [subagents.md](subagents.md).

> **Princípio:** 1 agent por problema independente. Trabalham em paralelo. Você (controller) integra os resultados.

Usado pelo Protocolo Dois-Eixos (Standards + Spec) em [review.md](../nano-spec:review/review.md) e por sessões de debug com múltiplas falhas em domínios separados.

---

## Decisão: paralelo vs sequencial vs single agent

```
Tem 2+ problemas?
  ↓ sim
São independentes? (fix em A não muda entendimento de B)
  ├─ não, relacionados      → 1 agent investiga TODOS
  ├─ sim, mas shared state  → agents SEQUENCIAIS
  └─ sim, sem shared state  → DISPATCH PARALELO
```

**Critério-chave de independência:**

- Editariam **arquivos diferentes**?
- Cada um pode ser **entendido sem o contexto do outro**?
- Conserto de A **não muda** o que precisa ser feito em B?

Se qualquer resposta é "não" → não paralelize.

---

## Use when

- 3+ test files falhando com **root causes diferentes**
- Múltiplos subsistemas quebrados **independentemente**
- Cada problema é entendível sem contexto dos outros
- Zero shared state entre investigações
- Review especializado em eixos ortogonais (ex: Standards vs Spec compliance)

---

## Don't use when

- Falhas **relacionadas** (fix em uma pode resolver outras) — investigar juntas primeiro
- Precisa entender **estado completo** do sistema antes de agir
- Exploratory debugging — você ainda não sabe o que está quebrado
- Agents iriam **editar os mesmos arquivos** ou competir pelos mesmos recursos

Paralelizar errado **causa conflitos silenciosos** — dois agents editam o mesmo arquivo, o último write vence, fixes ficam parciais.

---

## Estrutura do prompt (cada agent)

Cada prompt paralelo precisa de **4 atributos obrigatórios**:

| Atributo | Por que |
|---|---|
| **Specific scope** | Um test file, um subsistema, um eixo. NÃO "fix all tests". |
| **Clear goal** | "Make these tests pass". NÃO "improve quality". |
| **Constraints** | "Don't change production code", "Edit only X file". Previne refactor não pedido. |
| **Expected output** | "Return summary of root cause and what you fixed, with file:line refs". |

Sem esses 4 atributos, o agent ou se perde ou faz mudanças laterais que conflitam com os outros agents.

**Sempre incluir contexto inline:**
- Cole as **error messages reais**, não "fix the race condition"
- Cole os **test names** específicos que falham
- Liste os **arquivos permitidos** para edição

---

## Pre-dispatch — checklist anti-conflito (OBRIGATÓRIO)

Antes de despachar qualquer paralelo, validar **na ordem**:

```
1. Mapear arquivos que cada agent vai TOCAR
   └─ Liste os arquivos esperados para cada agent (mesmo que aproximado)

2. Os conjuntos são DISJUNTOS?
   ├─ SIM → prosseguir para step 3
   └─ NÃO → CANCELAR paralelo, virar SEQUENCIAL ou re-particionar

3. Resources compartilhados (DB, ports, arquivos de config, env vars)?
   ├─ Cada agent escreve em namespace próprio → OK
   ├─ Agents leem o mesmo recurso sem escrever → OK
   └─ Múltiplos agents escrevem no mesmo recurso → CANCELAR paralelo

4. Tasks dependem do RESULTADO uma da outra?
   ├─ SIM → CANCELAR paralelo, virar SEQUENCIAL
   └─ NÃO → prosseguir

5. Restrições em cada prompt:
   - "Edit ONLY <lista de arquivos>"
   - "Do NOT touch files outside the listed scope"
   - "If you need to edit a file not in scope, STOP and report"

Se passou todos os 5 → dispatch em paralelo.
Se falhou qualquer um → re-pensar a decomposição.
```

**Sinais que indicam re-particionar:**

- Dois agents precisariam editar o mesmo arquivo de config (`package.json`, `requirements.txt`, etc.) → unificar em UM agent que faz ambas as mudanças
- Dois agents precisariam adicionar import na mesma `index.ts` → reorder em sequencial
- Agents iriam rodar migrations contra o mesmo schema → sequencial, OU rodar contra DBs isoladas

**Sinais de que paralelo está OK:**

- Cada agent fica numa subpasta diferente (`src/feature-a/` vs `src/feature-b/`)
- Cada agent tem seu próprio test file
- Mudanças de config são todas em arquivos diferentes (um por agent)
- Domínios completamente disjuntos (auth vs billing vs analytics)

---

## Pattern de dispatch (Task tool)

Use **uma única mensagem** com múltiplos `Agent` tool calls — eles rodam concorrentemente:

```
Agent({description: "Fix file-A.test.ts", subagent_type: "general-purpose", prompt: "..."})
Agent({description: "Fix file-B.test.ts", subagent_type: "general-purpose", prompt: "..."})
Agent({description: "Fix file-C.test.ts", subagent_type: "general-purpose", prompt: "..."})
```

Despachar em mensagens separadas serializa o trabalho — anula o ganho.

**Para o Protocolo Dois-Eixos** (review pre-commit Large/Complex): 2 agents (Standards reviewer + Spec reviewer), prompts em [review.md > Dois-Eixos](../nano-spec:review/review.md#protocolo-dois-eixos-largecomplex-pré-commit).

---

## Verification pós-retorno (4 passos obrigatórios)

Quando os agents retornarem, **antes** de marcar o conjunto como done:

1. **Review each summary** — entenda o que cada agent mudou
2. **Check for conflicts** — agents editaram o mesmo arquivo ou linhas próximas? Se sim, revisar manualmente o merge
3. **Run full suite** — verificar que **todos** os fixes funcionam juntos (não só cada um isoladamente)
4. **Spot check** — agents podem cometer erros sistemáticos (ex: todos os 3 aplicaram o mesmo workaround errado); rode read em pelo menos um arquivo de cada agent

Pular o step 2 (conflict check) é o erro mais comum — o agent pode reportar success enquanto sobrescreveu o fix do outro.

---

## Common Mistakes

| ❌ Errado | ✅ Certo |
|---|---|
| "Fix all the tests" | "Fix `agent-tool-abort.test.ts`" |
| "Fix the race condition" (sem onde) | Cole error messages + test names |
| Sem constraints | "Do NOT change production code" / "Edit only X" |
| "Fix it" (vague output) | "Return summary of root cause + changes with file:line" |
| Despachar em mensagens separadas | Múltiplos `Agent` tool calls em **uma** mensagem |
| Não checar conflicts | Step 2 da verification é obrigatório |

---

## Real-world impact

Exemplo da skill original:

> 6 falhas em 3 arquivos após refactor.
> 3 agents paralelos despachados (cada um focado em 1 arquivo, com constraints).
> Tempo total = tempo do mais lento, não soma.
> Zero conflitos (arquivos disjuntos).
> Full suite green após integração.

A vantagem só aparece quando os domínios são **realmente** disjuntos. Em domínio acoplado, o ganho de paralelização vira custo de reconciliação.

---

## Integração com nano-spec

| Fase / Skill | Quando usar parallel dispatch |
|---|---|
| **Execute** (multiple unrelated tasks) | Tasks marcadas `[P]` em `tasks.md` com **dependências disjuntas** |
| **Review pre-commit Large/Complex** | Protocolo Dois-Eixos (Standards + Spec) |
| **Debug** (multiple failures) | Sintomas em subsistemas claramente separados (ver [debug.md](../systematic-debugging/debug.md)) |

**Nunca paralelize:**
- Implementer subagents (per task) — conflitos no working tree
- Tasks com dependências em `tasks.md` (`Depends on: T1`)
- Investigations onde o problema pode ter root cause comum
