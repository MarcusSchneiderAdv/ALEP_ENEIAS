import os
import sys
import json
import time
import requests
import urllib3

urllib3.disable_warnings()

# ==============================================================================
# SCRIPT ENEIAS - FASE ENE: EXTRACAO DE NORMAS LEGAIS
# ==============================================================================
# Objetivo: Consultar a API publica da ALEP para mapear as Leis (Normas Legais)
# convertidas e sancionadas durante a legislatura estudada (2023-2026).
#
# NOTA SOBRE O FILTRO: o parametro de exercicio e "ano". Um nome divergente
# (ex.: "anoLei") NAO produz erro: o servico ignora o filtro desconhecido,
# varre a base inteira -- o que leva cerca de dois minutos e estoura timeouts
# curtos -- e devolve todos os exercicios misturados. Falha silenciosa dessa
# especie e a mesma classe de defeito descrita na secao 5.2 da monografia.
# ==============================================================================

# Raiz do repositorio: este arquivo vive em <raiz>/execution/
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

URL_API_NORMAS = "http://webservices.assembleia.pr.leg.br/api/public/norma-legal/filtrar"
PASTA_DESTINO = os.path.join(RAIZ, ".tmp", "raw_normas")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ALEP-Crawler/1.0',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

ANOS_ALVO = [2023, 2024, 2025, 2026]
TIMEOUT = 120


def coletar_normas():
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    total_leis = 0
    falhas = []

    for ano in ANOS_ALVO:
        print(f"[*] Solicitando base de Normas Legais do ano {ano}...")

        payload = {
            "ano": ano,
            "offset": 0,
            "limit": 10000
        }

        try:
            r = requests.post(URL_API_NORMAS, json=payload, headers=HEADERS,
                              verify=False, timeout=TIMEOUT)
            if r.status_code == 200:
                dados = r.json()
                lista_normas = dados.get('lista', [])

                if not lista_normas:
                    print(f"[-] Nenhuma norma aprovada para {ano}.")
                    continue

                # Conferencia de integridade: o filtro foi de fato aplicado?
                fora = {n.get('ano') for n in lista_normas} - {ano}
                if fora:
                    print(f"[!] ATENCAO: resposta de {ano} contem exercicios "
                          f"estranhos ao filtro: {sorted(x for x in fora if x)}")
                    falhas.append(ano)
                    continue

                caminho = os.path.join(PASTA_DESTINO, f"normas_{ano}_ws_raw.json")
                with open(caminho, 'w', encoding='utf-8') as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)

                print(f"[+] Sucesso: {len(lista_normas)} leis salvas para {ano}.")
                total_leis += len(lista_normas)
            else:
                print(f"[!] Erro de requisicao no ano {ano}: HTTP {r.status_code}")
                falhas.append(ano)

        except Exception as e:
            print(f"[!] Erro de conexao para o ano {ano}: {type(e).__name__}: {e}")
            falhas.append(ano)

        time.sleep(2)  # Delay etico

    print(f"\n[OK] FINALIZADO! {total_leis} normas legais extraidas.")

    # Falha de coleta e declarada, nunca absorvida em silencio.
    # Ver GOVERNANCE.md e .agents/rules/eneias.md, secao 5.
    if falhas:
        print(f"[!] {len(falhas)} exercicio(s) sem coleta: "
              f"{', '.join(str(a) for a in falhas)}")
        sys.exit(1)


if __name__ == '__main__':
    coletar_normas()
