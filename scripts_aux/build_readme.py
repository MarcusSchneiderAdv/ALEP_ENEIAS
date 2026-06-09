import os
import re

# Caminhos dos arquivos
base_dir = r"c:\Users\Marcus Schneider\Documents\Marcus\2026\Projetos Antigravity\ALEP"
input_path = os.path.join(base_dir, "docs", "monografia", "Projeto_ALEP_Revisao_08_06_2026.txt")
output_path = os.path.join(base_dir, "README.md")

# Diagramas Mermaid para embutir
DIAGRAM_ARQUITETURA = """
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
"""

DIAGRAM_GOVERNANCA = """
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
"""

DIAGRAM_COAUTORIA = """
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

def main():
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Separar o apêndice de fluxogramas original se existir (para não duplicar)
    content_main = content.split("--- APÊNDICE: FLUXOGRAMAS E.N.E.I.A.S. ---")[0].strip()

    # Formatar títulos e subtítulos da Monografia para Markdown
    # Exemplo: "1. INTRODUÇÃO" -> "## 1. INTRODUÇÃO"
    # "1.1. O Problema..." -> "### 1.1. O Problema..."
    lines = content_main.split("\n")
    formatted_lines = []
    
    for line in lines:
        line_strip = line.strip()
        # Se for um título principal (ex: 1. INTRODUÇÃO)
        if re.match(r"^\d+\.\s+[A-ZÂÃÇÉÍÓÚ\s]+$", line_strip):
            formatted_lines.append(f"\n## {line_strip}\n")
        # Se for um subtítulo de segundo nível (ex: 1.1. O Problema...)
        elif re.match(r"^\d+\.\d+\.\s+[A-Z]", line_strip):
            formatted_lines.append(f"\n### {line_strip}\n")
        # Se for um subtítulo de terceiro nível (ex: 5.3.1. Orquestração...)
        elif re.match(r"^\d+\.\d+\.\d+\.\s+[A-Z]", line_strip):
            formatted_lines.append(f"\n#### {line_strip}\n")
        else:
            formatted_lines.append(line)

    full_text = "\n".join(formatted_lines)

    # Inserção inteligente dos diagramas e fluxogramas
    
    # 1. Fluxograma de Governança (LGPD) em "4.3. Conformidade Regulatória no Tratamento de Dados Governamentais (LGPD e PL 2338/2023)"
    # Encontra o final da seção 4.3 e insere o diagrama
    target_lgpd = "respeita integralmente o rigor ético, legal e regulatório do Estado brasileiro."
    lgpd_diagram_block = f"\n\n#### **Fluxograma 03: Governança de Dados e Conformidade (LGPD)**\n\n{DIAGRAM_GOVERNANCA}\n\n*Figura 3: Representação visual do fluxo de dados efêmeros sob as diretrizes de privacidade por design.*\n\n"
    full_text = full_text.replace(target_lgpd, target_lgpd + lgpd_diagram_block)

    # 2. Fluxograma de Processamento de Coautoria em "5.2. Processamento Estrutural e Classificação Temática"
    target_coautoria = "eliminando omissões estatísticas sem a necessidade de intervenção humana."
    coautoria_diagram_block = f"\n\n#### **Fluxograma 02: Lógica de Processamento Estrutural (Coautoria)**\n\n{DIAGRAM_COAUTORIA}\n\n*Figura 2: Diagrama de decisão sobre a fragmentação e distribuição de mérito de coautoria.*\n\n"
    full_text = full_text.replace(target_coautoria, target_coautoria + coautoria_diagram_block)

    # 3. Fluxograma de Arquitetura ENEIAS em "5.3.1. Orquestração e Sequência de Execução do Pipeline"
    # A Figura 1 ilustra a arquitetura E.N.E.I.A.S. em sua totalidade...
    target_arquitetura = "culmina na entrega da carga útil estática na interface do usuário."
    arquitetura_diagram_block = f"\n\n#### **Fluxograma 01: Arquitetura Geral E.N.E.I.A.S.**\n\n{DIAGRAM_ARQUITETURA}\n\n*Figura 1: Visão geral da arquitetura E.N.E.I.A.S. e fluxo de dados do backend ao front-end.*\n\n"
    full_text = full_text.replace(target_arquitetura, target_arquitetura + arquitetura_diagram_block)

    # Construir o README.md final
    readme_template = f"""# Projeto ALEP: Ecossistema Nativo de Extração, Investigação e Aprendizado Supervisionado (E.N.E.I.A.S.)

Repositório oficial do Projeto ALEP. Este projeto consiste em uma ferramenta tecnológica de código aberto (Open Source) voltada para a estruturação, auditoria e exibição transparente dos dados legislativos da Assembleia Legislativa do Estado do Paraná (ALEP).

---

## 📖 Monografia e Estudo de Caso

Abaixo, encontra-se a monografia completa detalhando os fundamentos jurídicos, teóricos e a arquitetura tecnológica do ecossistema E.N.E.I.A.S.

{full_text}

---

## 🏗 Estrutura do Repositório (Apêndice A)

*   `/directives/`: Diretrizes de negócio, SOPs, conformidade legal e critérios de auditoria.
*   `/execution/`: Scripts Python determinísticos focados na coleta (API) e transformação (ETL).
*   `/docs/`:
    *   `/monografia/`: Textos originais e revisões da pesquisa.
    *   `/assets/`: Fluxogramas e recursos visuais em formato de imagem.
*   `/scripts_aux/`: Scripts auxiliares de manutenção e tratamento de texto.
*   `.gitignore`: Filtro de exclusão de arquivos de dados pesados e efêmeros (`.tmp/`, `DADOS_ALEP_20.js`, `Citações/`).
*   `GOVERNANCE.md`: Regras de orquestração do pipeline de dados e arquitetura.
*   `README.md`: Este arquivo com o estudo completo integrado.

---
*Estudo acadêmico-tecnológico desenvolvido para fins de transparência material e cognitiva no controle social.*
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_template)
    print("README.md gerado com sucesso com a monografia e os fluxogramas integrados!")

if __name__ == "__main__":
    main()
