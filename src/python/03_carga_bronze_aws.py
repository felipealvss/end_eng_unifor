import os
import logging
from pyspark.sql import SparkSession
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
logger.info("----- Inicio de execucao do script: 03_carga_bronze_aws.py -----")

# Parâmetros de Informação AWS
aws_access_key_id     = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name           = os.getenv('S3_BUCKET_NAME')
region                = os.getenv('AWS_REGION')
landingzone_dir       = os.getenv('LANDINGZONE_DIR')
bronze_dir            = os.getenv('BRONZE_DIR')
ano                   = int(os.getenv('ANO_API'))
mes                   = int(os.getenv("MES_API"))

origem = (
    f"s3a://{bucket_name}/{landingzone_dir}/"
    f"ano={ano}/mes={mes:02d}/"
)
destino = (
    f"s3a://{bucket_name}/{bronze_dir}/"
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

    df_bruto = spark.read.parquet(origem)
    logger.info(f"Número de linhas originais: {df_bruto.count()}")

    df_limpo = df_bruto.dropDuplicates()
    logger.info(f"Número de linhas após a remoção de duplicatas: {df_limpo.count()}")

    df_limpo.write.format("delta").mode("overwrite").save(destino)
    logger.info("Dados salvos com sucesso em formato Delta.")

except Exception as e:
    logger.info(f"Ocorreu um erro durante o processamento: {e}")

finally:
    spark.stop()
    logger.info("SparkSession encerrada.")
