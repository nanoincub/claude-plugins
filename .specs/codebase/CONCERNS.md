# Concerns

## Manutenção

### Tamanho total do processo (SKILL.md + 21 references)

**Evidência:** O SKILL.md tem ~370 linhas, mas referencia 21 arquivos em `references/` que totalizam ~3100 linhas. O hook de SessionStart injeta apenas ~5KB.
**Risco:** Baixo — o design lazy-loading (hook leve + SKILL.md + references sob demanda) mantém o consumo de contexto controlado.
**Abordagem de correção:** Já mitigado pelo design atual. Monitorar se o crescimento continuar.

## Validação

### Ausência de validação automatizada

**Evidência:** Não há testes automatizados, linting, ou validação de schema.
**Risco:** Baixo — o projeto é pequeno e de documentação, mas links quebrados ou JSON inválido podem passar despercebidos.
**Abordagem de correção:** Adicionar validação de links internos e schema JSON como CI básico.

## Compatibilidade

### Dependência do formato de plugin do Claude Code

**Evidência:** `marketplace.json` e `plugin.json` seguem schemas definidos pela Anthropic que podem mudar.
**Risco:** Médio — breaking changes no formato de plugin podem exigir atualizações.
**Abordagem de correção:** Monitorar changelog do Claude Code e manter schemas atualizados.
