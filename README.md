# Nano Incub — Claude Code Plugins

Marketplace interno de plugins da Nano Incub para Claude Code.

## Plugins disponíveis

| Plugin | Descrição | Versão |
|--------|-----------|--------|
| **nano-spec** | Processo Spec-Driven com 8 fases e quality gates confirmativos | 2.5.0 |

## Instalação do marketplace

Na interface do Claude Code (Organização → Plugins → Adicionar plugins → Sincronizar do GitHub):

1. Selecionar o repositório `nano-incub/claude-plugins`
2. Ativar sincronização automática
3. Criar

Após sincronizar, os plugins ficam disponíveis para todos os membros da organização.

## Adicionando novos plugins

Editar `.claude-plugin/marketplace.json` e adicionar uma entrada no array `plugins`:

```json
{
  "name": "nome-do-plugin",
  "description": "Descrição do plugin",
  "category": "development",
  "source": {
    "source": "git",
    "url": "https://github.com/org/repo.git",
    "ref": "main"
  },
  "homepage": "https://github.com/org/repo"
}
```
