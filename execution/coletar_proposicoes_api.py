import requests
import json
import os
import time
import urllib3

urllib3.disable_warnings()

# ==============================================================================
# SCRIPT ENEIAS - FASE ENE: EXTRAÇÃO DE PROPOSIÇÕES ABERTAS (ALEP WS)
# ==============================================================================
# Objetivo: Realizar a raspagem em lote de todas as proposições via WebService Oficial
# da Assembleia. O script varre a 20ª Legislatura inteira e salva os JSONs brutos.
#
# URL Base: http://webservices.assembleia.pr.leg.br/api/public
# Método: POST /proposicao/filtrar
# ==============================================================================

URL_API = "http://webservices.assembleia.pr.leg.br/api/public/proposicao/filtrar"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Analytics/1.0',
    'Content-Type': 'application/json'
}

ANOS_ALVO = [2023, 2024, 2025, 2026]
PASTA_DESTINO = "../.tmp/raw_proposicoes"

def coletar_proposicoes():
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    
    total_geral = 0
    for ano in ANOS_ALVO:
        print(f"[*] Iniciando extração do ano {ano}...")
        
        # Paginação configurada alta para extração full-dump no WebService
        payload = {
            "ano": ano,
            "offset": 0,
            "limit": 10000
        }
        
        try:
            r = requests.post(URL_API, json=payload, headers=HEADERS, verify=False, timeout=30)
            if r.status_code == 200:
                dados = r.json()
                lista_proposicoes = dados.get('lista', [])
                
                if not lista_proposicoes:
                    print(f"[-] Nenhuma proposição encontrada para {ano}.")
                    continue
                
                # Salvando dump bruto localmente para reuso da API (Fase ENE)
                caminho_arquivo = os.path.join(PASTA_DESTINO, f"proposicoes_{ano}_ws_raw.json")
                with open(caminho_arquivo, "w", encoding='utf-8') as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)
                    
                print(f"[+] Sucesso! Ano {ano} salvo com {len(lista_proposicoes)} registros em {caminho_arquivo}")
                total_geral += len(lista_proposicoes)
            else:
                print(f"[!] Erro no ano {ano}: Código {r.status_code} - {r.text}")
                
        except Exception as e:
            print(f"[!] Falha crítica de conexão no ano {ano}: {str(e)}")
            
        # Rate limit respeitoso para WS Governamental
        time.sleep(2)
        
    print(f"\n[✔️] FINALIZADO! Total de Proposições Extraídas: {total_geral}")

if __name__ == "__main__":
    coletar_proposicoes()
