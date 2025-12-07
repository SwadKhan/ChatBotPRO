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
Use ONLY the context provided below to answer the question.

DO NOT copy or include internal citation numbers such as [1], [2], [3], or references from the PDF's bibliography.
Ignore any citation numbers present in the text.

If the answer is not in the context, say:
"I don't know based on the provided documents."

Provide the answer in clean paragraphs.

After the answer, include ONLY the page-level citations that the system provides.
Do NOT generate or rewrite citation numbers yourself.

Context:
{context}

Question:
{question}

Answer:
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

# 6. Ask function (clean output + citation fix)
def ask(question):
    result = qa({"query": question})
    answer = result["result"]

    print("\nANSWER:")
    print(answer)

    # If answer says "I don't know", do NOT show citations
    if "I don't know" in answer or "don't know" in answer:
        print("\nCITATIONS:")
        print("No relevant sources found.")
        return

    # Otherwise show relevant citations
    print("\nCITATIONS:")
    seen = set()

    for doc in result["source_documents"]:
        name = os.path.basename(doc.metadata.get("source", ""))
        page = doc.metadata.get("page", "?")

        key = (name, page)
        if key not in seen:
            seen.add(key)
            print(f"- {name}, p.{page}")


# 7. Chat loop
if __name__ == "__main__":
    print("Multi-Query RAG Chatbot Ready.")

    while True:
        q = input("\nAsk: ")
        if q.lower().strip() in ["exit", "quit"]:
            break
        ask(q)
