import os
from pathlib import Path
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import qdrant_client
from qdrant_client.models import Distance, VectorParams
from llama_index.readers.file import PyMuPDFReader
from llama_index.core import SimpleDirectoryReader
print("Imports complete..")

# Path to your PDFs (adjust if needed)
pdf_directory = "./data/user manual"  # This should match the folder in your screenshot

# Use the PDF loader (PyMuPDF)
reader = SimpleDirectoryReader(
    input_dir=pdf_directory,
    file_extractor={".pdf": PyMuPDFReader()}
)

documents = reader.load_data()
print(f"Loaded {len(documents)} documents from PDF.")

PERSIST_DIR = "./qdrant_db_test"
COLLECTION_NAME = "data_collection"
EMBEDDING_DIM = 384  # Dimension for the all-MiniLM-L6-v2 model

os.makedirs(PERSIST_DIR, exist_ok=True)

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

qdrant_client_instance = qdrant_client.QdrantClient(
    path=PERSIST_DIR,  # Local persistence
    prefer_grpc=False  # Using HTTP protocol
)

collections = qdrant_client_instance.get_collections().collections
collection_names = [collection.name for collection in collections]

if COLLECTION_NAME not in collection_names:
    qdrant_client_instance.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIM,
            distance=Distance.COSINE
        )
    )
    print(f"Created new collection: {COLLECTION_NAME}")
else:
    print(f"Using existing collection: {COLLECTION_NAME}")
    
vector_store = QdrantVectorStore(
        client=qdrant_client_instance,
        collection_name=COLLECTION_NAME
)
    
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model
)

print(f"Successfully created embeddings for {len(documents)} documents")

collection_info = qdrant_client_instance.get_collection(COLLECTION_NAME)
count = qdrant_client_instance.count(collection_name=COLLECTION_NAME).count
print(f"Number of items in vector store: {count}")