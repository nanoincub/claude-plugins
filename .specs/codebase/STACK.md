# Tech Stack

**Analisado:** 2026-03-31

## Core

- Plataforma: Claude Code (CLI da Anthropic para Claude)
- Formato: Plugin Marketplace (`$schema: anthropic.com/claude-code/marketplace.schema.json`)
- Linguagens: Markdown (skills, documentação), Bash (hooks)
- Compatibilidade: macOS, Linux, Windows (via polyglot wrapper batch/bash)

## Plugin System

- **Skills:** Arquivos `.md` com frontmatter YAML que definem prompts estruturados carregados sob demanda pelo Claude Code
- **Hooks:** Scripts executados em eventos do Claude Code (ex: `SessionStart`) configurados via `hooks.json`
- **Marketplace:** Repositório GitHub com `marketplace.json` que registra plugins disponíveis

## Dependências

- `superpowers` (plugin externo, `claude-plugins-official`) — motor opcional que fornece TDD, debugging, worktrees, code review, brainstorming, writing-plans
- Git — versionamento e distribuição via GitHub
- Bash — execução de hooks (no Windows via Git Bash)

## Ferramentas de Desenvolvimento

- Git: versionamento e distribuição
- Claude Code: plataforma de execução e teste dos plugins
- GitHub: hospedagem do marketplace e sincronização com organizações
