# Regras de Conformidade ENEIAS

Este documento estabelece o padrão de conformidade para todas as investigações jurídicas.

## Limites da LGPD
- **Anonimização**: Dados de pessoas físicas estranhas ao processo auditado devem ser anonimizados.
- **Finalidade**: O uso dos dados deve ser estritamente para auditoria de legalidade e jurimetria acadêmica.

## Protocolo de Extração (ENE)
- Somente portais oficiais de transparência.
- Respeitar o `robots.txt` onde aplicável, priorizando APIs oficiais.
- Armazenar o JSON bruto em `.tmp/` para rastreabilidade.

## Auditoria de NLP (IAS)
- O agente deve citar a fonte (URL ou Arquivo) de cada afirmação.
- Alertas de "Grave" devem ser verificados por um humano.
