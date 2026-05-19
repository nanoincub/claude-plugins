---
name: code-review
description: >
  Code review com 5 eixos (Correctness, Performance, Maintainability, Security, Testing).
  Inclui security review (OWASP, secrets, injection, authZ) e protocolo de recepção de
  feedback (zero performative agreement — verify antes de implementar). Subagent reviewer
  com BASE_SHA/HEAD_SHA delta. Usado standalone ou pelo Protocolo Dois-Eixos do nano-spec.
  Triggers: "review desse código", "code review", "revise esse PR", "audite segurança",
  "security review", "5 eixos", "feedback de review", "recebi um review",
  "implementar feedback", "pushback de review".
  Não use para: validate / UAT contra acceptance criteria (use validate em nano-disciplines:
  umbrella), TDD (use tdd), debug (use debug).
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 1.0.0
---

# Code Review — 5 Eixos

**Goal**: Review estruturado de PR/diff em 5 dimensões. Saída acionável com BASE_SHA/HEAD_SHA explícitos.

## Os 5 eixos

Aplicar [code-review.md](references/code-review.md):

1. **Correctness** — código faz o que a spec/comment promete?
2. **Performance** — hot paths, alocações, queries, N+1
3. **Maintainability** — naming, complexidade, duplicação, layering
4. **Security** — input validation, secrets, authZ, injection — detalhado em [security.md](references/security.md)
5. **Testing** — cobertura, naming, anti-patterns

## Subagent reviewer

Para Large/Complex, despachar subagent code-reviewer com prompt em [code-reviewer-prompt.md](references/code-reviewer-prompt.md). Prompt completo, autocontido, BASE_SHA/HEAD_SHA explícitos.

## Security review (subdiscipline)

Quando o foco é só segurança (auditoria pré-release, audit externa, OWASP), aplicar [security.md](references/security.md) diretamente — OWASP Top 10, secrets handling, authZ patterns, injection, SSRF.

## Recebendo feedback (quando VOCÊ é o autor)

Quando recebido feedback (de um subagent, dev, ou review externo), aplicar [receiving-feedback.md](references/receiving-feedback.md):

- **READ** completo antes de responder
- **UNDERSTAND** o argumento técnico
- **VERIFY** com o código (não confiar cegamente)
- **EVALUATE** se procede tecnicamente
- **RESPOND** com posição clara (concordar OU push back com razão)
- **IMPLEMENT** só após convergência

**Zero performative agreement.** Implementar feedback errado é pior que pushback bem feito.

## Versão

1.0.0 — Promoted skill em `nano-disciplines` 1.1.0. Conteúdo adaptado do `superpowers:requesting-code-review` + `superpowers:receiving-code-review` por Jesse Vincent (Anthropic). Adapta para Nano: adiciona eixo Security explícito (subdiscipline própria), prompt PT-BR, integração com Protocolo Dois-Eixos do nano-spec.
