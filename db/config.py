import os
from dotenv import load_dotenv

load_dotenv()


class PostgresConfig:
    dbname = os.getenv('POSTGRES_NAME', 'db_task')
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'd9128969')
    port = os.getenv('POSTGRES_PORT', '5432')
    url = rf'postgresql+psycopg2://{user}:{password}@localhost:{port}/{dbname}'
