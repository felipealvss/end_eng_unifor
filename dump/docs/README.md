
# 📊 Projeto de Engenharia de Dados Híbrido

## 🔍 Visão Geral

Este projeto tem como objetivo construir um pipeline de dados híbrido, integrando uma fonte externa (API pública), armazenamento em banco NoSQL na nuvem (MongoDB Atlas), processamento analítico local (DuckDB), e estruturação dos dados em camadas de valor (bronze, prata e ouro). O pipeline é encapsulado com Docker, garantindo portabilidade e consistência entre ambientes.

---

## 📁 Arquitetura Conceitual

### Etapas do Pipeline:

1. **Ingestão**: Coleta de dados de uma API pública.
2. **Armazenamento inicial**: Inserção dos dados brutos no MongoDB Atlas (camada bronze).
3. **Extração local**: Leitura dos dados do Atlas para ambiente local.
4. **Processamento com DuckDB**:
   - Bronze: dados crus.
   - Prata: dados limpos e padronizados.
   - Ouro: dados enriquecidos e prontos para análise.
5. **Armazenamento final**: Upload dos arquivos transformados para um Blob Storage (ex: Amazon S3).
6. **Disponibilização**: Acesso para áreas de negócio ou ferramentas de BI.

---

## 🔁 Fluxograma Conceitual

```text
[1] API Pública (Fonte de Dados)
        |
        v
[2] Ingestão via Python (requests)
        |
        v
[3] Armazenamento Bruto em MongoDB Atlas (Camada Bronze)
        |
        v
[4] Extração Local via PyMongo
        |
        v
[5] Processamento Local com DuckDB
        |        |        |
        |        |        |
    [Bronze] [Prata] [Ouro]
        |        |        |
        |        |        |
        v        v        v
[6] Salvamento Local (Parquet/CSV por camada)
        |
        v
[7] Upload para Blob Storage (Amazon S3 ou equivalente)
        |
        v
[8] Acesso por Times de Negócio / Ferramentas de BI
````

---

## 📅 Cronograma de Execução

| Semana | Etapa                                | Objetivo                                                           |
| ------ | ------------------------------------ | ------------------------------------------------------------------ |
| 1      | Definição de escopo e escolha da API | Determinar domínio, dados necessários, API a ser usada             |
| 2      | Criação do cluster MongoDB Atlas     | Configurar banco, testar conexão e estrutura inicial de documentos |
| 3      | Implementação da ingestão de dados   | Escrever script para coletar dados da API e salvar no Atlas        |
| 4      | Extração local e estudo do DuckDB    | Aprender uso do DuckDB e testar conexão e carregamento             |
| 5      | Construção da camada Bronze          | Armazenar dados crus localmente (sem alterações)                   |
| 6      | Construção da camada Prata           | Limpeza, padronização de tipos, estruturação                       |
| 7      | Construção da camada Ouro            | Enriquecimento, agregações, indicadores                            |
| 8      | Upload para Blob Storage             | Configurar conta e salvar os arquivos por camada                   |
| 9      | Implementação e teste com Docker     | Criar Dockerfile, montar ambiente e testar pipeline containerizado |
| 10     | Acesso e documentação para o negócio | Organizar dados finais e criar documentação de acesso/uso para BI  |
| 11     | Testes finais e orquestração simples | Automatizar execução com cron ou orquestrador leve                 |
| 12     | Entrega final do projeto             | Apresentação, relatório e checklist técnico-final                  |

---

## 🐳 Docker no Projeto

### Objetivo:

* Garantir isolamento de ambiente, reprodutibilidade e facilidade de uso.

### Componentes:

* Dockerfile com ambiente Python e bibliotecas (`pandas`, `requests`, `pymongo`, `duckdb`, etc).
* Montagem de volumes para persistência local dos dados.
* (Opcional) MongoDB local com `docker-compose` para desenvolvimento off-cloud.

---

## 📦 Organização do Projeto (Sugestão de Estrutura)


project-root/
├── src/                  # Scripts Python
│   ├── ingest.py         # Coleta da API
│   ├── extract.py        # Leitura do MongoDB
│   ├── transform.py      # Processamento com DuckDB
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docker/
│   └── Dockerfile
├── requirements.txt
├── README.md
└── roadmap.md

---

## 📌 Resultados Esperados

* Pipeline funcional e automatizado.
* Redução de custos com uso de processamento local.
* Dados organizados em camadas com governança.
* Entregáveis analíticos acessíveis a áreas de negócio.

---

## 📄 Especificação das Transformações por Camada (Bronze, Prata, Ouro)

### 🥉 Bronze: Dados Brutos

* **Objetivo:** Armazenar dados exatamente como recebidos da API, garantindo rastreabilidade.
* **Operações:** Nenhuma transformação; apenas ingestão e persistência no MongoDB Atlas.
* **Formato:** JSON, com marcação de tempo (`data_ingestao`).
* **Regras:** Nada é alterado; foco é histórico bruto e íntegro.

---

### 🥈 Prata: Dados Limpos e Estruturados

* **Objetivo:** Preparar os dados para uso técnico e analítico.
* **Operações:**

  * Remoção de duplicatas.
  * Padronização de nomes de campos.
  * Conversão de tipos (string → float, string → datetime etc).
  * Explosão de campos aninhados.
* **Formato:** CSV/Parquet.
* **Regras:** Dados íntegros, normalizados, com schema padronizado.

---

### 🥇 Ouro: Dados Enriquecidos e Prontos para Consumo

* **Objetivo:** Fornecer dados analíticos prontos para o negócio.
* **Operações:**

  * Agregações (médias, contagens, etc.).
  * Enriquecimentos (ex: geográficos, temporais).
  * Join com tabelas auxiliares, derivação de indicadores.
* **Formato:** CSV/Parquet.
* **Regras:** Dados finais consumíveis diretamente por dashboards ou relatórios, sem pós-processamento.

---

### ✅ Resumo das Camadas

| Camada | Tipo de Dados   | Operações                      | Destino Final             |
| ------ | --------------- | ------------------------------ | ------------------------- |
| Bronze | Bruto (JSON)    | Nenhuma                        | MongoDB Atlas             |
| Prata  | Limpo (Tabular) | Limpeza e padronização         | Arquivos locais (Parquet) |
| Ouro   | Enriquecido     | Agregações, joins, indicadores | Blob Storage / BI         |

---
