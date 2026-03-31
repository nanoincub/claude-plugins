# Integrações Externas

## Claude Code Plugin System

**Serviço:** Sistema de plugins do Claude Code (Anthropic)
**Propósito:** Plataforma de distribuição e execução dos plugins
**Implementação:** `marketplace.json` + `plugin.json` seguindo schemas da Anthropic
**Configuração:** Registro via `claude plugin marketplace add`
**Autenticação:** Via organização do Claude Code (sincronização automática)

### Pontos de integração

- **Marketplace registration:** `.claude-plugin/marketplace.json` registra plugins disponíveis
- **Plugin metadata:** `.claude-plugin/plugin.json` em cada plugin define nome, descrição, autor
- **Skill loading:** `skills/[name]/SKILL.md` é carregado via `Skill` tool do Claude Code
- **Hook execution:** `hooks/hooks.json` configura eventos; scripts são executados pelo Claude Code

## Superpowers (Plugin Externo)

**Serviço:** Plugin `superpowers` do marketplace `claude-plugins-official`
**Propósito:** Motor de ferramentas que o nano-spec orquestra (TDD, debug, worktrees, code review, brainstorming, writing-plans)
**Implementação:** Integração via delegação de skills — nano-spec invoca skills do superpowers quando disponíveis
**Configuração:** `claude plugin install superpowers@claude-plugins-official`

### Mapping de skills

| Skill superpowers | Fase nano-spec | Uso |
|---|---|---|
| `brainstorming` | Specify, Design | Exploração de requisitos e decisões |
| `writing-plans` | Tasks | Geração de plano de implementação |
| `test-driven-development` | Execute | TDD no ciclo de implementação |
| `systematic-debugging` | Execute | Debug estruturado |
| `using-git-worktrees` | Execute | Isolamento de trabalho |
| `dispatching-parallel-agents` | Execute | Paralelização de tasks |
| `verification-before-completion` | Review | Verificação antes de finalizar |
| `finishing-a-development-branch` | Commit | Finalização de branch |

## GitHub

**Serviço:** GitHub (hospedagem de repositório)
**Propósito:** Distribuição do marketplace e sincronização com organizações
**Implementação:** Repositório `nanoincub/claude-plugins`
**Configuração:** Sincronização automática via interface de organização do Claude Code

## Context7 MCP (Opcional)

**Serviço:** Context7 MCP Server
**Propósito:** Consulta de documentação atualizada de bibliotecas durante o Knowledge Verification Chain do nano-spec
**Implementação:** Usado no Step 3 da chain de verificação (após codebase e project docs)
**Configuração:** Disponível como MCP server no Claude Code
