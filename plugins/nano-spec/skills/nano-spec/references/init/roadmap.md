# Criação de Roadmap

**Trigger:** "criar roadmap", "planejar features", "mapear fases do projeto"

## Processo

Baseado em `PROJECT.md`, decompor a visão em:

- Milestones (incrementos releasable)
- Features (capacidades user-facing)
- Tracking de status (planejado / em andamento / concluído)

## Output: `.specs/project/ROADMAP.md`

**Estrutura:**

```markdown
# Roadmap

**Milestone atual:** [nome do milestone]
**Status:** Planejamento | Em andamento | Concluído

---

## [Nome do Milestone 1]

**Objetivo:** [o que torna este milestone releasable]
**Alvo:** [data ou critério de conclusão]

### Features

**[Nome da Feature]** - STATUS

- [Capacidade 1]
- [Capacidade 2]
- [Capacidade 3]

**[Nome da Feature]** - STATUS

- [Capacidade 1]
- [Capacidade 2]

---

## [Nome do Milestone 2]

**Objetivo:** [o que este milestone agrega]

### Features

**[Nome da Feature]** - PLANEJADA
**[Nome da Feature]** - PLANEJADA

---

## Considerações Futuras

- [Capacidade potencial futura]
- [Capacidade potencial futura]
```

**Valores de status:**

- PLANEJADA: não iniciada
- EM ANDAMENTO: sendo implementada agora
- CONCLUÍDA: entregue e verificada

**Limite de tamanho:** 3.000 tokens (~1.800 palavras)

**Estratégia de atualização:**

- Marcar PLANEJADA → EM ANDAMENTO ao iniciar
- Marcar EM ANDAMENTO → CONCLUÍDA quando verificado
- Adicionar novos milestones conforme projeto evolui

**Validação:**

- Cada milestone tem outcome releasable claro?
- Features são capacidades user-facing?
- Status reflete a realidade atual?
