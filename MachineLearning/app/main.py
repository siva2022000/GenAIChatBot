from fastapi import FastAPI
from app.api import answerExtraction  
from app.services.answerExtraction import preprocess_resources
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.include_router(answerExtraction.router)

print("Preprocessing resources")     
if(os.getenv("PROCESS_RESOURCES") == "true"):
    preprocess_resources()
print("Preprocessing resources done")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}