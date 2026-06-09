import os
import json
import requests
import time
import urllib3

urllib3.disable_warnings()

# ==============================================================================
# SCRIPT ENEIAS - FASE ENE: EXTRAÇÃO REGISTROS DE PRESENÇA (BETA)
# ==============================================================================
# Objetivo: Realizar consultas de assiduidade parlamentar no portal da Transparência
# / API da ALEP para cruzar o comparecimento às Sessões Plenárias.
# ==============================================================================

URL_PRESENCA = "https://www.assembleia.pr.leg.br/api/deputado/{id}/presenca"
PASTA_DESTINO = "../.tmp/raw_presenca"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ALEP-Transparencia-Datalake/1.0',
    'Accept': 'application/json'
}

# IDs fictícios/mapeados da rede E-Processo da ALEP (exemplo estático referencial para a rotina)
DEPUTADOS_IDS = [1, 2, 3, 4]  # Esta base dinamicamente derivará das Proposições

def coletar_presencas():
    os.makedirs(PASTA_DESTINO, exist_ok=True)
    print(f"[*] Iniciando mapeamento de presença para {len(DEPUTADOS_IDS)} deputados mapeados...")
    
    sucessos = 0
    for dep_id in DEPUTADOS_IDS:
        url = URL_PRESENCA.format(id=dep_id)
        
        try:
            r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
            if r.status_code == 200:
                dados = r.json()
                caminho = os.path.join(PASTA_DESTINO, f"presenca_deputado_{dep_id}.json")
                
                with open(caminho, 'w', encoding='utf-8') as f:
                    json.dump(dados, f, ensure_ascii=False, indent=2)
                sucessos += 1
                
        except Exception as e:
            print(f"[!] Erro ao varrer presença do ID {dep_id}: {e}")
            
        time.sleep(1)
        
    print(f"\n[✔️] ROTINA CONCLUÍDA! {sucessos} extratos de presença gerados.")

if __name__ == '__main__':
    coletar_presencas()
