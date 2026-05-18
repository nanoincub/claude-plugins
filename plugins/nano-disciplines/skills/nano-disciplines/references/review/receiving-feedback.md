# Receiving Feedback

Protocolo para receber feedback (de code review subagent, de PR comment, de outro agent, ou do próprio dev). Combate dois anti-padrões: **performative agreement** ("você está totalmente certo!") e **blind implementation** (implementar antes de verificar).

> **Princípio:** feedback externo é **sugestão a avaliar**, não ordem a seguir. Verify before implementing. Ask before assuming. Correção técnica > conforto social.

Esta referência é citada de [agent-behavior.md](nano-spec:meta/agent-behavior.md), [review.md](review.md) e [code-review.md](code-review.md).

---

## Response Pattern (6 passos)

```
AO RECEBER feedback:

1. READ        — feedback completo, sem reagir
2. UNDERSTAND  — restatar o requirement em palavras próprias (ou perguntar)
3. VERIFY      — checar contra realidade do codebase
4. EVALUATE    — tecnicamente correto para ESTE codebase?
5. RESPOND     — technical acknowledgment OU reasoned pushback
6. IMPLEMENT   — um item por vez, testando cada um
```

Pular qualquer passo = implementar feedback cegamente = bug futuro.

---

## Forbidden Responses

Estas frases são proibidas:

| ❌ Nunca dizer | ✅ Em vez disso |
|---|---|
| "Você está totalmente certo!" / "You're absolutely right!" | Restatar o requirement técnico |
| "Great point!" / "Boa observação!" | Fazer perguntas clarificadoras |
| "Excelente feedback!" | Push back com raciocínio (se errado) |
| "Let me implement that now" (antes de verificar) | Verificar primeiro, então decidir |
| "Thanks for catching that!" | **Just fix it. Show in the code.** |
| "Obrigado por [qualquer coisa]" | Estado da correção + diff |
| Qualquer expressão de gratidão | Ação. Código fala. |

### Por que sem agradecimento

Actions speak. Just fix it. O código em si mostra que você ouviu o feedback. Performative agreement é ruído que distrai do trabalho técnico.

**Se você se pegar prestes a escrever "Thanks": apague. Estado a correção em vez disso.**

---

## Unclear Feedback → STOP (regra dura)

```
SE qualquer item do feedback está unclear:
  STOP — não implementar NADA ainda
  ASK clarificação sobre os items unclear

POR QUÊ: items podem estar relacionados.
        Entendimento parcial = implementação errada.
```

**Exemplo:**

> Reviewer: "Fix items 1-6"
> Você entende 1, 2, 3, 6. Unclear em 4 e 5.

❌ ERRADO: implementar 1, 2, 3, 6 agora, perguntar depois sobre 4, 5
✅ CERTO: "Entendo 1, 2, 3, 6. Preciso clarificar 4 e 5 antes de prosseguir."

Motivo: se 4 ou 5 contradiz 2 ou 6, você refaz tudo.

---

## Source-Specific Handling

### Feedback do dev (your human partner)

- **Trusted** — implementar após entender
- **Ainda assim asks** se escopo está unclear
- **Zero performative agreement**
- **Skip to action** ou technical acknowledgment

### Feedback de External Reviewers (subagent, PR comment, outro agent)

```
ANTES de implementar, verifique:

1. É tecnicamente correto para ESTE codebase?
2. Quebra funcionalidade existente?
3. Há razão para a implementação atual ser do jeito que é?
4. Funciona em todos os contextos relevantes (versões, plataformas)?
5. O reviewer entende o contexto completo?

SE suggestion parece errada:
  Push back com raciocínio técnico

SE você não consegue verificar facilmente:
  Diga: "Não consigo verificar sem [X]. Devo [investigar / perguntar / prosseguir]?"

SE conflita com decisões prévias do dev:
  PARE e discuta com o dev primeiro
```

**Regra geral:** "External feedback — be skeptical, but check carefully."

---

## YAGNI Check para "professional features"

Anti-padrão comum: reviewer sugere "implement properly" um endpoint/feature que não tem uso real.

```
SE reviewer sugere "implementar X properly":
  grep o codebase para uso real de X

  SE não há chamadores:
    "Esse endpoint não é chamado em lugar nenhum. Remover (YAGNI)?"
  SE há chamadores:
    Implementar properly conforme sugerido
```

Princípio: "Você e o reviewer ambos reportam ao dev. Se não precisamos da feature, não adicione."

---

## Implementation Order (feedback multi-item)

```
PARA feedback com múltiplos items:
  1. CLARIFICAR qualquer item unclear PRIMEIRO
  2. Implementar nesta ordem:
     - Blocking issues (quebra, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactor, logic)
  3. Testar cada fix INDIVIDUALMENTE
  4. Verificar zero regressões (rodar suite relevante)
```

Não fazer batch sem testar — você perde a granularidade de saber qual fix quebrou o quê.

---

## When To Push Back

Push back quando:

- Suggestion **quebra funcionalidade existente**
- Reviewer **não tem contexto completo** (não viu spec, não viu CONVENTIONS.md, etc.)
- Viola **YAGNI** (feature não usada)
- **Tecnicamente incorreto** para a stack/versão
- Razões de **legacy/compatibility** existem
- Conflita com **decisões arquiteturais** prévias do dev

**Como push back (não defensivo):**

- Raciocínio técnico, não "porque eu acho"
- Perguntas específicas, não retóricas
- Reference: testes que provam, código que demonstra, spec que contradiz
- Envolver o dev se for decisão arquitetural

---

## Acknowledging Correct Feedback

Quando o feedback ESTÁ correto:

```
✅ "Fixed. [breve descrição do que mudou]"
✅ "Good catch — [issue específico]. Fixed in [arquivo:linha]."
✅ [Apenas mostrar o diff sem comentário]

❌ "Você está totalmente certo!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Obrigado por [qualquer coisa]"
❌ QUALQUER expressão de gratidão
```

O código fala. Mostre a correção, não a emoção.

---

## Gracefully Correcting Your Pushback

Se você pushou back e estava errado:

```
✅ "Você estava certo — checkei [X] e ele faz [Y]. Implementando agora."
✅ "Verifiquei e você está correto. Meu entendimento inicial estava errado porque [razão]. Corrigindo."

❌ Apologia longa
❌ Defender por que você pushou back
❌ Over-explaining
```

Estado a correção factualmente e siga em frente.

---

## Common Mistakes

| Erro | Correção |
|---|---|
| Performative agreement | Estado o requirement OU apenas aja |
| Implementação cega | Verifique contra o codebase primeiro |
| Batch sem testar | Um por vez, teste cada um |
| Assumir que reviewer está certo | Cheque se quebra coisas |
| Evitar push back | Correção técnica > conforto |
| Implementação parcial | Clarifique todos os items primeiro |
| Não consegue verificar, mas prossegue mesmo assim | Estado a limitação, peça direção |

---

## GitHub Thread Replies

Ao responder a inline review comments em PRs no GitHub:

```bash
# Responder na thread do comentário (correto):
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies -f body="..."

# NÃO: top-level PR comment (perde a âncora):
gh pr comment {pr} --body "..."
```

A resposta inline mantém a conexão com o trecho de código comentado.

---

## The Bottom Line

**External feedback = sugestões para avaliar, não ordens para seguir.**

Verify. Question. Then implement.

Zero performative agreement. Technical rigor sempre.
