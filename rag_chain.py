import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

def get_rag_chain():

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = Chroma(persist_directory="chroma_index", embedding_function=embeddings)
    
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    prompt_template = PromptTemplate.from_template(
        "You are a financial assistant. Use the following context to answer the question.\n\n"
        "{context}\n\n"
        "Question: {question}\n"
        "Answer:"
    )

    llm = ChatGoogleGenerativeAI(
        temperature=0,
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template},
        return_source_documents=False,
        input_key="question", 
    )


