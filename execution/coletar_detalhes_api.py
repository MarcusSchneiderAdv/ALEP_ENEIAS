import os
import glob
import json
import time
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()

# ==============================================================================
# SCRIPT ENEIAS - FASE ENE: EXTRAÇÃO DE DETALHES DE PROPOSIÇÕES
# ==============================================================================
# Objetivo: Acessar a API pública `/proposicao/{código}` para baixar a ementa
# detalhada, histórico de trâmites e coautorias (quando aplicável) de todas as
# proposições coletadas no script anterior.
# ==============================================================================

URL_BASE = "http://webservices.assembleia.pr.leg.br/api/public/proposicao/{}"
PASTA_PROPOSICOES = "../.tmp/raw_proposicoes"
PASTA_DETALHES = "../.tmp/raw_detalhes"
MAX_WORKERS = 10  # Pool assíncrono

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ALEP-Dados-Abertos/1.0',
    'Accept': 'application/json'
}

def carregar_proposicoes_alvo():
    """Lê todas as proposições já baixadas na Fase ENE Primária."""
    arquivos = glob.glob(os.path.join(PASTA_PROPOSICOES, "*.json"))
    codigos_alvo = set()
    
    for arq in arquivos:
        try:
            with open(arq, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                for p in dados.get('lista', []):
                    codigo = p.get('codigo')
                    if codigo:
                        codigos_alvo.add(str(codigo))
        except Exception as e:
            print(f"[!] Erro ao ler {arq}: {e}")
            
    return list(codigos_alvo)

def baixar_detalhe(codigo):
    arquivo_local = os.path.join(PASTA_DETALHES, f"{codigo}.json")
    if os.path.exists(arquivo_local):
        return None  # Já processado
        
    url = URL_BASE.format(codigo)
    try:
        r = requests.get(url, headers=HEADERS, verify=False, timeout=15)
        if r.status_code == 200:
            dados = r.json()
            with open(arquivo_local, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False)
            return True
    except Exception:
        pass
    
    return False

def coletar_detalhes():
    os.makedirs(PASTA_DETALHES, exist_ok=True)
    alvos = carregar_proposicoes_alvo()
    print(f"[*] Total de {len(alvos)} códigos de proposições detectados para mineração de detalhes.")
    
    novos = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futuros = {executor.submit(baixar_detalhe, cod): cod for cod in alvos}
        
        for idx, futuro in enumerate(as_completed(futuros)):
            if futuro.result() is True:
                novos += 1
            
            if (idx + 1) % 500 == 0:
                print(f"[>] Processado {idx + 1} de {len(alvos)}... ({novos} baixados até agora)")
                
    print(f"\n[✔️] FINALIZADO! {novos} novos arquivos de detalhes salvos em .tmp/raw_detalhes/")

if __name__ == '__main__':
    coletar_detalhes()
