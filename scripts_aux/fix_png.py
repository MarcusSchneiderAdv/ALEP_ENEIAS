import requests
import os

code = """
graph TD
    classDef api fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef tmp fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5;
    classDef process fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    classDef front fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef citizen fill:#111,stroke:#333,stroke-width:2px,color:#fff;

    subgraph FASE_1 ["1. INGESTÃO VIA APIs REST"]
        API_A("API ALEP: Proposições") --> |coletar_proposicoes_api.py| RAW1
        API_B("API ALEP: Detalhes") --> |coletar_detalhes_api.py| RAW2
        API_C("API ALEP: Normas Legais") --> |coletar_normas_api.py| RAW3
    end
    class API_A,API_B,API_C api;

    subgraph FASE_2 ["2. GOVERNANÇA EFÊMERA /.tmp/"]
        RAW1[("raw_proposicoes/*.json")]
        RAW2[("raw_detalhes/*.json")]
        RAW3[("raw_normas/*.json")]
    end
    class RAW1,RAW2,RAW3 tmp;

    RAW1 --> ETL
    RAW2 --> ETL
    RAW3 --> ETL

    subgraph FASE_3 ["3. PIPELINE ETL & ORQUESTRAÇÃO"]
        ETL[["agrupar_dados_dashboard.py"]]
        ETL --> |"1. Leitura JSON"| P1("Higienização Termos")
        P1 --> |"2. Segmentação"| P2("Co-Autoria Distribuição")
        P2 --> |"3. Tipologia"| P3("Cálculo Estático")
    end
    class ETL,P1,P2,P3 process;

    subgraph FASE_4 ["4. STATIC PAYLOAD"]
        PAYLOAD[("DADOS_ALEP_20.js")]
        HTML{{"dashboard_20_leg.html"}}
        
        P3 -->|"Serialização"| PAYLOAD
        PAYLOAD -.->|"Consumo (Browser)"| HTML
    end
    class PAYLOAD,HTML front;

    HTML --> CITIZEN(("Cidadão/Eleitor"))
    class CITIZEN citizen;
"""

root_dir = r"c:\Users\Marcus Schneider\Documents\Marcus\2026\Projetos\Fase_final_Apresentação\ALEP"

print("Gerando Fluxograma 01 corrigido...")
try:
    r = requests.post(
        "https://kroki.io/mermaid/png", 
        headers={"Content-Type": "text/plain"},
        data=code.encode('utf-8')
    )
    if r.status_code == 200:
        file_path = os.path.join(root_dir, "Fluxograma_01_Arquitetura_ENEIAS.png")
        with open(file_path, "wb") as f:
            f.write(r.content)
        print(f"[OK] Salvo: {file_path}")
    else:
        print(f"[ERRO] {r.status_code} - {r.text}")
except Exception as e:
    print(f"[EXCEP] {e}")
