# Fase: Concerns do Codebase

**Trigger:** parte do brownfield mapping, ou explicitamente "documentar riscos", "achar tech debt", "o que é arriscado neste codebase"

**Propósito:** trazer à tona avisos acionáveis sobre o codebase. Foco em "o que prestar atenção ao fazer mudanças". Documentação viva, não lista de queixas.

## Quando Gerar

`CONCERNS.md` é gerado como parte do fluxo de brownfield mapping (junto com `STACK.md`, `ARCHITECTURE.md`, etc.). Pode também ser criado ou atualizado de forma independente quando:

- Explorar uma nova área do codebase revela riscos
- Investigação de bug descobre problemas sistêmicos
- Implementação de feature encontra fragilidade inesperada
- Auditoria de dependências revela riscos

## Processo

### 1. Coletar evidência

Durante a exploração do codebase, procurar sinais **concretos** — não opiniões. Fontes de evidência:

- Padrões de código que indicam atalhos (comentários TODO/FIXME/HACK, lógica duplicada, falta de tratamento de erro)
- Lacunas de cobertura de testes (caminhos críticos sem teste, edge cases ausentes)
- Manifestos de dependências (pacotes desatualizados, bibliotecas deprecadas, advisories de segurança)
- Indicadores de performance (queries N+1, índices ausentes, chamadas síncronas que bloqueiam)
- Padrões de segurança (checks de auth só no client-side, inputs não validados, segredos expostos)

### 2. Classificar e documentar

Cada concern deve ter: **o que** é o problema, **onde** mora (paths de arquivo), **por que** importa (impacto) e **como** corrigir (abordagem).

### 3. Priorizar por risco

Foco em concerns que podem causar dano real — perda de dados, brechas de segurança, falhas user-facing, paredes de escalabilidade. Problemas menores de estilo e TODOs normais **não** entram aqui.

---

## Template: `.specs/codebase/CONCERNS.md`

**Limite de tamanho:** 5.000 tokens (~3.000 palavras)

```markdown
# Codebase Concerns

**Data da análise:** [YYYY-MM-DD]

## Tech Debt

**[Área/Componente]:**

- Issue: [qual é o atalho/workaround]
- Arquivos: [paths específicos com crase]
- Por quê: [por que foi feito assim]
- Impacto: [o que quebra ou degrada por causa disso]
- Abordagem de fix: [como endereçar properly]

## Bugs Conhecidos

**[Descrição do bug]:**

- Sintomas: [o que acontece]
- Trigger: [como reproduzir]
- Arquivos: [onde o bug mora]
- Workaround: [mitigação temporária, se houver]
- Root cause: [se conhecido]
- Bloqueado por: [se está esperando algo]

## Considerações de Segurança

**[Área que requer cuidado de segurança]:**

- Risco: [o que pode dar errado]
- Arquivos: [onde o risco mora]
- Mitigação atual: [o que já está no lugar]
- Recomendações: [o que deveria ser adicionado]

## Gargalos de Performance

**[Operação/endpoint lento]:**

- Problema: [o que está lento]
- Arquivos: [onde o gargalo mora]
- Medição: [números reais: "500ms p95", "2s load time"]
- Causa: [por que está lento]
- Caminho de melhoria: [como acelerar]

## Áreas Frágeis

**[Componente/Módulo]:**

- Arquivos: [onde a fragilidade mora]
- Por que frágil: [o que faz quebrar fácil]
- Falhas comuns: [o que tipicamente dá errado]
- Modificação segura: [como mudar sem quebrar]
- Cobertura de testes: [tem teste? lacunas?]

## Limites de Escala

**[Recurso/Sistema]:**

- Capacidade atual: [números: "100 req/seg", "10k usuários"]
- Limite: [onde quebra]
- Sintomas no limite: [o que acontece]
- Caminho de scaling: [como aumentar capacidade]

## Dependências em Risco

**[Pacote/Serviço]:**

- Risco: [ex: "deprecado", "não mantido", "breaking changes vindo"]
- Impacto: [o que quebra se falhar]
- Plano de migração: [alternativa ou caminho de upgrade]

## Features Críticas Faltando

**[Gap de feature]:**

- Problema: [o que está faltando]
- Workaround atual: [como usuários se viram]
- Bloqueia: [o que não pode ser feito sem isso]
- Complexidade de implementação: [estimativa de esforço]

## Lacunas de Cobertura de Testes

**[Área sem teste]:**

- O que não tem teste: [funcionalidade específica]
- Risco: [o que pode quebrar despercebido]
- Prioridade: [Alta/Média/Baixa]
- Dificuldade de testar: [por que ainda não tem teste]

---

_Auditoria de concerns: [data]_
_Atualizar conforme issues são corrigidos ou novos descobertos_
```

**Incluir apenas seções que têm achados.** Seções vazias devem ser omitidas inteiramente.

---

## O que Entra vs. O que Não Entra

**Incluir:**

- Tech debt com impacto claro e abordagem de fix
- Bugs conhecidos com steps de reprodução
- Gaps de segurança e recomendações de mitigação
- Gargalos de performance com medições
- Código frágil que quebra fácil
- Limites de escala com números
- Dependências que precisam de atenção
- Features faltando que bloqueiam workflows
- Lacunas de cobertura de testes

**Excluir:**

- Opiniões sem evidência ("código está bagunçado")
- Queixas sem solução ("auth é horrível")
- Ideias de feature futura (isso é planejamento de produto)
- TODOs normais (vivem em comentários no código)
- Decisões arquiteturais que estão funcionando
- Problemas menores de estilo de código

---

## Diretrizes de Escrita

- **Sempre incluir paths de arquivo** — Concerns sem localização não são acionáveis. Use crase: `src/file.ts`
- Ser específico com medições ("500ms p95", não "lento")
- Incluir steps de reprodução para bugs
- Sugerir abordagens de fix, não só problemas
- Focar em itens acionáveis
- Priorizar por risco/impacto

**Tom:** profissional, não emocional. Orientado a solução. Focado em risco. Factual.

- ✅ "Padrão de query N+1 em `app/api/courses/route.ts` — 1.2s p95 com 50+ courses"
- ❌ "Queries horríveis, tudo está lento"
- ✅ "Fix: adicionar índice em `user_id` na tabela `subscriptions`"
- ❌ "Precisa consertar"

---

## Como `CONCERNS.md` é Usado

- **Planejamento de feature:** consultar `CONCERNS.md` antes de projetar features que tocam áreas flagged
- **Estimativa de risco:** usar áreas frágeis e limites de escala para estimar risco de mudança
- **Onboarding de sessões novas:** carregar `CONCERNS.md` para dar contexto sobre o que prestar atenção
- **Priorização de refactor:** usar tech debt e gaps de cobertura para planejar sprints de melhoria
- **Fase de implementação:** consultar antes de modificar qualquer componente flagged

Documentação viva. Atualizar conforme issues são corrigidos ou novos descobertos durante qualquer fase do workflow.
