# Grill (opt-in no Specify)

**Goal**: Stress-testar a spec contra o domínio existente do projeto, afiar terminologia e atualizar `.specs/` inline conforme decisões cristalizam.

Adaptado de `grill-with-docs` (matpocock-skills) para o padrão Nano Incub: usa `.specs/codebase/CONVENTIONS.md` como glossário canônico e `.specs/decisions/` como ADR store.

**Quando NÃO usar — usar [discuss.md](discuss.md):** se o tópico é HOW a feature se comporta (gray areas de comportamento user-facing, interação, layout, fluxo), use `discuss.md`. `grill.md` é para WHAT um termo significa (terminologia, fronteiras de domínio, glossário). Na dúvida, comportamento → discuss; conceito → grill.

---

## Quando ativar

Gate automático (sincronizado com tabela canônica em [agent-behavior.md](agent-behavior.md)):

- **Complex** — sempre
- **Large** — quando a spec inicial usa termos conflitantes com `.specs/codebase/CONVENTIONS.md` OU introduz conceitos não presentes no glossário
- **Medium** — opt-in quando há ambiguidade de domínio
- **Small/Quick** — nunca

**Ordem:** grill roda **antes** do discovery do [specify.md](../specify/specify.md) quando há `CONVENTIONS.md` populado — afia vocabulário primeiro, discovery explora abordagens depois usando os termos canônicos. Quando não há `CONVENTIONS.md` (projeto novo), pular direto para o discovery do Specify.

---

## Princípio

Entrevistar o dev **uma pergunta por vez**, descendo cada ramo da árvore de decisão e resolvendo dependências entre elas. Para cada pergunta, o agente propõe a resposta recomendada antes de esperar feedback.

> Se uma pergunta pode ser respondida explorando o codebase, **explorar primeiro** — não perguntar ao dev o que o código já diz.

---

## Domínio e documentação

### Estrutura de referência

A Nano usa um único contexto por projeto:

```
.specs/
├── project/
│   └── PROJECT.md
├── codebase/
│   ├── CONVENTIONS.md      ← glossário canônico
│   ├── ARCHITECTURE.md
│   └── CONCERNS.md
├── decisions/              ← ADRs (criado lazily)
│   └── 0001-titulo.md
└── features/
    └── [feature]/
        └── spec.md
```

Criar arquivos **lazy**: só escrever quando há algo concreto a registrar. Sem `.specs/decisions/`? Criar quando a primeira ADR for necessária.

---

## Durante a sessão

### 1. Challenge contra o glossário

Quando o dev usa um termo que conflita com a definição em `CONVENTIONS.md`, sinalizar imediatamente:

> "Seu glossário define 'cancelamento' como X, mas você parece estar usando como Y — qual é?"

### 2. Afinar linguagem fuzzy

Termos vagos ou sobrecarregados → propor termo canônico preciso:

> "Você falou 'conta' — é Cliente ou Usuário? São coisas diferentes neste projeto."

### 3. Stress-test com cenários concretos

Ao discutir relações de domínio, inventar cenários específicos que sondam edge cases e forçam precisão nos limites entre conceitos.

### 4. Cross-reference com código

Quando o dev afirma como algo funciona, verificar se o código concorda. Contradição? Trazer à tona:

> "O código atual cancela Pedidos inteiros, mas você acabou de dizer que cancelamento parcial é possível — qual é o correto?"

### 5. Atualizar CONVENTIONS.md inline

Quando um termo é resolvido, atualizar `.specs/codebase/CONVENTIONS.md` **na hora**. Não bufferizar.

Formato mínimo por termo:

```markdown
### [Termo]

[Definição em uma frase. PT-BR, sem jargão de implementação.]

**Não confundir com:** [termos próximos]
**Aparece em:** [scopes/features onde o termo é usado]
```

> Não acoplar `CONVENTIONS.md` a detalhes de implementação. Só incluir termos significativos para experts de domínio.

### 6. Oferecer ADR com parcimônia

Só oferecer criar uma ADR em `.specs/decisions/` quando os três forem verdadeiros:

1. **Difícil de reverter** — custo real de mudar de ideia depois
2. **Surpreendente sem contexto** — leitor futuro vai perguntar "por que assim?"
3. **Resultado de trade-off real** — havia alternativas genuínas e escolhemos uma por razões específicas

Se faltar qualquer um dos três, **não criar ADR**.

Formato:

```markdown
# ADR NNNN — [Título curto e descritivo]

**Status:** Aceita | Substituída por ADR-XXXX | Revertida
**Data:** YYYY-MM-DD
**Feature(s):** [refs em .specs/features/]

## Contexto

[O que motivou a decisão. Constraint, incidente, requisito.]

## Decisão

[O que foi decidido, em 1-2 frases.]

## Alternativas consideradas

- **[Alt A]** — [por que rejeitada]
- **[Alt B]** — [por que rejeitada]

## Consequências

- **Positivas:** [o que ganhamos]
- **Negativas:** [o que aceitamos perder]
- **Reversibilidade:** [como reverter, se preciso]
```

---

## Fluxo

```
Specify iniciado
    │
    ▼
Gate de grilling dispara? (Complex sempre / Large condicional)
    │
    ├── Não → seguir Specify normal
    │
    └── Sim
        │
        ▼
    Loop de grilling (1 pergunta por vez)
        │
        ├── Termo conflitante → atualizar CONVENTIONS.md inline
        ├── Decisão hard-to-reverse → oferecer ADR
        └── Cenário ambíguo → resolver com edge case concreto
        │
        ▼
    Shared understanding alcançado
        │
        ▼
    Escrever spec.md com vocabulário canônico
        │
        ├─ Alimentar a seção "## Glossário" do spec.md
        │  com TODOS os termos consolidados + sinônimos descartados
        │
        ├─ Se decisões consolidadas vão além da feature → atualizar
        │  .specs/codebase/CONVENTIONS.md (seção do domínio relevante)
        │
        ▼
    Spec self-review (ver specify.md)
```

**Output do grill alimenta dois lugares:**

| Destino | O que vai | Quando |
|---|---|---|
| `spec.md` seção `## Glossário` | Termos canônicos da feature + sinônimos descartados | Sempre que grill rodou |
| `.specs/codebase/CONVENTIONS.md` | Termos que valem para o domínio inteiro do projeto (não só esta feature) | Quando consolidação tem alcance > feature atual |
| `.specs/decisions/NNNN-titulo.md` (ADR) | Decisão hard-to-reverse + surprising + trade-off real | Quando os 3 critérios estão presentes |

---

## Como invocar

O agente pode entrar no grill de duas formas:

1. **Automaticamente** quando o gate dispara no Specify
2. **Sob pedido** quando o dev diz "grill", "entreviste", "stress-test minha spec"

Grill **complementa** (não substitui) o discovery do Specify — discovery explora abordagens; grill afia terminologia e atualiza docs. Rodar grill **antes** do discovery quando há `.specs/codebase/CONVENTIONS.md` populado.

---

## Limites

- **Sem convergência após várias perguntas** → escalar: "Vamos pausar e fazer uma sessão de design separada?"
- **Não inventar termos** — se não há canonical no `CONVENTIONS.md`, propor um e pedir aprovação antes de gravar
- **Não criar ADR sem aprovação explícita** do dev — o agente propõe, dev aprova
