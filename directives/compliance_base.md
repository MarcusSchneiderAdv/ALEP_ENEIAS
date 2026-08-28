# Regras de Conformidade ENEIAS

Este documento estabelece o padrão de conformidade para todas as investigações jurídicas.

## Limites da LGPD
- **Anonimização**: Dados de pessoas físicas estranhas ao processo auditado devem ser anonimizados.
- **Finalidade**: O uso dos dados deve ser estritamente para auditoria de legalidade e jurimetria acadêmica.

## Protocolo de Extração (ENE)
- Somente portais oficiais de transparência.
- Respeitar o `robots.txt` onde aplicável, priorizando APIs oficiais.
- Armazenar o JSON bruto em `.tmp/` para rastreabilidade.

## Auditoria da Investigação Supervisionada (IAS)
- O agente deve citar a fonte (URL ou arquivo bruto) de cada afirmação.
- Toda métrica publicada deve ser reconduzível à regra determinística que a produziu.
- **Vedado ao agente**: classificar, qualificar ou pontuar a atuação de agente público
  identificado. A camada de adjudicação pertence às rotinas determinísticas em `execution/`
  (ver `GOVERNANCE.md`).
- **Vedado ao agente**: suprir dado ausente por inferência. Lacunas são declaradas com sua
  extensão exata.
- Achados classificados como graves devem ser verificados por um humano antes de qualquer
  divulgação.
