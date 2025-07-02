import os
import requests
import wikipedia
import yfinance as yf
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def load_pdfs(directory="./docs/pdfs"):
    docs = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            path = os.path.join(directory, filename)
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            docs.append(Document(page_content=text, metadata={"source": filename}))
    return docs

def load_wikipedia_topics(topics):
    docs = []
    for topic in topics:
        try:
            content = wikipedia.page(topic).content
            docs.append(Document(page_content=content, metadata={"source": f"wikipedia:{topic}"}))
        except Exception as e:
            print(f"[Wikipedia] Skipped {topic}: {e}")
    return docs

def load_newsapi_articles(query, api_key):
    docs = []
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=5&apiKey={api_key}"
    try:
        response = requests.get(url)
        articles = response.json().get("articles", [])
        for article in articles:
            content = article.get("description", "") + "\n" + article.get("content", "")
            docs.append(Document(page_content=content, metadata={"source": article.get("url")}))
    except Exception as e:
        print(f"[NewsAPI] Failed: {e}")
    return docs

def load_yfinance_data(symbols):
    docs = []
    for symbol in symbols:
        try:
            info = yf.Ticker(symbol).info
            text = "\n".join(f"{k}: {v}" for k, v in info.items() if isinstance(v, (str, int, float)))
            docs.append(Document(page_content=text, metadata={"source": f"yfinance:{symbol}"}))
        except Exception as e:
            print(f"[yFinance] Failed for {symbol}: {e}")
    return docs

def build_vectorstore():
    print("🔍 Loading sources...")
    pdf_docs = load_pdfs()
    wiki_docs = load_wikipedia_topics(["Investment", "Financial_management", "Risk_management", "Stock_market"])
    news_docs = load_newsapi_articles("stock market", os.getenv("NEWSAPI_KEY"))
    yf_docs = load_yfinance_data(["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "META", "NFLX",
    "INTC", "AMD", "ADBE", "CRM", "PFE", "JNJ", "WMT", "DIS", "NKE", "KO"])

    all_docs = pdf_docs + wiki_docs + news_docs + yf_docs
    print(f"📄 Total documents: {len(all_docs)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = splitter.split_documents(all_docs)
    print(f"✂️ Chunks created: {len(split_docs)}")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(split_docs, embeddings, persist_directory="chroma_index")
    vectorstore.persist()
    print("✅ Vector store created at")

if __name__ == "__main__":
    build_vectorstore()
