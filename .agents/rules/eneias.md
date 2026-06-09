# Regra: Framework E.N.E.I.A.S.

Esta regra rege o comportamento deste agente para garantir conformidade jurídica e técnica.

## 1. Governança de Dados (LGPD)
- **Diferenciação**: Dados Pessoais vs. Dados Públicos (Princípio da Publicidade).
- **Armazenamento**: Use APENAS o diretório `.tmp/` para arquivos intermediários e dados brutos.
- **Destruição**: Ao finalizar a tarefa, informe que os dados brutos em `.tmp/` podem ser descartados.

## 2. Faseamento de Tarefase
- **ENE**: Jamais realize extrações complexas manualmente. Use scripts em `execution/`.
- **IAS**: Utilize sua capacidade analítica para interpretar os resultados dos scripts, nunca para inventar dados.

## 3. Ciclo de Auditoria
1.  **Check**: Verificar se existe diretriz em `directives/`.
2.  **Execute**: Chamar scripts em `execution/`.
3.  **Analyze**: Investigar resultados (IAS).
4.  **Report**: Gerar entregáveis limpos de dados sensíveis desnecessários.

## 4. Auto-Reparo (Self-Annealing)
Se um portal de transparência ou API falhar:
- Identifique a mudança técnica.
- Atualize o script em `execution/`.
- Documente a mudança na diretriz correspondente.
