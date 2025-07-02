from fastapi import APIRouter
from pydantic import BaseModel
from llms.langchain_chain import qa_chain

router = APIRouter()

class AskQuery(BaseModel):
    question: str

@router.post("/ask")
async def ask(query: AskQuery):
    answer = qa_chain.run(query.question)
    return {"answer": answer}
