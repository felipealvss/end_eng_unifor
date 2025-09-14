import os
import logging
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import pandas as pd

# Importa dados do Env
load_dotenv()

# Parâmetros de LOG
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
logger.info("----- Inicio de execucao do script: 01_ingestao_api.py -----")

# Parâmetros para API
api        = os.getenv('LINK_API')
ano        = os.getenv('ANO_API')
mes        = os.getenv('MES_API')
pagina_ini = os.getenv('PAGINA_INI')
output_dir = os.getenv('RAW_DIR')
data = []

# Garante a existência do diretório
os.makedirs(output_dir, exist_ok=True)

# Definição de URL da API
def url_api(ano, mes, pagina_ini):
    return (
        f"{api}?year={ano}&month={mes}&page={pagina_ini}"
    )

# Realizar requisição inicial
try:
    response = requests.get(url_api(ano, mes, pagina_ini), headers={"accept": "application/json"})
    dados = response.json()
    logger.info("Conexão bem-sucedida.")

    total_pages = dados['sumary']['total_pages']
    logger.info(f"Ano: {ano} Mês: {mes} Total de páginas: {total_pages}")
except requests.RequestException as e:
    logger.info(f"Erro ao acessar a API: {e}")

# Cria função para extrair dados
def get_data(i):
    response = requests.get(url_api(ano, mes, i),
            headers={'accept':'application/json'}).json()
    return response['data']

# Obtém todos os dados com consultas paralelas via ThreadPool
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(get_data, i): i for i in range(1, total_pages + 1)}
    for future in as_completed(futures):
        try:
            result = future.result()
            data.extend(result)
        except Exception as e:
            logger.info(f"Erro ao processar a página {futures[future]}: {e}")

logger.info("Extração concluída.")
logger.info(f"Total de registros obtidos: {len(data)}")

# Salvar dados em parquet (pasta raw local)
df = pd.DataFrame(data)

mes = int(os.getenv("MES_API"))
timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
output_file = os.path.join(output_dir, f"salarios_{ano}_{mes:02d}_{timestamp}.parquet")

df.to_parquet(output_file, engine="pyarrow", index=False)

logger.info(f"Arquivo salvo em: {output_file}")
