from test_db_connection import connect_db
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from accelerate import init_empty_weights
print("Imports successful")

# Load model once globally to avoid reloading on every call
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
print(f"model loaded! {model}")

# Load model and precomputed data
phrase_embeddings = np.load("embeddings/phrase_embeddings.npy")
intent_labels = np.load("embeddings/intent_labels.npy")
query_keys = np.load("embeddings/queries_keys.npy")
query_values = np.load("embeddings/queries_values.npy")
queries = dict(zip(query_keys, query_values))

def fetch_from_database(user_input):
    print(user_input)
    """Maps user queries to SQL queries using semantic similarity and retrieves data."""

    # Embed the user's query
    user_embedding = model.encode([user_input])[0]

    # Compute similarity scores
    similarities = cosine_similarity([user_embedding], phrase_embeddings)[0]

    # Find best match
    best_idx = np.argmax(similarities)
    best_score = similarities[best_idx]
    best_intent = intent_labels[best_idx]

    print(f"Matched intent: '{best_intent}' (score: {best_score:.2f})")

    if best_score >= 0.50:
        query = queries[best_intent]
        print(f"Running query: {query}")

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()

            return [str(row) for row in results] if results else ["No data found."]
        except Exception as e:
            return [f"Database error: {str(e)}"]
    else:
        return ["Sorry, I couldn't understand your query. Please try rephrasing."]

if __name__ == "__main__":
    print(fetch_from_database("when is next mass in the church"))
