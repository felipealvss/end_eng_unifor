# 🚀 Projeto Data Lake & Pipeline de ETL

![Python](https://img.shields.io/badge/python-3.10+-blue)
![PySpark](https://img.shields.io/badge/pyspark-3.4.0-orange)
![Delta Lake](https://img.shields.io/badge/delta-lake-green)
![Poetry](https://img.shields.io/badge/poetry-dependencies-blueviolet)
![Docker](https://img.shields.io/badge/docker-ready-informational)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Este projeto implementa um **pipeline de dados** com arquitetura em camadas (**Bronze**, **Silver** e **Gold**) usando **PySpark**, **Delta Lake** e **AWS S3**.  
O objetivo é transformar dados brutos em **insights prontos para análise de negócio**, garantindo **qualidade, governança e escalabilidade**.

---

## 🏗 Arquitetura do Pipeline

A estrutura do projeto segue o seguinte fluxo:

* **API** → **Raw/Landingzone** → **Bronze** → **Silver** → **Gold**

O pipeline segue a **arquitetura em 3 camadas**:

| Camada  | Função                                                                 |
|---------|------------------------------------------------------------------------|
| **Landing Zone / Raw** | Armazena os dados brutos coletados da API. Mantém histórico de arquivos originais. |
| **Bronze** | Dados ingeridos e armazenados em Delta Lake. Preserva dados originais e garante rastreabilidade. |
| **Silver** | Dados limpos, validados e enriquecidos: tipagem, normalização e deduplicação. |
| **Gold**   | Dados agregados e sumarizados, prontos para consumo por ferramentas de BI. |

---

## ⚙️ Estrutura do Projeto

```

.
├── data
│   └── raw
│       └── salarios_*.parquet
├── docs
│   └── Pipeline ETL API.html
├── log
│   └── log.txt
├── src
│   ├── dashboard
│   │   └── Painel_ETL.py
│   └── python
│       ├── 01_ingestao_api.py
│       ├── 02_envio_landingzone_aws.py
│       ├── 03_carga_bronze_aws.py
│       ├── 04_transform_silver_aws.py
│       └── 05_gera_gold_aws.py
├── .env
├── Dockerfile
├── poetry.lock
├── pyproject.toml
├── README.md
└── run_pipeline.sh

```

- `data/raw/` → Armazena os arquivos brutos baixados da API.  
- `log/` → Armazena logs do pipeline (`log.txt`).  
- `src/python/` → Scripts de ETL (ordem sequencial).  
- `src/dashboard/` → Painel interativo em Streamlit (`Painel_ETL.py`).  
- `run_pipeline.sh` → Script para execução sequencial com Docker.  

---

## 🔧 Configuração

Crie um arquivo `.env` na raiz do projeto (ou copie de `.env.example`) e configure as variáveis de ambiente:

```env
# Definições de ambiente
LOG_DIR=./log
LOG_FILE=log.txt
RAW_DIR=./data/raw
RAW_FILE=dados_brutos.parquet

# Informações para API
LINK_API=https://api-dados-abertos.cearatransparente.ce.gov.br/transparencia/servidores/salarios
ANO_API=2025
MES_API=6
PAGINA_INI=1

# Destinos folders AWS S3
LANDINGZONE_DIR=landingzone
BRONZE_DIR=bronze
SILVER_DIR=silver
GOLD_DIR=gold

# Credenciais AWS
AWS_ACCESS_KEY_ID=CHAVEACESSOAWS
AWS_SECRET_ACCESS_KEY=CHAVESECRETAAWS
AWS_REGION=REGAOAWS
S3_BUCKET_NAME=BUCKETAWS
```

> **Dica:** Sempre use `.env` para não expor credenciais sensíveis.

---

## 📦 Instalação

Instale as dependências com Poetry:

```bash
poetry install --no-root
```

---

## 🏃‍♂️ Formas de Execução

Atualmente o projeto possui **3 modos de execução**:

### 🔹 1. Execução direta individual

Executando cada script manualmente via terminal:

```bash
poetry run python src/python/01_ingestao_api.py
poetry run python src/python/02_envio_landingzone_aws.py
poetry run python src/python/03_carga_bronze_aws.py
poetry run python src/python/04_transform_silver_aws.py
poetry run python src/python/05_gera_gold_aws.py
```

---

### 🔹 2. Execução sequencial via `run_pipeline.sh`

Arquivo que executa todos os scripts na ordem correta, dentro de um container Docker:

```bash
./run_pipeline.sh
```

Conteúdo do arquivo:

```bash
#!/bin/bash
set -e

docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/01_ingestao_api.py
docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/02_envio_landingzone_aws.py
docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/03_carga_bronze_aws.py
docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/04_transform_silver_aws.py
docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/05_gera_gold_aws.py
```

---

### 🔹 3. Execução via Docker + Dashboard Streamlit

A imagem já está publicada no Docker Hub:
👉 [felipealvss/pipeline-etl](https://hub.docker.com/r/felipealvss/pipeline-etl)

Basta executar:

```bash
docker pull felipealvss/pipeline-etl
docker run -p 8501:8501 --env-file .env felipealvss/pipeline-etl
```

Isso iniciará um **painel Streamlit** no navegador, onde cada botão executa individualmente os scripts do pipeline de forma **interativa e visual**.

---

## 📈 Futuras Melhorias

* Suporte a múltiplas fontes de dados
* Omplementações de testes automatizados (com Pytest)
* Monitoramento e alertas automáticos do pipeline
* Versionamento e histórico dos datasets Delta

---

## 📚 Referências

* [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
* [Delta Lake Documentation](https://delta.io/)
* [AWS S3 Documentation](https://aws.amazon.com/s3/)
* [Poetry - Python Dependency Management](https://python-poetry.org/)
* [Streamlit](https://streamlit.io/)
* [Docker Hub - pipeline-etl](https://hub.docker.com/r/felipealvss/pipeline-etl)

---

## 💡 Dicas

* Explore os scripts em `src/python/` para customizar transformações.
* Use o painel `Painel_ETL.py` para uma experiência mais interativa.
* Monitore logs em `log/log.txt` para depuração e auditoria.
* Ajuste os caminhos no `.env` conforme seu ambiente local ou bucket S3.
