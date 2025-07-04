from fastapi import APIRouter
from elastic_modules.index_properties import Indexer

# No imports from main.py to avoid circular dependencies

router = APIRouter()
indexer = Indexer()

# ---- Core function ----
def do_index_properties():
    return indexer.index_properties()

# ---- HTTP Endpoint ----
@router.post("/index-properties")
async def index_properties_route():
    return {"message": do_index_properties()}
