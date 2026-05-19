# Inicialização de Projeto

**Trigger:** "inicializar projeto", "setup projeto", "começar projeto novo"

## Processo

Extrair a visão do projeto via Q&A iterativo (máximo 3-5 perguntas por mensagem):

**Perguntas essenciais:**

1. O que você está construindo?
2. Para quem é, e que problema resolve?
3. Qual stack tecnológica (se já decidida)?
4. O que entra no v1? O que está explicitamente fora?
5. Restrições críticas? (prazo, técnicas, recursos)

**Parar quando:** entendimento claro de visão, objetivos e limites.

## Output: `.specs/project/PROJECT.md`

**Estrutura:**

```markdown
# [Nome do Projeto]

**Visão:** [descrição em 1-2 frases]
**Para:** [usuários-alvo]
**Resolve:** [problema central endereçado]

## Objetivos

- [Objetivo primário com métrica de sucesso mensurável]
- [Objetivo secundário com métrica de sucesso mensurável]

## Stack Tecnológica

**Core:**

- Framework: [nome + versão]
- Linguagem: [nome + versão]
- Banco de dados: [nome]

**Dependências-chave:** [3-5 bibliotecas/frameworks críticos]

## Escopo

**v1 inclui:**

- [Capacidade central 1]
- [Capacidade central 2]
- [Capacidade central 3]

**Explicitamente fora de escopo:**

- [O que NÃO está sendo construído]
- [O que NÃO está sendo construído]

## Restrições

- Prazo: [se aplicável]
- Técnicas: [se aplicável]
- Recursos: [se aplicável]
```

**Limite de tamanho:** 2.000 tokens (~1.200 palavras)

**Validação:**

- Visão clara em 1-2 frases?
- Objetivos têm métricas mensuráveis?
- Limites de escopo explícitos?
