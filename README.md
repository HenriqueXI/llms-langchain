📄 Documentação Técnica — Tarefa

**Projeto:** Implementação de IA para Busca Semântica na Plataforma Imobiliária
**Responsável:** Henrique Dellosso
**Data:** 02/07/2025

---

## ✅ Objetivo

Implantar um **assistente de IA** embutido na plataforma, que permita **consultas semânticas** sobre os imóveis cadastrados.
Cada **`namespace`** da plataforma (imobiliária) possui seu próprio índice **Elasticsearch**, mantendo **isolamento de dados** e **IA especializada** em seu banco.

---

## ✅ Resumo da solução

- **Backend** em **FastAPI**
- **LangChain** para orquestrar o LLM (OpenAI ou Google Gemini) + embeddings
- **Elasticsearch** como **banco de vetores**
- Cada item (imóvel) indexado com **embeddings vetoriais**
- Recuperação por **KNN** (`ElasticVectorSearch`)
- Permite rodar **HuggingFace Embeddings** grátis ou **OpenAI Embeddings** pago
- Tudo acionado via **API REST**

---

## ✅ Fluxo geral

1️⃣ **Cadastro de imóveis**
2️⃣ **Indexação** via `POST /index-properties`
3️⃣ **Consulta (Pergunta)** via `POST /ask`

---

## ✅ Estrutura do código

- 📂 `indexer.py` → Classe `Indexer` para Elastic + Embeddings + indexação
- 📂 `main.py` → FastAPI com rotas `/index-properties` e `/ask`
- 📂 `langchain_chain.py` → Configuração do retriever, embeddings e QA Chain

---

## ✅ Requisitos

- 📂 `fastapi`
- 📂 `uvicorn`
- 📂 `elasticsearch`
- 📂 `langchain`
- 📂 `langchain-community`
- 📂 `langchain-openai`
- 📂 `langchain-google-genai`
- 📂 `langchain-huggingface`
- 📂 `sentence-transformers`


---

## ✅ Chaves necessárias

- **OPENAI_API_KEY**
- **GEMINI_API_KEY**
- Guardadas em `.env` ou `llm_keys.py`

---

## ✅ Porta de execução

- Local: `http://localhost:8000` (ou `:8080`)
- Swagger: `http://localhost:8000/docs`

---

## ✅ Execução

```bash
uvicorn main:app --reload --port 8000
