# Coding Principles

Behavioral bias, not checklist. Read before every implementation.

---

## Carregar Contexto do Projeto (OBRIGATÓRIO)

Antes de qualquer implementação, verificar se o CLAUDE.md do projeto define:
- **Convenções de código** (naming, sufixos, strict_types, etc.)
- **Regras arquiteturais** (multi-tenancy, migrations centralizadas, etc.)
- **Comandos específicos** (artisan via Docker, etc.)
- **Restrições** (nunca criar migrations fora de X, sempre usar Y)

Estas regras do projeto TÊM PRECEDÊNCIA sobre os princípios genéricos abaixo.

---

## Before Coding

- State assumptions explicitly. If uncertain, ask.
- Multiple interpretations exist? Present all—don't pick silently.
- Simpler approach exists? Say so. Push back when warranted.
- Something unclear? Stop. Name what's confusing. Ask.
- User's approach seems wrong? Disagree honestly. Don't be sycophantic.

---

## During Implementation

### Simplicity

- No features beyond what was asked
- No abstractions for single-use code
- No "flexibility" or "configurability" not requested
- No error handling for impossible scenarios
- 200 lines that could be 50? Rewrite it.

### Surgical Changes

- Don't "improve" adjacent code, comments, or formatting
- Don't refactor things that aren't broken
- Match existing style, even if you'd do differently
- Unrelated dead code noticed? Mention it—don't delete it
- Remove ONLY imports/variables/functions YOUR changes orphaned
- Don't remove pre-existing dead code unless asked

### Goal-Driven

- Transform vague tasks into verifiable goals
- Multi-step work? State brief plan with verify checkpoints
- Every changed line must trace directly to user's request

---

## After Each Change

Ask: "Would senior engineer call this overcomplicated?"
If yes → simplify before proceeding.
