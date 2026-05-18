---
name: tdd
description: >
  Test-Driven Development com Iron Law (NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST).
  Ciclo RED → Verify RED → GREEN → Verify GREEN → REFACTOR. Inclui anti-patterns de testing
  (5 padrões + Gate Functions para detectar testar mock em vez de comportamento real) e
  condition-based-waiting para testes async.
  Triggers: "aplicar TDD", "test-driven", "escrever teste antes", "RED-GREEN-REFACTOR",
  "tdd cycle", "failing test first", "teste para essa lógica", "anti-pattern de teste".
  Não use para: tasks de config/docs/rename (verificação manual basta), debug de bug
  existente (use debug), code review (use code-review).
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 1.0.0
---

# TDD — Test-Driven Development

**Goal**: Escrever testes ANTES do código de produção. Iron Law: `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`.

## Quando aplicar

Tasks que tocam:
- Lógica de negócio
- Mutação de estado
- API / contratos
- Fluxo condicional
- Cálculos / transformações

## Quando NÃO aplicar (verificação manual basta)

- Config / env vars
- Docs / READMEs
- Rename / refactor mecânico
- Setup de scaffold

## O ciclo completo

Aplicar [tdd.md](references/tdd.md) — RED → Verify RED → GREEN → Verify GREEN → REFACTOR. Cada passo tem gate verificável.

## Anti-patterns

Antes de escrever mocks ou testes async, ler [testing-anti-patterns.md](references/testing-anti-patterns.md) — 5 anti-padrões comuns com Gate Functions para evitar testar mock em vez de comportamento real.

## Testes async (condition-based waiting)

Para testes que precisam aguardar estado, ler [condition-based-waiting.md](references/condition-based-waiting.md) e exemplo em [condition-based-waiting-example.ts](references/condition-based-waiting-example.ts) — evita `setTimeout` arbitrários, usa polling em condição.

## Naming convention (quando usado pelo nano-spec)

Quando esta skill é invocada pelo `nano-spec`, os testes DEVEM ser nomeados com o ID do requisito da spec (ex: `test_PAY03_expired_card_returns_declined`). Cada critério testável de `spec.md` tem ao menos um teste correspondente — rastreabilidade Spec → Teste → Commit.

## Versão

1.0.0 — Promoted skill em `nano-disciplines` 1.1.0. Conteúdo adaptado do `superpowers:test-driven-development` por Jesse Vincent (Anthropic).
