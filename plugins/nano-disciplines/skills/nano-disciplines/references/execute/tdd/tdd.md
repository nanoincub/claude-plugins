# TDD — Test-Driven Development

Disciplina para evitar que "teste primeiro" vire "teste depois". Esta referência opera junto com [implement.md](../implement.md) (seção 6) e [testing-anti-patterns.md](testing-anti-patterns.md).

---

## Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

**Não tem exceção sem permissão explícita do dev.**

Escreveu código antes do teste? **Delete.** Não guarde "como referência". Não "adapte" enquanto escreve o teste. Não olhe. Implemente fresh a partir do teste.

> Delete means delete.

**Quando NÃO se aplica** (perguntar ao dev antes de pular):
- Protótipos descartáveis (throwaway)
- Código gerado
- Config files, docs, renames puros

Tarefas que tocam lógica de negócio, mutação de estado, API ou fluxo condicional **sempre** entram no ciclo TDD.

---

## Ciclo RED → Verify RED → GREEN → Verify GREEN → REFACTOR

Cada um destes é um **passo separado e obrigatório**. "Verify RED" não é etapa decorativa — é o coração da skill: **se você não viu o teste falhar, você não sabe se ele testa a coisa certa.**

### 1. RED — escrever teste que falha

Um teste mínimo descrevendo o comportamento esperado.

Requisitos:
- Um único comportamento
- Nome descritivo (sem "and", sem `test1`)
- Código real (mocks só quando inevitável)
- **Naming com ID do requisito da spec** — ex: `test_AUTH01_invalid_email_returns_422`. Cada critério QUANDO/ENTÃO da spec gera ao menos um teste rastreável.

### 2. Verify RED — assistir falhar (MANDATORY)

Rodar o teste. Confirmar:
- Falha (não erra com TypeError/import)
- Mensagem de falha é a esperada
- Falha porque a feature não existe (não por typo, path errado, fixture quebrada)

**Teste passou de cara?** Você está testando comportamento já existente. Conserte o teste.

**Teste deu erro em vez de falhar?** Corrija o erro, rode de novo até falhar **corretamente**.

### 3. GREEN — código mínimo para passar

Só o suficiente para o teste passar. Sem features extras, sem refatorar código adjacente, sem "melhorar" além do que o teste cobre. **YAGNI ruthlessly.**

### 4. Verify GREEN — assistir passar (MANDATORY)

Rodar o teste. Confirmar:
- Teste passa
- Outros testes continuam passando
- Output limpo (sem warnings, sem erros laterais)

**Outros testes quebraram?** Conserte agora, não depois.

### 5. REFACTOR — limpar (opcional, mantendo verde)

Depois do GREEN, só então:
- Remover duplicação
- Melhorar nomes
- Extrair helpers

**Sem adicionar comportamento.** Testes continuam passando o tempo todo.

---

## Verificação red-green completa (bug fixes)

Para correções de bug, o ciclo RED→GREEN não basta — é preciso provar que o teste **realmente testa o bug**:

1. Rodar teste novo → **PASS** (depois do fix)
2. Reverter o fix
3. Rodar teste → **MUST FAIL** (prova que o teste captura o bug)
4. Restaurar o fix
5. Rodar teste → **PASS**

Sem o passo 2-3, o teste pode ser falso positivo (passa por motivo errado).

---

## Tabela de Racionalizações

Estas são as desculpas comuns para pular TDD. Cada uma tem uma resposta. Não negocie com elas:

| Desculpa | Realidade |
|---|---|
| "Simples demais pra testar" | Código simples quebra. Teste leva 30 segundos. |
| "Testo depois" | Teste que passa de cara não prova nada. |
| "Tests-after atingem o mesmo objetivo" | Tests-after responde "o que isto faz?". Tests-first responde "o que isto **deveria** fazer?". |
| "Já testei manualmente" | Ad-hoc ≠ sistemático. Sem registro, não re-roda. |
| "Apagar X horas de trabalho é desperdício" | Falácia do custo afundado. Manter código não-verificado é tech debt. |
| "Mantenho como referência, escrevo teste primeiro" | Você vai adaptar. Isso é testing after. **Delete means delete.** |
| "Preciso explorar primeiro" | OK. Jogue a exploração fora, comece com TDD. |
| "Teste é difícil = design não está claro" | Escute o teste. Difícil de testar = difícil de usar. |
| "TDD vai me atrasar" | TDD é mais rápido que debugar. Pragmático = test-first. |
| "Teste manual é mais rápido" | Manual não prova edge cases. Você re-testa a cada mudança. |
| "Código existente não tem testes" | Você está melhorando. Adicione testes pro código existente também. |
| "TDD é dogmático, sou pragmático" | TDD **é** pragmático. Atalhos = debug em produção = mais lento. |
| "É espírito, não ritual" | Não. Tests-after são enviesados pela implementação. Você testa o que construiu, não o que era preciso. |

---

## Red Flags — STOP and Start Over

Se você se pegar em qualquer um destes, **delete o código e recomece com TDD**:

- Código escrito antes do teste
- Teste escrito depois da implementação
- Teste passa imediatamente
- Não consigo explicar por que o teste falhou
- "Adiciono testes depois"
- Racionalizando "só dessa vez"
- "Já testei manualmente"
- "Tests after atingem o mesmo objetivo"
- "É sobre espírito, não ritual"
- "Vou manter como referência" / "adapto o código existente"
- "Já gastei X horas, deletar é desperdício"
- "TDD é dogmático, estou sendo pragmático"
- "Este caso é diferente porque..."

---

## When Stuck — diagnóstico via teste

| Problema | Saída |
|---|---|
| Não sei como testar | Escreva a API desejada. Comece pela assertion. Pergunte ao dev. |
| Teste fica complicado demais | O design é que está complicado. Simplifique a interface. |
| Preciso mockar tudo | Código está acoplado demais. Use dependency injection. |
| Setup do teste é gigante | Extraia helpers. Ainda complexo? Simplifique o design. |

**Princípio:** dificuldade para testar é sintoma de problema de design, não de teste. Escute o teste.

---

## Checklist antes de marcar task como Done

- [ ] Toda função/método novo tem teste
- [ ] Assisti cada teste falhar antes de implementar
- [ ] Cada teste falhou pelo motivo esperado (feature ausente, não typo)
- [ ] Código mínimo para passar cada teste
- [ ] Todos os testes passam
- [ ] Output limpo (sem erros, sem warnings)
- [ ] Testes usam código real (mocks só quando inevitável)
- [ ] Edge cases e erros cobertos
- [ ] Cada teste é nomeado com ID do requisito (`test_FEAT01_...`)

Não consigo marcar todos? Pulei TDD. Voltar.

---

## Testes flaky (timing arbitrário)

Se um teste passa às vezes e falha sob carga / CI / paralelo, o problema costuma ser `setTimeout`/`sleep` arbitrário esperando por uma condição assíncrona. Substituir por polling de condição real (ver [condition-based-waiting.md](condition-based-waiting.md)).

---

## Quando lidar com mocks

Se a task envolve mocks, ler [testing-anti-patterns.md](testing-anti-patterns.md) antes. Resumo dos 5 anti-padrões:

1. **Testar mock behavior em vez de comportamento real** → STOP, teste real ou unmock
2. **Métodos test-only em classes de produção** → mover para test utilities
3. **Mockar sem entender deps** → rodar com impl real primeiro, depois mockar minimamente
4. **Mocks incompletos** (campos faltando) → espelhar a estrutura real completa
5. **Tests como afterthought** → TDD cycle: test → impl → refactor → done

Cada anti-padrão tem uma Gate Function (pseudocódigo de bloqueio) no arquivo dedicado.

---

## Final Rule

```
Production code → teste existe e falhou primeiro
Caso contrário → não é TDD
```

Sem exceção sem permissão explícita do dev.
