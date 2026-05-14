# Review (opt-in)

**Desativado por padrão.** Ativar via defaults opt-out no início da feature ou quando o dev pedir explicitamente.

**Goal**: Garantir que o código está correto, limpo e eficiente.

**Nota:** A qualidade de código é garantida por /simplify (obrigatório) + verificação executável por task. Esta fase adicional é recomendada para projetos críticos ou quando o dev preferir uma camada extra de revisão.

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

**Sinais servem para perguntas antecipadas** — quando review está ativado, se detectados durante ajustes, o agente pergunta se quer rodar review agora.

## Fluxo Confirmativo

1. Após cada ajuste, o agente avalia o diff contra os sinais R1-R8
2. Se sinal detectado → avisar o dev: "Detectei [sinal]. Quer rodar review agora ou deixar pro commit?"
3. Se dev diz "agora" → rodar /review imediatamente
4. Se dev diz "depois" → anotar sinal como pendente
5. Antes do commit → rodar /review sobre diff acumulado (se review ativado)

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
    └── Limpo → Avançar
    │
    ▼
3. verification-before-completion (obrigatório)
    └── Invocar superpowers:verification-before-completion
        └── Evidência FRESH antes de qualquer claim de "pronto"
    │
    ▼
4. [Large/Complex] requesting-code-review (subagent reviewer)
    └── Despachar superpowers:requesting-code-review com BASE_SHA e HEAD_SHA
    │
    ▼
Commit
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

### 3. Verificação Formal (obrigatório)

**Iron Law: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"**

O agente DEVE invocar `superpowers:verification-before-completion`. Antes de qualquer claim de "pronto", o agente DEVE:

1. Identificar o comando que prova o claim (testes, build, lint, etc.)
2. Executar o comando FRESH — nunca reusar output anterior
3. Ler o output completo — não assumir sucesso
4. Verificar se o output confirma o claim — evidência concreta

**Red flags que PARAM o agente** (não prosseguir sem corrigir):
- Usar "should", "probably", "seems to" em claims de completude
- Expressar satisfação antes de verificar
- Referenciar output de execuções anteriores como prova

**Quando superpowers NÃO detectado** — self-check manual:
- Rodar testes relevantes e verificar output antes de claims
- Confirmar que build/lint passam sem erros
- O agente NÃO pode declarar "pronto" sem ter executado e verificado

### 3.1. Code Review por Subagente (obrigatório para Large/Complex com superpowers)

Quando superpowers ativo E escopo é Large/Complex, o agente DEVE despachar `superpowers:requesting-code-review` — um subagent code-reviewer fresh que avalia o código sem contexto da sessão, trazendo perspectiva independente.

Parâmetros obrigatórios:
- **BASE_SHA** — commit base antes das mudanças
- **HEAD_SHA** — commit head com as mudanças

O reviewer analisa o diff isoladamente, sem acesso ao histórico de conversa — isso garante avaliação imparcial. O agente principal DEVE verificar os achados do reviewer conforme seção 4 abaixo.

### 4. Verificação de achados de subagentes

> **Regra de ouro:** Se o agente principal não fez `Read` da linha de código citada, o achado **NÃO** entra no relatório. Nenhuma exceção.

Quando subagentes (Agent tool) ou skills externas retornam findings de review, o agente principal **DEVE** verificar cada um antes de reportar ou corrigir:

- [ ] `Read` do arquivo e linha exata — o código existe como descrito?
- [ ] `git diff` — o issue foi introduzido nesta branch ou é pré-existente?
- [ ] Contexto de framework — o framework já mitiga? (escape de templates, CSRF automático, ORM com prepared statements)
- [ ] Contexto de domínio — é decisão intencional? Na dúvida, perguntar ao dev

**Prompts para subagentes de review** devem instruir: "Retorne conteúdo de arquivos e observações factuais. NÃO classifique severidade nem recomende correções."

**Gate de aprovação:** Após verificação, apresentar achados verificados ao dev com evidência (arquivo, linha, código real, motivo). O dev é o juiz final — decide se o achado é realmente um issue e como corrigir. O agente **NÃO** implementa correções sem aprovação.

**Separação no relatório:**
- **Issues introduzidos pela branch** — escopo do review, ação requerida
- **Observações pré-existentes** (opcional) — seção separada, fora do escopo da branch

Ver [agent-behavior.md](agent-behavior.md) para regras gerais de confiabilidade e padrões de falso positivo.

### 5. Recepção de Feedback

Quando superpowers ativo, invocar `superpowers:receiving-code-review`. Protocolo: READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT. NUNCA implementar feedback cegamente — verificar tecnicamente primeiro. Push back com raciocínio técnico se errado.

---

## Protocolo Dois-Eixos (Large/Complex pré-commit)

Adaptado de `review` (matpocock-skills). **Substitui** o `requesting-code-review` da seção 3.1 em features Large/Complex pré-commit — não rodar ambos (o Dois-Eixos é o `requesting-code-review` particionado em dois eixos especializados).

| Eixo | O que verifica | Fonte |
|------|----------------|-------|
| **Standards** | Código segue convenções do repo? | `.specs/codebase/CONVENTIONS.md`, `CLAUDE.md`, `react-best-practices` (se aplicável) |
| **Spec** | Código implementa fielmente o que foi pedido? | `.specs/features/YYYY-MM-DD-[feature]/spec.md` (acceptance criteria + `[FEAT]-XX` IDs), `tasks.md` (tudo marcado?) |

### Quando ativar

- **Complex** — sempre, antes de `nano-commit` (no slot do `requesting-code-review`)
- **Large** — default; dev pode pular explicitamente
- **Medium/Small/Quick** — skip (manter `requesting-code-review` padrão se ativo)

### Fluxo

Roda no **step 3.1 do fluxo principal** (substitui `requesting-code-review` em Large/Complex):

1. Capturar fixed point: `git merge-base HEAD main` (sem perguntar ao dev)
2. Despachar 2 sub-agentes em paralelo via `superpowers:dispatching-parallel-agents`
3. Aplicar a regra de verificação da **seção 4** abaixo: `Read` da linha citada antes de reportar; descartar achados que não conferem
4. Apresentar relatório dois-eixos; dev decide endereçar/pular/discutir

### Prompt template — Standards agent

```
Você é reviewer de Standards. NÃO classifique severidade nem proponha fixes
(regra geral da seção 4 de review.md).

Inputs:
- Diff: <output de `git diff <merge-base>...HEAD`>
- Convenções: .specs/codebase/CONVENTIONS.md
- Regras gerais: CLAUDE.md (raiz do projeto)

Para cada violação detectada, retorne arquivo + linha + convenção violada
(cite a regra textualmente) + trecho de código real (não parafraseado).
NÃO inclua observações pré-existentes (fora do diff).
```

### Prompt template — Spec agent

```
Você é reviewer de Spec compliance. NÃO classifique severidade nem proponha fixes
(regra geral da seção 4 de review.md).

Inputs:
- Diff: <output de `git diff <merge-base>...HEAD`>
- Spec: .specs/features/YYYY-MM-DD-[feature]/spec.md
- Tasks: .specs/features/YYYY-MM-DD-[feature]/tasks.md

Para cada [FEAT]-XX da spec, verifique se o critério QUANDO/ENTÃO está
implementado no diff e se as tasks marcadas como done realmente entregaram
o comportamento. Retorne factualmente gaps e contradições com arquivo + linha.
```

### Formato do relatório

```markdown
## Review pré-commit — dois eixos

### Eixo Standards
- [arquivo:linha] — [convenção violada] — [trecho real]

### Eixo Spec
- [FEAT]-XX — [gap entre acceptance criteria e implementação] — [arquivo:linha]

**Decisão:** endereçar antes do commit? (sim / pular / discutir)
```

---

## Limites

| Tool | Max re-runs | Após limite |
|------|-------------|-------------|
| /review | 3 | Escalar para dev com lista de issues |
| /simplify | 3 | Escalar para dev |

---

## Quick Mode

No Quick Mode (≤3 files): /review só executa quando ativado e dev confirma. /simplify continua obrigatório (conforme quick-mode.md).

---

## Tips

- Review é opt-in — ativar via defaults ou quando dev pedir
- Foque em Critical/Important primeiro
- Suggestions são para o futuro — anote em STATE.md
- Re-review após correção — correções podem introduzir problemas
