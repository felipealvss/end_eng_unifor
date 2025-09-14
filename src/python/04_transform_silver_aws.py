import os
import logging
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, trim, lower, regexp_replace, year, month, row_number, desc
from dotenv import load_dotenv

# Importa dados do Env
load_dotenv()

# Parâmetros de LOG
log_dir = os.getenv("LOG_DIR")
log_arq = os.getenv("LOG_FILE")

os.makedirs(log_dir, exist_ok=True)

log_dir_file = os.path.join(log_dir, log_arq)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",  # formato mais completo
    handlers=[
        logging.FileHandler(log_dir_file, mode="a", encoding="utf-8"),  # salva no arquivo
        logging.StreamHandler()  # continua mostrando no console
    ]
)

logger = logging.getLogger(__name__)
logger.info("----- Inicio de execucao do script: 04_transform_silver_aws.py -----")

# Parâmetros de Informação AWS
aws_access_key_id     = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name           = os.getenv('S3_BUCKET_NAME')
region                = os.getenv('AWS_REGION')
bronze_dir            = os.getenv('BRONZE_DIR')
silver_dir            = os.getenv('SILVER_DIR')
ano                   = int(os.getenv('ANO_API'))
mes                   = int(os.getenv("MES_API"))

origem = (
    f"s3a://{bucket_name}/{bronze_dir}/"
    f"ano={ano}/mes={mes:02d}/"
)
destino = (
    f"s3a://{bucket_name}/{silver_dir}/"
    f"ano={ano}/mes={mes:02d}/"
)

# Lista de pacotes Maven necessários para S3 e Delta Lake
delta_package = "io.delta:delta-core_2.12:2.4.0"
hadoop_aws_package = "org.apache.hadoop:hadoop-aws:3.3.1"
aws_sdk_package = "com.amazonaws:aws-java-sdk-bundle:1.11.901"

# Junta todos os pacotes em uma string separada por vírgulas
all_packages = f"{delta_package},{hadoop_aws_package},{aws_sdk_package}"

builder = (
    SparkSession.builder.appName("ProcessamentoDadosS3")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    # Configurações para conexão com S3
    .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id)
    .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key)
    .config("spark.hadoop.fs.s3a.endpoint", f"s3.{region}.amazonaws.com")
    # Adiciona os pacotes ao SparkSession de forma direta
    .config("spark.jars.packages", all_packages)
)

# Gerando sessão Spark
spark = builder.getOrCreate()
logger.info("SparkSession e Delta Lake configurados com sucesso.")

# Realizando envio de dados
try:
    logger.info(f"Lendo dados do caminho: {origem}")

    # Agora a leitura é feita no formato Delta
    df_bruto = spark.read.format("delta").load(origem)
    logger.info(f"Número de linhas originais: {df_bruto.count()}")

    # Aplica as transformações e limpezas
    df_enriquecido = df_bruto.select(
        col("id").cast("long").alias("id"),
        lower(trim(col("nome_servidor"))).alias("nome_servidor"),
        col("total_proventos").cast("double").alias("total_proventos"),
        col("proventos_liquidos").cast("double").alias("proventos_liquidos"),
        col("diarias").cast("double").alias("diarias"),
        col("total_descontos").cast("double").alias("total_descontos"),
        col("desconto_teto").cast("double").alias("desconto_teto"),
        col("outros_descontos").cast("double").alias("outros_descontos"),
        col("criacao").cast("date").alias("criacao"),
        col("atualizacao").cast("date").alias("atualizacao"),
        col("competencia").cast("date").alias("competencia"),
        year(col("competencia")).alias("ano"),
        month(col("competencia")).alias("mes"),
        col("situacao_funcional"),
        lower(trim(regexp_replace(col("dsc_cargo"), "\\s+", " "))).alias("dsc_cargo"),
        col("codigo_orgao").cast("long").alias("codigo_orgao"),
        lower(trim(col("descricao_orgao"))).alias("descricao_orgao"),
        lower(trim(col("sigla"))).alias("sigla")
    )

    # Particionamento e ordenação dos dados
    window_spec = Window.partitionBy("id", "competencia").orderBy(desc("atualizacao"))
    # Aplicando enumeração para cada partição
    df_deduplicado = df_enriquecido.withColumn("row_number", row_number().over(window_spec))
    # Mantendo apenas a linha mais recente (row_number = 1)
    df_final = df_deduplicado.filter(col("row_number") == 1).drop("row_number")

    logger.info(f"Número de linhas após a deduplicação: {df_final.count()}")

    df_final.write.format("delta").mode("overwrite").save(destino)
    logger.info("Dados processados, enriquecidos e salvos com sucesso em formato Delta.")

except Exception as e:
    logger.info(f"Ocorreu um erro durante o processamento: {e}")

finally:
    spark.stop()
    logger.info("SparkSession encerrada.")
