# Projeto ALEP: Ecossistema Nativo de Extração, Investigação e Aprendizado Supervisionado (E.N.E.I.A.S.)

Bem-vindo ao repositório do Projeto ALEP. Este projeto consiste em uma ferramenta tecnológica de código aberto (Open Source) voltada para a estruturação, auditoria e exibição transparente dos dados legislativos da Assembleia Legislativa do Estado do Paraná (ALEP).

## 📌 Sobre o Projeto

A presente solução foi desenvolvida para mitigar o problema da "obscuridade por volume" na transparência pública. Por meio de integrações via APIs REST oficiais do Estado e um processamento algorítmico determinístico, a plataforma converte milhares de atos legislativos desestruturados em um painel analítico (Dashboard) cognitivamente acessível.

**Objetivos Principais:**
- Garantir transparência material e cognitiva.
- Mitigar assimetrias informacionais por meio da categorização temática das proposições.
- Fornecer uma interface visual estática, rápida e econômica (sem dependência de banco de dados ativo do lado do cliente).
- Obedecer rigorosamente à LGPD e ao PL 2338/2023 (Marco Legal da Inteligência Artificial), operando de forma 100% auditável.

## 🏗 Arquitetura (E.N.E.I.A.S.)

O projeto segue a arquitetura de Separação de Responsabilidades (Separation of Concerns):

1. **Camada de Diretriz (`directives/`)**: Regras de negócio, hipóteses jurídicas e limites de conformidade (LGPD) em formato Markdown.
2. **Camada de Orquestração (`GOVERNANCE.md`)**: Roteamento inteligente que define a sequência de execução garantindo a integridade dos dados e transparência algorítmica.
3. **Camada de Execução (`execution/`)**: Scripts determinísticos em Python que extraem dados via API, higienizam, categorizam e geram a estrutura de visualização.

## 📁 Estrutura de Diretórios

- `/directives/`: Diretrizes, regras de negócio e governança.
- `/execution/`: Scripts responsáveis pela extração (API) e agrupamento (ETL).
- `/docs/`: Relatórios técnicos, monografia e recursos visuais (fluxogramas).
- `/scripts_aux/`: Scripts utilitários e de manutenção secundária.
- `/index.html`: Dashboard final, estático e de alta performance.

## 🚀 Como Executar

A extração baseia-se em APIs públicas. Para atualizar o banco de dados e gerar um novo dashboard, a sequência de scripts em Python (`execution/`) deve ser orquestrada (conforme detalhado na seção técnica e em `GOVERNANCE.md`).

Os dados brutos coletados habitam o diretório transitório `.tmp/` e são expurgados/regressados com o fluxo de vida do sistema (Privacy by Design).

---
*Projeto desenvolvido para fins de auditoria cívica e transparência governamental.*
