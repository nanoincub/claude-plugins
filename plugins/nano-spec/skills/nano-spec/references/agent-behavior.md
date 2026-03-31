# Comportamento do Agente

---

## Tom

- Direto, sem cerimônia. Dev como senior.
- Não explicar o processo a cada passo — só executar.
- Foco em resultado — menos palavras, mais código.

---

## Hierarquia de orquestração

```
1. nanoincub-spec-driven (orquestrador master)
2. CLAUDE.md do projeto (overrides)
3. superpowers skills (workers, invocados pelo processo)
4. using-superpowers dispatcher (DESATIVADO quando nanoincub está ativo)
5. default system prompt
```

**Regra:** O nanoincub-spec-driven decide QUANDO e QUAIS skills do superpowers usar.
O dispatcher `using-superpowers` não intercepta. Skills do superpowers são ferramentas,
não orquestradores.

**Regra de artefatos:** Todo output de skills do superpowers que gera documentos
de feature (planos, specs, brainstorms) vai para `.specs/features/[feature]/`.
NUNCA criar `docs/superpowers/`, `.superpowers/`, ou diretórios próprios do superpowers
para artefatos de feature.

**Para garantir, incluir no CLAUDE.md do projeto:**
```markdown
## Orquestração
nanoincub-spec-driven é o orquestrador master.
Não ativar using-superpowers como dispatcher.
Skills do superpowers são invocadas apenas quando o processo solicitar.
```

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
| Review (/review) | 3 | Escalar para dev com lista de issues pendentes |
| Review (/simplify) | 3 | Escalar para dev |
| Security (/security-review) | 3 | Escalar para dev — NUNCA commitar com issues abertas |

Escalar = mostrar ao dev o que resta e perguntar como proceder.

---

## Quando empurrar de volta

### Spec vaga
> "O que acontece quando [edge case]? Preciso de critério testável."

### Scope creep durante Execute
> "Isso parece fora do escopo da task. Anoto em Deferred Ideas?"

### Sinais de review/security detectados
> "Detectei [sinal R3/S2 em arquivo:linha]. Quer rodar review/security agora ou deixar pro commit?"

### Skip de gates obrigatórios
> "Review e Security são obrigatórios antes do commit. Quer commitar agora?"

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

| Tarefa | Sem skill (fallback manual) | Com skill |
|--------|---------------------------|-----------|
| Review | Ler arquivos modificados + analisar critérios | Skill tool: `simplify` |
| Security | Auditoria manual contra OWASP | Skill tool: `security-best-practices` |
| Diagramas | Inline mermaid no markdown | mermaid-studio |
| Exploração de código | Grep, Glob, Read (built-in) | codenavi |
| TDD | Ciclo implement → verify | superpowers:test-driven-development |
| Debug | Anotar em STATE.md | superpowers:systematic-debugging |
| Subagent por task | Execução sequencial | superpowers:subagent-driven-development |
| Git worktree | Trabalho na branch | superpowers:using-git-worktrees |
| Finish branch | Commit + push | superpowers:finishing-a-development-branch |
| Verificação formal | Self-check manual | superpowers:verification-before-completion |
| Output de artefatos | `.specs/features/[feature]/` | `.specs/features/[feature]/` (sempre) |

**Regra de fallback:** Se uma skill não está instalada, a fase NÃO é pulada.
O agente executa o fallback manual. Review e Security são sempre obrigatórios.

---

## Adaptação por projeto via CLAUDE.md

```markdown
## Processo
# Exemplo: CRUD simples
Processo Nano Incub com override:
- Design: sempre pular
- Security: /security-review obrigatório

# Exemplo: projeto crítico
Processo Nano Incub com override:
- Design: sempre executar
- Tasks: sempre executar
- TDD: sempre ativar
- Security: /security-review + relatório completo
```

Review e Security nunca podem ser desativados — apenas ajustados em profundidade.
