# Protocolo Dois-Eixos (Large/Complex pré-commit)

Code review pré-commit **particionado em dois subagents paralelos** especializados — um para Standards, outro para Spec compliance. Substitui o code reviewer geral ([code-review.md](code-review.md)) no slot pré-commit em features Large/Complex.

Adaptado de `review` (matpocock-skills).

> **Princípio:** um reviewer monolítico revisando 5 eixos (plan/quality/architecture/testing/production) tende a misturar severidades e diluir foco. Dois reviewers em paralelo, cada um com um único critério, produzem achados mais factuais e auditáveis — e rodam mais rápido.

---

## Por que dois eixos (e não um, ou cinco)

| Aspecto | Reviewer monolítico (5 eixos) | Dois-Eixos (Standards + Spec) |
|---|---|---|
| Foco | Disperso entre 5 categorias | Cada agent tem 1 critério |
| Severidade | Subjetiva (Critical/Important/Minor) | Sem classificação — só factual (violação ou gap) |
| Velocidade | Sequencial, lento | Paralelo (via [parallel-dispatch.md](../execute/subagents/parallel-dispatch.md)) |
| Verdict | "Ready to merge: Yes/No/With fixes" — opina | Dev decide: endereçar / pular / discutir |
| Auditabilidade | Verdict subjetivo, difícil revisar depois | Cada achado tem fonte textual (regra cited + arquivo:linha) |
| Architecture / testing depth | ✅ Cobre | ❌ NÃO cobre (use code-review.md em outros slots) |

**O Dois-Eixos é mais rigoroso, mais rápido, e preserva agência do dev — mas troca cobertura por foco.** Se precisar de arquitetura/produção: code-review.md geral.

---

## Os dois eixos

| Eixo | O que verifica | Fonte |
|---|---|---|
| **Standards** | Código segue convenções do repo? | `.specs/codebase/CONVENTIONS.md`, `CLAUDE.md`, `react-best-practices` (se aplicável à stack) |
| **Spec** | Código implementa fielmente o que foi pedido? | `.specs/features/YYYY-MM-DD-[feature]/spec.md` (acceptance criteria + `[FEAT]-XX` IDs), `tasks.md` (tudo marcado como done?) |

---

## Quando ativar

- **Complex** — sempre, antes de `nano-commit` (no slot do code reviewer geral)
- **Large** — default; dev pode pular explicitamente
- **Medium/Small/Quick** — skip (usar [code-review.md](code-review.md) se o dev pedir review)

---

## Fluxo (substitui step 3.1 do [review.md](review.md) em Large/Complex)

```
1. Capturar fixed point: git merge-base HEAD main
   └─ Sem perguntar ao dev — usar o ancestral comum
2. Validar anti-conflito (paralelo é OK aqui?)
   └─ Os dois agents só LEEM; sem risco de conflito de escrita
3. Despachar 2 subagents EM PARALELO via parallel-dispatch.md
   ├─ Agent A: Standards (prompt abaixo)
   └─ Agent B: Spec (prompt abaixo)
4. Receber relatórios
5. Aplicar regra de verificação: Read da linha citada antes de aceitar
   └─ Descartar achados que não conferem com o código real
6. Apresentar relatório dois-eixos ao dev
7. Dev decide: endereçar antes do commit? (sim / pular / discutir)
```

---

## Prompts dos subagents

> Mantidos em PT-BR pois o Dois-Eixos é específico do nano-spec e tem fontes (CONVENTIONS.md, spec.md) que normalmente estão em PT-BR no projeto.

### Standards agent

```
Você é reviewer de Standards. NÃO classifique severidade nem proponha fixes.

Inputs:
- Diff: <output de `git diff <merge-base>...HEAD`>
- Convenções: .specs/codebase/CONVENTIONS.md
- Regras gerais: CLAUDE.md (raiz do projeto)

Para cada violação detectada, retorne:
- arquivo:linha
- convenção violada (cite a regra TEXTUALMENTE de CONVENTIONS.md ou CLAUDE.md)
- trecho de código REAL (não parafraseado, copy literal)

NÃO inclua observações pré-existentes (fora do diff).
NÃO recomende correções — apenas reporte violações.
Se não houver violações, retornar lista vazia.
```

### Spec agent

```
Você é reviewer de Spec compliance. NÃO classifique severidade nem proponha fixes.

Inputs:
- Diff: <output de `git diff <merge-base>...HEAD`>
- Spec: .specs/features/YYYY-MM-DD-[feature]/spec.md
- Tasks: .specs/features/YYYY-MM-DD-[feature]/tasks.md

Para cada [FEAT]-XX da spec.md, verifique:
1. O critério QUANDO/ENTÃO está implementado no diff?
2. As tasks de tasks.md marcadas como done realmente entregaram o comportamento?

Retorne factualmente:
- [FEAT]-XX — gap ou contradição — arquivo:linha (se aplicável)

NÃO recomende correções — apenas reporte gaps.
Se cobertura está completa, retornar lista vazia.
```

---

## Formato do relatório consolidado

```markdown
## Review pré-commit — dois eixos

**Base SHA:** <merge-base com main>
**Head SHA:** <HEAD atual>

### Eixo Standards
- [arquivo:linha] — [convenção violada cited] — [trecho real]
- (...)

### Eixo Spec
- [FEAT]-XX — [gap entre acceptance criteria e implementação] — [arquivo:linha]
- (...)

**Decisão:** endereçar antes do commit? (sim / pular / discutir)
```

---

## Como reconciliar discordâncias entre eixos

Se Standards diz "X viola convenção Y" e Spec diz "X é necessário para [FEAT]-Z":

| Situação | Tratamento |
|---|---|
| Convenção é regra dura (segurança, type safety) | Convenção vence — refatorar para atender spec sem violar convenção |
| Convenção é estilo (naming, ordem de imports) | Spec vence — registrar exceção em STATE.md, opcionalmente atualizar CONVENTIONS.md para acomodar o padrão |
| Convenção e spec genuinamente conflitam (legacy) | Escalar para o dev — decisão arquitetural |
| Standards reporta violação que não existe (achado falso) | Descartar (regra de verificação do step 5: Read da linha antes de aceitar) |

---

## Limites

| Tool | Max re-runs | Após limite |
|---|---|---|
| Protocolo Dois-Eixos | 3 (por ciclo de review) | Escalar para dev — provável conflito real spec ↔ convenção |

Loop infinito é sinal de:
- Spec contradiz CONVENTIONS.md (decisão arquitetural pendente)
- Implementação genuinamente não atende `[FEAT]-XX` (re-fazer task, não re-revisar)

---

## Recepção do retorno

Aplicar [receiving-feedback.md](receiving-feedback.md). Os achados do Dois-Eixos **não são opiniões** — são fatos com fonte textual. Mas a recepção do protocolo continua valendo (zero performative agreement, verify antes de implementar).
