
# 📚 Sugestões de Tecnologias e Estratégias para Projeto de Engenharia de Dados Híbrido

## 1. Linguagem e Ambiente de Desenvolvimento

- **Python**  
  - Biblioteca principal para ingestão, transformação e orquestração dos dados.  
  - Ecossistema rico em ferramentas para integração com APIs, bancos NoSQL, SQL e processamento analítico.  
  - Frameworks/bibliotecas úteis:  
    - `requests` (API HTTP)  
    - `pymongo` (MongoDB)  
    - `duckdb` (processamento local SQL embutido)  
    - `pandas` (manipulação de dados tabulares)  

- **SQL**  
  - Utilizado principalmente via DuckDB para consultas analíticas locais em formato SQL padrão.  
  - Importante para modelagem das camadas bronze, prata e ouro com transformações claras e auditáveis.

---

## 2. Banco de Dados / Armazenamento

- **MongoDB Atlas (Plano Free Tier)**  
  - Armazenamento inicial dos dados brutos da API (camada bronze).  
  - Suporte a dados semi-estruturados (JSON) e escalabilidade na nuvem.  
  - Gratuito até um limite razoável, perfeito para protótipos e projetos acadêmicos.  

- **DuckDB**  
  - Banco SQL embutido e orientado a analytics para processamento local.  
  - Funciona diretamente com arquivos Parquet e CSV, eliminando a necessidade de grandes clusters.  
  - Código aberto e gratuito.

- **Blob Storage Gratuito / Baixo Custo**  
  - Exemplos:  
    - **Amazon S3 (Free Tier)**: até 5GB gratuito, ideal para armazenar arquivos finais.  
    - **Google Cloud Storage (Free Tier)**: similar à AWS.  
    - **Azure Blob Storage (Free Tier)**.  
    - **MinIO** (open source, pode ser instalado localmente em Docker para simular Blob Storage).  
  - Recomendado para disponibilização e compartilhamento dos dados processados.

---

## 3. Containerização

- **Docker**  
  - Para garantir portabilidade, isolamento e reprodutibilidade do ambiente.  
  - Facilita a replicação do ambiente em qualquer máquina, reduzindo problemas de dependências.  
  - Pode incluir: Python, DuckDB, ferramentas para conexão ao MongoDB, e scripts do pipeline.  
  - Opcionalmente, uso de `docker-compose` para orquestrar serviços, como um MongoDB local durante desenvolvimento.

---

## 4. Orquestração e Automação

- **Cron Jobs (Linux/Mac)** ou **Task Scheduler (Windows)**  
  - Simples, gratuito e suficiente para agendamento básico do pipeline.

- **Prefect (Community Edition)** ou **Apache Airflow (Open Source)**  
  - Para orquestração mais robusta, monitoramento e visualização.  
  - Ambas as ferramentas possuem versões gratuitas e podem ser executadas em containers Docker.

---

## 5. Estratégias Técnicas

- **Pipeline em Camadas (Bronze, Prata, Ouro)**  
  - Organizar o pipeline em etapas claras para facilitar qualidade, governança e rastreabilidade.  
  - Bronze: dados brutos da API no MongoDB.  
  - Prata: dados limpos e transformados localmente.  
  - Ouro: dados enriquecidos e prontos para análise, armazenados em Blob Storage.

- **Processamento Híbrido Cloud + Local**  
  - Dados coletados e armazenados inicialmente no MongoDB Atlas (cloud).  
  - Extração para processamento local com DuckDB, reduzindo custos computacionais em cloud.  
  - Upload dos dados finais em Blob Storage para consumo de áreas de negócio.

- **Versionamento e Governança**  
  - Versionar arquivos de dados finais usando nomenclatura clara (datas, versões).  
  - Documentar todas as transformações feitas em cada camada para garantir auditabilidade.

---

## 6. Outras Ferramentas e Dicas

- **Visualização e Consumo dos Dados**  
  - Ferramentas gratuitas como **Metabase** (open source) ou o **Google Data Studio** para criação de dashboards.  
  - Integração direta com arquivos Parquet/CSV do Blob Storage.

- **Controle de Código e Documentação**  
  - GitHub ou GitLab para versionamento do código.  
  - README.md e documentação clara para facilitar replicação.

- **Monitoramento e Logs**  
  - Logs simples via Python para registrar execução do pipeline.  
  - Pode usar sistemas gratuitos de alertas (ex: email simples).

---

## 7. Resumo das Tecnologias Sugeridas

| Camada/Papel          | Tecnologia                    | Tipo       | Custo           | Observações                         |
|----------------------|------------------------------|------------|-----------------|-----------------------------------|
| Ingestão API         | Python + requests             | Linguagem  | Gratuito        | Essencial para coleta              |
| Armazenamento inicial | MongoDB Atlas (Free Tier)     | NoSQL DB   | Gratuito (limite)| Documentos JSON                   |
| Processamento local   | DuckDB                       | SQL DB     | Gratuito        | Analytics local eficiente          |
| Armazenamento final   | Amazon S3 / MinIO            | Blob Storage| Gratuito/OSS    | Arquivos organizados para consumo |
| Orquestração         | Cron / Prefect / Airflow      | Ferramenta | Gratuito        | Agendamento e monitoramento       |
| Containerização      | Docker                       | Infraestrutura | Gratuito      | Ambiente isolado e portável        |

---
