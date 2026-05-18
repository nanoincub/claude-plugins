# Brownfield Mapping

**Trigger:** "mapear codebase", "analisar código existente", "documentar arquitetura atual"

**Propósito:** entender a estrutura do projeto existente antes de adicionar features.

## Processo

Antes de começar, verificar se a skill `codenavi` está disponível para exploração de código (ver Skill Integrations no SKILL.md). Se estiver, preferir para todas as tarefas de discovery/navegação abaixo.

**Abordagem em alto nível:**

1. Explorar estrutura de diretórios sistematicamente
2. Identificar stack tecnológica a partir dos manifestos de dependências
3. Extrair padrões de amostras representativas de código
4. Documentar convenções e arquiteturas observadas
5. Catalogar integrações externas
6. Identificar concerns: tech debt, bugs conhecidos, riscos de segurança, gargalos de performance, áreas frágeis

**Profundidade da análise:**

- Amostrar 5-10 arquivos representativos por categoria
- Foco em consistência e padrões, não cobertura exaustiva
- Extrair exemplos reais, não suposições

## Output: 7 arquivos em `.specs/codebase/`

---

### 1. STACK.md

**Propósito:** documentar stack tecnológica e dependências.

**Limite de tamanho:** 2.000 tokens (~1.200 palavras)

**Extrair de:**

- Arquivos de manifesto de dependências
- Configuração de build
- Configuração de runtime

**Documentar:**

```markdown
# Tech Stack

**Analisado em:** [data]

## Core

- Framework: [nome detectado + versão]
- Linguagem: [nome detectado + versão]
- Runtime: [nome detectado + versão]
- Gerenciador de pacotes: [gerenciador detectado]

## Frontend (se aplicável)

- Framework de UI: [nome + versão]
- Styling: [abordagem + ferramentas]
- State management: [biblioteca/padrão]
- Form handling: [biblioteca, se presente]

## Backend (se aplicável)

- Estilo de API: [REST/GraphQL/gRPC + framework]
- Banco de dados: [ORM/query builder + sistema de banco]
- Autenticação: [biblioteca/abordagem]

## Testing

- Unit: [framework]
- Integration: [framework]
- E2E: [framework, se presente]

## Serviços Externos

- [Categoria]: [Nome do serviço]
- [Categoria]: [Nome do serviço]

## Ferramentas de Desenvolvimento

- [Categoria de ferramenta]: [Nome da ferramenta]
```

**Instruções:**

- Extrair dos arquivos reais de dependência
- Incluir versões das dependências principais
- Categorizar por propósito
- Anotar frameworks de teste explicitamente

---

### 2. ARCHITECTURE.md

**Propósito:** documentar padrões arquiteturais e fluxo de dados.

**Limite de tamanho:** 4.000 tokens (~2.400 palavras)

**Extrair de:**

- Organização de diretórios
- Análise de estrutura de código
- Padrões repetidos entre arquivos

**Documentar:**

```markdown
# Architecture

**Padrão:** [padrão identificado — monolito/microservices/modular/etc]

## Estrutura em Alto Nível

[Criar diagrama/descrição baseado na organização real]

## Padrões Identificados

### [Nome do padrão]

**Localização:** [onde este padrão mora]
**Propósito:** [o que isto atinge]
**Implementação:** [como está estruturado]
**Exemplo:** [referência a arquivo/função real]

### [Nome do padrão]

[Mesma estrutura]

## Fluxo de Dados

### [Fluxo-chave — ex: Autenticação/Pagamento/etc]

[Mapear fluxo real a partir da análise de código]

### [Fluxo-chave]

[Mapear fluxo real]

## Organização de Código

**Abordagem:** [feature-based/layer-based/domain-driven/etc]

**Estrutura:**
[Documentar a organização real de diretórios]

**Fronteiras de módulos:**
[Como o código está dividido em módulos/pacotes]
```

**Instruções:**

- Identificar padrões a partir do código real, não suposições
- Documentar decisões arquiteturais observadas
- Criar diagramas de fluxo para caminhos críticos
- Referenciar exemplos concretos do codebase

---

### 3. CONVENTIONS.md

**Propósito:** documentar estilo de código e convenções de nomenclatura.

**Limite de tamanho:** 3.000 tokens (~1.800 palavras)

**Extrair de:**

- Análise de 5-10 arquivos representativos
- Identificação de padrões consistentes
- Observação de convenções em uso

**Documentar:**

```markdown
# Convenções de Código

## Nomenclatura

**Arquivos:**
[Padrão observado — documentar a abordagem real]
Exemplos: [nomes reais de arquivos do codebase]

**Funções/Métodos:**
[Padrão observado]
Exemplos: [nomes reais de funções]

**Variáveis:**
[Padrão observado]
Exemplos: [nomes reais de variáveis]

**Constantes:**
[Padrão observado]
Exemplos: [nomes reais de constantes]

## Organização de Código

**Declaração de imports/dependências:**
[Padrão de ordenação observado]
[Exemplo de arquivo real]

**Estrutura de arquivos:**
[Organização observada dentro dos arquivos]
[Exemplo de arquivo real]

## Type Safety / Documentação

**Abordagem:** [sistema de tipos/abordagem de documentação em uso]
[Exemplo de código real]

## Tratamento de Erros

**Padrão:** [abordagem observada]
[Exemplo de código real]

## Comentários / Documentação

**Estilo:** [quando/como comentários são usados]
[Exemplo de código real]
```

**Instruções:**

- Extrair padrões de amostras reais de código
- Documentar convenções **observadas**, não ideais
- Incluir exemplos concretos do codebase
- Anotar exceções ou variações quando encontradas

---

### 4. STRUCTURE.md

**Propósito:** documentar layout de diretórios e organização de arquivos.

**Limite de tamanho:** 2.000 tokens (~1.200 palavras)

**Documentar:**

```markdown
# Estrutura do Projeto

**Root:** [path raiz do projeto]

## Árvore de Diretórios

[Representação visual em árvore — máximo 3 níveis de profundidade]

## Organização de Módulos

### [Nome do módulo/área]

**Propósito:** [o que esta área cobre]
**Localização:** [onde os arquivos moram]
**Arquivos-chave:** [arquivos importantes desta área]

### [Nome do módulo/área]

[Mesma estrutura]

## Onde as Coisas Moram

**[Capacidade/Feature]:**

- UI/Interface: [localização]
- Lógica de negócio: [localização]
- Acesso a dados: [localização]
- Configuração: [localização]

**[Capacidade/Feature]:**
[Mesma estrutura]

## Diretórios Especiais

**[Nome do diretório]:**
**Propósito:** [o que pertence aqui]
**Exemplos:** [arquivos-chave deste diretório]
```

**Instruções:**

- Criar visão em árvore da estrutura real
- Limitar profundidade para manter legibilidade
- Documentar propósito dos diretórios-chave
- Mapear capacidades para localizações físicas

---

### 5. TESTING.md

**Propósito:** documentar infraestrutura e padrões de testes.

**Limite de tamanho:** 4.000 tokens (~2.400 palavras)

**Documentar:**

```markdown
# Infraestrutura de Testes

## Test Frameworks

**Unit/Integration:** [nome do framework + versão]
**E2E:** [nome do framework + versão]
**Cobertura:** [ferramenta, se usada]

## Organização de Testes

**Localização:** [onde os testes moram]
**Naming:** [padrão de nomenclatura de arquivos de teste]
**Estrutura:** [como os testes estão organizados]

## Padrões de Teste

### Unit Tests

**Abordagem:** [padrão observado]
**Localização:** [onde os unit tests moram]
[Descrição do padrão real em uso]

### Integration Tests

**Abordagem:** [padrão observado]
**Localização:** [onde os integration tests moram]
[Descrição do padrão real em uso]

### E2E Tests

**Abordagem:** [padrão observado se presente]
**Localização:** [onde os E2E tests moram]
[Descrição do padrão real em uso]

## Execução de Testes

**Comandos:** [como rodar os testes]
**Configuração:** [abordagem de configuração de testes]

## Metas de Cobertura

**Atual:** [se mensurável]
**Objetivos:** [se documentado]
**Enforcement:** [se automatizado]
```

**Instruções:**

- Identificar frameworks de teste a partir de dependências e código
- Documentar padrões de teste reais observados
- Anotar abordagem de organização de testes
- Incluir instruções de execução

---

### 6. INTEGRATIONS.md

**Propósito:** documentar integrações com serviços externos.

**Limite de tamanho:** 5.000 tokens (~3.000 palavras)

**Documentar:**

```markdown
# Integrações Externas

## [Categoria do serviço]

**Serviço:** [nome do serviço]
**Propósito:** [o que esta integração provê]
**Implementação:** [onde a integração mora no código]
**Configuração:** [como o serviço é configurado]
**Autenticação:** [abordagem de auth se aplicável]

## [Categoria do serviço]

[Mesma estrutura]

## Integrações de API

### [Nome da API]

**Propósito:** [o que esta API provê]
**Localização:** [onde o cliente/código da API mora]
**Autenticação:** [método de auth]
**Endpoints-chave:** [endpoints principais usados]

## Webhooks

### [Origem do webhook]

**Propósito:** [que eventos são tratados]
**Localização:** [localização do handler de webhook]
**Eventos:** [tipos de evento processados]

## Background Jobs

**Sistema de fila:** [sistema se usado]
**Localização:** [onde as definições de job moram]
**Jobs:** [background jobs principais]
```

**Instruções:**

- Identificar integrações a partir de código e configuração
- Documentar abordagens de autenticação
- Anotar handlers de webhook se presentes
- Incluir infraestrutura de background jobs

---

### 7. CONCERNS.md

**Propósito:** trazer à tona avisos acionáveis sobre o codebase — tech debt, bugs conhecidos, gaps de segurança, gargalos de performance, áreas frágeis, limites de escala, dependências arriscadas, features faltando e lacunas de cobertura de testes.

**Limite de tamanho:** 5.000 tokens (~3.000 palavras)

Ver [concerns.md](concerns.md) para o template completo, diretrizes e exemplos.

**Instruções:**

- Documentar apenas concerns apoiados por evidência (paths, medições, steps de reprodução)
- Incluir abordagens de fix, não só problemas
- Omitir seções sem achados
- Priorizar por risco/impacto
- Tom profissional, orientado a solução

---

## Orçamento Total de Contexto

**Combinado:** ~19.000 tokens (10% da janela de contexto)
**Aceitável para:** projetos brownfield que requerem entendimento do codebase
**Estratégia de carregamento:** carregar docs relevantes on-demand baseado na task
