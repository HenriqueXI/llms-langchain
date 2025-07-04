# router/agent_router.py

from fastapi import APIRouter, Request, HTTPException, status
from pydantic import BaseModel

# Importe os componentes do cliente
from mcp.client.websocket import websocket_client
from mcp.client.session import ClientSession
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from llms.llm_keys import OPENAI_API_KEY

router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)

class Question(BaseModel):
    query: str

@router.post("/create-agent", status_code=status.HTTP_200_OK)
async def start_agent(request: Request):
    """
    Inicia e configura o cliente MCP e o agente ReAct.
    Esta operação é idempotente: se o agente já estiver rodando, não faz nada.
    """
    if request.app.state.agent_executor:
        return {"message": "Agente já está iniciado."}

    mcp_url = "ws://127.0.0.1:8080/mcp/sse"

    # uri = "ws://localhost:8080/mcp/messages/"

    # async with websocket_client(uri) as client:

    try:
        print('passou 3')
        client_context = websocket_client(mcp_url)
        print('passou mcp_url', mcp_url)
        read, write = await client_context.__aenter__()
        print('passou 2')
        session = ClientSession(read, write)
        await session.initialize()
        print('passou 1')
        tools = await load_mcp_tools(session)
        llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4", temperature=0)
        agent = create_react_agent(llm, tools)
        print('passou')
        request.app.state.agent_executor = agent
        request.app.state.mcp_client_context = client_context
        request.app.state.mcp_session = session

        print("Agente iniciado e pronto para uso.")
        return {"message": "Agente iniciado com sucesso!"}

    except ConnectionRefusedError as error:
        print(f"Falha ao conectar ao servidor MCP. O servidor está rodando? {error}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Não foi possível conectar ao servidor MCP. Verifique se o serviço está no ar."
        )
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao iniciar o agente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao iniciar o agente: {e}"
        )


@router.post("/agent-ask")
async def ask_agent(question: Question, request: Request):
    """
    Envia uma pergunta para o agente (previamente iniciado) e retorna a resposta.
    """
    if not request.app.state.agent_executor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="O agente não foi iniciado. Por favor, chame a rota /agent/iniciar primeiro."
        )

    print(f"💬 Recebida pergunta para o agente: {question.query}")

    agent_executor = request.app.state.agent_executor

    try:
        result = await agent_executor.ainvoke({"messages": [("user", question.query)]})
        final_answer = result.get('messages', [])[-1].content
        return {"answer": final_answer}

    except Exception as e:
        print(f"Erro ao invocar o agente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"O agente encontrou um erro: {e}"
        )