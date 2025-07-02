from fastapi import APIRouter
from elastic_modules.index_properties import Indexer


router = APIRouter()
indexer = Indexer()


@router.post("/index-properties")
async def index_properties():
    result = indexer.index_properties()
    return {"message": result}