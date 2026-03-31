# Claude Code Plugins — Nano Incub

**Visão:** Marketplace interno de plugins para Claude Code que padroniza e automatiza fluxos de desenvolvimento da equipe Nano Incub através de processos estruturados com IA.

**Para:** Equipe interna da Nano Incub (desenvolvedores que usam Claude Code no dia a dia).

**Resolve:** Falta de padronização nos fluxos de desenvolvimento com IA — sem processo definido, cada dev interage com o Claude Code de forma diferente, sem quality gates, sem rastreabilidade de decisões, sem documentação estruturada.

## Goals

- Padronizar o processo de desenvolvimento com IA via spec-driven workflow (8 fases com quality gates)
- Garantir qualidade de código através de gates confirmativos obrigatórios (review + security antes de todo commit)
- Documentar decisões e artefatos automaticamente em `.specs/` como fonte de verdade
- Distribuir plugins automaticamente para toda a equipe via sincronização de organização

## Tech Stack

**Core:**

- Plataforma: Claude Code (CLI da Anthropic)
- Formato: Plugin marketplace para Claude Code
- Linguagem: Markdown (skills, docs) + Bash (hooks)
- Compatibilidade: Cross-platform (macOS, Linux, Windows via polyglot wrapper)

**Dependências:**

- `superpowers` (plugin externo, recomendado) — motor de TDD, debugging, worktrees, code review
- Claude Code Plugin System — marketplace, skills, hooks

## Scope

**v1 inclui:**

- Plugin `nano-spec` com processo spec-driven completo (8 fases)
- Auto-sizing por complexidade (Small/Medium/Large/Complex)
- Quality gates confirmativos (Review, Security, Commit)
- Sistema de sinais (R1-R8 review, S1-S11 security)
- Hook de SessionStart para injeção de contexto
- 21 guias de referência para cada fase e aspecto do processo
- Integração com superpowers como motor opcional

**Explicitamente fora de escopo:**

- Outros plugins além do nano-spec (foco atual é aperfeiçoar o nano-spec)
- Abertura do marketplace para comunidade externa
- Interface gráfica ou dashboard

## Constraints

- Depende da API de plugins do Claude Code (formato definido pela Anthropic)
- Licença CC-BY-4.0 (baseado em tlc-spec-driven v2.0.0 por Felipe Rodrigues)
