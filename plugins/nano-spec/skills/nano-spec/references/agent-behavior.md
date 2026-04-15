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
| /simplify | 3 | Escalar para dev com lista de issues pendentes |

Escalar = mostrar ao dev o que resta e perguntar como proceder.

---

## Qualidade de código

A qualidade é garantida incrementalmente durante o Execute:

1. **Verificação executável por task** — após implementar cada task, avaliar se precisa de teste. Se sim, criar e rodar. Rodar testes do módulo afetado.
2. **/simplify após todas as tasks** — análise de reuse, qualidade e eficiência sobre o diff acumulado.
3. **Suite completa de testes** — o agente pede ao dev para rodar, informando o comando. Evita gasto de tokens em output extenso.

### Review e Security (opt-in)

Review e Security estão **desativados por padrão**. Ativar via defaults opt-out no início da feature ou quando o dev pedir.

- Review: ver [review.md](review.md)
- Security: ver [security.md](security.md) — recomendado usar skill de segurança específica da stack do projeto

### Subagentes (quando usados)

Se subagentes forem usados (ex: /simplify, subagent-driven-development), lembrar que são **coletores de dados, não juízes**. O agente principal é o responsável por classificar e filtrar findings.

> **Regra de ouro:** Se o agente principal não fez `Read` da linha de código citada, o achado **NÃO** entra no relatório.

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

| Tarefa | Sem skill (fallback manual) | Com skill |
|--------|---------------------------|-----------|
| /simplify | Ler diff + analisar reuse/quality/efficiency | Skill tool: `simplify` |
| Review (opt-in) | Ler arquivos modificados + analisar critérios | Skill tool: `simplify` |
| Security (opt-in) | Auditoria manual contra OWASP | Skill de segurança da stack |
| Diagramas | Inline mermaid no markdown | mermaid-studio |
| Exploração de código | Grep, Glob, Read (built-in) | codenavi |
| TDD | Ciclo implement → verify | superpowers:test-driven-development |
| Debug | Anotar em STATE.md | superpowers:systematic-debugging |
| Subagent por task | Execução sequencial | superpowers:subagent-driven-development |
| Git worktree | Trabalho na branch | superpowers:using-git-worktrees |
| Finish branch | Commit + push | superpowers:finishing-a-development-branch |
| Verificação formal | Self-check manual | superpowers:verification-before-completion |
| Output de artefatos | `.specs/features/[feature]/` | `.specs/features/[feature]/` (sempre) |

**Regra de fallback:** Se a skill `simplify` não está instalada, o agente executa o fallback manual (ler diff + analisar). /simplify é sempre obrigatório antes do commit.

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
