# Detailed Storage Process in RAG Chatbot Project

## Overview

This document provides a comprehensive explanation of the storage process implemented in this Retrieval-Augmented Generation (RAG) chatbot project. The system uses ChromaDB as the vector database to store document embeddings and enables efficient retrieval of relevant information for question answering.

## Architecture Components

### 1. Data Sources

The system supports multiple document formats for knowledge base construction:

- **PDF Documents**: Text-based documents loaded using PyPDFLoader
- **Images**: JPG, PNG, JPEG files processed with OCR (Tesseract)
- **Videos**: MP4, AVI, MOV files with frame-by-frame OCR extraction
- **PowerPoint Presentations**: PPTX/PPT files with slide text extraction

### 2. Text Processing Pipeline

#### Document Loading (`build_kb.py`)

```python
# Load ALL PDFs from data/ folder and split into chunks
def load_all_pdfs():
    pdf_files = glob.glob(f"{DATA_DIR}/*.pdf")
    all_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        docs = loader.load()
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)
```

**Key Parameters:**

- **Chunk Size**: 800 characters
- **Chunk Overlap**: 150 characters
- **Purpose**: Maintains context continuity between chunks while keeping them manageable for embedding

#### Image Processing

```python
def load_images():
    image_files = glob.glob(f"{DATA_DIR}/*.jpg") + glob.glob(f"{DATA_DIR}/*.png")
    for img_file in image_files:
        img = Image.open(img_file)
        text = pytesseract.image_to_string(img)
        if text.strip():
            doc = Document(page_content=text, metadata={"source": img_file})
```

**OCR Configuration:**

- Uses Tesseract OCR engine
- Configured path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Extracts text content from images for vectorization

#### Video Processing

```python
def load_videos():
    video_files = glob.glob(f"{DATA_DIR}/*.mp4") + glob.glob(f"{DATA_DIR}/*.avi")
    for vid_file in video_files:
        cap = cv2.VideoCapture(vid_file)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * 30)  # every 30 seconds
```

**Video Processing Logic:**

- Extracts frames every 30 seconds of video
- Applies OCR to each extracted frame
- Stores text with metadata including frame number

#### PowerPoint Processing

```python
def load_slides():
    pptx_files = glob.glob(f"{DATA_DIR}/*.pptx")
    for file in pptx_files:
        prs = Presentation(file)
        text = ""
        for slide_num, slide in enumerate(prs.slides, start=1):
            slide_text = f"Slide {slide_num}:\n"
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    slide_text += shape.text + "\n"
```

**Slide Processing:**

- Extracts text from all shapes on each slide
- Maintains slide numbering in content
- Preserves presentation structure

### 3. Embedding Generation

#### FastEmbed Embeddings

```python
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

embeddings = FastEmbedEmbeddings()
```

**Characteristics:**

- Uses FastEmbed library for efficient embedding generation
- Creates dense vector representations of text chunks
- Optimized for speed and memory usage
- Default model provides good semantic similarity capture

### 4. Vector Database Storage

#### ChromaDB Configuration

```python
from langchain_community.vectorstores import Chroma

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_DIR
)
```

**Storage Details:**

- **Database Location**: `chroma_db/` directory
- **Persistence**: Automatic persistence to disk
- **Index Type**: HNSW (Hierarchical Navigable Small World) for efficient similarity search
- **Metadata Storage**: Preserves source file information and page/frame numbers

#### Database Structure

```
chroma_db/
├── chroma.sqlite3          # SQLite database for metadata
└── [collection_id]/        # Collection-specific data
    ├── data_level0.bin     # Vector data
    ├── header.bin          # Index headers
    ├── length.bin          # Length information
    └── link_lists.bin      # HNSW graph structure
```

### 5. Retrieval Process

#### Retriever Configuration

```python
retriever = vectordb.as_retriever(search_kwargs={"k": 20})
```

**Retrieval Parameters:**

- **k**: Number of top similar documents to retrieve (default: 20)
- **Search Type**: Cosine similarity (default)
- **Search Algorithm**: Approximate nearest neighbor search using HNSW

#### Query Processing

```python
def ask(question, return_data=False):
    docs = retriever.invoke(question)
    citations = []
    for doc in docs:
        src = doc.metadata.get("source", "Unknown")
        pg = doc.metadata.get("page", doc.metadata.get("slide", "N/A"))
        citations.append((src, pg))
```

**Citation Tracking:**

- Extracts source file names
- Captures page numbers for PDFs
- Tracks slide numbers for PowerPoint
- Records frame numbers for videos

### 6. Dynamic Knowledge Base Updates

#### Runtime Document Addition (`app.py`)

```python
if uploaded_file.type == "application/pdf":
    loader = PyPDFLoader(temp_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    vectordb.add_documents(chunks)
```

**Update Process:**

- Processes uploaded files in real-time
- Applies same chunking and embedding as initial build
- Adds new vectors to existing ChromaDB collection
- Maintains consistency with existing data

### 7. RAG Chain Implementation

#### Chain Construction

```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
```

**Chain Components:**

1. **Retriever**: Fetches relevant documents
2. **Format Docs**: Concatenates retrieved document content
3. **Prompt**: Structures context and question for LLM
4. **LLM**: Generates response using Groq (llama-3.1-8b-instant)
5. **Output Parser**: Extracts clean text response

### 8. Performance Metrics

#### Latency Measurement

```python
start_time = time.time()
answer = rag_chain.invoke(question)
end_time = time.time()
latency = end_time - start_time
```

#### Citation Accuracy

```python
total_retrieved = len(citations)
accurate_citations = len(unique_citations)
citation_accuracy = (accurate_citations / total_retrieved * 100)
```

**Metrics Tracked:**

- Response latency in seconds
- Citation accuracy percentage
- Number of retrieved vs. knowledge base documents

### 9. Data Flow Diagram

```
Raw Documents → Text Extraction → Chunking → Embedding → ChromaDB Storage
      ↓              ↓            ↓         ↓           ↓
   PDFs/Images/   OCR/Parsing  800 chars   FastEmbed   HNSW Index
   Videos/PPTX    → Documents  + 150 overlap         → Vectors

Query → Embedding → Similarity Search → Retrieved Chunks → LLM → Answer
         ↓            ↓                    ↓              ↓       ↓
     FastEmbed    ChromaDB (k=20)     Format Context   Groq    Parsed
```

### 10. Dependencies and Configuration

#### Core Libraries

- **langchain**: Framework for RAG pipeline
- **chromadb**: Vector database
- **fastembed**: Embedding generation
- **pytesseract**: OCR for images/videos
- **python-pptx**: PowerPoint processing
- **opencv-python**: Video frame extraction
- **streamlit**: Web interface

#### Environment Variables

- **GROQ_API_KEY**: Required for LLM inference
- **TESSERACT_PATH**: Configured for OCR functionality

### 11. Storage Optimization Strategies

#### Chunking Strategy

- **Size Selection**: 800 characters balances context preservation with embedding efficiency
- **Overlap**: 150 characters maintains continuity across chunk boundaries
- **Document-Specific Handling**: PDFs chunked during loading, others after text extraction

#### Embedding Optimization

- **Model Choice**: FastEmbed prioritizes speed over maximum accuracy
- **Batch Processing**: Processes multiple chunks simultaneously
- **Memory Management**: Efficient vector storage and retrieval

#### Database Optimization

- **Persistence**: Disk-based storage allows for large knowledge bases
- **Indexing**: HNSW enables sub-linear search complexity
- **Incremental Updates**: Supports adding new documents without full rebuild

### 12. Error Handling and Robustness

#### File Processing Errors

```python
try:
    # Processing logic
except Exception as e:
    print(f"Error processing {file}: {e}")
```

**Error Recovery:**

- Continues processing other files if one fails
- Logs specific error messages
- Graceful degradation for unsupported content

#### Database Integrity

- Automatic persistence ensures data durability
- Metadata preservation maintains source attribution
- Duplicate handling prevents redundant storage

### 13. Scalability Considerations

#### Current Limitations

- In-memory processing for initial build
- Single-threaded document processing
- SQLite-based metadata storage

#### Potential Improvements

- Batch embedding generation
- Distributed processing for large document sets
- External metadata database for better performance
- GPU acceleration for embedding computation

### 14. Security and Privacy

#### Data Handling

- Local storage in project directory
- No external data transmission during storage
- Source file metadata preserved for attribution
- Temporary files cleaned up after processing

#### API Security

- Environment variables for API keys
- No hardcoded credentials
- Secure LLM API communication via Groq

This comprehensive storage system enables efficient knowledge base construction and retrieval for the RAG chatbot, supporting multiple document types and providing accurate, cited responses to user queries.
