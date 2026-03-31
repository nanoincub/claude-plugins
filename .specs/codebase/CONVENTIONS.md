# Convenções de Código

## Convenções de Nomenclatura

**Diretórios de plugin:**
Padrão: kebab-case
Exemplos: `nano-spec`, `claude-plugins`

**Arquivos de skill:**
Padrão: SCREAMING_CASE para arquivos principais, kebab-case para referências
Exemplos: `SKILL.md`, `PROJECT.md`, `quick-mode.md`, `session-handoff.md`

**Arquivos de configuração:**
Padrão: kebab-case com extensão JSON
Exemplos: `marketplace.json`, `plugin.json`, `hooks.json`

**Hooks:**
Padrão: kebab-case sem extensão (Unix) ou `.cmd` para wrapper
Exemplos: `session-start`, `run-hook.cmd`

## Organização de Conteúdo

**Skills (SKILL.md):**
- Frontmatter YAML com `name`, `description`, `license`, `metadata`
- Seções com headers Markdown (`##`, `###`)
- Tabelas para comparações e matrizes de decisão
- Diagramas ASCII para fluxos visuais
- Links relativos para referências: `[nome](references/arquivo.md)`

**References:**
- Header `# Nome da Fase`
- Seção `**Trigger:**` com exemplos de ativação
- Seção `## Process` com passos numerados
- Seção `## Output` com template de saída
- Limite de tamanho documentado por arquivo

## Idioma

- Documentação técnica: Português (PT-BR) com acentuação correta
- Frontmatter e identificadores: Inglês
- Mensagens do agente: Português (PT-BR)
- Nomes de arquivo: Inglês

## Commits

- Formato: Conventional Commits (`tipo(escopo): descrição`)
- Scopes observados: `docs`, `fix`, `feat`
- Idioma do commit: Português para descrição
- Co-author: incluir quando gerado por IA

## Documentação

- READMEs em cada nível (raiz, plugin)
- Templates com limites de tokens definidos
- Estrutura `.specs/` como fonte de verdade para artefatos de planejamento
