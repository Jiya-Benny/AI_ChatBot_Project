from query_handler import fetch_from_database
import requests
import re
import os

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def generate_llm_response(sql_data, user_query, rag_response):
    """Passes SQL query results to Llama 3 LLM on Groq for response refinement."""
    print("SQL Data : ", sql_data, user_query)
    print("Rag response : ",rag_response)
    
    if "Sorry,  I couldn't understand your query." in sql_data :
        prompt = f"""
            Based on the following database information, generate a precise response:
            Data: {rag_response}
            User Question: {user_query}
            Provide interactive, concise and human friendly response.
            """
    else : 
        prompt = f"""
            Based on the following database information, generate a precise response:
            Data: {sql_data}
            Response: {rag_response}
            User Question: {user_query}
            Provide interactive, concise and human friendly response.
            """

    Headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-70b-8192",  # Llama 3 70B model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }

    print("Sending request to:", GROQ_API_URL)
    print("Headers:", {k: v for k, v in Headers.items() if k != "Authorization"})
    print("Payload model:", payload["model"])

    # response = requests.get(API_URL, headers=HEADERS)
    # print(response.status_code)

    response = requests.post(GROQ_API_URL, headers=Headers, json=payload)
    
    print("Status Code:", response.status_code)
    print("Response Content:", response.text)

    if response.status_code == 200:
        response_json = response.json()
        raw_response = response_json["choices"][0]["message"]["content"]
    
        # print("LLM Response:", raw_response)

        cleaned_response = clean_generated_text(raw_response)
        
        return cleaned_response
        
    else:
        print("Error Response:", response.text)
        return f"Sorry, I couldn't process the request. Error: {response.status_code}"
    
def clean_generated_text(text):
    """Removes unnecessary template text and extracts the main message."""
    if "Provide interactive, concise and human friendly response." in text:
        text = text.split("Provide interactive, concise and human friendly response.")[-1].strip()

    # Remove any leading numbers or formatting
    # text = text.lstrip("1. ").strip()

    # Remove extra explanations that start with phrases like "This code defines..."
    text = re.split(r'\bThis code\b|\bThe function\b|\bpython import\b', text)[0].strip()

    return text

if __name__ == "__main__":
    result = fetch_from_database("priest of holy trinity church")
    print(generate_llm_response(result, "priest of holy trinity church"))