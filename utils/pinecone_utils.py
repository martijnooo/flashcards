import time
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from tqdm.auto import tqdm
import hashlib

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
