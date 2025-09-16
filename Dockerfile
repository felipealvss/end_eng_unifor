# Use uma imagem base Python 3.10
FROM python:3.10-slim-bullseye

# Variáveis de ambiente
ENV SPARK_VERSION="3.4.0" \
    HADOOP_VERSION="3" \
    SPARK_HOME="/opt/spark"

# Adicione o Spark e o Poetry ao PATH para que os comandos sejam reconhecidos
ENV PATH="/root/.local/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"

# Instala ferramentas necessárias e baixa o Spark
# Usando a versão 21 de Java, pois a 17 não está disponível
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jre-headless \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -o /tmp/spark.tgz "https://archive.apache.org/dist/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION.tgz" \
    && tar -xzf /tmp/spark.tgz -C /opt \
    && mv /opt/spark-$SPARK_VERSION-bin-hadoop$HADOOP_VERSION $SPARK_HOME \
    && rm /tmp/spark.tgz

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock ./

# Instala as dependências do Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta do Streamlit
EXPOSE 8501

# Comando padrão para iniciar a aplicação Streamlit
CMD ["poetry", "run", "streamlit", "run", "src/dashboard/Painel_ETL.py", "--server.port", "8501", "--server.address", "0.0.0.0"]