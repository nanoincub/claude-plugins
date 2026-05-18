# nano-disciplines

Caixa de ferramentas das disciplinas técnicas universais da Nano Incub. Não é orquestrador — é o conjunto reutilizável de práticas adotadas pela Nano Incub para qualquer plugin ou processo.

## Instalação

```bash
claude plugin install nano-disciplines@nano-incub
```

## O que tem

| Disciplina | Quando aplicar |
|---|---|
| **verification** (Iron Law) | Antes de qualquer claim "feito/passou/funciona" |
| **TDD** | Tasks com lógica — RED→GREEN→REFACTOR + anti-patterns de testing |
| **systematic-debugging** | Bug encontrado — 4 fases + defense-in-depth + root cause tracing |
| **subagents** | Large/Complex — fresh subagent per task + two-stage review |
| **parallel-dispatch** | Tasks independentes em paralelo + Protocolo Dois-Eixos |
| **code-review** | Review de PR/diff — 5 eixos |
| **receiving-feedback** | Recepção de review — zero performative agreement |
| **security** | Auditoria de segurança — OWASP + secrets + authZ |
| **validate** | UAT contra critérios de aceite |
| **code-analysis**, **coding-principles** | Pré-`/simplify` |
| **docs-update** | Sincronizar `.specs/codebase/` |

## Como usar

Plugins consumidores (como `nano-spec`) referenciam disciplinas via:

```
[verification.md](nano-disciplines:verification.md)
[tdd.md](nano-disciplines:execute/tdd/tdd.md)
```

Diretamente pelo dev: invocar a skill `nano-disciplines` e pedir a disciplina específica.

## Estrutura

```
plugins/nano-disciplines/
├── .claude-plugin/plugin.json
├── README.md
└── skills/nano-disciplines/
    ├── SKILL.md                  # índice das disciplinas
    └── references/
        ├── verification.md       # Iron Law
        ├── execute/
        │   ├── tdd/              # ciclo TDD + anti-patterns
        │   ├── systematic-debugging/   # debug 4 fases
        │   ├── subagents/        # subagent dispatch + parallel
        │   ├── code-analysis.md
        │   └── coding-principles.md
        ├── review/
        │   ├── code-review.md
        │   ├── code-reviewer-prompt.md
        │   ├── receiving-feedback.md
        │   ├── security.md
        │   └── validate.md
        └── docs/
            └── docs-update.md
```

## Versão

**1.0.0** — Extração das disciplinas internalizadas em `nano-spec` 4.0.0. Disponibilizadas como plugin standalone. `nano-spec` 5.0.0 depende deste plugin via HARD BLOCK.

Adaptadas do [superpowers](https://github.com/obra/superpowers) por Jesse Vincent (Anthropic). Licença CC-BY-4.0.
