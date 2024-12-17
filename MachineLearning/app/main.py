from fastapi import FastAPI
from app.api import answerExtraction  
from app.services.answerExtraction import preprocess_resources
import os
import threading
app = FastAPI()

app.include_router(answerExtraction.router)
 
@app.on_event("startup")
def startup_event():
    if(os.getenv("PROCESS_RESOURCES") == "true"):
        print("Preprocessing resources")    
        threading.Thread(target=preprocess_resources).start()   


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI"}

print("Server started")