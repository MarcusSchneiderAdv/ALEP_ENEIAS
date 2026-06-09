# Metodologia Acadêmica: Auditoria de Presença Parlamentar (ENEIAS)

Este documento descreve a metodologia aplicada para a auditoria de dados públicos da ALEP.

## 1. Introdução
A metodologia baseia-se no framework **E.N.E.I.A.S.**, que utiliza agentes de IA supervisionados para processar grandes volumes de dados públicos com rigor acadêmico e técnico.

## 2. Fases da Pesquisa

### Fase I: Extração Nativa (ENE)
- **Objetivo**: Garantir a integridade dos dados brutos e um banco de dados unificado.
- **Método**: Coleta automatizada via APIs oficiais:
    - **API de Presença**: Dados de assiduidade parlamentar.
    - **API de Proposições**: Captura de projetos de lei, requerimentos e indicações.
- **Armazenamento**: Todos os documentos brutos permanecem em `.tmp/` para processamento posterior.
- **Justificativa**: Evitar viés de pré-processamento e garantir a auditabilidade total da base fria.

### Fase II: Investigação e Aprendizado (IAS)
- **Objetivo**: Detectar padrões e anomalias.
- **Método**: Aplicação de NLP sobre as justificativas de ausência para categorização (Saúde, Missão Oficial, Particular).
- **Métrica**: Cálculo do Índice de Assiduidade Plenária (IAP).

### Fase III: Explicabilidade (XAI)
- **Objetivo**: Rastreabilidade total.
- **Método**: Cada métrica deve estar vinculada ao arquivo bruto em `.tmp/` correspondente.

## 3. Passo a Passo de Aplicação
1. **Identificação**: Mapeamento dos endpoints da API.
2. **Coleta**: Execução dos scripts de captura determinística.
3. **Saneamento**: Remoção de duplicatas e correção de nomes (ex: nomes parciais).
4. **Cálculo**: Processamento estatístico.
5. **Divulgação**: Geração de entregáveis em nuvem para escrutínio público.
