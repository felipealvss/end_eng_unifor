#!/bin/bash
set -e

docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/01_ingestao_api.py
docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/02_envio_landingzone_aws.py
docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/03_carga_bronze_aws.py
docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/04_transform_silver_aws.py
docker run --rm -it --env-file .env pipeline-etl poetry run python src/python/05_gera_gold_aws.py