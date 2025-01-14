from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from services.vector_store import load_vector_store
import os

def chat_with_document(query, vector_dir):
    # Load vector store
    client = load_vector_store(vector_dir)
    retriever = client.as_retriever()

    # Set up the QA chain
    chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.environ.get("OPENAI_API_KEY")),
        retriever=retriever
    )

    # Run query and return response
    response = chain.run(query)
    return response
