# -*- coding: utf-8 -*-
"""
Conferencia independente dos numeros publicados, contra a fonte.

Por que existe
    Reexecutar o pipeline nao comprova veracidade: ele e deterministico, de
    modo que dados iguais produzem resultado igual. Provaria apenas que o
    programa concorda consigo mesmo.

    Este script confere por outra via. Vai a Assembleia, baixa as proposicoes
    do zero e conta com logica propria, sem reaproveitar uma linha sequer de
    agrupar_dados_dashboard.py. Se os dois caminhos chegam ao mesmo numero,
    o numero resistiu a uma verificacao independente.

Uso
    python scripts_aux/conferir_parlamentar.py                 lista os nomes
    python scripts_aux/conferir_parlamentar.py arruda          busca parcial
    python scripts_aux/conferir_parlamentar.py arruda --leis   confere tambem as normas
    python scripts_aux/conferir_parlamentar.py --todos         confere a Casa inteira

Opcoes
    --atualizar   ignora o cache local e consulta a Assembleia de novo
    --leis        confere as normas sancionadas (uma requisicao por proposicao)
    --todos       confere os 63 parlamentares e grava um relatorio publicavel

Observacao sobre o navegador
    Nao ha versao em pagina web porque a Assembleia nao habilita CORS: o
    preflight devolve 403 e a resposta nao traz cabecalhos Access-Control.
    Uma pagina hospedada em outro dominio e impedida pelo navegador de
    consultar a API, e a conferencia precisa rodar fora dele.
"""

import gzip
import json
import os
import re
import sys
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor

import requests
import urllib3

urllib3.disable_warnings()

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL_LISTA = "http://webservices.assembleia.pr.leg.br/api/public/proposicao/filtrar"
URL_DETALHE = "http://webservices.assembleia.pr.leg.br/api/public/proposicao/{}"
ANOS = [2023, 2024, 2025, 2026]
HEADERS = {"Content-Type": "application/json", "Accept": "application/json",
           "User-Agent": "ALEP-Conferencia/1.0"}
CACHE = os.path.join(RAIZ, ".tmp", "conferencia_cache.json")
VALIDADE_CACHE = 3600  # segundos


def normalizar(texto):
    """Remove acentos e padroniza caixa, para comparar nomes sem tropecar."""
    t = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", t).strip().upper()


def signatarios(campo_autor):
    """Separa o campo de autoria em nomes. Leitura propria, do zero."""
    nomes = []
    for parte in (campo_autor or "").split(","):
        n = normalizar(parte).replace("DEPUTADO ", "").replace("DEPUTADA ", "").strip()
        if n:
            nomes.append(n)
    return nomes


# ─────────────────────────── coleta ───────────────────────────

def baixar_da_assembleia(forcar=False):
    """Consulta a Assembleia, reaproveitando cache recente por cortesia."""
    if not forcar and os.path.exists(CACHE):
        idade = time.time() - os.path.getmtime(CACHE)
        if idade < VALIDADE_CACHE:
            with open(CACHE, encoding="utf-8") as f:
                print("    usando consulta de %d min atras (--atualizar para refazer)"
                      % (idade / 60))
                return json.load(f)

    todas = []
    for ano in ANOS:
        print("    consultando %d..." % ano, end=" ", flush=True)
        r = requests.post(URL_LISTA, json={"ano": ano, "offset": 0, "limit": 10000},
                          headers=HEADERS, verify=False, timeout=120)
        r.raise_for_status()
        lista = r.json().get("lista", [])
        todas += lista
        print("%d proposicoes" % len(lista))
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(todas, f, ensure_ascii=False)
    return todas


def contar_normas(codigos):
    """Conta normas sancionadas consultando o detalhe de cada proposicao."""
    total = [0]

    def uma(cod):
        try:
            r = requests.get(URL_DETALHE.format(cod), headers=HEADERS,
                             verify=False, timeout=30)
            if r.status_code == 200:
                v = r.json().get("valor") or {}
                return len(v.get("normasLegais") or [])
        except Exception:
            pass
        return 0

    with ThreadPoolExecutor(max_workers=8) as ex:
        for n in ex.map(uma, codigos):
            total[0] += n
    return total[0]


def ler_snapshot():
    """Le o universo congelado da pesquisa, sem passar pelo pipeline."""
    base = os.path.join(RAIZ, "dados")
    if not os.path.isdir(base):
        return None, None
    pastas = sorted(d for d in os.listdir(base) if d.startswith("snapshot_"))
    if not pastas:
        return None, None
    pasta = os.path.join(base, pastas[-1])
    todas = []
    for nome in sorted(os.listdir(pasta)):
        if nome.endswith(".json.gz"):
            with gzip.open(os.path.join(pasta, nome), "rt", encoding="utf-8") as f:
                todas += json.load(f).get("lista", [])
    return todas, pastas[-1].replace("snapshot_", "")


def ler_painel():
    """Le o que o painel publica, sem recalcular nada."""
    caminho = os.path.join(RAIZ, "DADOS_ALEP_20.js")
    if not os.path.exists(caminho):
        return {}
    with open(caminho, encoding="utf-8") as f:
        bruto = f.read()
    dados = json.loads(bruto.split("const DADOS = ", 1)[1].rsplit(";", 1)[0])
    return {normalizar(d["nome"]): d for d in dados}


# ─────────────────────────── conferencia ───────────────────────────

def contagem(proposicoes, alvo):
    dele = [p for p in proposicoes if alvo in signatarios(p.get("autor"))]
    tipos = {}
    for p in dele:
        tipos[p.get("tipoProposicao")] = tipos.get(p.get("tipoProposicao"), 0) + 1
    return dele, tipos


def resolver_nome(busca, painel):
    """Aceita nome parcial e sem acento. Devolve o nome canonico."""
    alvo = normalizar(busca)
    if alvo in painel:
        return alvo
    achados = [n for n in painel if alvo in n]
    if len(achados) == 1:
        return achados[0]
    if not achados:
        print("Nenhum parlamentar contem '%s'." % busca)
        print("Rode sem argumento para ver a lista completa.")
    else:
        print("'%s' corresponde a mais de um parlamentar:" % busca)
        for n in sorted(achados):
            print("    %s" % n)
        print("Refine a busca.")
    return None


def listar(painel):
    print("Parlamentares disponiveis para conferencia:\n")
    for n in sorted(painel):
        print("    %-34s %d proposicoes" % (n, painel[n]["proposicoes_count"]))
    print("\nUse: python scripts_aux/conferir_parlamentar.py \"<parte do nome>\"")


def conferir_um(alvo, hoje, congelado, marca, painel, com_leis):
    pub = painel.get(alvo)
    dele_hoje, tipos_hoje = contagem(hoje, alvo)
    dele_cong, tipos_cong = (contagem(congelado, alvo) if congelado else ([], {}))

    print("\n" + "=" * 64)
    print("CONFERENCIA INDEPENDENTE: %s" % alvo)
    print("=" * 64)
    print("  Assembleia hoje .................: %d proposicoes" % len(dele_hoje))
    if congelado:
        print("  Universo congelado (%s) ..: %d proposicoes" % (marca, len(dele_cong)))
    if pub:
        print("  Publicado no painel ..............: %d proposicoes" % pub["proposicoes_count"])

    ok = pub and congelado and pub["proposicoes_count"] == len(dele_cong)
    print("")
    if ok:
        print("  [OK] O painel reproduz a contagem independente sobre o mesmo")
        print("       universo. O numero resistiu a verificacao.")
    elif pub and congelado:
        print("  [!!] DIVERGENCIA: painel %d, contagem independente %d."
              % (pub["proposicoes_count"], len(dele_cong)))

    novas = len(dele_hoje) - len(dele_cong)
    if congelado and novas:
        print("")
        print("  Diferenca para hoje: %+d. Nao e erro: sao protocolos" % novas)
        print("  posteriores ao fechamento do universo da pesquisa.")

    print("\n  Composicao por especie:")
    print("    %-38s %6s %8s" % ("", "hoje", marca or ""))
    for t, c in sorted(tipos_hoje.items(), key=lambda kv: -kv[1]):
        print("    %-38s %6d %8s" % (t, c, tipos_cong.get(t, 0) if congelado else ""))

    if com_leis and congelado:
        print("\n  Conferindo normas sancionadas (uma requisicao por proposicao)...")
        n = contar_normas([p.get("codigo") for p in dele_cong])
        print("    contagem independente ...: %d" % n)
        if pub:
            print("    publicado no painel .....: %d" % pub["leis_count"])
            print("    %s" % ("[OK] confere" if n == pub["leis_count"] else "[!!] DIVERGE"))
    return ok


def conferir_todos(hoje, congelado, marca, painel):
    linhas = []
    conferem = divergem = 0
    for alvo in sorted(painel):
        dele_cong, _ = contagem(congelado, alvo)
        dele_hoje, _ = contagem(hoje, alvo)
        pub = painel[alvo]["proposicoes_count"]
        bate = pub == len(dele_cong)
        conferem += bate
        divergem += not bate
        linhas.append((alvo, pub, len(dele_cong), len(dele_hoje), bate))
        print("    %-34s painel %4d | independente %4d  %s"
              % (alvo, pub, len(dele_cong), "OK" if bate else "<<< DIVERGE"))

    print("\n  %d conferem, %d divergem." % (conferem, divergem))

    destino = os.path.join(RAIZ, "dados", "conferencia")
    os.makedirs(destino, exist_ok=True)
    caminho = os.path.join(destino, "CONFERENCIA.md")
    with open(caminho, "w", encoding="utf-8") as f:
        f.write("# Conferencia independente dos numeros publicados\n\n")
        f.write("Contagem feita por rotina propria, sem reaproveitar o codigo do\n")
        f.write("pipeline, sobre o universo congelado em %s. A coluna \"hoje\"\n" % marca)
        f.write("mostra o estado atual da Assembleia, maior porque a legislatura\n")
        f.write("segue em curso.\n\n")
        f.write("Resultado: **%d conferem, %d divergem**.\n\n" % (conferem, divergem))
        f.write("| Parlamentar | Painel | Contagem independente | Confere | Hoje |\n")
        f.write("|---|---:|---:|:---:|---:|\n")
        for nome, pub, cong, hj, bate in linhas:
            f.write("| %s | %d | %d | %s | %d |\n"
                    % (nome, pub, cong, "sim" if bate else "**NAO**", hj))
        f.write("\nPara repetir: `python scripts_aux/conferir_parlamentar.py --todos`\n")
    print("  Relatorio gravado em dados/conferencia/CONFERENCIA.md")
    return divergem == 0


def main():
    args = [a for a in sys.argv[1:]]
    forcar = "--atualizar" in args
    com_leis = "--leis" in args
    todos = "--todos" in args
    busca = " ".join(a for a in args if not a.startswith("--"))

    painel = ler_painel()
    if not painel:
        sys.exit("[ERRO] DADOS_ALEP_20.js nao encontrado. Rode 'python executar.py' antes.")

    if not busca and not todos:
        listar(painel)
        return

    print("[1] Consultando a Assembleia")
    hoje = baixar_da_assembleia(forcar)
    print("[2] Lendo o universo congelado da pesquisa")
    congelado, marca = ler_snapshot()
    if congelado:
        print("    snapshot de %s: %d proposicoes" % (marca, len(congelado)))

    if todos:
        print("\n[3] Conferindo os %d parlamentares\n" % len(painel))
        ok = conferir_todos(hoje, congelado, marca, painel)
    else:
        alvo = resolver_nome(busca, painel)
        if not alvo:
            return
        ok = conferir_um(alvo, hoje, congelado, marca, painel, com_leis)

    print("\n  Conferencia manual, sem instalar nada: https://www.assembleia.pr.leg.br")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
