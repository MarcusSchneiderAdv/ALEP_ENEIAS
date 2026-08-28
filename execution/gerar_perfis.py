# -*- coding: utf-8 -*-
"""
FASE 5: geracao de dossies legiveis por pessoas e por modelos de linguagem.

O painel HTML serve a quem quer navegar. Este modulo serve a quem quer
perguntar: produz arquivos de texto que podem ser anexados a um assistente
de IA para consultas em linguagem natural sobre a atuacao parlamentar.

Saidas em dados/perfis/:
    _PANORAMA.md          visao da Casa inteira, compacta
    _CONSOLIDADO.csv      uma linha por parlamentar, todas as metricas
    <NOME>.md             dossie individual

Criterio editorial: os arquivos descrevem, nao qualificam. Nao contem nota,
ranking, media comparativa nem juizo de desempenho. A interpretacao pertence
a quem le, conforme a regra de alocacao exposta no capitulo 4 da monografia.
"""

import csv
import json
import os
import re
import unicodedata
from collections import Counter

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAYLOAD = os.path.join(WORKSPACE_ROOT, "DADOS_ALEP_20.js")
DESTINO = os.path.join(WORKSPACE_ROOT, "dados", "perfis")

# Requerimentos sao 73% do volume e altamente repetitivos. Detalhar cada um
# incharia o arquivo sem informar; sao agregados por assunto. Ja as especies
# normativas sao listadas uma a uma, com ementa.
ESPECIES_DETALHADAS = ("PROJETO DE LEI", "PROPOSTA DE EMENDA", "PROJETO DE RESOLU",
                       "PROJETO DECRETO", "PROJETO DE LEI COMPLEMENTAR")


def eh_detalhada(tipo):
    t = (tipo or "").upper()
    return any(e in t for e in ESPECIES_DETALHADAS)


def slug(nome):
    n = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_").upper()


def data_br(iso):
    if not iso:
        return "sem data"
    return "%s/%s/%s" % (iso[8:10], iso[5:7], iso[0:4])


def carregar():
    with open(PAYLOAD, encoding="utf-8") as f:
        bruto = f.read()
    meta = {}
    if "const META = " in bruto:
        meta = json.loads(bruto.split("const META = ", 1)[1].split(";\n", 1)[0])
    dados = json.loads(bruto.split("const DADOS = ", 1)[1].rsplit(";", 1)[0])
    return meta, dados


def metricas(dep):
    props = dep["proposicoes_lista"]
    tipos = Counter(p.get("tipo") or "NAO INFORMADO" for p in props)
    return {
        "nome": dep["nome"],
        "partido": dep["partido"],
        "proposicoes": dep["proposicoes_count"],
        "leis": dep["leis_count"],
        "autoria_primaria": sum(1 for p in props if not p.get("is_coautor")),
        "coautoria": sum(1 for p in props if p.get("is_coautor")),
        "arquivadas": sum(1 for p in props if (p.get("status") or "").upper() == "ARQUIVADA"),
        "tramitando": sum(1 for p in props if (p.get("status") or "").upper() == "TRAMITANDO"),
        "tipos": tipos,
    }


CABECALHO_METODO = """
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
"""


def escrever_dossie(dep, meta):
    m = metricas(dep)
    props = dep["proposicoes_lista"]
    L = []
    A = L.append

    A("# %s (%s)" % (m["nome"], m["partido"]))
    A("")
    A("Dossie de atuacao parlamentar. 20a Legislatura da Assembleia Legislativa do Parana.")
    # A data de extracao fica apenas no panorama. Carimba-la em cada dossie
    # faria toda regeracao alterar os 63 arquivos, ainda que nenhum dado
    # tivesse mudado, enterrando as alteracoes reais em ruido de versionamento.
    periodo = ""
    if meta.get("ano_inicio") and meta.get("ano_fim"):
        periodo = " Proposicoes de %s a %s." % (meta["ano_inicio"], meta["ano_fim"])
    A("%s Datas de extracao e de observacao do estado processual constam"
      % periodo.strip())
    A("de `_PANORAMA.md`, no mesmo diretorio.")
    A("")

    A("## Numeros")
    A("")
    A("| Indicador | Valor |")
    A("|---|---:|")
    A("| Proposicoes vinculadas | %d |" % m["proposicoes"])
    A("| Como autor primario | %d |" % m["autoria_primaria"])
    A("| Como coautor | %d |" % m["coautoria"])
    A("| Normas sancionadas vinculadas | %d |" % m["leis"])
    A("| Arquivadas | %d |" % m["arquivadas"])
    A("| Em tramitacao | %d |" % m["tramitando"])
    A("")

    A("## Distribuicao por especie")
    A("")
    A("| Especie | Quantidade |")
    A("|---|---:|")
    for t, c in m["tipos"].most_common():
        A("| %s | %d |" % (t, c))
    A("")

    # ─── Normas sancionadas: o resultado normativo do mandato ───
    leis = []
    for p in props:
        for lei in (p.get("leis") or []):
            leis.append((lei, p))
    if leis:
        A("## Normas sancionadas (%d)" % len(leis))
        A("")
        for lei, p in sorted(leis, key=lambda x: str(x[0].get("data") or ""), reverse=True):
            sit = lei.get("situacao")
            A("- **%s** (%s)%s" % (lei.get("desc"), data_br(str(lei.get("data") or "")),
                                   " - %s" % sit if sit else ""))
            if lei.get("ementa"):
                A("  - %s" % lei["ementa"])
            A("  - Origem: %s %s/%s" % (p.get("tipo"), p.get("numero"), p.get("ano")))
            if lei.get("observacao"):
                A("  - Observacao: %s" % lei["observacao"])
        A("")

    # ─── Especies normativas, uma a uma ───
    normativas = [p for p in props if eh_detalhada(p.get("tipo"))]
    if normativas:
        A("## Proposicoes normativas (%d)" % len(normativas))
        A("")
        A("Projetos de lei e demais especies que inovam o ordenamento, listados")
        A("individualmente com ementa.")
        A("")
        for p in sorted(normativas, key=lambda x: (-(x.get("ano") or 0), x.get("numero") or 0)):
            papel = "coautoria" if p.get("is_coautor") else "autoria"
            virou = " | virou norma" if p.get("leis") else ""
            A("- **%s %s/%s** (%s, %s%s)" % (p.get("tipo"), p.get("numero"), p.get("ano"),
                                             papel, (p.get("status") or "").lower(), virou))
            if p.get("ementa"):
                A("  - %s" % p["ementa"])
        A("")

    # ─── Requerimentos e demais: agregados por assunto ───
    outras = [p for p in props if not eh_detalhada(p.get("tipo"))]
    if outras:
        A("## Requerimentos e demais atos de expediente (%d)" % len(outras))
        A("")
        A("Agregados por assunto atribuido pela Casa, por serem numerosos e repetitivos.")
        A("")
        A("| Assunto | Quantidade |")
        A("|---|---:|")
        for t, c in Counter((p.get("tema") or "NAO INFORMADO") for p in outras).most_common():
            A("| %s | %d |" % (t, c))
        A("")

    A(CABECALHO_METODO)
    return "\n".join(L)


def escrever_panorama(dados, meta):
    L = []
    A = L.append
    A("# Panorama da 20a Legislatura da ALEP")
    A("")
    A("Visao consolidada da Casa. Para questoes sobre um parlamentar especifico,")
    A("use o dossie individual correspondente.")
    A("")
    A("| Contexto | Valor |")
    A("|---|---|")
    A("| Universo fechado em | %s |" % meta.get("universo_fechado_em", "coleta corrente"))
    A("| Estado processual observado em | %s |" % data_br(str(meta.get("gerado_em", ""))[:10]))
    A("| Proposicoes protocoladas | %s |" % f"{meta.get('proposicoes_brutas', 0):,}".replace(",", "."))
    A("| Vinculos autor-proposicao | %s |" % f"{meta.get('vinculos', 0):,}".replace(",", "."))
    A("| Parlamentares | %d |" % meta.get("deputados", 0))
    A("| Normas sancionadas vinculadas | %s |" % f"{meta.get('leis', 0):,}".replace(",", "."))
    A("")

    A("## Parlamentares")
    A("")
    A("| Parlamentar | Partido | Proposicoes | Autoria | Coautoria | Normas |")
    A("|---|---|---:|---:|---:|---:|")
    for dep in sorted(dados, key=lambda d: -d["proposicoes_count"]):
        m = metricas(dep)
        A("| %s | %s | %d | %d | %d | %d |" % (m["nome"], m["partido"], m["proposicoes"],
                                               m["autoria_primaria"], m["coautoria"], m["leis"]))
    A("")

    A("## Agregado por partido")
    A("")
    part = {}
    for dep in dados:
        m = metricas(dep)
        d = part.setdefault(m["partido"], {"props": 0, "leis": 0, "n": 0})
        d["props"] += m["proposicoes"]; d["leis"] += m["leis"]; d["n"] += 1
    A("| Partido | Parlamentares | Proposicoes | Normas |")
    A("|---|---:|---:|---:|")
    for p, d in sorted(part.items(), key=lambda kv: -kv[1]["props"]):
        A("| %s | %d | %d | %d |" % (p, d["n"], d["props"], d["leis"]))
    A("")

    A("## Distribuicao por especie na Casa")
    A("")
    tot = Counter()
    vistos = set()
    for dep in dados:
        for p in dep["proposicoes_lista"]:
            if p["id"] in vistos:
                continue
            vistos.add(p["id"])
            tot[p.get("tipo") or "NAO INFORMADO"] += 1
    soma = sum(tot.values())
    A("Contagem de proposicoes distintas, sem duplicar coautoria.")
    A("")
    A("| Especie | Quantidade | Participacao |")
    A("|---|---:|---:|")
    for t, c in tot.most_common():
        A("| %s | %d | %.1f%% |" % (t, c, c / soma * 100))
    A("")
    A(CABECALHO_METODO)
    return "\n".join(L)


def escrever_csv(dados, caminho):
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["parlamentar", "partido", "proposicoes", "autoria_primaria",
                    "coautoria", "normas_sancionadas", "arquivadas", "tramitando",
                    "projetos_de_lei", "requerimentos"])
        for dep in sorted(dados, key=lambda d: -d["proposicoes_count"]):
            m = metricas(dep)
            pl = sum(c for t, c in m["tipos"].items() if "PROJETO DE LEI" in (t or "").upper())
            rq = sum(c for t, c in m["tipos"].items() if "REQUERIMENTO" in (t or "").upper())
            w.writerow([m["nome"], m["partido"], m["proposicoes"], m["autoria_primaria"],
                        m["coautoria"], m["leis"], m["arquivadas"], m["tramitando"], pl, rq])


LEIAME = """# Perfis parlamentares para consulta com Inteligencia Artificial

Estes arquivos foram gerados pelo pipeline deste repositorio a partir dos dados
publicos da Assembleia Legislativa do Parana. Servem para que qualquer pessoa
possa consultar a atuacao parlamentar em linguagem natural.

## Como usar

1. Abra um assistente de IA de sua preferencia.
2. Anexe o arquivo do parlamentar que deseja consultar, por exemplo
   `NEY_LEPREVOST.md`. Para perguntas sobre a Casa inteira ou comparacoes,
   anexe `_PANORAMA.md`.
3. Pergunte em linguagem natural.

## Perguntas que os dados respondem

- Quais normas de autoria deste parlamentar foram sancionadas, e sobre o que tratam?
- Qual a proporcao entre projetos de lei e requerimentos na atuacao dele?
- Quantas proposicoes ele assinou como autor e quantas como coautor?
- Que assuntos concentram os requerimentos apresentados?
- Quantas das proposicoes foram arquivadas e quantas seguem tramitando?

## Perguntas que os dados NAO respondem

Os arquivos contem fatos registrais, nao avaliacoes. Nao ha nota, ranking,
media comparativa nem classificacao de merito, e isso e deliberado: a
qualificacao do desempenho pertence ao cidadao, nao ao sistema que organiza
os dados.

Se voce pedir a uma IA que julgue o desempenho de um parlamentar, o julgamento
sera dela, nao dos dados. Trate a resposta como opiniao de quem leu a planilha,
e confira as afirmacoes contra os numeros do arquivo.

## Ressalvas de leitura

**Coautoria conta para todos.** Uma proposicao com seis signatarios aparece nos
seis dossies. Somar os totais de todos os parlamentares nao devolve o numero de
proposicoes da Casa.

**Taxa de conversao nao mede qualidade.** Proposicoes sao arquivadas por perda de
objeto, absorcao por materia correlata, opcao de merito da Casa e fim de
legislatura. Uma taxa baixa nao indica, por si, baixa qualidade.

**Requerimento nao e lei.** Votos de louvor, congratulacoes e mencoes honrosas
sao atos de expediente parlamentar, nao percorrem o processo legislativo e nao
inovam o ordenamento. Cumprem funcao propria e legitima, distinta da normativa.

## Procedencia

Cada arquivo declara a data de fechamento do universo e a data de observacao do
estado processual. Para reproduzir os dados do zero, consulte o README do
repositorio.
"""


def gerar():
    if not os.path.exists(PAYLOAD):
        raise SystemExit("[ERRO] %s nao encontrado. Execute agrupar_dados_dashboard.py antes."
                         % os.path.basename(PAYLOAD))

    meta, dados = carregar()
    os.makedirs(DESTINO, exist_ok=True)

    with open(os.path.join(DESTINO, "LEIAME.md"), "w", encoding="utf-8") as f:
        f.write(LEIAME)
    with open(os.path.join(DESTINO, "_PANORAMA.md"), "w", encoding="utf-8") as f:
        f.write(escrever_panorama(dados, meta))
    escrever_csv(dados, os.path.join(DESTINO, "_CONSOLIDADO.csv"))

    maior = 0
    for dep in dados:
        texto = escrever_dossie(dep, meta)
        maior = max(maior, len(texto.encode("utf-8")))
        with open(os.path.join(DESTINO, "%s.md" % slug(dep["nome"])), "w", encoding="utf-8") as f:
            f.write(texto)

    print("[OK] %d dossies gerados em dados/perfis/" % len(dados))
    print("     maior arquivo: %.0f KB" % (maior / 1024))
    print("     panorama e consolidado CSV tambem gravados")


if __name__ == "__main__":
    gerar()
