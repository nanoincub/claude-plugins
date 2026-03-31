# Claude Code Plugins — Nano Incub

Marketplace interno de plugins para Claude Code. Foco atual: aperfeiçoamento do nano-spec.

## Stack

- Plataforma: Claude Code (Anthropic)
- Formato: Plugin Marketplace
- Linguagens: Markdown (skills), Bash (hooks)
- Dependência: superpowers (recomendado)

## Convenções

- Idioma: PT-BR (com acentuação correta)
- Commits: Conventional Commits em português — `tipo(escopo): descrição`
- Scopes: `docs`, `fix`, `feat`
- Nomes de arquivo: inglês, kebab-case
- Skills: SKILL.md (SCREAMING_CASE), references em kebab-case

## Referência .specs/

Documentação estruturada do projeto. Consultar antes de tomar decisões.

### Projeto
- `.specs/project/PROJECT.md` — Visão, goals, stack, scope
- `.specs/project/ROADMAP.md` — Features planejadas e milestones

### Codebase
- `.specs/codebase/STACK.md` — Stack tecnológica e dependências
- `.specs/codebase/ARCHITECTURE.md` — Padrões arquiteturais e fluxo de dados
- `.specs/codebase/CONVENTIONS.md` — Convenções de código e naming
- `.specs/codebase/STRUCTURE.md` — Estrutura de diretórios
- `.specs/codebase/TESTING.md` — Infraestrutura e padrões de teste
- `.specs/codebase/INTEGRATIONS.md` — Integrações externas
- `.specs/codebase/CONCERNS.md` — Tech debt, riscos e áreas frágeis

### Features (criados por feature via nano-spec)
- `.specs/features/[feature]/spec.md` — Requisitos e critérios de aceite
- `.specs/features/[feature]/design.md` — Arquitetura e componentes
- `.specs/features/[feature]/tasks.md` — Tasks atômicas de implementação
