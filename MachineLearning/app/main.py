from fastapi import FastAPI
from app.api import answerExtraction  
from app.services.answerExtraction import preprocess_handbook
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.include_router(answerExtraction.router)

handbook_dir = "../resources/handbook/content/handbook"
print("Preprocessing handbook")
# data_chunks = preprocess_handbook(handbook_dir)
print("Preprocessing handbook done")

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}