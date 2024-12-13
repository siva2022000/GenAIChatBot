from fastapi import APIRouter
from pydantic import BaseModel
from app.services.answerExtraction import extractAnswerSummary

router = APIRouter()

class RequestModel(BaseModel):
    question: str

class ResponseModel(BaseModel):
    answer: str

@router.get("/extractanswer", response_model=ResponseModel)
def extractAnswer(request: RequestModel):
    print(request)
    answerSummary = extractAnswerSummary(request.question)
    return {"answer": answerSummary}