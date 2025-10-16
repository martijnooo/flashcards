import time
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from tqdm.auto import tqdm
import hashlib
from utils.env_loader import load_env, get_env_var
import streamlit as st

def init_pinecone(api_key: str):
    pc = Pinecone(api_key=api_key)
    return pc

def ensure_index(pc, index_name="flashcards", dimension=1536):
    existing = [idx["name"] for idx in pc.list_indexes()]
    if index_name not in existing:
        spec = ServerlessSpec(cloud="aws", region="us-east-1")
        pc.create_index(index_name, dimension=dimension, metric="dotproduct", spec=spec)
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
    return pc.Index(index_name)

def create_embeddings(openai_api_key: str):
    return OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=openai_api_key)
    

def upsert_flashcards(index, embedder, flashcards):
    batch_size = 100
    for i in tqdm(range(0, len(flashcards), batch_size)):
        batch = flashcards[i:i+batch_size]
        ids = [hashlib.md5((fc["question"] + fc["answer"]).encode("utf-8")).hexdigest() for fc in batch]
        texts = ["Question: " + fc["question"] + " - Answer: " + fc["answer"] for fc in batch]
        embeds = embedder.embed_documents(texts)
        metadatas = [{"question": fc["question"], "answer": fc["answer"], "category": fc["category"], "type": fc["type"]} for fc in batch]
        index.upsert(vectors=list(zip(ids, embeds, metadatas)))

def create_vectorstore(embedder, index):
    return PineconeVectorStore(embedding=embedder, index=index, text_key="question")

# Cache the Pinecone initialization
@st.cache_resource
def initialize_pinecone():
    # Load environment variables
    load_env()
    OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
    PINECONE_API_KEY = get_env_var("PINECONE_API_KEY")
    
    # Initialize Pinecone components
    pc = init_pinecone(PINECONE_API_KEY)
    index = ensure_index(pc)
    embedder = create_embeddings(OPENAI_API_KEY)
    vectorstore = create_vectorstore(embedder, index)
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'k': 6, 'score_threshold': 0.9}
    )
    return index, embedder, retriever, vectorstore
