
# 📄 Especificação das Transformações por Camada (Bronze, Prata, Ouro)

## 🔍 Objetivo
Este documento descreve, de forma estruturada, as transformações aplicadas aos dados ao longo das camadas de um pipeline de engenharia de dados: **Bronze**, **Prata** e **Ouro**. Cada camada tem propósitos distintos e critérios próprios de qualidade, estrutura e tratamento.

---

## 🥉 Camada Bronze: Dados Brutos

### 🧠 Propósito:
- Armazenar os dados **exatamente como foram recebidos** da fonte (API).
- Garantir rastreabilidade completa da origem.

### ⚙️ Operações Realizadas:
- Ingestão direta da API (normalmente em JSON).
- Armazenamento no MongoDB Atlas, sem transformação.
- Registro do timestamp da coleta (`data_ingestao`).

### 📦 Estrutura:
- JSON bruto ou estrutura aninhada.
- Schema flexível, conforme a fonte.

### ✅ Regras:
- Não realizar limpeza nem enriquecimento.
- Garantir versionamento ou armazenamento com timestamp.

---

## 🥈 Camada Prata: Dados Limpos e Estruturados

### 🧠 Propósito:
- Padronizar, limpar e estruturar os dados para análises intermediárias ou uso técnico.
- Reduzir inconsistências e facilitar processamento analítico.

### ⚙️ Operações Realizadas:
- Remoção de duplicatas.
- Padronização de campos (`camelCase` para `snake_case`, nomes em português para inglês se necessário).
- Conversão de tipos (string → float, string → datetime, etc.).
- Validação de dados obrigatórios (ex: campos `latitude`, `temperatura`, etc.).
- Explosão de listas ou aninhamentos, se existirem.

### 📦 Estrutura:
- Tabelas planas (Parquet/CSV).
- Tipagem explícita.

### ✅ Regras:
- Garantir integridade mínima (sem `null` em campos chave).
- Nomenclatura e tipos uniformes.
- Organização em diretórios por data (`/silver/2025-05-24/`).

---

## 🥇 Camada Ouro: Dados Enriquecidos e Prontos para Consumo

### 🧠 Propósito:
- Produzir dados de **alto valor analítico**, consumíveis por áreas de negócio, BI ou relatórios.

### ⚙️ Operações Realizadas:
- Cálculos agregados (média, soma, percentis).
- Derivação de métricas e indicadores.
- Join com fontes auxiliares (ex: dicionários, tabelas de referência).
- Enriquecimento temporal (semana, mês, feriado, etc.).
- Normalização geográfica (ex: cidade, estado, país).

### 📦 Estrutura:
- Tabelas finalizadas, agregadas ou modeladas por negócio.
- Arquivos em formato Parquet ou CSV otimizados.

### ✅ Regras:
- Pronto para ser usado diretamente por dashboards, relatórios, ou análises.
- Sem necessidade de pós-processamento por parte do consumidor.
- Organização clara por tema (ex: `/gold/indicadores_clima/2025-05-24.parquet`).

---

## 📌 Resumo da Evolução dos Dados

| Camada | Descrição                 | Estrutura       | Tipo de Dados           | Transformações Principais                 |
|--------|---------------------------|------------------|--------------------------|--------------------------------------------|
| Bronze | Dados brutos da API       | JSON/MongoDB     | Semi-estruturado         | Nenhuma                                     |
| Prata  | Dados limpos e padronizados| Parquet/CSV      | Tabelado com schema fixo | Limpeza, tipagem, padronização             |
| Ouro   | Dados enriquecidos         | Parquet/CSV      | Modelo analítico final   | Agregações, joins, cálculos, derivações    |

---

## ✅ Observações Finais

- Todas as transformações devem ser documentadas em logs ou em README técnicos.
- As camadas são cumulativas: **Ouro = Prata + enriquecimento**, **Prata = Bronze + limpeza**.
- A separação em camadas facilita auditoria, versionamento e governança de dados.

---
