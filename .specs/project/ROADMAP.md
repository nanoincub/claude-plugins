# Roadmap

**Milestone atual:** Aperfeiçoamento do nano-spec
**Status:** In Progress

---

## Milestone 1 — nano-spec Estável

**Goal:** Plugin nano-spec robusto, documentado e distribuído para toda a equipe.
**Target:** Quando o processo estiver maduro o suficiente para uso diário sem fricção.

### Features

**Processo Spec-Driven (8 fases)** — COMPLETE

- Specify → Design → Tasks → Execute → Review → Security → Docs → Commit
- Auto-sizing por complexidade (Small/Medium/Large/Complex)
- Quality gates confirmativos obrigatórios

**Sistema de Sinais** — COMPLETE

- Sinais de Review (R1-R8): lógica, state, APIs, fluxo, estruturas, mudanças estruturais, volume, testes
- Sinais de Security (S1-S11): input, auth, authz, dados sensíveis, crypto, APIs externas, DB, rendering, config, keywords, deps

**Integração com Superpowers** — COMPLETE

- Brainstorming → context.md
- Writing-plans → tasks.md
- TDD, worktrees, subagents, debug no Execute
- Verification-before-completion no Review

**Hook de SessionStart** — COMPLETE

- Injeção de contexto leve (~5KB) em cada sessão
- Wrapper cross-platform (bash + batch)

**Documentação do Projeto** — IN PROGRESS

- Artefatos `.specs/` (PROJECT, ROADMAP, codebase docs)
- CLAUDE.md com referência estruturada
- READMEs expandidos

**Aperfeiçoamento Contínuo** — IN PROGRESS

- Refinamento de templates e referências
- Ajuste de comportamento do agente baseado em feedback
- Melhoria da adaptação por projeto

---

## Milestone 2 — Expansão do Marketplace

**Goal:** Adicionar novos plugins ao marketplace conforme necessidades da equipe.

### Features

**Novos Plugins** — PLANNED

- Plugins a definir conforme demanda da equipe
- Cada plugin segue a estrutura padrão (plugin.json, skills, hooks)

---

## Considerações Futuras

- Versionamento semântico automatizado dos plugins
- Métricas de adoção e uso pela equipe
- Possível abertura para comunidade externa (sem timeline definida)
