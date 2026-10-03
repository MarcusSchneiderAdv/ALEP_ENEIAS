# MARCIO NUNES (PSD)

Dossie de atuacao parlamentar. 20a Legislatura da Assembleia Legislativa do Parana.
Proposicoes de 2023 a 2026. Datas de extracao e de observacao do estado processual constam
de `_PANORAMA.md`, no mesmo diretorio.

## Numeros

| Indicador | Valor |
|---|---:|
| Proposicoes vinculadas | 37 |
| Como autor primario | 2 |
| Como coautor | 35 |
| Normas sancionadas vinculadas | 0 |
| Arquivadas | 36 |
| Em tramitacao | 1 |
| Homenagens (mencao, congratulacoes, louvor) | 0 |
| Votos de pesar | 1 |

Homenagem e pesar vem separados porque a Casa os classifica como assuntos
distintos: voto de pesar registra falecimento, nao concede honraria.

## Distribuicao por familia de assunto

| Familia | Quantidade |
|---|---:|
| EXPEDIENTE E TRÂMITE | 33 |
| ORGANIZAÇÃO INTERNA | 3 |
| PESAR | 1 |

## Distribuicao por especie

| Especie | Quantidade |
|---|---:|
| EMENDA DE PLENÁRIO | 33 |
| REQUERIMENTO | 4 |

## Requerimentos e demais atos de expediente (37)

Agregados por assunto atribuido pela Casa, por serem numerosos e repetitivos.

Primeiro por familia, depois pelo rotulo oficial dentro de cada uma.
As familias constam de directives/familias_de_assunto.md, que declara a
que grupo cada rotulo da Casa pertence. Nenhuma ementa foi interpretada.

| Familia | Quantidade |
|---|---:|
| **EXPEDIENTE E TRÂMITE** | **33** |
| **ORGANIZAÇÃO INTERNA** | **3** |
| **PESAR** | **1** |

**EXPEDIENTE E TRÂMITE** (33)

| Rotulo oficial | Quantidade |
|---|---:|
| EMENDAS | 33 |

**ORGANIZAÇÃO INTERNA** (3)

| Rotulo oficial | Quantidade |
|---|---:|
| FRENTE PARLAMENTAR | 2 |
| ALEP | 1 |

**PESAR** (1)

| Rotulo oficial | Quantidade |
|---|---:|
| VOTOS DE PESAR | 1 |

## Como conferir estes numeros na fonte

Nao e preciso confiar neste arquivo. Cada proposicao tem um codigo no
sistema da Assembleia, e o registro oficial de qualquer uma delas abre
direto no navegador, sem instalar nada:

    http://webservices.assembleia.pr.leg.br/api/public/proposicao/CODIGO

A pagina devolve o registro bruto da Casa, com autor, ementa, situacao,
historico de tramitacao e normas vinculadas. E a fonte primaria: o que
aparece ali nao passou por este projeto.

### Conferindo com ajuda de uma IA

Se preferir nao ler o registro bruto, que vem em formato tecnico:

1. Abra um dos enderecos acima no navegador.
2. Selecione tudo (Ctrl+A), copie (Ctrl+C).
3. Cole num assistente de IA junto com este dossie e peca:
   *"Confira se o que o dossie afirma sobre esta proposicao bate com o
   registro oficial que colei. Aponte qualquer divergencia."*

A IA le o formato tecnico por voce. A conferencia continua sendo contra
a fonte, porque o texto colado veio da Assembleia, nao deste projeto.

### Conferindo os totais

Os totais deste dossie, como "37 proposicoes", nao se conferem por um
endereco so: exigem somar o conjunto inteiro. Dois caminhos:

- `dados/conferencia/CONFERENCIA.md`, no repositorio, traz a recontagem
  de todos os parlamentares feita por rotina independente do pipeline.
- Quem tiver Python instalado roda a conferencia por conta propria:
  `python scripts_aux/conferir_parlamentar.py "MARCIO NUNES"`

### Uma ressalva sobre o site da Assembleia

As paginas de perfil dos deputados em assembleia.pr.leg.br estao com
exibicao suspensa durante o periodo eleitoral, por forca do art. 73 da
Lei nº 9.504/1997. Os enderecos de dados indicados acima seguem no ar,
porque sao servico de dados abertos, nao publicidade institucional.


---

## Nota metodologica

Dados extraidos do servico publico da Assembleia Legislativa do Parana
(`webservices.assembleia.pr.leg.br/api/public`) e reorganizados por regras
deterministicas, sem inferencia estatistica.

Uma proposicao em coautoria e contabilizada para cada signatario. Por isso a
soma das contagens individuais de todos os parlamentares excede o numero de
proposicoes distintas protocoladas na Casa.

Este arquivo descreve, nao qualifica. Nao contem nota, ranking nem juizo de
desempenho: a leitura e a conclusao pertencem a quem consulta.
