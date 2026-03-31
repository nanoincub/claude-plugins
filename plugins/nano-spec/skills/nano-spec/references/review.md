# Review

**Goal**: Garantir que o código está correto, limpo e eficiente antes de Security e Commit.

**Obrigatória antes de qualquer commit.** Durante ajustes, o agente detecta sinais no diff e pergunta ao dev se quer rodar agora ou deixar pro commit.

## Sinais de Review (baseados no diff)

O agente avalia o diff real após cada ajuste. Se ALGUM sinal é detectado, avisa o dev.

| # | Sinal | Descrição |
|---|-------|-----------|
| R1 | Lógica condicional/loops | Conditionals, loops, switch, ternários com lógica de negócio |
| R2 | Mutação de estado | State, variáveis de instância, stores, databases |
| R3 | Chamadas de API | Fetch, axios, HTTP calls, query builders |
| R4 | Controle de fluxo | Routing, middleware, error handling, redirects, guards |
| R5 | Estrutura de dados | Models, schemas, migrations, interfaces de API, DTOs |
| R6 | Mudança estrutural | Reorganização de módulos, imports, dependências entre arquivos |
| R7 | Volume com lógica | >5 arquivos com código (não docs/config) |
| R8 | Testes | Testes novos ou modificados |

**Sinais servem para perguntas antecipadas** — se detectados durante ajustes, o agente pergunta se quer rodar review agora. Mas review roda SEMPRE antes do commit, com ou sem sinais detectados.

## Fluxo Confirmativo

1. Após cada ajuste, o agente avalia o diff contra os sinais R1-R8
2. Se sinal detectado → avisar o dev: "Detectei [sinal]. Quer rodar review agora ou deixar pro commit?"
3. Se dev diz "agora" → rodar /review imediatamente
4. Se dev diz "depois" → anotar sinal como pendente
5. Antes do commit → rodar /review sobre diff acumulado (SEMPRE — obrigatório)

**Regra:** Não interromper para todo sinal trivial. Agrupar sinais relacionados e avisar uma vez.
**Escape hatch:** Na dúvida entre rodar ou skipar → RODAR.

---

## Fluxo

```
Execute concluído
    │
    ▼
1. /review (bugs, lógica, edge cases)
    │
    ├── Critical/Important → Corrigir → /review novamente (max 3x)
    ├── Suggestions → Registrar em STATE.md → Continuar
    └── Limpo → Continuar
    │
    ▼
2. /simplify (reuse, quality, efficiency)
    │
    ├── Issues → Corrigir → /simplify novamente (max 3x)
    └── Limpo → Avançar para Security
    │
    ▼
3. [Opcional] superpowers:verification-before-completion
    └── Evidência antes de claims (se superpowers instalado)
```

---

## Como invocar

O `/review` e `/simplify` são skills nativas do Claude Code (não são MCPs externos).
Para executá-los, o agente deve usar o **Skill tool**:

```
Skill tool: skill: "simplify"
```

Se `/review` não estiver disponível como skill, o agente DEVE fazer a revisão manualmente:
1. Ler todos os arquivos modificados
2. Analisar contra os critérios abaixo
3. Reportar findings no mesmo formato

**Nunca pular esta fase por não encontrar o comando.** A revisão manual é o fallback.

---

## Processo

### 1. Executar `/review` (ou revisão manual)

Analisa bugs, edge cases, convenções, performance, testes.

| Severidade | Ação |
|------------|------|
| **Critical/Important** | Corrigir. Re-executar `/review`. |
| **Suggestion** | Registrar em STATE.md (Deferred Ideas). Continuar. |
| **Limpo** | Avançar para `/simplify`. |

### 2. Executar `/simplify`

Analisa reuse, quality, efficiency em paralelo.

- Issues → Corrigir → Re-executar `/simplify`
- Limpo → Avançar para Security

### 3. Verificação formal (opcional)

Se `superpowers` instalado e dev optou por verificação nos defaults:
→ `superpowers:verification-before-completion` — exige evidência concreta (output de testes,
comandos executados) antes de claims de "pronto".

Se `subagent-driven-development` NÃO foi usado no Execute E escopo é Large/Complex:
→ perguntar se quer `superpowers:requesting-code-review` (subagent reviewer fresh).

---

## Limites

| Tool | Max re-runs | Após limite |
|------|-------------|-------------|
| /review | 3 | Escalar para dev com lista de issues |
| /simplify | 3 | Escalar para dev |

---

## Quick Mode

No Quick Mode (≤3 files): /review apenas (sem /simplify). Só executa quando sinais R1-R8 detectados e dev confirma commit.

---

## Tips

- Review é obrigatória antes de qualquer commit quando sinais são detectados — na dúvida, rodar
- Foque em Critical/Important primeiro
- Suggestions são para o futuro — anote em STATE.md
- Re-review após correção — correções podem introduzir problemas
