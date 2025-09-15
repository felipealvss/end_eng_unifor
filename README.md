# 🚀 Projeto Data Lake & Pipeline de ETL

![Python](https://img.shields.io/badge/python-3.10+-blue)
![PySpark](https://img.shields.io/badge/pyspark-3.4.0-orange)
![Delta Lake](https://img.shields.io/badge/delta-lake-green)
![Poetry](https://img.shields.io/badge/poetry-dependencies-blueviolet)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

Este projeto implementa um **pipeline de dados** com arquitetura em camadas (**Bronze**, **Silver** e **Gold**) usando **PySpark**, **Delta Lake** e **AWS S3**.  
O objetivo é transformar dados brutos em **insights prontos para análise de negócio**, garantindo **qualidade, governança e escalabilidade**.

---

## 🏗 Arquitetura do Pipeline

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
├── log
│   └── log.txt
├── poetry.lock
├── pyproject.toml
├── README.md
└── src
└── python
├── 01_ingestao_api.py
├── 02_envio_landingzone_aws.py
├── 03_carga_bronze_aws.py
├── 04_transform_silver_aws.py
└── 05_gera_gold_aws.py

```

- `data/raw/` → Armazena os arquivos brutos baixados da API.  
- `log/` → Armazena logs do pipeline (`log.txt`).  
- `src/python/` → Contém os scripts de ETL, seguindo a ordem de execução.

---

## 🔧 Configuração

Crie um arquivo `.env` na raiz do projeto (ou copie de `.env.example`) e configure as variáveis de ambiente:

```env
# Definições de ambiente
LOG_DIR = ./log
LOG_FILE = log.txt
RAW_DIR = ./data/raw
RAW_FILE = dados_brutos.parquet

# Informações para API
LINK_API = "https://api-dados-abertos.cearatransparente.ce.gov.br/transparencia/servidores/salarios"
ANO_API = 2025
MES_API = 6
PAGINA_INI = 1

# Destinos folders AWS S3
LANDINGZONE_DIR = landingzone
BRONZE_DIR = bronze
SILVER_DIR = silver
GOLD_DIR = gold

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
poetry install -no-root
```

---

## 🏃‍♂️ Execução do Pipeline

O pipeline é executado na **ordem dos scripts**, garantindo que os dados fluam corretamente do raw até o Gold:

### 1️⃣ Ingestão da API

Coleta os dados da API e salva localmente:

```bash
poetry run python src/python/01_ingestao_api.py
```

### 2️⃣ Envio para Landing Zone AWS

Envia os arquivos brutos para o bucket S3:

```bash
poetry run python src/python/02_envio_landingzone_aws.py
```

### 3️⃣ Carga Bronze

Ingestão dos dados na camada Bronze em Delta Lake:

```bash
poetry run python src/python/03_carga_bronze_aws.py
```

### 4️⃣ Transformação Silver

Aplica limpeza, normalização e deduplicação:

```bash
poetry run python src/python/04_transform_silver_aws.py
```

### 5️⃣ Geração Gold

Executa agregações e gera datasets prontos para análise:

```bash
poetry run python src/python/05_gera_gold_aws.py
```

---

## 📈 Futuras Melhorias

* Suporte a múltiplas fontes de dados
* Integração com ferramentas de BI (PowerBI, Tableau)
* Monitoramento e alertas automáticos do pipeline
* Versionamento e histórico dos datasets Delta

---

## 📚 Referências

* [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
* [Delta Lake Documentation](https://delta.io/)
* [AWS S3 Documentation](https://aws.amazon.com/s3/)
* [Poetry - Python Dependency Management](https://python-poetry.org/)

---

## 💡 Dicas

* Explore os scripts em `src/python/` para customizar transformações.
* Monitore logs em `log/log.txt` para depuração e auditoria.
* Ajuste os caminhos no `.env` conforme seu ambiente local ou bucket S3.
