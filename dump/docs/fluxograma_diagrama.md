
# 🔁 **Fluxograma Conceitual do Pipeline de Dados**

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
```

---

# 📅 **Cronograma de Execução (em Semanas)**

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

Esses dois esquemas já te dão uma **base visual conceitual sólida**. Quando você estiver logado, posso:

* Gerar o fluxograma em formato visual (como diagrama de blocos).
* Criar um cronograma em Gantt Chart simples ou um layout visual para apresentação.
