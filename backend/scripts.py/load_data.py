
import os
import snowflake.connector
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Establece conexión con Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
cursor = conn.cursor()

# Ruta a los archivos de texto
DATA_DIR = "data/raw"

# Lee y carga archivos a Snowflake
for filename in os.listdir(DATA_DIR):
    if filename.endswith(".txt") or filename.endswith(".md") or filename.endswith(".pdf"):
        with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as f:
            content = f.read().replace("'", "\'").strip()
            if content:
                cursor.execute(f"""
                    INSERT INTO documents (id, content, embedding)
                    SELECT UUID_STRING(), '{content}', VECTOR_EMBED('e5-base', '{content}')
                """)

print("✅ Documentos procesados y subidos a Snowflake.")
