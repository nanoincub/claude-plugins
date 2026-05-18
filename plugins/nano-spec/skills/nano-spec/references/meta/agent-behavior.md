# Comportamento do Agente

---

## Tom

- Direto, sem cerimônia. Dev como senior.
- Não explicar o processo a cada passo — só executar.
- Foco em resultado — menos palavras, mais código.

---

## Progress Tracker (OBRIGATÓRIO)

O agente DEVE exibir o progresso ao iniciar cada fase. Formato:

```
[SPECIFY] ← atual
──────────────────────────
✅ Gitflow gate
→  Specify
   Design
   Tasks
   Execute
   /simplify
   Docs
   Commit
```

**Regras:**
- Exibir **sempre** ao entrar em uma nova fase — sem exceção
- Fases concluídas: `✅`
- Fase atual: `→` (seta)
- Fases futuras: indentadas, sem marcador
- Fases puladas (por auto-sizing): omitir da lista
- No Quick Mode, usar o pipeline simplificado: Describe → Gitflow → Implement → Verify → /simplify → Docs → Commit
- Manter compacto — máximo 10 linhas. Não adicionar explicações ao tracker

---

## Gates não-negociáveis (HARD BLOCKs)

Aplicar **antes** de qualquer outro comportamento. Sem exceção, sem skip silencioso.

| Gate | Quando | Onde |
|---|---|---|
| **Project Init Gate** | Primeira ação da sessão, antes de qualquer feature | Se `.specs/project/` ou `.specs/codebase/` faltar → rodar [project-init.md](../init/project-init.md) + [roadmap.md](../init/roadmap.md) + [brownfield-mapping.md](../init/brownfield-mapping.md). NUNCA pular. |
| **git-flow-next instalado** | Primeira interação git da sessão | Ver [commit/gitflow.md](../commit/gitflow.md). Desativar só via `CLAUDE.md → Branching: Sem gitflow`. |
| **Baseline Test Gate** | Antes de criar branch de trabalho | Ver [execute/implement.md](../execute/implement.md#baseline-test-gate-entry-gate). RED → alerta P0 com [1] stop / [2] override + STATE.md entry. |
| **Iron Law (verification)** | Antes de qualquer claim "pronto/passou/feito" e antes do commit | Ver [verification.md](nano-disciplines:verification.md). Evidência fresh **nesta mensagem**, sem exceção. |
| **`/simplify` antes dos testes finais** | Pre-commit | Ordem fixa: `/simplify` → testes → commit. Inverter deixa janela para regressões silenciosas. |
| **Confirmação tipada `discard`** | Antes de descartar branch (opção 4 do nano-commit) | String exata `discard` (lowercase). Variações não contam. |

Se o agente se pegar prestes a pular qualquer um destes, **PARAR** e voltar ao gate.

---

## Hierarquia de orquestração

```
1. nanoincub-spec-driven (orquestrador master)
2. CLAUDE.md do projeto (overrides)
3. Disciplinas internas do nano-spec (TDD, debug, verification, subagents — em references/)
4. default system prompt
```

**Regra:** O nanoincub-spec-driven decide QUANDO e COMO aplicar cada disciplina técnica em cada fase. As disciplinas estão **internalizadas** nas references — sem dependência de plugins externos.

**Regra de artefatos:** Todo output de feature (specs, plans, context, design) vai para `.specs/features/YYYY-MM-DD-[feature]/`. Nunca espalhar artefatos em outros diretórios do projeto.

---

## Defaults opt-out

Ferramentas opcionais são apresentadas como DEFAULTS, não como perguntas individuais.

```
Escopo detectado: [X]
Defaults: [lista de tools para este escopo]
Opções disponíveis: [tools opcionais]
Quer ajustar algo? (Enter para seguir com defaults)
```

**Regras:**
- Uma pergunta, uma vez por feature
- Se dev respondeu "não" a uma opção, respeitar na sessão inteira
- Se CLAUDE.md tem preferências, seguir sem perguntar
- Nunca fazer 5 perguntas separadas — agrupar

---

## Limites de re-run

| Fase | Máximo de re-runs | Após limite |
|------|------------------|-------------|
| /simplify | 3 | Escalar para dev com lista de issues pendentes |

Escalar = mostrar ao dev o que resta e perguntar como proceder.

---

## Qualidade de código

A qualidade é garantida incrementalmente durante o Execute:

1. **Verificação executável por task** — após implementar cada task, avaliar se precisa de teste. Se sim, criar e rodar. Rodar testes do módulo afetado.
2. **/simplify após todas as tasks** — análise de reuse, qualidade e eficiência sobre o diff acumulado.
3. **Suite completa de testes** — o agente pede ao dev para rodar, informando o comando. Evita gasto de tokens em output extenso.
4. **Rastreabilidade spec → testes**: Testes DEVEM ser nomeados com IDs de requisito da spec.md (ex: `test_AUTH01_...`). Cada critério QUANDO/ENTÃO DEVE ter pelo menos um teste correspondente.
5. **Verificação formal obrigatória**: Antes de qualquer claim de "pronto", o agente DEVE ter executado o comando de verificação E lido o output. "Should pass" não é evidência.

### Review e Security (opt-in)

Review e Security estão **desativados por padrão**. Ativar via defaults opt-out no início da feature ou quando o dev pedir.

- Review: ver [review.md](../review/review.md)
- Security: ver [security.md](nano-disciplines:review/security.md) — recomendado usar skill de segurança específica da stack do projeto

### Subagentes (quando usados)

Se subagentes forem usados (ex: /simplify, subagent-driven-development), lembrar que são **coletores de dados, não juízes**. O agente principal é o responsável por classificar e filtrar findings.

> **Regra de ouro:** Se o agente principal não fez `Read` da linha de código citada, o achado **NÃO** entra no relatório.

Quando receber feedback de code review (externo ou de subagent), o agente DEVE seguir o protocolo em [receiving-feedback.md](nano-disciplines:review/receiving-feedback.md): READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT. NUNCA implementar feedback cegamente — verificar tecnicamente primeiro. Push back com raciocínio técnico se errado. Zero performative agreement ("você está totalmente certo!", "great point!", "thanks for...").

---

## Quando empurrar de volta

### Spec vaga
> "O que acontece quando [edge case]? Preciso de critério testável."

### Scope creep durante Execute
> "Isso parece fora do escopo da task. Anoto em Deferred Ideas?"

### Skip de /simplify ou testes
> "/simplify é obrigatório e dev deve rodar suite de testes antes do commit. Quer pular?"

Se dev confirmar skip → aceitar e registrar em STATE.md.

### Complexidade não reconhecida
> "Isso revelou mais de 5 steps. Recomendo criar tasks.md formal."

---

## Quando flexibilizar

| Situação | Ação |
|----------|------|
| Dev pede para pular fase | Aceitar, registrar em STATE.md |
| Projeto legado sem .specs/ | Criar estrutura incrementalmente |
| Hotfix urgente | Quick Mode com gates de qualidade |
| Override no CLAUDE.md | Seguir o override |

---

## Integração com skills

Superpowers é obrigatório (HARD BLOCK no SessionStart). Todas as skills abaixo são garantidas em qualquer sessão do nano-spec.

| Tarefa | Skill invocada |
|--------|----------------|
| Specify | [specify/specify.md](../specify/specify.md) — discovery (2-3 abordagens) + [spec-document-reviewer](../specify/spec-document-reviewer-prompt.md) para Large/Complex |
| Tasks | [tasks/tasks.md](../tasks/tasks.md) — TDD steps inline + [plan-document-reviewer](../tasks/plan-document-reviewer-prompt.md) para Large/Complex |
| TDD | [execute/tdd/tdd.md](nano-disciplines:execute/tdd/tdd.md) — Iron Law + RED→Verify RED→GREEN→Verify GREEN→REFACTOR |
| Debug | [execute/systematic-debugging/debug.md](nano-disciplines:execute/systematic-debugging/debug.md) — Iron Law "no fix without root cause" + 4 fases + 4.5 (questionar arquitetura) |
| Subagent por task | [execute/subagents/subagents.md](nano-disciplines:execute/subagents/subagents.md) — implementer → spec compliance review → code quality review (ordem obrigatória) |
| Dispatch paralelo | [execute/subagents/parallel-dispatch.md](nano-disciplines:execute/subagents/parallel-dispatch.md) — múltiplos subagents em uma mensagem + check de conflitos pós-retorno |
| Verificação formal | [verification.md](nano-disciplines:verification.md) — Iron Law: evidência fresh antes de qualquer claim |
| Code review | [review/code-review.md](nano-disciplines:review/code-review.md) — template em [code-reviewer-prompt.md](nano-disciplines:review/code-reviewer-prompt.md); Protocolo Dois-Eixos para pre-commit Large/Complex |
| Recepção de feedback | [review/receiving-feedback.md](nano-disciplines:review/receiving-feedback.md) — READ → UNDERSTAND → VERIFY → EVALUATE → RESPOND → IMPLEMENT |
| Finish branch | Skill [`nano-commit`](../../../nano-commit/SKILL.md) — seção "Pós-Commit: Fechamento de Branch" (4 opções estruturadas) |
| /simplify | Skill tool: `simplify` |
| Diagramas | mermaid-studio (se instalado, opcional) |
| Exploração de código | codenavi (se instalado, opcional) |

**Skills auxiliares opcionais** (mermaid-studio, codenavi): se não instaladas, o agente usa ferramentas built-in (inline mermaid, Grep/Glob/Read). As disciplinas técnicas (TDD, debug, verification, code review, subagents, parallel dispatch) são **internalizadas** nas references do nano-spec — sem dependência externa.

---

## Adaptação por projeto via CLAUDE.md

```markdown
## Processo
# Exemplo: CRUD simples
Processo Nano Incub com override:
- Design: sempre pular
- Security: opt-in (skill de segurança da stack)

# Exemplo: projeto crítico
Processo Nano Incub com override:
- Design: sempre executar
- Tasks: sempre executar
- TDD: sempre ativar
- Security: /security-review + relatório completo
```

/simplify e suite de testes nunca podem ser desativados — apenas ajustados em profundidade. Review e Security são opt-in.
