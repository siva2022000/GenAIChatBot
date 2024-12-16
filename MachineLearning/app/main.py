from fastapi import FastAPI
from app.api import answerExtraction  
from app.services.answerExtraction import preprocess_resources
import os
import asyncio

app = FastAPI()

app.include_router(answerExtraction.router)
 
if(os.getenv("PROCESS_RESOURCES") == "true"):
    print("Preprocessing resources")    
    asyncio.create_task(preprocess_resources())



@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}

print("Server started")