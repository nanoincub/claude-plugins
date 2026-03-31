# Infraestrutura de Testes

## Situação Atual

Este projeto **não possui testes automatizados** no sentido tradicional (unit, integration, E2E). Isso é esperado dado que o projeto é composto inteiramente de Markdown (skills, documentação) e Bash (hooks), sem código de aplicação.

## Validação

A validação do projeto acontece de forma diferente:

### Validação de Skills

- **Manual:** Testar invocando a skill via Claude Code e verificando o comportamento
- **Critérios:** A skill é carregada corretamente, o auto-sizing funciona, os gates são respeitados

### Validação de Hooks

- **Manual:** Iniciar uma sessão do Claude Code e verificar se o contexto é injetado
- **Cross-platform:** Testar o wrapper `run-hook.cmd` em macOS/Linux e Windows

### Validação de Estrutura

- **Schema:** `marketplace.json` e `plugin.json` seguem schemas definidos pela Anthropic
- **Links:** Referências em SKILL.md apontam para arquivos que existem em `references/`

## Comandos

Não há comandos de teste configurados. A validação é feita via uso direto no Claude Code.

## Oportunidades

- Validação automática de links internos (referências em SKILL.md → references/)
- Validação de schema JSON (marketplace.json, plugin.json)
- Linting de Markdown para consistência
