from langchain_community.vectorstores import ElasticVectorSearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from llms.llm_keys import GEMINI_API_KEY
from llms.llm_models import GEMINI_FLASH

# Elasticsearch configuration
ELASTIC_URL = "http://localhost:9201"
INDEX_NAME = "properties"

# Create embeddings instance
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create LLM instance
llm = ChatGoogleGenerativeAI(
    api_key=GEMINI_API_KEY,
    model=GEMINI_FLASH
)

# Initialize vectorstore with ElasticVectorSearch
vectorstore = ElasticVectorSearch(
    elasticsearch_url=ELASTIC_URL,
    index_name=INDEX_NAME,
    embedding=embeddings
)

# Initialize QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)
