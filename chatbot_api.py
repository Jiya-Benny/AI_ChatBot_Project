from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query_handler import fetch_from_database
from llm_engine import generate_llm_response
from rag_query_handler import rag_response

app = FastAPI()

# Enable CORS for all origins (equivalent to CORS(app, resources={...}))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to a specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model using Pydantic
class QuestionRequest(BaseModel):
    question: str

# Optional: Extract first sentence utility
# def extract_first_sentence(response: str) -> str:
#     return re.split(r'\n|```', response)[0]

# In-memory conversation store (replace with DB in production)

@app.post("/ask")
async def ask_chatbot(payload: QuestionRequest):
    try:
        user_question = payload.question

        # Step 1: Retrieve relevant data from SQL
        sql_response = fetch_from_database(user_question)

        # Step 2: Retrieving the rag response
        rag_response_data = rag_response(user_question)

        # Step 3: Pass SQL data and rag response to LLM
        human_friendly_response = generate_llm_response(sql_response, user_question, rag_response_data)

        # clean_response = extract_first_sentence(human_friendly_response)

        return {"answer": human_friendly_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
