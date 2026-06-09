import requests
import os

DIAGRAMS = {
    "Fluxograma_01_Arquitetura_ENEIAS": """
graph TD
    classDef api fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef tmp fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5;
    classDef process fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    classDef front fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef citizen fill:#111,stroke:#333,stroke-width:2px,color:#fff;

    subgraph FASE_1 [1. INGESTÃO VIA APIs REST]
        API_A(API ALEP: Proposições) --> |coletar_proposicoes_api.py| RAW1
        API_B(API ALEP: Detalhes/Assíncrono) --> |coletar_detalhes_api.py| RAW2
        API_C(API ALEP: Normas Legais) --> |coletar_normas_api.py| RAW3
    end
    class API_A,API_B,API_C api;

    subgraph FASE_2 [2. GOVERNANÇA EFÊMERA /.tmp/]
        RAW1[(raw_proposicoes/*.json)]
        RAW2[(raw_detalhes/*.json)]
        RAW3[(raw_normas/*.json)]
    end
    class RAW1,RAW2,RAW3 tmp;

    RAW1 ==> ETL
    RAW2 ==> ETL
    RAW3 ==> ETL

    subgraph FASE_3 [3. PIPELINE ETL & ORQUESTRAÇÃO]
        ETL[[agrupar_dados_dashboard.py]]
        ETL --> |1. Leitura JSON| P1(Higienização Termos)
        P1 --> |2. Segmentação| P2(Co-Autoria Distribuição)
        P2 --> |3. Tipologia| P3(Cálculo Estático)
    end
    class ETL,P1,P2,P3 process;

    subgraph FASE_4 [4. STATIC PAYLOAD]
        PAYLOAD[(DADOS_ALEP_20.js)]
        HTML{{dashboard_20_leg.html}}
        
        P3 -->|Serialização| PAYLOAD
        PAYLOAD -.->|Consumo (Browser)| HTML
    end
    class PAYLOAD,HTML front;

    HTML ==> CITIZEN((Cidadão/Eleitor))
    class CITIZEN citizen;
    """,

    "Fluxograma_02_Processamento_Deterministico": """
graph TD
    classDef extract fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef logic fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef out fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;

    IN[Matriz JSON Bruta ALEP] --> P1{Institucional?}
    P1 -->|Sim| DROP[Descartar Governo e Comissões]
    P1 -->|Não| P2[Filtrar Deputados]
    
    P2 --> P3{Nº Autores > 1?}
    P3 -->|Sim| LOOP[Loop: Fragmentar P/ Coautores]
    P3 -->|Não| SINGLE[Processar Autor Primário]
    
    LOOP --> LOGIC
    SINGLE --> LOGIC
    
    LOGIC[Extrair Metadado Oficial: <br>'tipoProposicao' e 'assunto'] --> CAT{Filtragem Rule-Based}
    
    CAT --> |Projeto de Lei| G1[Eixo Normativo Material]
    CAT --> |Requerimentos| G2[Eixo Administrativo/Fiscalização]
    CAT --> |Homenagens| G3[Eixo Simbólico]
    
    G1 --> OK[Estatísticas consolidadas por Deputado]
    G2 --> OK
    G3 --> OK

    class IN,DROP extract;
    class P1,P2,P3,LOOP,SINGLE,LOGIC,CAT logic;
    class G1,G2,G3,OK out;
    """,

    "Fluxograma_03_Governanca_Efêmera_LGPD": """
sequenceDiagram
    participant API as Portal ALEP (REST)
    participant ENEIAS as Extração Python
    participant TMP as .tmp/ (Data Lake)
    participant PROCESS as ETL / Pipeline
    participant FRONT as Memória Final (.js)

    API->>ENEIAS: Payload 100% Bruto (Contém lixo e dados excendentes)
    ENEIAS->>TMP: Salva json íntegro na pasta oculta
    Note over TMP: Isolamento Transiente<br/>(Gov. Efêmera)
    PROCESS->>TMP: Busca o JSON para parsing
    PROCESS->>PROCESS: Filtro Minimização (Elimina terceiros não notórios)
    PROCESS->>PROCESS: Segrega apenas Metadados Matemáticos (Autor, Tipologia, Voto)
    PROCESS->>FRONT: Monta o Mega-Dicionário Final
    Note over TMP,PROCESS: Ao finalizar processamento,<br/>a pasta efêmera pode ser purgada
    """
}

root_dir = r"c:\Users\Marcus Schneider\Documents\Marcus\2026\Projetos\Fase_final_Apresentação\ALEP"

def baixar_mermaids():
    for name, code in DIAGRAMS.items():
        print(f"Gerando {name}.png...")
        try:
            # Serviço robusto: Kroki
            # Pode passar plain-text via POST
            r = requests.post(
                "https://kroki.io/mermaid/png", 
                headers={"Content-Type": "text/plain"},
                data=code.encode('utf-8')
            )
            
            if r.status_code == 200:
                file_path = os.path.join(root_dir, f"{name}.png")
                with open(file_path, "wb") as f:
                    f.write(r.content)
                print(f"[OK] Salvo: {file_path}")
            else:
                print(f"[ERRO] Falhou para {name}. Codigo: {r.status_code}")
        except Exception as e:
            print(f"[EXCEP] Erro ao conectar com API para {name}: {e}")

if __name__ == "__main__":
    baixar_mermaids()
