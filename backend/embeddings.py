import yaml
import os
import openai
import cortex
import pdfminer.high_level
from dotenv import load_dotenv

load_dotenv()

# Load API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
cortex.configure(
    api_key=os.getenv("CORTEX_API_KEY"),
    environment=os.getenv("CORTEX_ENVIRONMENT"),
    organization=os.getenv("CORTEX_ORG")
)
DATASET = os.getenv("CORTEX_DATASET", "recruiter-profile")

def read_profile_yaml(path: str) -> str:
    with open(path, "r") as f:
        profile = yaml.safe_load(f)

    parts = []
    for key, value in profile.items():
        parts.append(f"{key.capitalize()}: {value}")
    return "\n".join(parts)

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        return pdfminer.high_level.extract_text(pdf_path)
    except Exception as e:
        print(f"Failed to extract {pdf_path}: {e}")
        return ""

def gather_documents(data_dir: str) -> list[dict]:
    docs = []

    # Profile YAML
    profile_path = os.path.join(data_dir, "profile.yaml")
    profile_text = read_profile_yaml(profile_path)
    docs.append({"text": profile_text, "source": "profile.yaml"})

    # PDF files
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".pdf"):
                full_path = os.path.join(root, file)
                pdf_text = extract_text_from_pdf(full_path)
                if pdf_text.strip():
                    docs.append({"text": pdf_text, "source": file})

    return docs

def generate_embedding(text: str) -> list[float]:
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response["data"][0]["embedding"]

def upload_to_cortex(docs: list):
    index = cortex.Index(DATASET)

    for doc in docs:
        vector = generate_embedding(doc["text"])
        metadata = {"source": doc["source"]}
        index.upsert(
            id=doc["source"],
            vector=vector,
            metadata=metadata
        )
        print(f"✅ Uploaded: {doc['source']}")

if __name__ == "__main__":
    docs = gather_documents("data")
    upload_to_cortex(docs)
    print("✅ All documents embedded and uploaded.")
