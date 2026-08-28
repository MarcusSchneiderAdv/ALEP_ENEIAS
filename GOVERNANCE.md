# Arquitetura E.N.E.I.A.S. — Governança do Pipeline

**E.N.E.I.A.S.** — Ecossistema Nativo de Extração, Investigação e Aprendizado Supervisionado.

> **Precisão terminológica.** "Aprendizado supervisionado" **não** designa aqui a técnica
> estatística homônima (*supervised learning*). Designa o regime de operação da camada de
> orquestração: o agente de IA opera sob supervisão humana permanente e sob diretrizes
> escritas que não pode alterar unilateralmente. **Nenhum modelo é treinado neste projeto e
> nenhuma inferência estatística produz resultado exibido ao cidadão.** A supervisão é
> jurídica e processual, não estatística.

Este projeto opera sob uma arquitetura de três camadas. A repartição não é preferência de
engenharia: implementa a **regra de alocação de competência algorítmica** formulada no
capítulo 4 da monografia (`docs/monografia/MONOGRAFIA.md`).

## A regra que organiza as camadas

> Processamento probabilístico é admissível nas camadas cujos erros são recuperáveis pelo
> próprio sistema e invisíveis ao sujeito auditado; é **interditado** nas camadas cujos erros
> se convertem em afirmação pública sobre pessoa determinada.

O critério não pergunta se a técnica é acurada. Pergunta **quem suporta o erro**.

---

## Camada 1 — Diretriz (o quê)

- **Local:** `directives/`
- **Conteúdo:** SOPs em Markdown que definem objetivos, limites legais (LGPD), parâmetros
  técnicos e critérios de auditoria.
- **Competência:** estritamente humana. O agente lê a diretriz e a ela se vincula; **não a
  redige nem a altera**. Um sistema que pudesse redefinir a própria finalidade tornaria
  inoperante o princípio da finalidade (LGPD, art. 6º, I).
- **Regra:** o agente DEVE ler a diretriz correspondente antes de iniciar qualquer tarefa.

## Camada 2 — Orquestração (quem e quando)

- **Executor:** o agente de IA.
- **Competência:** roteamento entre rotinas, ordem de execução, tratamento de falhas de rede,
  diagnóstico de alterações no contrato das APIs, proposição de correções ao código da
  Camada 3.
- **Fronteira:** atribuições de **meio**. Um erro aqui produz ausência, atraso ou
  reprocessamento — nunca afirmação sobre pessoa identificada.
- **Vedação:** é proibido ao agente suprir dado ausente por inferência. Lacuna de coleta é
  declarada com sua extensão, jamais estimada.
- **Rastreabilidade:** toda decisão de roteamento e todo tratamento de falha devem deixar
  registro auditável.

## Camada 3 — Execução (o quê é verdade sobre quem)

- **Local:** `execution/`
- **Conteúdo:** rotinas determinísticas em Python para extração, transformação e consolidação.
- **Competência:** camada de **adjudicação**. Aqui a IA é interditada.
- **Propriedade definidora:** determinismo. A partir dos mesmos dados de origem, produz sempre
  o mesmo resultado — sem estado oculto, sem amostragem, sem parâmetros ajustados por treino.
- **Fundamento jurídico:** o determinismo é o que torna o sistema *contestável* nos termos do
  art. 20 da LGPD e do PL nº 2.338/2023. Correlação estatística distribuída por parâmetros
  não constitui critério enunciável, e portanto não é contestável.
- **Regra:** o agente não simula trabalho pesado; ele invoca as ferramentas desta camada.

---

## Ciclo de operação

1. **Fase ENE — Extração Nativa.** Rotinas determinísticas consomem as APIs públicas oficiais
   da ALEP (proposições, detalhes de tramitação, normas legais). Os dados brutos são
   depositados na camada efêmera.
2. **Fase IAS — Investigação supervisionada.** O agente interpreta os resultados das rotinas,
   detecta divergências entre o contrato esperado e o contrato efetivo das APIs, e corrige a
   Camada 3. **Interpreta resultados; nunca inventa dados.**
3. **Entrega.** A consolidação serializa uma carga útil estática (`DADOS_ALEP_20.js`)
   consumida diretamente pelo navegador, sem banco de dados em operação no servidor.

## Princípios

- **Privacy by Design.** Todos os dados brutos vivem exclusivamente em `.tmp/`, isolado do
  repositório publicado por regra de exclusão versionada.
- **Efemeridade.** `.tmp/` é camada de trânsito, regenerável a partir da fonte oficial e
  descartável ao fim do ciclo.
- **Minimização.** O artefato distribuído deve conter apenas os campos necessários à finalidade
  declarada. Dados colaterais — notadamente antropônimos de terceiros alheios ao objeto da
  auditoria — devem ser suprimidos antes da distribuição, ainda que constem de ato público
  (LGPD, art. 7º, § 3º, c/c art. 6º, III).
- **Self-Annealing.** Se algo quebrar, corrija a execução, teste e atualize a diretriz.
- **Rastreabilidade.** Toda métrica deve ser reconduzível ao arquivo bruto que a originou.
- **Cortesia.** Requisições a servidores do Estado observam limites de concorrência e intervalo
  definidos na diretriz aplicável.

## Vedações do projeto

1. Atribuir automaticamente nota, ranking ou juízo de desempenho a agente público identificado.
2. Inferir natureza, tema ou relevância de um ato a partir de seu texto, quando houver campo
   oficial que cumpra a mesma função.
3. Preencher lacuna de coleta por estimativa, interpolação ou modelo preditivo.
4. Publicar resultado cuja regra de formação não possa ser exibida ao sujeito auditado.
5. Tratar a publicidade primária do dado como autorização irrestrita de tratamento.
