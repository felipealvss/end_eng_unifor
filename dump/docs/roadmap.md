
# 🚀 **Roadmap de Alto Nível – Projeto de Engenharia de Dados Híbrido**

---

## 🔹 **Etapa 1: Definição de Escopo e Domínio do Problema**

### ✅ Objetivos Conceituais:

* Definir o **problema de negócio** ou **domínio de dados** (ex: clima, finanças, mobilidade urbana, esportes, etc.).
* Identificar **quais dados são relevantes** para gerar valor (quais KPIs ou métricas o projeto pode entregar).
* Escolher uma **API pública confiável** como fonte inicial.

### 🔍 Resultado esperado:

* Documento de escopo com objetivo, fonte de dados, premissas, e metas de entrega.

---

## 🔹 **Etapa 2: Ingestão de Dados**

### ✅ Objetivos Conceituais:

* Entender o conceito de **ingestão de dados** como a **porta de entrada** do pipeline.
* Capturar dados de forma **automatizada, confiável e escalável**.
* Trabalhar com dados semi-estruturados (JSON), compreendendo as **diferenças entre schema fixo vs flexível**.

### 🧠 Conceitos-chave:

* Idempotência de ingestão.
* Versionamento de dados (quando aplicável).
* Qualidade da fonte (frequência de atualização, consistência).

### 🔍 Resultado esperado:

* Script funcional que coleta dados da API e armazena no MongoDB Atlas (dados **bronze**).

---

## 🔹 **Etapa 3: Armazenamento Inicial (MongoDB Atlas)**

### ✅ Objetivos Conceituais:

* Compreender a **função do MongoDB Atlas** como repositório de dados brutos.
* Aprender sobre **armazenamento orientado a documentos**.
* Avaliar vantagens do armazenamento **schema-less** em estágios iniciais do pipeline.

### 🧠 Conceitos-chave:

* Banco NoSQL vs SQL.
* Cluster na nuvem (alta disponibilidade e escalabilidade).
* Modelagem de documentos (documentos aninhados, arrays, tipos dinâmicos).

### 🔍 Resultado esperado:

* Dados brutos salvos com consistência no Atlas, prontos para extração.

---

## 🔹 **Etapa 4: Extração e Processamento Local (com DuckDB)**

### ✅ Objetivos Conceituais:

* Aplicar o conceito de **processamento descentralizado** ou híbrido (cloud-to-local).
* Otimizar custos e performance processando localmente dados que não exigem computação distribuída.
* Criar camadas de transformação baseadas em **governança de dados**.

### 🧠 Conceitos-chave:

* **ETL (Extract, Transform, Load)**: foco na transformação como coração da engenharia de dados.
* Organização em camadas:

  * **Bronze:** raw data (sem transformação)
  * **Prata:** dados limpos e padronizados
  * **Ouro:** dados enriquecidos para análise e consumo final
* Data lineage (rastreabilidade de origem → destino).

### 🔍 Resultado esperado:

* Arquivos estruturados (CSV/Parquet) organizados em diretórios por camada (`/bronze`, `/silver`, `/gold`).

---

## 🔹 **Etapa 5: Armazenamento Final em Blob Storage**

### ✅ Objetivos Conceituais:

* Entender o **papel do armazenamento de objetos** para soluções analíticas e de integração.
* Garantir **disponibilidade e escalabilidade** para múltiplos consumidores (BI, analytics, ciência de dados).
* Viabilizar a separação entre processamento e consumo.

### 🧠 Conceitos-chave:

* Arquitetura desacoplada.
* Governança e versionamento de arquivos.
* Permissões de leitura e integração com ferramentas externas (Power BI, Tableau, etc.).

### 🔍 Resultado esperado:

* Arquivos das camadas processadas disponíveis na nuvem, com estrutura de pastas organizada por data e camada.

---

## 🔹 **Etapa 6: Empacotamento com Docker**

### ✅ Objetivos Conceituais:

* Promover **portabilidade, reprodutibilidade e isolamento de ambiente**.
* Eliminar problemas de "funciona na minha máquina".
* Facilitar integração contínua e testes.

### 🧠 Conceitos-chave:

* Imagens e containers.
* Ambientes imutáveis.
* Volumes para persistência de dados locais.
* Definição declarativa do ambiente (`Dockerfile`).

### 🔍 Resultado esperado:

* Container funcional com todo o pipeline configurado.
* Possibilidade de rodar o projeto em qualquer máquina com Docker instalado.

---

## 🔹 **Etapa 7: Disponibilização e Acesso para Áreas de Negócio**

### ✅ Objetivos Conceituais:

* Fornecer os dados finais de forma **acessível, segura e útil** para diferentes áreas da organização.
* Garantir que o pipeline entregue valor de negócio.

### 🧠 Conceitos-chave:

* Data as a product.
* Governança de dados (quem consome, como e quando).
* Integração com dashboards, notebooks ou APIs.

### 🔍 Resultado esperado:

* Times de negócio acessando os dados (camada ouro) para análises, relatórios e decisões.

---

## 🔹 **Etapa 8: Orquestração e Automatização (opcional)**

### ✅ Objetivos Conceituais:

* Tornar o pipeline **agendado e resiliente**, garantindo reprocessamentos e monitoramento.
* Separar responsabilidade de cada etapa (modularização).

### 🧠 Conceitos-chave:

* DAG (Directed Acyclic Graph) de pipeline.
* Reprocessamento idempotente.
* Logging e monitoramento.

### 🔍 Resultado esperado:

* Pipeline orquestrado (com Airflow, Prefect ou cron jobs simples), capaz de executar periodicamente com mínima intervenção.

---

## ✅ Conclusão

Este roadmap garante que o projeto não se limite à implementação técnica, mas tenha **bases conceituais sólidas** em engenharia de dados. Ele abrange:

* Arquitetura de dados moderna.
* Camadas de transformação (bronze, prata, ouro).
* Estratégia de armazenamento híbrido.
* Automatização e portabilidade com Docker.
* Entrega de valor real aos usuários de negócio.

---
