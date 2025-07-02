from langchain_elasticsearch import ElasticsearchStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import ElasticVectorSearch
from langchain.chains import RetrievalQA

from llms.llm_keys import GEMINI_API_KEY, OPENAI_API_KEY
from llms.llm_models import GEMINI_FLASH

# Configuração do Elastic
ELASTIC_URL = "http://localhost:9201"
INDEX_NAME = "properties"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

llm = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model=GEMINI_FLASH
)

# llm = ChatOpenAI(
#     api_key=OPENAI_API_KEY,
#     model="gpt-4o"
# )

vectorstore = ElasticsearchStore(
    es_url=ELASTIC_URL,
    index_name=INDEX_NAME,
    embedding=embeddings,
    vector_query_field="description_embedding",
    query_field="description"
)

# ------------------------
# QA Chain: RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
