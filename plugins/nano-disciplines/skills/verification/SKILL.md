---
name: verification
description: >
  Iron Law: evidência antes da afirmação, sempre. Regra transversal para qualquer claim
  de "feito/passou/funciona/completo". Antes de marcar algo como concluído, rodar o
  comando que prova e mostrar saída fresh nesta mensagem.
  Triggers: "verificar", "iron law", "antes de marcar pronto", "evidência de teste",
  "testes passando", "verification before completion", "claim de feito".
  Não use para: orquestração de processo (use nano-spec), TDD (use tdd), debug (use debug).
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 1.0.0
---

# Verification Before Completion

Regra transversal para qualquer claim de "feito/passou/funciona/completo": **evidência antes da afirmação, sempre.**

Esta referência é citada de commit ([nano-commit](nano-spec:nano-commit:SKILL.md)), review ([review.md](nano-spec:review/review.md)), execute ([subagents.md](nano-disciplines:skills/nano-disciplines/references/subagents/subagents.md)) e do orquestrador nano-spec (fases Review/Commit + rastreabilidade Spec→Testes→Commit).

---

## Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Se você **não rodou** o comando de verificação **nesta mensagem**, você **não pode** afirmar que passa.

> Verificação de 5 mensagens atrás não conta — pode ter mudado código desde então.

---

## Gate Function (5 passos obrigatórios)

```
ANTES de afirmar qualquer status ou expressar satisfação:

1. IDENTIFY   — Que comando prova esta claim?
2. RUN        — Executar o comando FULL (fresh, completo)
3. READ       — Output completo, exit code, contar falhas
4. VERIFY     — Output confirma a claim?
                ├─ NÃO: declarar status real COM evidência
                └─ SIM: declarar claim COM evidência
5. ONLY THEN  — Fazer a claim

Pular qualquer passo = mentir, não verificar.
```

---

## Common Failures

| Claim | Requer | NÃO suficiente |
|---|---|---|
| "Tests pass" | Output do comando de teste: 0 falhas | "Should pass", run anterior |
| "Linter clean" | Output do linter: 0 erros | Check parcial, extrapolação |
| "Build succeeds" | Comando de build: exit 0 | Linter passou, "logs look good" |
| "Bug fixed" | Teste do sintoma original passa | Código mudou, fix presumido |
| "Regression test works" | Ciclo red-green completo verificado | Teste passa uma vez |
| "Agent completed" | VCS diff mostra mudanças reais | "Agent reported success" |
| "Requirements met" | Checklist linha-a-linha contra spec | "Tests passing" |

**Linha-chave:** "Requirements met" **≠** "tests passing". São coisas diferentes. Teste passando prova que o código faz o que o teste afirma — não que o código atende todos os critérios QUANDO/ENTÃO da spec.

---

## Red Flags — palavras proibidas até verificar

Estes padrões linguísticos significam que você está prestes a fazer uma claim **sem evidência**:

**Palavras-gatilho de incerteza disfarçada:**
- EN: `should`, `probably`, `seems to`, `looks like`
- PT: `deveria`, `provavelmente`, `parece que`, `acho que`

**Expressões de satisfação antes de verificar:**
- EN: `Great!`, `Perfect!`, `Done!`, `All set!`
- PT: `Pronto!`, `Beleza!`, `Funciona!`, `Tudo certo!`

**Comportamentos:**
- Prestes a commitar / abrir PR sem ter rodado verificação nesta mensagem
- Confiar em report de subagent sem checar VCS diff
- Aceitar verificação parcial como suficiente
- Racionalizar com `só dessa vez` / `just this once`
- `Estou cansado, quero acabar` ou variação

**Regra geral:** qualquer fraseado que sugira sucesso **sem você ter rodado a verificação nesta mensagem** é red flag.

---

## Prevenção de Racionalizações

| Desculpa | Realidade |
|---|---|
| "Deveria funcionar agora" | RODE a verificação |
| "Estou confiante" | Confiança ≠ evidência |
| "Só dessa vez" | Sem exceções |
| "O linter passou" | Linter ≠ compilador |
| "O agent disse que funcionou" | Verifique independentemente |
| "Estou cansado" | Cansaço ≠ desculpa |
| "Check parcial é suficiente" | Parcial não prova nada |
| "Usei palavras diferentes, então a regra não se aplica" | Espírito sobre letra |

---

## Key Patterns por tipo de claim

### Testes

```
✅  [Run test command] → [See: 34/34 pass] → "All tests pass"
❌  "Should pass now" / "Looks correct"
```

### Regression test (red-green completo)

```
✅  Write → Run (pass)
    → Revert fix → Run (MUST FAIL)
    → Restore → Run (pass)
❌  "I've written a regression test" (sem o ciclo red-green)
```

Ver também o ciclo completo em [tdd.md > Verificação red-green completa](../execute/tdd/tdd.md#verificação-red-green-completa-bug-fixes).

### Build

```
✅  [Run build] → [See: exit 0] → "Build passes"
❌  "Linter passed" (linter não compila)
```

### Requirements (spec coverage)

```
✅  Re-ler spec.md → criar checklist por ID de requisito
    → verificar cada um (código + teste)
    → reportar gaps OU completude
❌  "Tests pass, phase complete"
```

### Agent delegation (subagents)

```
✅  Agent reporta success → checar VCS diff → verificar mudanças
    → reportar estado real (não o claim do agent)
❌  Confiar no report do agent
```

---

## Aplicações no nano-spec (onde esta regra é gate)

| Fase / Skill | Como aplica |
|---|---|
| **Execute → Done por task** ([implement.md](nano-spec:execute/implement.md)) | Antes de marcar task Done, verificar "Done When" rodando os comandos listados |
| **Subagents → review loops** ([subagents.md](nano-disciplines:skills/nano-disciplines/references/subagents/subagents.md)) | Spec reviewer DEVE ler o código e rodar testes — não confiar no report do implementer |
| **Review** ([review.md](nano-spec:review/review.md)) | Iron Law obrigatória antes de marcar review como completo |
| **Pre-commit** ([nano-commit](nano-spec:nano-commit:SKILL.md)) | **Gate bloqueante:** testes devem ter passado (evidência fresca) antes do dev ver opções de commit. Se falharam, BLOQUEAR o fluxo. |
| **Spec → Commit traceability** | Antes do commit final, verificar que **todos** os requisitos `[FEAT]-XX` da spec.md têm código + teste correspondente, não só "tests pass" geral |

---

## Suite de testes — política do nano-spec

O agente **não roda** a suite completa por conta própria — pede ao dev e aguarda confirmação. Motivo: evita gastar tokens com output de centenas/milhares de testes.

A Iron Law se aplica **à confirmação do dev**: você só pode dizer "testes passaram" quando o dev confirmar explicitamente nesta mensagem, com evidência (output ou afirmação direta). Confirmação de mensagens anteriores não vale se houve mudança de código desde então.

---

## Por que isso importa

Empiricamente, fazer claim sem verificar leva a três falhas recorrentes:

1. **Trust broken** — quando o dev diz "I don't believe you" / "tem certeza?", a relação de trabalho degrada.
2. **Shipping quebrado** — funções indefinidas, requisitos faltando, código que crasha em produção.
3. **Retrabalho** — tempo gasto em falsa completude → o dev pega o erro → reverte e refaz.

> Honestidade é valor central. Se você mente sobre completude, é mais útil dizer "não verifiquei ainda" do que arriscar uma claim falsa.

---

## The Bottom Line

**Sem atalhos para verificação.**

Rode o comando. Leia o output. **Aí** afirme o resultado.

Isto é não-negociável.
