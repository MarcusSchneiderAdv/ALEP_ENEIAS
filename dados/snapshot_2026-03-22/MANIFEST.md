# Snapshot do universo da pesquisa

Data da coleta: **21-22 de marco de 2026**
Data do congelamento deste snapshot: 22 de agosto de 2026
Fonte: `http://webservices.assembleia.pr.leg.br/api/public/proposicao/filtrar`

Este diretorio congela as matrizes JSON de proposicoes sobre as quais foram
calculados os resultados do capitulo 6 da monografia. Os anos de 2023 a 2025
estao encerrados e sao estaveis; 2026 corresponde a legislatura em curso e
continua recebendo protocolos apos esta data.

| Ano | Proposicoes | Arquivo (gz) | SHA-256 do JSON original |
|---|---:|---:|---|
| 2023 | 4672 | 398 KB | `a41ed2daec78c481d39ada15a29005726f54e5cb5c331af6be74ef7d062769f7` |
| 2024 | 4201 | 343 KB | `b0b1e88ff0f475e70dde7f066c53d07fa4c2e163cee6b732885070946d740053` |
| 2025 | 5468 | 450 KB | `2259da96ac137c7a0518dc269a6c42dc8c1d61bf5d1fc1f3be6087643052c31e` |
| 2026 | 1028 | 74 KB | `f01a4fbcf3cca4b465a7da6bfb409bb11c9c6d21317db97bb5d87847259c9ff2` |
| **Total** | **15369** | | |

## Restauracao

Para reproduzir exatamente os numeros publicados, descompacte este snapshot
na camada efemera antes de executar as fases 2 a 4:

```bash
python scripts_aux/restaurar_snapshot.py
```

Sem essa restauracao, a Fase 1 coletara o estado atual da API, que difere
do publicado na medida em que a legislatura de 2026 avancou.
