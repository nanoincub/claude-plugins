# Security (opt-in)

**Desativado por padrão.** Ativar via defaults opt-out no início da feature ou quando o dev pedir explicitamente.

**Goal**: Detectar vulnerabilidades de segurança antes do commit.

**Nota:** Cada linguagem e projeto tem necessidades de segurança específicas. Recomendado usar uma skill de segurança dedicada à stack do projeto (ex: OWASP para web, SAST para APIs) em vez de auditoria genérica. Se ativada, esta fase funciona como descrito abaixo.

## Sinais de Security (baseados no diff + keywords)

O agente avalia o diff real após cada ajuste. Se ALGUM sinal é detectado, avisa o dev.

| # | Sinal | Descrição |
|---|-------|-----------|
| S1 | Input de usuário | Forms, request params, headers, file uploads, query strings |
| S2 | Autenticação | Login, logout, token, session, JWT, OAuth |
| S3 | Autorização | Roles, permissions, policies, guards, middleware de acesso |
| S4 | Dados sensíveis | PII, passwords, credentials, dados financeiros |
| S5 | Criptografia | Hashing, encryption, certificates, secrets |
| S6 | Integração externa | APIs de terceiros, webhooks, URLs dinâmicas |
| S7 | Database queries | Raw SQL, query builders dinâmicos |
| S8 | Renderização dinâmica | `{!! !!}`, `v-html`, `dangerouslySetInnerHTML`, templates sem escape |
| S9 | Config de segurança | CORS, CSP, rate limiting, headers, `.env` |
| S10 | Keywords no diff | `password\|token\|auth\|secret\|query\|exec\|eval\|cookie\|session\|permission\|role\|admin\|encrypt\|hash` |
| S11 | Nova dependência | Pacote novo ou upgrade major em composer.json/package.json |

**Sinais servem para perguntas antecipadas** — quando security está ativado, se detectados durante ajustes, o agente pergunta se quer rodar security agora.

## Fluxo Confirmativo

1. Após cada ajuste, o agente avalia o diff contra os sinais S1-S11
2. Se sinal detectado → avisar o dev: "Detectei [sinal de segurança]. Quer rodar security agora ou deixar pro commit?"
3. Se dev diz "agora" → rodar /security-review imediatamente
4. Se dev diz "depois" → anotar sinal como pendente
5. Antes do commit → rodar /security-review sobre diff acumulado (se security ativado)

**Regra:** Não interromper para todo sinal trivial. Agrupar sinais relacionados e avisar uma vez.
**Escape hatch:** Na dúvida entre rodar ou skipar → RODAR.

---

## Fluxo

```
Review concluído
    │
    ▼
/security-review (scan de vulnerabilidades)
    │
    ├── Issues encontradas → Corrigir → /security-review novamente
    └── Limpo → Avançar para Commit
```

---

## Como invocar

O `/security-review` pode ser invocado de duas formas:

1. **Skill `security-best-practices`** (se instalada): `Skill tool: skill: "security-best-practices"`
2. **Revisão manual**: O agente analisa o código contra os critérios OWASP abaixo

Se nenhuma skill de segurança estiver disponível, o agente DEVE fazer a auditoria manualmente.
**Nunca pular esta fase por não encontrar o comando.** A revisão manual é o fallback.

---

## Processo

### 1. Executar `/security-review` (ou auditoria manual)

Analisa o código buscando:
- Injection (SQL, command, XSS)
- Broken authentication / authorization
- IDOR (Insecure Direct Object References)
- Hardcoded secrets / credentials
- Data exposure (logs, responses, errors)
- Criptografia fraca ou mal implementada
- Vulnerabilidades em dependências

### 2. Avaliar resultado

| Resultado | Ação |
|-----------|------|
| **Vulnerabilidade encontrada** | Corrigir imediatamente. Re-executar `/security-review` após correção (max 3x). |
| **Limpo** | Avançar para fase Commit. |

Não existe "suggestion" em segurança — toda vulnerabilidade detectada deve ser corrigida.

**Limite:** Max 3 re-runs. Após 3, escalar para dev com lista de issues pendentes.
NUNCA commitar com vulnerabilidades abertas — escalar, não skipar.

---

## Verificação de achados de subagentes

> **Regra de ouro:** Se o agente principal não fez `Read` da linha de código citada, o achado **NÃO** entra no relatório. Nenhuma exceção.

Falsos positivos de segurança são tão prejudiciais quanto falsos negativos — geram **alert fatigue** e fazem o dev ignorar findings reais. A verificação **NÃO** é opcional.

Quando subagentes (Agent tool) ou skills externas retornam findings de segurança, o agente principal **DEVE** verificar cada um:

- [ ] `Read` do arquivo e linha exata — o código existe como descrito?
- [ ] `git diff` — a vulnerabilidade foi introduzida nesta branch ou é pré-existente?
- [ ] Framework mitiga? — `$request->validate()` sanitiza, Eloquent usa prepared statements, template engines escapam por padrão, CSRF token automático
- [ ] Decisão intencional? — endpoint público por design, `{!! !!}` em conteúdo controlado, hasher legado para compatibilidade
- [ ] Classificação OWASP coerente? — o achado corresponde à categoria OWASP alegada no contexto real?

**Prompts para subagentes de security** devem instruir: "Liste trechos de código que manipulam [input/auth/crypto/etc] com o conteúdo exato das linhas. NÃO classifique como vulnerabilidade."

**Gate de aprovação:** Apresentar achados verificados ao dev com evidência concreta (arquivo, linha, código real, categoria OWASP, impacto). O dev é o juiz final — decide se o achado é realmente uma vulnerabilidade e como corrigir. O agente **NÃO** corrige automaticamente. Zero tolerância aplica-se apenas ao que o dev confirmar como vulnerabilidade real.

**Separação no relatório:**
- **Vulnerabilidades confirmadas da branch** — escopo da review, bloqueantes
- **Observações pré-existentes** (opcional) — seção separada, fora do escopo

Ver [agent-behavior.md](agent-behavior.md) para regras gerais de confiabilidade e padrões de falso positivo.

---

## Modo passivo durante Execute

Se a skill `security-best-practices` estiver instalada, ela opera de forma **passiva** durante a fase Execute, detectando vulnerabilidades enquanto o código é escrito. Isso não substitui o `/security-review` formal — serve como rede de segurança antecipada.

---

## Skills utilizadas

| Skill | Tipo | Obrigatória |
|-------|------|-------------|
| `/security-review` | Nativa Claude Code | Sim |
| `security-best-practices` | Skill instalada | Não (modo passivo) |

---

## Tips

- **Security é opt-in** — ativar via defaults ou quando dev pedir. Recomendado usar skill de segurança da stack
- **Zero tolerância** — toda vulnerabilidade detectada bloqueia o commit
- **Re-scan após correção** — correções de segurança podem introduzir novos vetores
- **Secrets são bloqueantes** — nunca commitar com hardcoded secrets, mesmo em dev
