# Usa uma imagem base leve com Python 3.10
FROM python:3.10-slim

# Define variáveis de ambiente para o Spark.
ENV SPARK_VERSION=3.4.0 \
    HADOOP_VERSION=3 \
    SPARK_HOME=/opt/spark \
    PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Instala ferramentas necessárias e baixa o Spark
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -o /tmp/spark.tgz "https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz" \
    && tar -xzf /tmp/spark.tgz -C /opt \
    && mv /opt/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION $SPARK_HOME \
    && rm /tmp/spark.tgz

# Instala o Poetry
RUN pip install poetry

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependência e instala
# A ordem é importante para aproveitar o cache do Docker (build caching)
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-root

# Copia todo o código do seu projeto
COPY . /app

# Exponha a porta do Streamlit
EXPOSE 8501

# Comando padrão para iniciar a aplicação Streamlit
CMD ["poetry", "run", "streamlit", "run", "src/dashboard/Painel_ETL.py", "--server.port", "8501", "--server.address", "0.0.0.0"]