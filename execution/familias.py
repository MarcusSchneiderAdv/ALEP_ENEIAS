# -*- coding: utf-8 -*-
"""
Leitura do de-para entre rotulos de assunto da ALEP e familias.

A tabela nao vive aqui. Vive em directives/familias_de_assunto.md, que e
Camada 1: decisao humana, versionada e conferivel linha a linha. Este modulo
apenas le aquele arquivo.

A separacao importa. Se o mapa estivesse no codigo, alterar a segmentacao
seria alterar o programa, e a regra deixaria de ser auditavel por quem nao
le Python. Como esta, qualquer pessoa abre o Markdown e confere a que
familia cada rotulo oficial foi atribuido.
"""

import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRETRIZ = os.path.join(RAIZ, "directives", "familias_de_assunto.md")
NAO_CLASSIFICADO = "NAO CLASSIFICADO"


def carregar_mapa():
    """Devolve {rotulo oficial: familia} a partir da diretriz."""
    if not os.path.exists(DIRETRIZ):
        return {}

    with open(DIRETRIZ, encoding="utf-8") as f:
        texto = f.read()

    # So a secao "## Familias" importa; o resto e prosa explicativa.
    corpo = texto.split("## Famílias", 1)[-1].split("## Manutenção", 1)[0]

    mapa = {}
    familia = None
    for linha in corpo.split("\n"):
        titulo = re.match(r"^###\s+(.+?)\s*$", linha)
        if titulo:
            familia = titulo.group(1).strip()
            continue
        if familia:
            # Os rotulos vem entre crases, separados por ponto medio.
            for rotulo in re.findall(r"`([^`]+)`", linha):
                mapa[rotulo.strip().upper()] = familia
    return mapa


_MAPA = None


def familia_de(assunto):
    """Familia de um rotulo oficial. Nunca adivinha."""
    global _MAPA
    if _MAPA is None:
        _MAPA = carregar_mapa()
    chave = (assunto or "SEM ASSUNTO").strip().upper()
    return _MAPA.get(chave, NAO_CLASSIFICADO)


def conferir_cobertura(rotulos):
    """Rotulos presentes nos dados que a diretriz nao cobre."""
    return sorted({r for r in rotulos if familia_de(r) == NAO_CLASSIFICADO})


if __name__ == "__main__":
    import collections
    import io
    import json
    import sys

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    mapa = carregar_mapa()
    print("Diretriz lida: %d rotulos em %d familias"
          % (len(mapa), len(set(mapa.values()))))
    for fam, n in collections.Counter(mapa.values()).most_common():
        print("   %-28s %3d rotulos" % (fam, n))

    payload = os.path.join(RAIZ, "DADOS_ALEP_20.js")
    if os.path.exists(payload):
        with open(payload, encoding="utf-8") as f:
            dados = json.loads(f.read().split("const DADOS = ", 1)[1].rsplit(";", 1)[0])
        vistos, rotulos = set(), set()
        for d in dados:
            for p in d["proposicoes_lista"]:
                if p["id"] in vistos:
                    continue
                vistos.add(p["id"])
                rotulos.add((p.get("tema") or "SEM ASSUNTO").strip().upper())
        faltam = conferir_cobertura(rotulos)
        print("\nRotulos nos dados: %d" % len(rotulos))
        print("Sem familia atribuida: %d" % len(faltam))
        for r in faltam:
            print("   %s" % r)
