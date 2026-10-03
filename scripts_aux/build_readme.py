# -*- coding: utf-8 -*-
"""
Monta o README.md do repositorio a partir da fonte canonica da monografia.

A fonte (docs/monografia/MONOGRAFIA.md) ja e Markdown valido: os titulos
nascem com o nivel correto de cabecalho. Este script nao reformata nada --
apenas envolve o texto no cabecalho de apresentacao do repositorio.

Historico: a versao anterior tentava inferir os cabecalhos por expressao
regular sobre texto plano, e a classe de caracteres empregada nao cobria
'E' com acento circunflexo nem os sinais ':' e '.'. Em consequencia, os
capitulos 2, 4, 5 e 8 eram publicados como paragrafo comum. Manter a fonte
em Markdown elimina a categoria inteira de defeito.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "docs", "monografia", "MONOGRAFIA.md")
OUTPUT_PATH = os.path.join(BASE_DIR, "README.md")

CABECALHO = """# Projeto ALEP: Inteligência Artificial como Meio de Civilidade

Repositório oficial do Projeto ALEP: uma ferramenta de código aberto para
estruturação, auditoria e exibição transparente dos dados legislativos da
Assembleia Legislativa do Estado do Paraná (ALEP), acompanhada da pesquisa
que a fundamenta.

O trabalho propõe uma **orientação técnica e jurídica** para o emprego de
Inteligência Artificial em sistemas de controle social. Sua tese central é uma
regra de alocação: a IA opera legitimamente na camada de **orquestração** de um
sistema cívico, e é interditada na camada de **adjudicação**, em que fatos são
imputados a agentes públicos identificados. Essa camada exige processamento
determinístico, reprodutível e integralmente explicável.

| | |
|---|---|
| **Recorte** | 20ª Legislatura da ALEP (2023–2026) |
| **Fonte** | Serviço público `webservices.assembleia.pr.leg.br/api/public` |
| **Corpus** | 15.369 proposições · 129.980 eventos de tramitação · 1.677 normas |
| **Licença** | MIT (ver [LICENSE](LICENSE)) |

---

## Instalar e rodar

O projeto não depende de servidor, banco de dados, credenciais ou chave de
acesso. O serviço de dados da ALEP é público e irrestrito. É preciso apenas
Python 3.6 ou superior, e duas bibliotecas.

```bash
git clone https://github.com/MarcusSchneiderAdv/ALEP_ENEIAS.git
```

```bash
cd ALEP_ENEIAS && pip install -r requirements.txt
```

Feito isso, escolha uma das duas formas de obter os dados. Ambas executam o
pipeline inteiro sozinhas, sem passo manual.

**Coletar os dados atuais.** Consulta a Assembleia e devolve o estado de hoje.
O universo será maior que o da pesquisa, porque a legislatura segue em curso.

```bash
python executar.py
```

**Usar os dados publicados.** Restaura o universo de 15.369 proposições sobre o
qual a monografia foi escrita, com integridade conferida por resumo
criptográfico. É o caminho de quem quer auditar os números publicados.

```bash
python executar.py --snapshot
```

Em ambos os casos o programa consulta a Assembleia para obter o estado
processual de cada proposição, o que exige uma requisição por proposição. Numa
coleta do zero isso leva cerca de **50 minutos**, com intervalos entre as
requisições para não sobrecarregar os servidores do Estado. A rotina preserva o
que já baixou, de modo que pode ser interrompida e retomada sem perda.

### Ver sem instalar nada

**Painel publicado: https://marcusschneideradv.github.io/ALEP_ENEIAS/**

Abre direto no navegador, sem baixar nem executar coisa alguma. A versão publicada omite o histórico de tramitação, para
caber na hospedagem; todo o restante está íntegro.

Para quem quiser conferir os números sem rodar o pipeline, há ainda
[`dados/conferencia/CONFERENCIA.md`](dados/conferencia/CONFERENCIA.md), com a
recontagem dos 63 parlamentares feita por rotina independente, e os dossiês em
[`dados/perfis/`](dados/perfis/), que trazem o endereço da fonte oficial de cada
proposição.

### O que você recebe ao rodar

**Um painel visual completo.** Abra `index.html` no navegador. Traz a produção por
parlamentar, distribuição por espécie, conversão em norma e a linha do tempo de
tramitação de cada proposição.

**Dossiês para consultar com Inteligência Artificial.** Em `dados/perfis/`,
um arquivo por parlamentar, mais um panorama da Casa e uma planilha consolidada.
Anexe o arquivo do parlamentar a um assistente de IA e pergunte em linguagem
natural: quais normas de autoria dele foram sancionadas e sobre o que tratam,
qual a proporção entre projetos de lei e requerimentos, que assuntos concentram
seus requerimentos. As instruções de uso e as ressalvas de leitura estão em
[`dados/perfis/LEIAME.md`](dados/perfis/LEIAME.md).

> Os dossiês descrevem, não qualificam. Não contêm nota, ranking nem juízo de
> desempenho, e isso é deliberado: a qualificação pertence ao cidadão, não ao
> sistema que organiza os dados. O capítulo 4 explica por quê.

As matrizes versionadas em `dados/snapshot_2026-03-22/` existem para auditoria do
que foi publicado, não para uso corrente. Quem quiser trabalhar com dados atuais
deve rodar a coleta.

---

"""

RODAPE = """

---

*Estudo acadêmico-tecnológico desenvolvido para fins de transparência material
e cognitiva no controle social. Documento gerado a partir de
`docs/monografia/MONOGRAFIA.md`. Edite a fonte, não este arquivo.*
"""


def main():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        monografia = f.read().strip()

    # A fonte abre com titulo, subtitulo e epigrafe, seguidos do primeiro
    # separador horizontal. No README esse bloco seria um segundo H1,
    # redundante com o cabecalho do repositorio -- entao e descartado.
    if "\n---\n" in monografia:
        monografia = monografia.split("\n---\n", 1)[1].strip()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(CABECALHO + monografia + RODAPE)

    print("README.md gerado a partir de %s" % os.path.relpath(INPUT_PATH, BASE_DIR))


if __name__ == "__main__":
    main()
