# Diretriz: Metodologia da Auditoria da Produção Legislativa (E.N.E.I.A.S.)

Camada 1. Define a finalidade e o método da pesquisa empírica. Fundamentação completa em
`docs/monografia/MONOGRAFIA.md`.

## 1. Finalidade do tratamento (LGPD, art. 6º, I)

Auditar a **produção legislativa** da 20ª Legislatura da ALEP (2023–2026), tornando-a
materialmente acessível ao cidadão, sem emitir juízo de mérito sobre parlamentares.

Esta finalidade é fixada por decisão humana e é anterior à coleta. O agente orquestrador não
pode alterá-la.

## 2. Objeto e recorte

- **Universo:** proposições protocoladas na ALEP entre 2023 e 2026.
- **Fonte única:** WebService público `webservices.assembleia.pr.leg.br/api/public`.
- **Segregação:** proposições de iniciativa institucional (Poder Executivo, comissões, Mesa)
  são identificadas e excluídas das métricas de desempenho individual, por não se prestarem a
  esse fim.

## 3. Fases

### Fase I — Extração Nativa (ENE)

- **Objetivo:** garantir integridade dos dados brutos.
- **Método:** coleta automatizada via APIs oficiais.
  - `proposicao/filtrar` — proposições por ano.
  - `proposicao/{codigo}` — tramitação e vínculos normativos.
  - `norma-legal/filtrar` — normas sancionadas, para referência cruzada.
- **Armazenamento:** documentos brutos permanecem em `.tmp/`.
- **Justificativa:** evitar viés de pré-processamento e garantir auditabilidade da base fria.

### Fase II — Investigação Supervisionada (IAS)

- **Objetivo:** validar a consolidação e detectar divergências entre o contrato esperado e o
  contrato efetivo das APIs.
- **Método:** análise pelo agente orquestrador, **sem inferência sobre parlamentares**.
- **Vedação expressa:** não aplicar classificação textual, análise semântica ou modelo
  preditivo sobre ementas para derivar tema, natureza ou relevância de proposição imputada a
  parlamentar identificado. Quando houver campo oficial que cumpra a função, ele prevalece.

### Fase III — Explicabilidade (XAI)

- **Objetivo:** rastreabilidade total.
- **Método:** cada métrica publicada deve ser reconduzível ao arquivo bruto correspondente em
  `.tmp/` e à regra determinística que a produziu.

## 4. Métricas admitidas

Todas derivam de contagem sobre campos oficiais. Nenhuma envolve inferência.

| Métrica | Definição |
|---|---|
| Proposições por espécie | Contagem por `tipoProposicao` atribuído pela Casa. |
| Vínculo autor-proposição | Fragmentação do campo `autor`; posição 0 = autor primário, demais = coautoria. |
| Conversão em norma | Presença de vínculo em `normasLegais`. |
| Situação processual | Campo `status` da fonte. |
| Eventos de tramitação | Registros de `tramites`, ordenados por data. |

**Métricas vedadas:** nota, ranking, índice de desempenho, classificação de mérito ou qualquer
agregado que qualifique — e não apenas descreva — a atuação de parlamentar identificado.

## 5. Passo a passo

1. **Identificação:** mapear os endpoints e registrar o contrato de resposta observado.
2. **Coleta:** executar as rotinas determinísticas de captura.
3. **Saneamento:** normalizar nomes de autoria (remoção de prefixos de tratamento, espaços,
   caixa) e desduplicar pares autor-proposição.
4. **Consolidação:** aplicar as regras da seção 4 e serializar a carga útil.
5. **Declaração de lacunas:** reportar a extensão exata de qualquer falha de coleta. É proibido
   estimar o dado ausente.
6. **Divulgação:** publicar código e resultados sob licença aberta, permitindo verificação
   independente.
