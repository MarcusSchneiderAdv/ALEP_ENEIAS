# ARQUITETURA DOE + ENEIAS (Ecossistema Nativo de Extração, Investigação e Aprendizado Supervisionado)

Este projeto opera sob uma arquitetura de 3 camadas para maximizar a confiabilidade, rastreabilidade e segurança (XAI).

## As 3 Camadas

### Camada 1: Diretriz (O "Quê")
- **Localização**: `directives/`
- **Descrição**: SOPs (Procedimentos Operacionais Padrão) em Markdown. Definem os objetivos, limites legais (LGPD), parâmetros técnicos e regras de negócio.
- **Regra**: O agente DEVE ler a diretriz correspondente antes de iniciar qualquer tarefa.

### Camada 2: Orquestração (O "Quem")
- **Descrição**: O Agente AI (Antigravity).
- **Responsabilidade**: Roteamento inteligente, tomada de decisão, aplicação de NLP em ambiente controlado, tratamento de erros e atualização de diretrizes.
- **Regra**: Atua como a ponte entre o intent humano e a execução determinística.

### Camada 3: Execução (O "Como")
- **Localização**: `execution/`
- **Descrição**: Scripts determinísticos (Python/Node) que realizam o trabalho pesado (Scraping, ETL, API calls).
- **Regra**: O agente não simula trabalho pesado; ele invoca as ferramentas desta camada.

---

## O Ecossistema E.N.E.I.A.S.

1.  **Fase ENE (Extração Nativa)**: Scripts determinísticos para raspagem de dados brutos (Diários Oficiais, Licitações, Contratos).
2.  **Fase IAS (Investigação e Aprendizado Supervisionado)**: Aplicação de NLP e ML para detecção de anomalias e conformidade jurídica.
3.  **Privacy by Design**: TODOS os dados brutos vivem **exclusivamente** em `.tmp/` e são transitórios. Deliverables vivem na nuvem (Google Sheets/Drive).

## Princípios de Operação
- **Self-Annealing**: Se algo quebrar, corrija a execução, teste e atualize a diretriz.
- **Efemeridade**: O diretório `.tmp/` deve ser regenerado ou descartado ao fim do ciclo.
- **Rastreabilidade**: Todo raciocínio lógico deve ser auditável e fundamentado em dados extraídos deterministicamente.
