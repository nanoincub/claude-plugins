---
name: debug
description: >
  Systematic Debugging em 4 fases (Root Cause → Pattern → Hypothesis → Fix) + Fase 4.5
  (defense-in-depth para prevenir reincidência). Iron Law: NO FIXES WITHOUT ROOT CAUSE FIRST.
  Inclui root cause tracing (cadeia causal além do sintoma) e defense-in-depth (estratégias
  para impedir que o mesmo bug volte por outra porta).
  Triggers: "debug isso", "bug encontrado", "erro inesperado", "investigar falha",
  "root cause", "por que isso quebrou", "esse fix falhou", "systematic debugging",
  "fixei mas voltou".
  Não use para: feature nova (use TDD), code review (use code-review), verificação de
  conclusão (use verification).
license: CC-BY-4.0
metadata:
  author: Nano Incub
  version: 1.0.0
---

# Debug — Systematic Debugging

**Goal**: Investigar causa raiz ANTES de fixar. Iron Law: `NO FIXES WITHOUT ROOT CAUSE FIRST`.

## As 4 fases

Aplicar [debug.md](references/debug.md):

1. **Root Cause** — investigar o porquê do bug (não o sintoma)
2. **Pattern** — esse tipo de bug já aconteceu antes? mesmo padrão?
3. **Hypothesis** — formular hipótese testável
4. **Fix** — implementar fix mínimo que ataca a causa raiz, com teste failing primeiro

## Fase 4.5 — Defense-in-Depth

Depois do fix, aplicar [defense-in-depth.md](references/defense-in-depth.md) — prevenir reincidência por outra rota (validação adicional, type guards, asserts em runtime, etc.). Reduz superfície de "mesmo bug volta por porta diferente".

## Root Cause Tracing

Se a causa raiz não é óbvia, aplicar [root-cause-tracing.md](references/root-cause-tracing.md) — protocolo para seguir a cadeia causal além do sintoma imediato (cada "porque" expõe a próxima camada).

## Escalation

Se 3 fixes consecutivos falharam para o mesmo bug → **escalar ao dev**. Questionar a arquitetura. Não tente fix #4 — provavelmente o problema é mais profundo do que o código.

## Test antes do fix

Sempre escrever teste **failing** que reproduz o bug ANTES de fixar (Iron Law TDD). Garante:
- Bug é realmente reprodutível
- Fix realmente corrige
- Regressão é detectada se voltar

## Versão

1.0.0 — Promoted skill em `nano-disciplines` 1.1.0. Conteúdo adaptado do `superpowers:systematic-debugging` por Jesse Vincent (Anthropic).
