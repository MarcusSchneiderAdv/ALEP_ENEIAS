# -*- coding: utf-8 -*-
"""
Restaura o snapshot congelado do universo da pesquisa para a camada efemera.

A ALEP e uma legislatura em curso: a API continua recebendo protocolos. Executar
a Fase 1 hoje produz um universo maior que o publicado no capitulo 6 da
monografia. Este script recompoe exatamente o universo da pesquisa, permitindo
reproduzir os numeros publicados.

Uso:
    python scripts_aux/restaurar_snapshot.py

Depois disso, execute as fases 2 a 4 normalmente (coletar_detalhes_api.py,
coletar_normas_api.py, agrupar_dados_dashboard.py) e PULE a fase 1.
"""

import glob
import gzip
import hashlib
import os
import re
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SNAPSHOT_DIR = os.path.join(BASE_DIR, "dados", "snapshot_2026-03-22")
DESTINO = os.path.join(BASE_DIR, ".tmp", "raw_proposicoes")
MANIFEST = os.path.join(SNAPSHOT_DIR, "MANIFEST.md")


def hashes_do_manifesto():
    """Extrai os SHA-256 esperados da tabela do MANIFEST.md."""
    if not os.path.exists(MANIFEST):
        return {}
    esperado = {}
    with open(MANIFEST, "r", encoding="utf-8") as f:
        for linha in f:
            m = re.match(r"\|\s*(\d{4})\s*\|.*`([0-9a-f]{64})`", linha)
            if m:
                esperado[m.group(1)] = m.group(2)
    return esperado


def main():
    if not os.path.isdir(SNAPSHOT_DIR):
        sys.exit("[ERRO] Snapshot nao encontrado em %s" % SNAPSHOT_DIR)

    arquivos = sorted(glob.glob(os.path.join(SNAPSHOT_DIR, "*.json.gz")))
    if not arquivos:
        sys.exit("[ERRO] Nenhum arquivo .json.gz no snapshot.")

    os.makedirs(DESTINO, exist_ok=True)
    esperado = hashes_do_manifesto()
    divergencias = 0

    for src in arquivos:
        nome = os.path.basename(src)[:-3]  # remove .gz
        dst = os.path.join(DESTINO, nome)

        with gzip.open(src, "rb") as fi, open(dst, "wb") as fo:
            shutil.copyfileobj(fi, fo)

        with open(dst, "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()

        ano = nome.split("_")[1]
        if ano in esperado:
            if sha == esperado[ano]:
                print("[OK] %s  (integridade conferida)" % nome)
            else:
                divergencias += 1
                print("[!!] %s  SHA-256 DIVERGENTE" % nome)
                print("     esperado: %s" % esperado[ano])
                print("     obtido:   %s" % sha)
        else:
            print("[OK] %s  (sem hash no manifesto)" % nome)

    print("\nSnapshot restaurado em %s" % os.path.relpath(DESTINO, BASE_DIR))
    if divergencias:
        sys.exit("[ERRO] %d arquivo(s) com integridade divergente." % divergencias)
    print("Prossiga com as fases 2 a 4. NAO execute coletar_proposicoes_api.py.")


if __name__ == "__main__":
    main()
