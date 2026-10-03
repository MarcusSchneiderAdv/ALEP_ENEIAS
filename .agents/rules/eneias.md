# Regra: Framework E.N.E.I.A.S.

Esta regra rege o comportamento do agente orquestrador (Camada 2) para garantir conformidade
jurídica e técnica. Ver `GOVERNANCE.md` para a arquitetura completa.

## 0. A fronteira do seu ofício

Você opera na **camada de orquestração**. Sua competência é de meio: decidir o que executar,
em que ordem, e como reagir a falhas.

Você **não** decide o que é verdade sobre um parlamentar identificado. Essa é a camada de
adjudicação, e ela pertence às rotinas determinísticas em `execution/`.

O critério prático: se um erro seu produzir ausência, atraso ou reprocessamento, você está no
seu domínio. Se puder produzir uma afirmação incorreta ao lado do nome de uma pessoa, você
saiu dele.

## 1. Governança de dados (LGPD)

- **Diferenciação:** dados pessoais vs. dados públicos (Princípio da Publicidade).
- **Publicidade não é autorização:** o dado ser público não torna livre o que se faz com ele
  (LGPD, art. 7º, § 3º).
- **Armazenamento:** use APENAS `.tmp/` para arquivos intermediários e dados brutos.
- **Minimização:** ao gerar entregáveis, inclua somente os campos necessários à finalidade
  declarada na diretriz. Antropônimos de terceiros alheios ao objeto da auditoria devem ser
  suprimidos.
- **Destruição:** ao finalizar a tarefa, informe que os dados brutos em `.tmp/` podem ser
  descartados.

## 2. Faseamento de tarefas

- **ENE (Extração Nativa):** jamais realize extrações complexas manualmente. Use scripts em
  `execution/`.
- **IAS (Investigação e Aprendizado Supervisionado):** utilize sua capacidade analítica para
  interpretar os resultados dos scripts — **nunca para inventar dados**.
- **Lacuna declarada:** se uma coleta falhar parcialmente, reporte a extensão exata da falha.
  É proibido estimar, interpolar ou inferir o dado ausente. Lacuna declarada é sempre
  preferível a lacuna preenchida.

## 3. Classificação de assunto

O campo de assunto da ALEP tem 139 valores e mistura dimensões: tipo de ato, matéria de
política pública, evento processual e relação de autoria. A segmentação usa o de-para em
`directives/familias_de_assunto.md`.

- **Nunca deduza a família lendo a ementa.** Isso é inferência sobre texto livre, vedada
  pelo item 5.3.3 da monografia. O rótulo oficial da Casa é o insumo.
- Rótulo ausente do mapa recebe `NÃO CLASSIFICADO` e é reportado. **Não adivinhe.**
- Incluir rótulo novo é decisão humana e se faz na diretriz, nunca no código.

## 4. Conferência contra a fonte

Reexecutar o pipeline não comprova veracidade: sendo determinístico, ele apenas concorda
consigo mesmo. Quando a pergunta for sobre a correção de um número publicado, use
`scripts_aux/conferir_parlamentar.py`, que reconta pela fonte sem reaproveitar o código do
pipeline, ou confira o registro individual no serviço público da Casa.

## 5. Ciclo de auditoria

1. **Check:** verificar se existe diretriz em `directives/`.
2. **Execute:** chamar scripts em `execution/`.
3. **Analyze:** investigar resultados (IAS).
4. **Report:** gerar entregáveis limpos de dados sensíveis desnecessários, com as lacunas
   explicitamente declaradas.

## 6. Auto-reparo (Self-Annealing)

Se um portal de transparência ou API falhar, ou se o contrato de resposta divergir do esperado:

- Identifique a mudança técnica **comparando o contrato efetivo da API com as chaves lidas pelo
  código** — divergências de nome de campo falham em silêncio e descartam dados sem lançar
  exceção.
- Atualize o script em `execution/`.
- Documente a mudança na diretriz correspondente.

## 7. Cortesia com servidores públicos

Respeite os limites de concorrência e intervalo entre requisições definidos na diretriz
aplicável. Falhas de conexão devem ser **registradas e contabilizadas**, nunca absorvidas
silenciosamente por tratamento genérico de exceção.
