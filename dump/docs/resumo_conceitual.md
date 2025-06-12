
# **Projeto de Engenharia de Dados: Processamento Híbrido com API, MongoDB Atlas, DuckDB e Docker**

---

## 1. **Visão Geral do Projeto**

Este projeto tem como objetivo desenvolver um pipeline de dados híbrido que integra uma fonte externa (API pública), armazenamento em banco NoSQL (MongoDB Atlas), processamento analítico local (DuckDB), organização dos dados em camadas (bronze, prata, ouro) e utilização do Docker para garantir portabilidade e isolamento do ambiente.

---

## 2. **Arquitetura de Dados e Fluxo**

### 2.1. **Ingestão de Dados**

* Coleta de dados brutos diretamente de uma API pública, normalmente no formato JSON.
* Ferramentas típicas: bibliotecas Python (`requests`).

### 2.2. **Armazenamento Inicial – MongoDB Atlas**

* MongoDB Atlas é um banco NoSQL orientado a documentos (JSON-like) hospedado na nuvem.
* Usado para armazenar os dados brutos em seu formato original.
* Plano gratuito (M0) permite uso inicial sem custo.
* Permite fácil consulta e recuperação dos dados.

### 2.3. **Extração e Processamento Local – DuckDB**

* DuckDB é um banco de dados analítico leve e embutido, que funciona localmente.
* Extrai-se dados do MongoDB Atlas para o ambiente local.
* Realiza transformações dos dados em três camadas conceituais:

  * **Bronze:** Dados crus, sem alteração, diretamente extraídos do MongoDB.
  * **Prata:** Dados limpos e organizados, com tratamento de qualidade (remoção de duplicatas, padronização de tipos).
  * **Ouro:** Dados enriquecidos e agregados, prontos para consumo analítico e geração de relatórios.

### 2.4. **Armazenamento Final – Blob Storage**

* Dados processados (especialmente as camadas prata e ouro) são armazenados em serviços de blob storage, que são otimizados para arquivos (exemplo: Amazon S3, Google Cloud Storage).
* Blob storage é econômico, escalável e ideal para armazenar arquivos como Parquet, CSV, JSON, backups.
* Facilita o acesso por áreas de negócio e ferramentas de BI.

---

## 3. **Principais Conceitos Técnicos**

### 3.1. **Pipeline de Dados**

* Conjunto de etapas sequenciais para coleta, armazenamento, processamento e disponibilização dos dados.
* Modularização por camadas (bronze, prata, ouro) para garantir qualidade e governança.

### 3.2. **MongoDB Atlas**

* Banco NoSQL orientado a documentos JSON.
* Armazena dados semi-estruturados, permite consultas flexíveis.
* Não recomendado para armazenar grandes arquivos binários (não é Blob Storage).

### 3.3. **DuckDB**

* Banco de dados analítico SQL que roda localmente, otimizado para operações analíticas e transformações.
* Ideal para manipulação eficiente de dados em disco (Parquet, CSV).

### 3.4. **Blob Storage**

* Armazenamento de objetos (arquivos) na nuvem, escalável e com baixo custo.
* Facilita o compartilhamento e integração com múltiplas ferramentas e equipes.

### 3.5. **Camadas Bronze, Prata e Ouro**

* **Bronze:** Dados brutos, entrada do pipeline.
* **Prata:** Dados limpos e validados, prontos para análise intermediária.
* **Ouro:** Dados prontos para uso final em BI e relatórios.

---

## 4. **Uso do Docker no Projeto**

### 4.1. **Objetivo do Docker**

* Criar um ambiente isolado, padronizado e reproduzível.
* Facilitar a instalação e execução do pipeline em qualquer máquina.
* Evitar problemas de incompatibilidade de versões de bibliotecas e ferramentas.
* Facilitar o trabalho em equipe e a replicação do ambiente para testes e produção.

### 4.2. **Como o Docker será usado**

* Dockerfile definindo ambiente Python com dependências (`pymongo`, `duckdb`, `pandas`, `requests`, etc.).
* Montagem de volumes para persistência de dados locais (arquivos intermediários e finais).
* Docker Compose para orquestrar múltiplos serviços, se necessário (exemplo: adicionar MongoDB local para desenvolvimento).

### 4.3. **Benefícios**

* Redução de complexidade para novos membros da equipe.
* Consistência entre ambiente de desenvolvimento e produção.
* Automatização do setup do ambiente.

---

## 5. **Considerações sobre Custos e Viabilidade**

* Uso do plano gratuito do MongoDB Atlas e DuckDB local minimiza custos.
* Utilização do Free Tier da AWS (ou equivalente) para blob storage reduz custos de armazenamento.
* Processamento local reduz custos com computação na nuvem.
* Arquitetura híbrida que equilibra custo e desempenho, garantindo dados disponíveis para negócio.

---

## 6. **Resultados Esperados**

* Pipeline robusto e escalável que coleta, armazena, processa e disponibiliza dados com qualidade.
* Dados organizados em camadas, facilitando governança e rastreabilidade.
* Ambiente isolado e portátil com Docker, garantindo replicabilidade.
* Dados finais acessíveis para times de negócio via serviços de armazenamento escaláveis.

---

## 7. **Próximos Passos**

* Escolher API pública para ingestão inicial.
* Configurar MongoDB Atlas e testar conexão.
* Esboçar scripts de ingestão e extração.
* Construir Dockerfile básico e testar ambiente local.
* Implementar pipeline de camadas (bronze, prata, ouro) usando DuckDB.
* Configurar armazenamento em blob para arquivos processados.

---
