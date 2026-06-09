# Diretriz: Coleta de Presença Parlamentar API ALEP

Esta diretriz define o protocolo para extração de dados de presença dos deputados estaduais do Paraná.

## 1. Fonte de Dados
- **Portal**: Transparência Assembleia Legislativa do Paraná.
- **API Base**: `https://transparencia.assembleia.pr.leg.br/api/presenca`
- **Legislaturas**: 19ª (2019-2022) e 20ª (2023-Atualmente).

## 2. Parâmetros Técnicos
- **Frequência**: Requisições com atraso (delay) randômico entre 1.0s e 3.0s para evitar sobrecarga (Princípio da Cortesia).
- **Tratamento de Erros**: Falhas de conexão devem ser registradas e tentadas novamente (Self-Annealing).

## 3. Protocolo ENE (Extração Nativa)
- Executar `execution/coletar_presenca_api.py`.
- O script deve baixar o JSON bruto por data de sessão.
- Salvar em `.tmp/raw_api/`.

## 4. Conformidade (LGPD)
- Não coletar dados de assessores ou terceiros.
- Manter apenas o nome parlamentar e o status de presença.
