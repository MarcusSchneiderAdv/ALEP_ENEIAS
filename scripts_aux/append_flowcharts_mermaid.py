import os

flowcharts = """

--- APÊNDICE: FLUXOGRAMAS E.N.E.I.A.S. ---

### 1. Arquitetura E.N.E.I.A.S. - Fluxo de Extração e Processamento
```mermaid
flowchart TD
    ALEP[("API REST ALEP - Fonte")]

    subgraph Fase1_2["Fase 1 e 2: Ingestão e Governança Efêmera"]
        Script1["coletar_proposicoes_api.py"]
        TMP[/"Diretório Temporário - Data Lake Efêmero"/]
    end

    subgraph Fase3["Fase 3: Enriquecimento Assíncrono"]
        Script2["coletar_detalhes_api.py"]
        Threads["Pool de Paralelismo - ThreadPoolExecutor"]
    end

    subgraph Fase4["Fase 4: Processamento Estrutural - ETL"]
        Script3["agrupar_dados_dashboard.py"]
        ETL_Steps["Higienização de Strings, Fragmentação e Categorização"]
        Payload["Static Payload - Dicionário Consolidado"]
    end

    subgraph Fase5["Fase 5: Interface Gráfica - Dashboard"]
        HTML["dashboard.html"]
        Browser["Navegador do Eleitor - Renderização Estática"]
    end

    ALEP -- "Requisição HTTP via JSON" --> Script1
    Script1 -- "Despejo de Matrizes Brutas - Privacy by Design" --> TMP
    TMP --> Script2
    Script2 -- "Consultas Paralelas de Trâmites" --> Threads
    Threads -- "Dados Enriquecidos" --> Script3
    Script3 --> ETL_Steps
    ETL_Steps -- "Serialização" --> Payload
    Payload -- "Injeção de Dados Estáticos" --> HTML
    HTML -- "Transparência Cognitiva" --> Browser

    classDef script fill:#f9f,stroke:#333,stroke-width:2px;
    classDef storage fill:#ff9,stroke:#333,stroke-width:2px;
    class TMP,Payload storage;
    class Script1,Script2,Script3 script;
```

### 2. Governança de Dados e Conformidade (LGPD e Transparência Algorítmica)
```mermaid
flowchart LR
    RawData[/"Dados Brutos da API - JSON Não Tratado"/]
    
    subgraph GovEf["Governança Efêmera - Privacy by Design"]
        DirTMP[("Data Lake Transitório - Pasta .tmp")]
        Purge["Expurgo Contínuo - Mitigação de Retenção"]
    end

    subgraph AudTransp["Processamento Determinístico e Auditável"]
        Regras["Regras Estruturais Fixas - Sem Viés de IA"]
        Separacao["Separação por Tipologia - Leis, Requerimentos"]
        OpenSource["Repositório Open Source - Transparência Algorítmica"]
    end

    Metric["Painel de Jurimetria Cívica - Sem Nomes de Terceiros / LGPD"]

    RawData -- "Ingestão" --> DirTMP
    DirTMP -. "Recriação e Limpeza" .-> Purge
    DirTMP -- "Consumo para ETL" --> Regras
    Regras --> Separacao
    Separacao -- "Código Aberto Auditável" --> OpenSource
    Separacao -- "Dados Minimizados" --> Metric
    
    classDef secure fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef logic fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    class DirTMP,Purge,Metric secure;
    class Regras,Separacao,OpenSource logic;
```

### 3. Lógica de Processamento Estrutural (Tratamento de Coautoria)
```mermaid
flowchart TD
    Input[/"Matriz JSON de Proposição - Lista de Autores"/]

    Iteracao{"Para cada parlamentar na lista"}
    Check{"O Índice é igual a zero?"}
    AutorPrincipal["Registrar como Autor Principal - Flag False"]
    Coautor["Registrar como Coautor - Flag True"]
    Dicionario[/"DICIONARIO_DEPUTADOS - Métricas Atualizadas"/]

    Input --> Iteracao
    Iteracao --> Check
    Check -- "Sim" --> AutorPrincipal
    Check -- "Não - Índice maior que zero" --> Coautor
    AutorPrincipal --> Dicionario
    Coautor --> Dicionario

    classDef process fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    class Iteracao,Check process;
```
"""

file_path = r'C:\Users\Marcus Schneider\Documents\Marcus\2026\Projetos Antigravity\ALEP\Projeto_ALEP_Revisao_08_06_2026.txt'
with open(file_path, 'a', encoding='utf-8') as f:
    f.write(flowcharts)
