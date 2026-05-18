# State Management

**Purpose:** Persistent memory across sessions - decisions, blockers, learnings.

## Structure

**Output:** `.specs/project/STATE.md`

```markdown
# State

**Last Updated:** [ISO timestamp]
**Current Work:** [Feature name] - [Task identifier]

---

## Recent Decisions (Last 60 days)

### AD-[NNN]: [Decision title] ([date])

**Decision:** [What was decided]
**Reason:** [Why this choice]
**Trade-off:** [What was sacrificed]
**Impact:** [How this affects implementation]

### AD-[NNN]: [Decision title] ([date])

[Same structure]

---

## Active Blockers

### B-[NNN]: [Blocker description]

**Discovered:** [Date]
**Impact:** [Severity and scope]
**Workaround:** [Temporary solution if available]
**Resolution:** [Path to permanent fix]

---

## Lessons Learned

### L-[NNN]: [Learning description]

**Context:** [Situation that occurred]
**Problem:** [What went wrong]
**Solution:** [How it was resolved]
**Prevents:** [What this knowledge prevents in future]

---

## Quick Tasks Completed

| #   | Description              | Date   | Commit | Status  |
| --- | ------------------------ | ------ | ------ | ------- |
| 001 | [Quick task description] | [date] | [hash] | ✅ Done |

---

## Deferred Ideas

Ideas captured during work that belong in future features or phases. Prevents scope creep while preserving good ideas.

- [ ] [Idea description] — Captured during: [feature/phase]
- [ ] [Idea description] — Captured during: [feature/phase]

---

## Todos

Capture in-progress thoughts and action items that don't fit in active tasks.

- [ ] [TODO: action item]
- [ ] [TODO: action item]
```

## When to Update — Triggers automáticos

Eventos que **DISPARAM** atualização do STATE.md automaticamente (não confiar na memória do agente — escrever no momento do evento):

| Evento (trigger) | Origem | Ação |
|---|---|---|
| Override do Baseline Test Gate aceito | [execute/implement.md](../execute/implement.md#baseline-test-gate-entry-gate) | Add entrada estruturada com base SHA + falhas + responsável + plano |
| `debug.md` Fase 4 fechou com fix | [execute/systematic-debugging/debug.md](nano-disciplines:execute/systematic-debugging/debug.md) | Add L-[NNN] (lesson learned com root cause + fix) |
| `debug.md` Fase 4.5 disparou (3 fixes falharam) | [execute/systematic-debugging/debug.md](nano-disciplines:execute/systematic-debugging/debug.md) | Add B-[NNN] + nota arquitetural |
| Scope guardrail no Execute disparou (ideia descartada) | [execute/implement.md](../execute/implement.md) step 8 | Add a Deferred Ideas |
| Bug encontrado durante outra task (não relacionado) | [execute/implement.md](../execute/implement.md) árvore de decisão | Add B-[NNN] + retomar task original |
| Decisão arquitetural sem ADR formal mas relevante | Design ou Execute | Add AD-[NNN] |
| Quick task completou | [quick-mode/quick-mode.md](../quick-mode/quick-mode.md) | Add row em Quick Tasks |
| Migração de pastas legadas recusada pelo dev | SKILL.md migração | Add nota "migração recusada nesta sessão" |
| Override de qualquer HARD BLOCK | [meta/agent-behavior.md](agent-behavior.md) | Add entrada documentando override + razão |
| Pausar sessão (handoff) | [meta/session-handoff.md](session-handoff.md) | Update "Last Updated" + "Current Work" + checkpoint detalhado |
| Sessão terminou | Sessão | Update "Last Updated" + "Current Work" |

### Eventos manuais (dev pede explicitamente)

| Evento | Ação |
|---|---|
| Dev diz "registra essa decisão" | Add AD-[NNN] |
| Dev diz "fica como deferred" | Add a Deferred Ideas |
| Dev diz "anote como lição" | Add L-[NNN] |
| Dev diz "isso é um blocker" | Add B-[NNN] |

**Regra de ouro:** se o agente está prestes a continuar para a próxima ação mas o evento merece persistência, **escrever no STATE.md ANTES** de prosseguir. Não acumular vários eventos para "atualizar no final" — risco de esquecer.

## Size Management (Hybrid Strategy)

**Zones:**

- 🟢 <7k tokens: No action
- 🟡 7-10k tokens: Footer note "STATE.md at [X]k. Cleanup recommended."
- 🔴 >10k tokens: Active prompt "STATE.md critical ([X]k). Cleanup now?"

**Cleanup process:**

- Move decisions >60 days to STATE-ARCHIVE.md
- Keep only active blockers
- Preserve recent learnings (<60 days)

**Validation:**

- Decisions have clear rationale?
- Blockers include resolution path?
- Learnings are actionable?

---

## Preferences

Track user-facing behavioral state in STATE.md:

```markdown
## Preferences

**Model Guidance Shown:** [ISO date or "never"]
```

**Update when:**

| Event                       | Action                   |
| --------------------------- | ------------------------ |
| First model tip given       | Set date                 |
| User acknowledges/dismisses | Keep date (don't repeat) |

This prevents repetitive suggestions while maintaining natural, helpful behavior.
