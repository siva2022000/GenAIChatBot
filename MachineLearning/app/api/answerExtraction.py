from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class RequestModel(BaseModel):
    question: str

class ResponseModel(BaseModel):
    answer: str

@router.get("/extractanswer", response_model=ResponseModel)
def extractAnswer(request: RequestModel):
    print(request)
    return {"answer": request.question}