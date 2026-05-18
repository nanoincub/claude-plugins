# Debug — Systematic Debugging

Disciplina para evitar fixes por chute. Fixes aleatórios desperdiçam tempo e introduzem bugs novos. Patches rápidos mascaram problemas reais.

> **Princípio:** SEMPRE achar root cause antes de propor fixes. Fix de sintoma é falha.

Esta referência opera junto com [tdd.md](../tdd/tdd.md) (failing test antes de fix) e [implement.md](../implement.md) (loop de Execute).

---

## Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Se você não completou a Fase 1, **você não pode propor fix.**

---

## Quando usar

Para qualquer issue técnica: test failure, bug em produção, comportamento inesperado, problema de performance, build falhando, integração quebrada.

**Use ESPECIALMENTE quando:**
- Sob pressão de tempo (urgência torna chute tentador)
- "Só esse fix rapidinho" parece óbvio
- Você já tentou múltiplos fixes
- Fix anterior não funcionou
- Você não entende totalmente o problema

**Não pule quando:**
- Issue parece simples (bugs simples também têm root cause)
- Está com pressa (correria garante retrabalho)
- Dev quer fix AGORA (sistemático é mais rápido que thrashing)

---

## As 4 Fases

Você DEVE completar cada fase antes de avançar para a próxima.

### Fase 1: Root Cause Investigation

**ANTES de tentar QUALQUER fix:**

1. **Leia mensagens de erro com cuidado.** Stack traces completos. Line numbers, paths, error codes. A solução exata costuma estar ali.

2. **Reproduza consistentemente.** Steps exatos. Acontece toda vez? Se não reproduzível → coletar mais dados, não chutar.

3. **Cheque mudanças recentes.** `git diff`, commits recentes, novas dependências, mudanças de config, diferenças de ambiente.

4. **Em sistemas multi-componente, instrumente os boundaries.**

   Quando o sistema tem múltiplas camadas (CI → build → signing, API → service → DB), **antes** de propor fix:

   ```
   Para CADA component boundary:
     - Logar o que ENTRA no componente
     - Logar o que SAI do componente
     - Verificar propagação de env/config
     - Checar estado em cada layer

   Rodar uma vez para coletar evidência mostrando ONDE quebra
   ENTÃO analisar evidência para identificar componente que falha
   ENTÃO investigar aquele componente específico
   ```

   Exemplo multi-layer:
   ```bash
   # Layer 1: Workflow
   echo "=== Secrets in workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Layer 2: Build script
   echo "=== Env vars in build: ==="
   env | grep IDENTITY || echo "IDENTITY not in env"

   # Layer 3: Operação real
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   Isso revela qual layer falha (secrets → workflow ✓, workflow → build ✗).

5. **Trace data flow** quando o erro está fundo no call stack:
   - Onde o valor ruim originou?
   - O que chamou isto com valor ruim?
   - Continue subindo até achar a fonte
   - **Fix na fonte, não no sintoma**

   Ver [root-cause-tracing.md](root-cause-tracing.md) para a técnica completa de backward tracing.

### Fase 2: Pattern Analysis

**Achar o padrão antes de corrigir:**

1. **Achar exemplos funcionando.** Código similar funcionando no mesmo codebase. O que funciona que é parecido com o que está quebrado?

2. **Comparar contra referência.** Se implementando um pattern, leia a referência **completa**. Não skim — leia toda linha. Entenda o pattern totalmente antes de aplicar.

3. **Identificar diferenças.** O que é diferente entre o que funciona e o que quebra? Liste **toda** diferença, por menor que pareça. Não presuma "isso não pode importar".

4. **Entender dependências.** Que outros componentes isto precisa? Settings, config, env? Que assumptions faz?

### Fase 3: Hypothesis and Testing

**Método científico:**

1. **Formular UMA hipótese.** Clara, escrita: "Acho que X é root cause porque Y". Específica, não vaga.

2. **Testar minimamente.** A **menor** mudança possível para testar a hipótese. **Uma variável por vez.** Não corrija múltiplas coisas ao mesmo tempo.

3. **Verificar antes de continuar.** Funcionou? → Fase 4. Não funcionou? → Forme **nova** hipótese. NÃO empilhe mais fixes em cima.

4. **Quando você não sabe.** Diga "Não entendo X". Não finja saber. Peça ajuda. Pesquise mais.

### Fase 4: Implementation

**Fix no root cause, não no sintoma:**

1. **Criar failing test case.** Reprodução mais simples possível. Teste automatizado se possível, script one-off se sem framework. **OBRIGATÓRIO antes do fix.** Ver [tdd.md](../tdd/tdd.md) para o ciclo correto.

2. **Implementar fix único.** Endereçar o root cause identificado. **UMA mudança por vez.** Sem "já que estou aqui" melhorias. Sem refactor bundled.

3. **Verificar fix.** Teste passa agora? Outros testes continuam passando? Issue realmente resolvido?

4. **Se o fix não funcionou:**
   - STOP
   - Conte: quantos fixes você já tentou?
   - Se < 3: voltar para Fase 1, re-analisar com nova informação
   - **Se ≥ 3: parar e questionar a arquitetura (Fase 4.5)**
   - NÃO tente Fix #4 sem discussão arquitetural

### Fase 4.5: Questione a Arquitetura (após 3 fixes falhos)

**Padrão indicando problema arquitetural:**
- Cada fix revela novo shared state / coupling / problema em lugar diferente
- Fixes exigem "refactor massivo" para implementar
- Cada fix cria sintomas novos em outro lugar

**PARE e questione fundamentos:**
- Este pattern é fundamentalmente sólido?
- Estamos "ficando com isto por inércia"?
- Devemos refatorar arquitetura em vez de continuar corrigindo sintomas?

**Discuta com o dev antes de tentar mais fixes.**

Isto **não é** hipótese falhada — é arquitetura errada.

---

## Defense-in-Depth (após achar root cause)

Depois de identificar o root cause e implementar o fix, considere adicionar validação em múltiplas camadas para **tornar o bug impossível**, não só corrigir uma instância.

Ver [defense-in-depth.md](defense-in-depth.md) — pattern de 4 camadas (Entry Point → Business Logic → Environment Guards → Debug Instrumentation).

Princípio: "Single validation: corrigimos o bug. Multiple layers: tornamos o bug **impossível**."

---

## Testes flaky

Se o bug envolve testes que passam às vezes e falham sob carga / em CI / em paralelo, o problema geralmente é **timing arbitrário** em vez de espera por condição. Ver [condition-based-waiting.md](../tdd/condition-based-waiting.md) — substitui `setTimeout`/`sleep` por polling de condição real.

---

## Red Flags — STOP e siga o processo

Se você se pegar pensando qualquer um destes:

- "Quick fix por agora, investigo depois"
- "Deixa eu mudar X e ver se funciona"
- "Adiciono várias mudanças, rodo os testes"
- "Pulo o teste, verifico manualmente"
- "Provavelmente é X, deixa eu corrigir"
- "Não entendo bem mas isso talvez funcione"
- "O pattern diz X mas vou adaptar diferente"
- "Aqui estão os problemas principais: [lista fixes sem investigação]"
- Propondo soluções antes de tracear data flow
- **"Mais uma tentativa de fix"** (quando já tentou 2+)
- **Cada fix revela problema novo em lugar diferente**

**TODOS estes significam: STOP. Volte para Fase 1.**

**Se 3+ fixes falharam:** Questione arquitetura (Fase 4.5).

---

## Sinais do dev/parceiro de que você está errando

Estas redireções vindas do dev são alertas explícitos:

| Sinal | Significado |
|---|---|
| "Isso não está acontecendo?" | Você presumiu sem verificar |
| "Vai nos mostrar...?" | Você deveria ter adicionado evidence gathering |
| "Pare de chutar" | Você está propondo fix sem entender |
| "Ultrathink isso" | Questione fundamentos, não sintomas |
| "Estamos travados?" (frustrado) | Sua abordagem não está funcionando |

Quando você ver qualquer um destes: **STOP. Volte para Fase 1.**

---

## Tabela de Racionalizações

| Desculpa | Realidade |
|---|---|
| "Issue é simples, não precisa do processo" | Bugs simples também têm root cause. Processo é rápido. |
| "Emergência, sem tempo pra processo" | Debug sistemático é **mais rápido** que thrashing por chute. |
| "Tento esse fix primeiro, depois investigo" | Primeiro fix define o padrão da sessão. Faça certo desde o começo. |
| "Escrevo teste depois de confirmar o fix" | Fix sem teste não gruda. Teste primeiro prova. |
| "Vários fixes ao mesmo tempo poupa tempo" | Não consegue isolar o que funcionou. Causa novos bugs. |
| "Referência é longa demais, vou adaptar o pattern" | Entendimento parcial garante bugs. Leia completo. |
| "Vejo o problema, deixa eu corrigir" | Ver sintomas ≠ entender root cause. |
| "Mais uma tentativa de fix" (após 2+ falhas) | 3+ falhas = problema arquitetural. Questione o pattern, não corrija de novo. |

---

## Quick Reference

| Fase | Atividades-chave | Critério de saída |
|---|---|---|
| **1. Root Cause** | Ler erros, reproduzir, checar diffs, instrumentar boundaries, tracear data flow | Entender **o quê** e **por quê** |
| **2. Pattern** | Achar exemplos funcionando, comparar contra referência | Identificar diferenças |
| **3. Hypothesis** | Formular UMA teoria, testar minimamente | Confirmada ou nova hipótese |
| **4. Implementation** | Failing test → fix único → verificar | Bug resolvido, testes verdes |
| **4.5. Architecture** | Se 3+ fixes falharam: parar e questionar fundamentos | Discussão com o dev |

---

## Quando o processo revela "sem root cause"

Se a investigação sistemática revela que o issue é genuinamente ambiental, dependente de timing, ou externo:

1. Você completou o processo
2. Documente o que investigou
3. Implemente tratamento apropriado (retry, timeout, error message)
4. Adicione monitoring/logging para investigação futura

**Mas:** 95% dos casos de "sem root cause" são investigação incompleta.

---

## Técnicas de apoio

| Técnica | Arquivo | Quando usar |
|---|---|---|
| **Backward call-stack tracing** | [root-cause-tracing.md](root-cause-tracing.md) | Erro aparece fundo no stack, valor ruim originado longe |
| **Defense-in-depth (4 camadas)** | [defense-in-depth.md](defense-in-depth.md) | Após fix do root cause, prevenir reintrodução |
| **Condition-based waiting** | [condition-based-waiting.md](../tdd/condition-based-waiting.md) | Testes flaky com `setTimeout`/`sleep` arbitrário |

---

## Impacto observado

Da skill original, observação empírica em sessões de debug:
- **Sistemático:** 15-30 min para fix
- **Chute aleatório:** 2-3 horas de thrashing
- **First-time fix rate:** 95% vs 40%
- **Novos bugs introduzidos:** próximo de zero vs comum
