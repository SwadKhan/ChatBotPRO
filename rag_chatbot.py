import os
from dotenv import load_dotenv

# Embeddings + Vector Store
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

# LLM (Groq)
from langchain_groq import ChatGroq

# RAG components
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# Advanced retrieval
from langchain.retrievers.multi_query import MultiQueryRetriever

load_dotenv()

CHROMA_DIR = "chroma_db"

# 1. Load embeddings and vector database
embeddings = FastEmbedEmbeddings()

vectordb = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings
)

# 2. Load the language model (Groq)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# 3. Build the retriever (Multi-Query Retrieval)
base_retriever = vectordb.as_retriever(search_kwargs={"k": 4})

retriever = MultiQueryRetriever.from_llm(
    retriever=base_retriever,
    llm=llm
)

# 4. RAG Prompt
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a strict RAG assistant.

RULES:
1. Use ONLY the information from the context below.
2. DO NOT generate your own citations, numbers, DOIs, authors, or references.
3. Only answer the question using plain natural language.
4. Citations will be added by the system later, so DO NOT include them inside your answer.

If the answer is not in the context, say:
"I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer (no citations, no references):
"""
)


# 5. Build the RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)
# ask for output
def ask(question, return_data=False):
    result = qa({"query": question})
    answer = result["result"]

    citations = []
    seen = set()

    if "I don't know" not in answer:
        for doc in result["source_documents"]:
            name = os.path.basename(doc.metadata.get("source", ""))
            page = doc.metadata.get("page", "?")
            key = (name, page)
            if key not in seen:
                seen.add(key)
                citations.append(key)

    if return_data:
        return answer, citations

    # Console fallback
    print("\nANSWER:")
    print(answer)
    print("\nCITATIONS:")
    if len(citations) == 0:
        print("No relevant sources found.")
    else:
        for src, pg in citations:
            print(f"- {src}, p.{pg}")


# 7. Chat loop
if __name__ == "__main__":
    print("Multi-Query RAG Chatbot Ready.")

    while True:
        q = input("\nAsk: ")
        if q.lower().strip() in ["exit", "quit"]:
            break
        ask(q)
