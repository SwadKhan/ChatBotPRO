from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

embeddings = FastEmbedEmbeddings()
vectordb = Chroma(persist_directory='chroma_db', embedding_function=embeddings)

# Search for the full question
docs = vectordb.similarity_search('What city does Alice live in?', k=20)
print(f'Found {len(docs)} docs for "What city does Alice live in?"')
for i, doc in enumerate(docs):
    print(f'Doc {i+1}: {doc.metadata.get("source")} - {doc.page_content[:100]}...')

# Also test retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 10})
retrieved_docs = retriever.invoke('What city does Alice live in?')
print(f'\nRetriever found {len(retrieved_docs)} docs')
for i, doc in enumerate(retrieved_docs):
    print(f'Retrieved Doc {i+1}: {doc.metadata.get("source")} - {doc.page_content[:100]}...')