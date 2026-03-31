# Docs Update

**Goal**: Garantir que a documentação do codebase reflita as mudanças implementadas.

**Fase obrigatória para Medium+** — executa após Security, antes do Commit.
**No Quick Mode (Small):** checklist inline, sem arquivo separado.

---

## Processo

### 1. Verificar impacto nos docs do codebase

Revisar se a implementação impactou algum dos seguintes arquivos em `.specs/codebase/`:

| Doc | Atualizar quando... |
|-----|---------------------|
| `ARCHITECTURE.md` | Novos módulos, camadas, patterns, ou mudanças em fluxos existentes |
| `STACK.md` | Novas dependências, versões, ou ferramentas |
| `INTEGRATIONS.md` | Novas APIs externas, webhooks, ou serviços de terceiros |
| `CONVENTIONS.md` | Novos padrões de código, naming, ou práticas adotadas |
| `STRUCTURE.md` | Novos diretórios, reorganização de pastas |
| `TESTING.md` | Novos padrões de teste, fixtures, ou setup |
| `CONCERNS.md` | Novos riscos identificados, débitos técnicos |

### 2. Atualizar docs impactados

Para cada doc que precisa de update:
1. Ler o doc atual
2. Atualizar **apenas** as seções relevantes
3. Manter o formato e tom existentes — não reescrever o doc inteiro

### 3. Atualizar spec.md da feature

Se decisões de design mudaram durante a implementação (vs. o que foi planejado na spec):
- Atualizar `spec.md` com as decisões finais
- Marcar divergências do plano original

### 4. Registrar resultado

- Se atualizou docs → incluir os arquivos de doc no commit junto com o código
- Se não impactou nenhum doc → registrar explicitamente: `Docs: sem impacto em .specs/codebase/`

---

## Quick Mode (Small)

No Quick Mode, o check é inline — sem arquivo separado, apenas uma verificação rápida:

```
Docs check: [sem impacto] ou [atualizou STACK.md — nova dependência X]
```

Listar no output da task, antes do commit.

---

## Regras

- **Não é relatório** — é uma verificação rápida. Leia os docs, veja se algo mudou, atualize.
- **Docs no mesmo commit** — atualizações de docs vão no mesmo commit da task (não em commit separado)
- **Só atualizar o que mudou** — não "melhorar" docs que não foram impactados pela feature
- **Se `.specs/codebase/` não existe** — pular a fase (projeto ainda não foi mapeado)

---

## Integração com Superpowers

Se a feature impactou significativamente a arquitetura e os docs ficaram muito defasados,
considerar rodar `brownfield-mapping` para regenerar os docs ao invés de atualizar manualmente.
Isso é raro — na maioria dos casos, atualizações cirúrgicas são suficientes.

---

## Tips

- **Docs atualizado = onboarding mais rápido** — o próximo dev (ou agente) que ler vai entender o estado atual
- **Se em dúvida, atualize** — melhor um doc levemente verbose que um doc desatualizado
- **Spec.md é contrato vivo** — se a implementação divergiu, a spec precisa refletir a realidade
