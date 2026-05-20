from sentence_transformers import SentenceTransformer
import os
import json

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

DOCUMENTS_PATH = "documents"

VECTOR_DB_FILE = "vector_db.json"


def chunk_text(text, chunk_size=2):

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    chunks = []

    for i in range(0, len(lines), chunk_size):

        chunk = "\n".join(
            lines[i:i + chunk_size]
        )

        chunks.append(chunk)

    return chunks


def load_documents():
    documents = []

    if not os.path.exists(DOCUMENTS_PATH):
        print(f"Documents folder not found: {DOCUMENTS_PATH}")
        return documents

    files = os.listdir(DOCUMENTS_PATH)
    print(f"Found files: {files}")

    for filename in files:
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(DOCUMENTS_PATH, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()

        if not content:
            print(f"Skipping empty file: {filename}")
            continue

        documents.append({
            "source": filename,
            "content": content
        })

    print(f"Loaded {len(documents)} documents.")
    return documents

def create_vector_db():

    all_chunks = []

    documents = load_documents()

    for doc in documents:

        chunks = chunk_text(
            doc["content"]
        )

        for chunk in chunks:

            all_chunks.append({
                "source": doc["source"],
                "text": chunk
            })

    texts = [
        chunk["text"]
        for chunk in all_chunks
    ]

    embeddings = model.encode(texts)

    vector_data = []

    for chunk, embedding in zip(
        all_chunks,
        embeddings
    ):

        vector_data.append({
            "source": chunk["source"],
            "text": chunk["text"],
            "embedding": embedding.tolist()
        })

    with open(
        VECTOR_DB_FILE,
        "w"
    ) as f:

        json.dump(vector_data, f)

    print(
        f"Stored {len(vector_data)} chunks."
    )


if __name__ == "__main__":

    create_vector_db()