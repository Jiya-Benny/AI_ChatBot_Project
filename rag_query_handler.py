import os
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import qdrant_client
from llama_index.llms.groq import Groq

def rag_response(query):
    # 1. Set up directories and parameters
    PERSIST_DIR = "./qdrant_db_test"
    COLLECTION_NAME = "data_collection"

    os.makedirs(PERSIST_DIR, exist_ok=True)

    # 2. Initialize embedding model
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # 3. Set up persistent Qdrant client
    qdrant_client_instance = qdrant_client.QdrantClient(
        path=PERSIST_DIR,  # Local persistence
        prefer_grpc=False  # Using HTTP protocol
    )

    # 4. Create Qdrant vector store
    vector_store = QdrantVectorStore(
        client=qdrant_client_instance,
        collection_name=COLLECTION_NAME
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store, embed_model=embed_model
    )
    # print(f"Successfully created embeddings for {len(documents)} documents")

    # Create a Groq LLM instance
    groq_api_key = os.environ.get("GROQ_API_KEY")  # Set your Groq API key here
    llm = Groq(api_key=groq_api_key, model="llama3-8b-8192")

    # 9. Test retrieval to verify embeddings work
    query_engine = index.as_query_engine(llm = llm)
    response = query_engine.query(query)

    return response

if __name__ == "__main__":
    result = rag_response("how to deactivate a module")
    print(result)