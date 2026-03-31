# Nano Incub — Claude Code Plugins

Marketplace interno de plugins da Nano Incub para Claude Code.

## Plugins disponíveis

| Plugin | Descrição | Versão |
|--------|-----------|--------|
| **nano-spec** | Processo Spec-Driven com 8 fases e quality gates confirmativos | 2.5.0 |

## Instalação

### Via terminal (recomendado)

Registre o marketplace (uma vez):

```bash
claude plugin marketplace add nanoincub/claude-plugins
```

Instale o plugin desejado:

```bash
claude plugin install nano-spec@nanoincub
```

### Via organização (automático)

Na interface do Claude Code (Organização → Plugins → Adicionar plugins → Sincronizar do GitHub):

1. Selecionar o repositório `nanoincub/claude-plugins`
2. Ativar sincronização automática
3. Criar
4. Alterar acesso para "Installed by default"

Após sincronizar, o plugin é instalado automaticamente para todos os membros.

## Adicionando novos plugins

1. Criar o plugin em `plugins/nome-do-plugin/` com a estrutura:

```
plugins/nome-do-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── ...
└── hooks/ (opcional)
```

2. Adicionar entrada em `.claude-plugin/marketplace.json`:

```json
{
  "name": "nome-do-plugin",
  "description": "Descrição do plugin",
  "category": "development",
  "source": "./plugins/nome-do-plugin",
  "homepage": "https://github.com/nanoincub/nome-do-plugin"
}
```

3. Fazer push — a sincronização automática distribui para a organização.
