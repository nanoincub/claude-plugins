# Security

**Goal**: Detectar vulnerabilidades de segurança antes do commit.

**Obrigatória antes de qualquer commit.** Durante ajustes, o agente detecta sinais de segurança no diff e pergunta ao dev se quer rodar agora ou deixar pro commit.

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

**Sinais servem para perguntas antecipadas** — se detectados durante ajustes, o agente pergunta se quer rodar security agora. Mas security roda SEMPRE antes do commit, com ou sem sinais detectados.

## Fluxo Confirmativo

1. Após cada ajuste, o agente avalia o diff contra os sinais S1-S11
2. Se sinal detectado → avisar o dev: "Detectei [sinal de segurança]. Quer rodar security agora ou deixar pro commit?"
3. Se dev diz "agora" → rodar /security-review imediatamente
4. Se dev diz "depois" → anotar sinal como pendente
5. Antes do commit → rodar /security-review sobre diff acumulado (SEMPRE — obrigatório)

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

- **Security é obrigatória antes de qualquer commit quando sinais são detectados** — na dúvida, rodar
- **Zero tolerância** — toda vulnerabilidade detectada bloqueia o commit
- **Re-scan após correção** — correções de segurança podem introduzir novos vetores
- **Secrets são bloqueantes** — nunca commitar com hardcoded secrets, mesmo em dev
