from fastapi import FastAPI
from app.api import answerExtraction      

app = FastAPI()

app.include_router(answerExtraction.router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}