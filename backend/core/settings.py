import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Feature flag – 1 = use dummy JSON, 0 = use real backends
USE_DUMMY_DATA = os.getenv("USE_DUMMY_DATA", "1") == "1"

# RDS (Postgres/MySQL) – fill these from env
RDS_HOST = os.getenv("RDS_HOST", "")
RDS_PORT = int(os.getenv("RDS_PORT", "5432"))
RDS_DB = os.getenv("RDS_DB", "")
RDS_USER = os.getenv("RDS_USER", "")
RDS_PASSWORD = os.getenv("RDS_PASSWORD", "")

# Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "")
NEO4J_USER = os.getenv("NEO4J_USER", "")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")

# Elasticsearch
ES_ENDPOINT = os.getenv("ES_ENDPOINT", "")

# Bedrock via API Gateway + Lambda
BEDROCK_API_URL = os.getenv("BEDROCK_API_URL", "")
BEDROCK_API_KEY = os.getenv("BEDROCK_API_KEY", "")
