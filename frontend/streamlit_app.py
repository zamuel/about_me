import streamlit as st
import snowflake.connector
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="RAG - Snowflake Arctic", layout="wide")
st.title("🔍 RAG: Consulta tu información profesional")

query = st.text_input("Haz una pregunta sobre tu experiencia, proyectos, educación, etc.")

if query:
    conn = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    cursor = conn.cursor()

    cursor.execute(f"""
        DECLARE query STRING;
        DECLARE query_vec VECTOR(FLOAT, 768);
        DECLARE context STRING;
        DECLARE final_prompt STRING;
        DECLARE response STRING;

        SET query = '{query}';
        SET query_vec = VECTOR_EMBED('e5-base', :query);

        SET context = (
            SELECT ARRAY_TO_STRING(ARRAY_AGG(content), '\n\n')
            FROM (
                SELECT content
                FROM documents
                ORDER BY VECTOR_COSINE_SIMILARITY(embedding, :query_vec) DESC
                LIMIT 5
            )
        );

        SET final_prompt = CONCAT(
            'Usa los siguientes documentos personales para responder la pregunta del usuario.\n\nDocumentos:\n',
            :context,
            '\n\nPregunta: ', :query
        );

        SET response = CORTEX.COMPLETE(
            MODEL_NAME => 'snowflake-arctic',
            PROMPT => :final_prompt,
            TEMPERATURE => 0.3,
            MAX_TOKENS => 1024
        );

        SELECT :response AS answer;
    """)

    result = cursor.fetchone()
    st.markdown("### 💬 Respuesta:")
    st.write(result[0])
