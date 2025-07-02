from fastapi import FastAPI
from router.properties_router import router as properties_router
from router.ask_router import router as ask_router

app = FastAPI(
    title="RAG Real Estate API",
    version="0.1.0"
)

app.include_router(ask_router)
app.include_router(properties_router)
