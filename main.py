import uvicorn
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi_mcp import FastApiMCP
from contextlib import asynccontextmanager
from router.properties_router import router as properties_router
from router.ask_router import router as ask_router
from router.client_router import router as client_router
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Inicializando servidor MCP embutido...")
    mcp.setup_server()
    yield
    if hasattr(app.state, 'mcp_client_context') and app.state.mcp_client_context:
        print("Finalizando cliente MCP...")
        await app.state.mcp_client_context.__aexit__(None, None, None)
    print("🛑 Aplicação finalizada.")



app = FastAPI(
    title="RAG Real Estate API",
    version="0.2.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou só ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.agent_executor = None
app.state.mcp_client_context = None
app.state.mcp_session = None

mcp = FastApiMCP(app)
mcp.mount()

app.include_router(ask_router)
app.include_router(properties_router)
app.include_router(client_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)