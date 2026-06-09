import os
import glob
import json
import time
import requests
import urllib3

urllib3.disable_warnings()

# ==============================================================================
# SCRIPT ENEIAS - FASE ENE: EXTRAÇÃO DE NORMAS LEGAIS
# ==============================================================================
# Objetivo: Realizar consultas na API Pública da ALEP para mapear as Leis
# (Normas Legais) convertidas, estruturadas e aprovadas durante a
# respectiva legislatura estudada (2023-2026).
# ==============================================================================

URL_API_NORMAS = "http://webservices.assembleia.pr.leg.br/api/public/norma-legal/filtrar"
PASTA_DESTINO = "../.tmp/raw_normas"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ALEP-Crawler/1.0',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

ANOS_ALVO = [2023, 2024, 2025, 2026]

def coletar_normas():
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    total_leis = 0
    
    for ano in ANOS_ALVO:
        print(f"[*] Solicitando base de Normas Legais do ano {ano}...")
        
        # Paginação máxima
        payload = {
            "anoLei": ano,
            "offset": 0,
            "limit": 10000
        }
        
        try:
            r = requests.post(URL_API_NORMAS, json=payload, headers=HEADERS, verify=False, timeout=30)
            if r.status_code == 200:
                dados = r.json()
                lista_normas = dados.get('lista', [])
                
                if not lista_normas:
                    print(f"[-] Nenhuma norma aprovada para {ano}.")
                    continue
                    
                caminho = os.path.join(PASTA_DESTINO, f"normas_{ano}_ws.json")
                with open(caminho, 'w', encoding='utf-8') as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)
                    
                print(f"[+] Sucesso salvando {len(lista_normas)} leis para {ano}.")
                total_leis += len(lista_normas)
            else:
                print(f"[!] Erro de requisição no ano {ano}: {r.status_code}")
                
        except Exception as e:
            print(f"[!] Erro fatal de conexão para o ano {ano}: {e}")
            
        time.sleep(2)  # Delay ético

    print(f"\n[✔️] FINALIZADO! {total_leis} NORMAS LEGAIS EXTRAÍDAS TOTAL.")

if __name__ == '__main__':
    coletar_normas()
