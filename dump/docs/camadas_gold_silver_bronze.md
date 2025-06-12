
### ✅ Estrutura de Diretórios Recomendada:

```
data/
├── bronze/
│   └── README.md
├── silver/
│   └── README.md
└── gold/
    └── README.md
```

---

### 📂 `data/bronze/README.md`

```markdown
# 🥉 Camada Bronze - Dados Brutos

## 📌 Objetivo

Armazenar os dados coletados diretamente da fonte (API pública), sem qualquer tipo de transformação, para garantir rastreabilidade total e servir como base de versionamento histórico.

---

## 📄 Características dos Dados

- **Fonte**: API pública definida no projeto.
- **Formato**: JSON bruto.
- **Estrutura**: Pode conter dados aninhados ou listas.
- **Validação**: Nenhuma (dados brutos).

---

## 📁 Organização dos Arquivos

- Os arquivos são armazenados com marcação temporal para garantir controle de versões.
- Exemplo de nomenclatura:

```bash
dados\_api\_2025-05-24T10-00-00.json

````

---

## 🛠️ Geração dos Dados

Gerados pelo script:

```bash
src/ingest.py
````

Utilizando as bibliotecas `requests` e `pymongo`.

---

## 📝 Observações

* Não são realizadas limpezas ou verificações.
* É fundamental manter a integridade dos arquivos nesta camada.

````

---

### 📂 `data/silver/README.md`

```markdown
# 🥈 Camada Prata - Dados Limpos e Estruturados

## 📌 Objetivo

Transformar os dados brutos em estruturas tabulares padronizadas, removendo ruídos, padronizando tipos e preparando-os para análises mais robustas.

---

## ⚙️ Transformações Realizadas

- Remoção de duplicatas.
- Padronização de nomes de colunas (`snake_case`).
- Conversão de tipos (ex: string → float/datetime).
- Explosão de listas e campos aninhados.
- Tratamento de valores ausentes.

---

## 📁 Organização dos Arquivos

- Os arquivos são armazenados em formato Parquet ou CSV.
- Diretórios por data de processamento:

````

silver/2025-05-24/dados\_limpos.parquet

````

---

## 🛠️ Geração dos Dados

Gerados pelo script:

```bash
src/transform.py
````

Utilizando `pandas` e `duckdb`.

---

## ✅ Critérios de Qualidade

* Ausência de `null` em campos obrigatórios.
* Consistência no tipo de dados.
* Integridade básica validada.

---

## 📝 Observações

* Esta camada representa a versão "tecnicamente pronta" dos dados.
* Serve como base para análises internas e como input para a camada ouro.

````

---

### 📂 `data/gold/README.md`

```markdown
# 🥇 Camada Ouro - Dados Enriquecidos e Prontos para Consumo

## 📌 Objetivo

Oferecer dados analíticos de alto valor para áreas de negócio, com agregações, enriquecimentos e métricas derivadas.

---

## ⚙️ Transformações Realizadas

- Cálculo de indicadores e métricas (ex: médias, totais, percentis).
- Agregações temporais e espaciais.
- Joins com tabelas auxiliares (ex: regiões, calendários).
- Derivação de colunas estratégicas (ex: níveis de alerta, categorias).

---

## 📁 Organização dos Arquivos

- Formato final: Parquet ou CSV.
- Organização por tema e data:

````

gold/indicadores\_clima/2025-05-24/indicadores.parquet

````

---

## 🛠️ Geração dos Dados

Gerados pelo script:

```bash
src/transform.py
````

Utilizando `duckdb` e SQL para agregações e joins.

---

## ✅ Critérios de Prontidão

* Dados completos e consistentes.
* Sem necessidade de transformação adicional por parte do consumidor.
* Pronto para uso em BI, dashboards ou relatórios.

---

## 📝 Observações

* Esta camada é a mais sensível e estratégica do projeto.
* Deve ser versionada e armazenada com backup em Blob Storage.

