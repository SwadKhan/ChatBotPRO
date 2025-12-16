import os
from dotenv import load_dotenv

from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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

# 3. Build the retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 20})

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
5. If the context does not provide information to answer the question, say "I don't have information on that topic in my knowledge base." and nothing else.

Context: {context}

Question: {question}

Answer:"""
)

# 5. Build the RAG chain
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Function to ask questions
def ask(question, return_data=False):
    try:
        answer = rag_chain.invoke(question)
        
        # Get sources
        docs = retriever.invoke(question)
        citations = []
        for doc in docs:
            src = doc.metadata.get("source", "Unknown")
            pg = doc.metadata.get("page", doc.metadata.get("slide", "N/A"))
            citations.append((src, pg))
        
        if return_data:
            return answer, citations
        else:
            return answer
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        if return_data:
            return error_msg, []  # Return tuple format to match expected output
        else:
            return error_msg


# General ask function (no RAG, may hallucinate)
def general_ask(question):
    try:
        prompt_general = PromptTemplate(
            input_variables=["question"],
            template="Answer the question: {question}"
        )
        general_chain = prompt_general | llm | StrOutputParser()
        return general_chain.invoke(question)
    except Exception as e:
        return f"Error: {str(e)}"


# 7. Chat loop
if __name__ == "__main__":
    print("Chatbot Pro is Ready.")

    while True:
        q = input("\nAsk: ")
        if q.lower().strip() in ["exit", "quit"]:
            break
        answer = ask(q)
        print(f"Answer: {answer}")
