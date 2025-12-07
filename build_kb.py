import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = "data"
CHROMA_DIR = "chroma_db"

# Load ALL PDFs from data/ folder and split into chunks
def load_all_pdfs():
    pdf_files = glob.glob(f"{DATA_DIR}/*.pdf")
    all_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    for pdf in pdf_files:
        print(f"Loading: {pdf}")

        loader = PyPDFLoader(pdf)
        docs = loader.load()

        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)

        print(f"  -> Pages: {len(docs)}, Chunks: {len(chunks)}")

    print(f"\nTotal chunks from ALL PDFs: {len(all_chunks)}")
    return all_chunks


# Build the vector database (ChromaDB)
def build_vector_db():
    chunks = load_all_pdfs()

    embeddings = FastEmbedEmbeddings()

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )

    vectordb.persist()
    print("\nVector DB created successfully!")


if __name__ == "__main__":
    build_vector_db()
