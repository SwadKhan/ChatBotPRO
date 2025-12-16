# ChatBotPRO - Complete Flowcharts & Visual Diagrams

## Table of Contents

1. [System Initialization Flowchart](#system-initialization-flowchart)
2. [Knowledge Base Building Flowchart](#knowledge-base-building-flowchart)
3. [Query Processing Flowchart](#query-processing-flowchart)
4. [Data Movement Diagrams](#data-movement-diagrams)
5. [Component Interaction Diagrams](#component-interaction-diagrams)
6. [Vector Space Visualization](#vector-space-visualization)
7. [Error Handling Flows](#error-handling-flows)

---

## System Initialization Flowchart

### Application Startup Flow

```
APPLICATION STARTUP (streamlit run app.py)
═══════════════════════════════════════════════════════════════════

                        START
                         │
                         ▼
            ┌────────────────────────┐
            │  Load environment      │
            │  variables (.env)      │
            │  GROQ_API_KEY          │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │  Initialize Streamlit  │
            │  • Page config         │
            │  • Session state       │
            │  • UI layout           │
            └────────┬───────────────┘
                     │
                     ▼
            ┌────────────────────────┐
            │  Import RAG modules    │
            │  (rag_chatbot.py)      │
            └────────┬───────────────┘
                     │
                     ▼
         ┌──────────────────────────────┐
         │  Load embeddings model       │
         │  (FastEmbedEmbeddings)       │
         │  • Initialize ONNX runtime   │
         │  • Load model weights        │
         └────────┬─────────────────────┘
                  │
                  ▼
         ┌──────────────────────────────┐
         │  Connect to ChromaDB         │
         │  • Load chroma_db/ folder    │
         │  • Initialize retriever      │
         │  • Load HNSW index           │
         └────────┬─────────────────────┘
                  │
          ┌───────┴───────┐
          │               │
     SUCCESS          ERROR
          │               │
          ▼               ▼
    ┌──────────┐    ┌──────────┐
    │Render UI │    │Show Error│
    └────┬─────┘    │Message   │
         │          └────┬─────┘
         │               │
         ▼               ▼
    READY FOR       EXIT OR
    USER INPUT      RETRY
         │
         ▼
    ┌────────────────┐
    │ Display:       │
    │ • Mode selector│
    │ • File uploader│
    │ • Chat input   │
    │ • History      │
    └────────────────┘
         │
         ▼
    WAITING FOR USER ACTION
```

---

## Knowledge Base Building Flowchart

### Complete build_kb.py Flow

```
KNOWLEDGE BASE CONSTRUCTION (python build_kb.py)
═══════════════════════════════════════════════════════════════════

                        START
                         │
                         ▼
            ┌────────────────────────┐
            │  Set configuration     │
            │  • DATA_DIR = "data"   │
            │  • CHROMA_DIR = "..."  │
            │  • chunk_size = 800    │
            │  • overlap = 150       │
            └────────┬───────────────┘
                     │
         ┌───────────┴───────────┬────────────┬──────────┐
         │                       │            │          │
         ▼                       ▼            ▼          ▼
    LOAD PDFs            LOAD IMAGES      LOAD VIDEOS  LOAD SLIDES
         │                   │               │           │
         ├─Discover         ├─Discover      ├─Discover ├─Discover
         │ glob(*.pdf)      │ glob(*.jpg)   │ glob(*.mp4) glob(*.pptx)
         │                  │               │           │
         ├─For each PDF:    ├─For each image: ├─For each video:
         │                  │               │           │
         ├─PyPDFLoader()    ├─PIL.Image     ├─cv2.     ├─python-pptx
         │                  │  .open()      │ VideoCapture()
         ├─Extract text     │               │           │
         │ + page#          ├─Tesseract     ├─Extract   ├─Iterate
         │                  │ .image_to_    │ frames    │ slides
         ├─Result:          │  string()     │           │
         │ List[Document]   │               ├─Tesseract├─Extract
         │ with page        ├─Result:       │ on frames│ text
         │                  │ List[Document]│           │
         │                  │ with source   ├─Result:  ├─Result:
         │                  │               │ List[...] │ List[...]
         │
         └───────────────────────────────────┬──────────┘
                                             │
                                    ┌────────▼────────┐
                                    │ MERGE ALL DOCS  │
                                    │ all_docs = []   │
                                    │ • PDFs + pages  │
                                    │ • Images        │
                                    │ • Videos        │
                                    │ • PowerPoints   │
                                    └────────┬────────┘
                                             │
                                             ▼
                            ┌────────────────────────────┐
                            │ TEXT CHUNKING              │
                            │ RecursiveCharacterSplitter │
                            │ • chunk_size = 800        │
                            │ • chunk_overlap = 150     │
                            │                            │
                            │ Process each document:     │
                            │ ├─ Split into chunks      │
                            │ ├─ Preserve metadata      │
                            │ └─ Return chunks list     │
                            └────────┬─────────────────┘
                                     │
                                     ▼
                        ┌────────────────────────┐
                        │  ALL CHUNKS CREATED    │
                        │  Example:              │
                        │  • 5000 PDF chunks     │
                        │  • 500 image chunks    │
                        │  • 200 video chunks    │
                        │  • 300 slide chunks    │
                        │                        │
                        │  TOTAL: 6000 chunks   │
                        └────────┬───────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │  INITIALIZE EMBEDDINGS     │
                    │  FastEmbedEmbeddings()     │
                    │                            │
                    │  • Load ONNX model        │
                    │  • Set dimension to 384   │
                    │  • Prepare for batch      │
                    └────────┬──────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  GENERATE EMBEDDINGS       │
                    │  For each chunk:           │
                    │  • Extract text           │
                    │  • Convert to vector      │
                    │  • Store with metadata    │
                    │                            │
                    │  Progress: 1/6000...      │
                    └────────┬──────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  INITIALIZE CHROMADB       │
                    │  Chroma.from_documents()   │
                    │                            │
                    │  • Create collection      │
                    │  • Set embeddings         │
                    │  • Set persist_directory  │
                    └────────┬──────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  STORE IN CHROMADB         │
                    │                            │
                    │  For each chunk:           │
                    │  • Save embedding vector  │
                    │  • Save metadata JSON     │
                    │  • Build HNSW index       │
                    │  • Progress: n/6000       │
                    └────────┬──────────────────┘
                             │
                             ▼
                    ┌────────────────────────────┐
                    │  PERSIST TO DISK           │
                    │  vectordb.persist()        │
                    │                            │
                    │  Creates:                  │
                    │  ├─ chroma_db/             │
                    │  │  ├─ chroma.sqlite3     │
                    │  │  └─ [collections]      │
                    │  └─ indices/               │
                    │     └─ hnswlib.index      │
                    └────────┬──────────────────┘
                             │
                    ┌────────▼──────────┐
                    │                   │
                 SUCCESS            ERROR
                    │                   │
                    ▼                   ▼
            ┌─────────────────┐  ┌──────────────┐
            │ Log success:    │  │ Log error    │
            │ "6000 chunks    │  │ Display error│
            │  indexed"       │  │ Stack trace  │
            └────────┬────────┘  └──────┬───────┘
                     │                  │
                     ▼                  ▼
            ┌─────────────────┐  ┌──────────────┐
            │ Knowledge Base  │  │ Fix & Retry  │
            │ Ready for       │  │ • Check docs │
            │ Queries!        │  │ • Rebuild    │
            └─────────────────┘  └──────────────┘
                     │
                     ▼
                   END
```

---

## Query Processing Flowchart

### RAG Mode Question Answering

```
QUERY PROCESSING (RAG Mode) - User asks a question
═══════════════════════════════════════════════════════════════════

                    USER ENTERS QUESTION
                    "What is mantrap?"
                            │
                            ▼
                    ┌───────────────────┐
                    │ Validate input    │
                    │ • Not empty?      │
                    │ • Not too long?   │
                    └────────┬──────────┘
                             │
                      ┌──────┴──────┐
                      │             │
                   VALID        INVALID
                      │             │
                      ▼             ▼
                  Continue    ┌──────────────┐
                              │ Show warning │
                              │ "Enter text" │
                              └──────┬───────┘
                                     │
                                     ▼
                                  RETURN
                      │
                      ▼
        ┌──────────────────────────────┐
        │  MODE CHECK                  │
        │  Selected mode = ?            │
        └──────────┬────────────┬───────┘
                   │            │
            RAG MODE       GENERAL MODE
                   │            │
                   ▼            │
        ┌──────────────────┐    │
        │ EMBEDDING PHASE  │    │
        │                  │    │
        │ 1. Get question  │    │
        │ 2. Load embeddings    │
        │ 3. Convert to     │   │
        │    384-dim vector │   │
        │                  │    │
        └────────┬─────────┘    │
                 │              │
                 ▼              │
        ┌──────────────────┐    │
        │ RETRIEVAL PHASE  │    │
        │                  │    │
        │ 1. Query ChromaDB│    │
        │ 2. HNSW search   │    │
        │ 3. Get top 20    │    │
        │    chunks        │    │
        │                  │    │
        └────────┬─────────┘    │
                 │              │
                 ▼              │
        ┌──────────────────┐    │
        │ CONTEXT ASSEMBLY │    │
        │                  │    │
        │ Combine 20       │    │
        │ chunks into:     │    │
        │ """              │    │
        │ Chunk 1 text...  │    │
        │ Chunk 2 text...  │    │
        │ ...              │    │
        │ """              │    │
        │                  │    │
        └────────┬─────────┘    │
                 │              │
        ┌────────┴─────────┐    │
        │                  │    │
        └──────────┬───────────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ PROMPT BUILDING      │
        │                      │
        │ Template:            │
        │ """                  │
        │ You are a strict RAG │
        │ assistant.           │
        │                      │
        │ RULES:               │
        │ 1. Use ONLY context  │
        │ 2. No hallucination  │
        │ 3. Say "I don't      │
        │    have..." if NA    │
        │                      │
        │ Context:             │
        │ {context}            │
        │                      │
        │ Question:            │
        │ {question}           │
        │                      │
        │ Answer:              │
        │ """                  │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ LLM INFERENCE        │
        │                      │
        │ Send to Groq API:    │
        │ • Model: llama-3.1-8b│
        │ • Temperature: 0     │
        │ • Prompt: built      │
        │                      │
        │ Groq processes:      │
        │ • Parse context      │
        │ • Understand question│
        │ • Generate answer    │
        │ • Enforce RAG rules  │
        │                      │
        │ Time: ~500-2000ms    │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ EXTRACT ANSWER       │
        │                      │
        │ Result from LLM:     │
        │ "A mantrap is a      │
        │  security device...."│
        │                      │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ CITATION EXTRACTION  │
        │                      │
        │ From 20 chunks:      │
        │ Extract:             │
        │ • source: filename   │
        │ • page: number       │
        │                      │
        │ Result:              │
        │ [                    │
        │  ("doc.pdf", 42),    │
        │  ("doc.pdf", 43),    │
        │  ("ch1.pdf", 15),    │
        │  ... (up to 20)      │
        │ ]                    │
        │                      │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ CITATION FILTERING   │
        │                      │
        │ Filter 1: Source     │
        │ Keep if:             │
        │ source.startswith()  │
        │ "data/"              │
        │                      │
        │ Filter 2: Duplicates │
        │ Remove if seen       │
        │ before in list       │
        │                      │
        │ Result:              │
        │ [                    │
        │  ("data/doc.pdf",42),│
        │  ("data/doc.pdf",43),│
        │  ("data/ch1.pdf",15) │
        │ ]                    │
        │                      │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ METRICS CALCULATION  │
        │                      │
        │ • latency = end_time │
        │             - start  │
        │ • total_retrieved=20 │
        │ • accurate_cit=3     │
        │ • accuracy%=         │
        │   (3/20)*100 = 15%   │
        │                      │
        └────────┬─────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
DISPLAY ANSWER          ADD TO HISTORY
│                       │
├─ Answer text         ├─ Store Q in history
├─ Citations           ├─ Store A in history
│  - doc.pdf, pg 42    ├─ Store citations
│  - ch1.pdf, pg 15    ├─ Keep last 5 pairs
│                       ├─ If >5: Remove oldest
└─ Metrics:             └─ Update UI display
  Latency: 1.23s
  Citation Acc: 15%

GENERAL MODE PATH (simpler):
│
├─ No embedding/retrieval
├─ Direct LLM call with question
├─ No citations
├─ Same display without citations
└─ End

                        USER SEES RESULTS
                              │
                              ▼
                        READY FOR NEXT QUESTION
```

### File Upload Processing

```
FILE UPLOAD FLOW
═══════════════════════════════════════════════════════════════════

            USER UPLOADS FILE
           (PDF/JPG/PNG/PPTX)
                    │
                    ▼
        ┌──────────────────────┐
        │ FILE TYPE CHECK      │
        │                      │
        │ if .pdf:             │
        │   → PDF_PROCESS      │
        │ elif .jpg/.png/.jpeg:│
        │   → IMAGE_PROCESS    │
        │ elif .pptx:          │
        │   → PPTX_PROCESS     │
        └─┬──┬──────────┬──────┘
          │  │          │
          ▼  ▼          ▼
        PDF IMG         PPTX
        │   │           │
        ├─ Create temp file
        │   │           │
        ├─ PyPDFLoader  ├─PIL.Image.open()
        │               │   │
        ├─ loader.load()├─tesseract.image_to_string()
        │               │   │
        ├─ Extract text ├─Extract text
        │   + metadata  │   + filename metadata
        │               │
        │               ├─python-pptx.Presentation()
        │               │
        │               ├─Iterate slides
        │               │
        │               ├─Extract text from shapes
        │               │
        │               └─Add slide metadata
        │
        └───────────┬───────────┘
                    │
                    ▼
        ┌──────────────────────┐
        │ CREATE DOCUMENT      │
        │ OBJECT               │
        │                      │
        │ Document(            │
        │   page_content=text, │
        │   metadata={         │
        │     "source":        │
        │       filename       │
        │   }                  │
        │ )                    │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ TEXT CHUNKING        │
        │                      │
        │ Same as build_kb:    │
        │ • chunk_size=800     │
        │ • overlap=150        │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ EMBEDDING GEN        │
        │                      │
        │ FastEmbedEmbeddings()│
        │ for each chunk       │
        └────────┬─────────────┘
                 │
                 ▼
        ┌──────────────────────┐
        │ CHROMADB ADD         │
        │                      │
        │ vectordb.add_documents
        │ (chunks)             │
        │                      │
        │ • Add to collection  │
        │ • Update index       │
        │ • Searchable now     │
        └────────┬─────────────┘
                 │
        ┌────────┴────────┐
        │                 │
     SUCCESS           ERROR
        │                 │
        ▼                 ▼
    ┌────────┐       ┌─────────┐
    │Success │       │Show error│
    │message │       │message   │
    └────┬───┘       └────┬─────┘
         │                │
         ▼                ▼
    FILE INDEXED    UPLOAD FAILED
    ADDED TO KB     TRY AGAIN
         │                │
         ▼                ▼
    READY FOR QUERIES
    OR NEXT UPLOAD
```

---

## Data Movement Diagrams

### End-to-End Data Flow

```
DATA FLOW THROUGH ENTIRE SYSTEM
═══════════════════════════════════════════════════════════════════

┌─────────────────────┐
│  DATA/ FOLDER       │ ◄─── User places documents
│ ┌─────────────────┐ │
│ │ document.pdf    │ │
│ │ image.jpg       │ │
│ │ slides.pptx     │ │
│ └─────────────────┘ │
└──────────┬──────────┘
           │
           │ (build_kb.py)
           │ Document Loading + OCR + Parsing
           ▼
┌─────────────────────────┐
│  TEXT DOCUMENTS         │
│ ┌─────────────────────┐ │
│ │ "Text from PDF"     │ │
│ │ "Text from image"   │ │
│ │ "Text from slides"  │ │
│ └─────────────────────┘ │
└──────────┬──────────────┘
           │
           │ Text Chunking
           │ (800 chars, 150 overlap)
           ▼
┌──────────────────────────┐
│  CHUNKS + METADATA       │
│ ┌────────────────────────┐
│ │ {                      │
│ │   page_content: "txt", │
│ │   metadata: {          │
│ │     source: "file",    │
│ │     page: 5            │
│ │   }                    │
│ │ }  (repeated 6000x)    │
│ └────────────────────────┘
└──────────┬───────────────┘
           │
           │ FastEmbed Embedding
           │ (Convert to 384-dim vectors)
           ▼
┌──────────────────────────┐
│  EMBEDDINGS              │
│ ┌────────────────────────┐
│ │ [0.23, -0.51, ...]     │ ◄─── 384-dim vector
│ │ [0.12, 0.34, ...]      │
│ │ [0.45, -0.22, ...]     │
│ │ ... (6000 vectors)     │
│ └────────────────────────┘
└──────────┬───────────────┘
           │
           │ ChromaDB Storage
           │ + HNSW Indexing
           ▼
┌──────────────────────────┐
│  CHROMA_DB/ FOLDER       │ ◄─── Persistent storage
│ ├─ chroma.sqlite3        │
│ ├─ collections/          │
│ │  ├─ embeddings.parquet │
│ │  ├─ metadata.parquet   │
│ │  └─ documents.parquet  │
│ └─ indices/              │
│    └─ hnswlib.index      │
└──────────┬───────────────┘
           │
           │ Query received (app.py)
           │
    ┌──────▼─────────┐
    │ "What is XYZ?" │
    └──────┬─────────┘
           │
           │ FastEmbed query embedding
           ▼
┌──────────────────────┐
│  QUERY VECTOR        │
│ [0.19, -0.48, ...]   │ ◄─── Same 384-dim space
└──────────┬───────────┘
           │
           │ HNSW Similarity Search
           │ (Find top 20 closest)
           ▼
┌──────────────────────────┐
│  TOP 20 CHUNKS           │
│ ┌────────────────────────┐
│ │ Chunk 1 (similarity:0.95)
│ │ Chunk 2 (similarity:0.92)
│ │ ...                     │
│ │ Chunk 20(similarity:0.71)
│ └────────────────────────┘
└──────────┬───────────────┘
           │
           │ Format Context
           │ + Build Prompt
           ▼
┌──────────────────────────┐
│  RAG PROMPT              │
│ "You are RAG assistant..."
│ "Context: [20 chunks]"  │
│ "Question: What is XYZ?"│
└──────────┬───────────────┘
           │
           │ Groq API Call
           │ (llama-3.1-8b)
           ▼
┌──────────────────────────┐
│  GENERATED ANSWER        │
│ "XYZ is a ... device...." │
└──────────┬───────────────┘
           │
           │ Extract Citations
           │ from Chunk Metadata
           ▼
┌──────────────────────────┐
│  CITATIONS               │
│ [                        │
│   ("data/doc.pdf", 42),  │
│   ("data/ch1.pdf", 15)   │
│ ]                        │
└──────────┬───────────────┘
           │
           │ Streamlit Display
           │ + Add to History
           ▼
┌──────────────────────────┐
│  USER SEES RESULTS       │
│ ✓ Answer                 │
│ ✓ Citations              │
│ ✓ Metrics                │
│ ✓ History                │
└──────────────────────────┘
```

---

## Component Interaction Diagrams

### Service Communication Diagram

```
COMPONENT INTERACTIONS
═══════════════════════════════════════════════════════════════════

         ┌──────────────────────────────────────┐
         │  USER (Browser)                      │
         │  • Streamlit Web Interface           │
         └────────────────┬─────────────────────┘
                          │
                          │ HTTP (Port 8501)
                          │
         ┌────────────────▼─────────────────────┐
         │  STREAMLIT APP (app.py)              │
         │  • UI Components                     │
         │  • Session State                     │
         │  • File Upload Handler               │
         │  • Display Formatter                 │
         └────────────────┬─────────────────────┘
                          │
                   ┌──────┴──────┬────────────┐
                   │             │            │
                   ▼             ▼            ▼
         ┌─────────────┐  ┌──────────────┐ ┌──────────────┐
         │ rag_chatbot │  │ build_kb.py  │ │ inspect_db.py│
         │             │  │              │ │              │
         │ • ask()     │  │ • Builds KB  │ │ • Inspects DB│
         │ • general_  │  │ • Processes  │ │ • Stats      │
         │   ask()     │  │   files      │ │              │
         └──────┬──────┘  └──────┬───────┘ └──────────────┘
                │                │
                │                │
         ┌──────┴────────────────┴──────┐
         │                              │
         ▼                              ▼
    ┌──────────────────┐    ┌──────────────────┐
    │ FastEmbeddings   │    │ ChromaDB         │
    │                  │    │                  │
    │ • Load model     │    │ • Vector storage │
    │ • Embed text     │    │ • HNSW index     │
    │ • 384-dim vecs   │    │ • Metadata DB    │
    └──────┬───────────┘    └────────┬─────────┘
           │                         │
           │                    ┌────▼─────┐
           │                    │ chroma_db/│
           │                    │ • Persists│
           │                    │   data    │
           │                    └───────────┘
           │
           └─────────────┬──────────────┐
                         │              │
                    ┌────▼────┐     ┌───▼──────┐
                    │Tesseract│     │LangChain │
                    │         │     │          │
                    │• OCR    │     │• Prompt  │
                    │• Images │     │• Chain   │
                    │• Text   │     │  building│
                    └─────────┘     └────┬─────┘
                                         │
                                    ┌────▼────────┐
                                    │ Groq API    │
                                    │             │
                                    │ • llama-3.1 │
                                    │ • Generate  │
                                    │   answers   │
                                    └─────────────┘
```

### Data Dependencies Graph

```
DEPENDENCY CHAIN
═══════════════════════════════════════════════════════════════════

BUILDING PHASE:
───────────────

data/ folder
    │
    ├─► PDFs ──► PyMuPDF
    │             │
    │             ▼
    │        Text + page#
    │             │
    │             └──┐
    │                │
    ├─► Images ──► Tesseract OCR
    │             │
    │             ▼
    │        Text from image
    │             │
    │             └──┐
    │                │
    ├─► PowerPoint ─► python-pptx
    │             │
    │             ▼
    │        Text + slide#
    │             │
    │             └──┐
    │                │
    └───────────────►┌────────────────┐
                     │ Text Splitting │
                     │ 800/150 config │
                     └────────┬───────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Chunks + Metadata│
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ FastEmbeddings   │
                    │ 384-dimensional  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ ChromaDB Storage │
                    │ HNSW Index       │
                    └──────────────────┘


QUERYING PHASE:
────────────────

User Question
    │
    ▼
FastEmbeddings (same model)
    │
    ▼
ChromaDB + HNSW
    │
    ▼
Top 20 Chunks
    │
    ▼
Context Assembly
    │
    ▼
RAG Prompt
    │
    ▼
Groq LLM
    │
    ▼
Generated Answer
    │
    ├─► Extract Citations from Chunks
    │       │
    │       ▼
    │   Filter by source (data/*)
    │       │
    │       ▼
    │   Remove duplicates
    │       │
    │       ▼
    │   Final Citations
    │
    └─► Display in Streamlit UI
        ├─ Answer
        ├─ Citations
        └─ Metrics
```

---

## Vector Space Visualization

### Embedding Space Representation

```
SEMANTIC VECTOR SPACE (Simplified 2D View)
═══════════════════════════════════════════════════════════════════

                    VECTOR SPACE (384 dimensions)
                    ↓ (Shown as 2D for visualization)

                          ▲ Dimension 2
                          │
                     "What is mantrap?"
                            ◇ (Query vector)
                            │
                            │ 0.95 ◄─── Similarity
                     "Mantrap device..." ●
                     (Chunk 1)          │
                            │          │ 0.92
                     "Types of..." ●    │
                     (Chunk 2)    │\    │
                                 │ \   │
                     "Design of..." ●  │
                     (Chunk 3)      \ │ 0.89
                                    \│
                            ┌────────●─────────► Dimension 1
                            │
                 "Food storage" ●
                 (Chunk 100)  0.23 (Low relevance)
                            │
                 "History of..." ●
                 (Chunk 256)  0.18 (Low relevance)

SEARCH PROCESS:
───────────────
1. Query embedded near relevant chunks
2. Calculate cosine distances
3. HNSW finds closest neighbors
4. Return top 20

VECTOR CHARACTERISTICS:
───────────────────────
• Dimension: 384
• Range: Real numbers (-1 to +1 typical)
• Similarity: Cosine distance (0=opposite, 1=identical)
• Model: FastEmbed (ONNX format)
• Speed: ~50ms for embedding generation
```

---

## Error Handling Flows

### Error Recovery Paths

```
ERROR HANDLING & RECOVERY
═══════════════════════════════════════════════════════════════════

DURING KNOWLEDGE BASE BUILDING:
───────────────────────────────

build_kb.py START
        │
        ├─► File not found error
        │       │
        │       ▼
        │   Catch exception
        │       │
        │       ├─► Log: "File not found: ..."
        │       │
        │       ├─► Skip file
        │       │
        │       └─► Continue with next file
        │
        ├─► Embedding generation error
        │       │
        │       ▼
        │   • Text too long?
        │   • Model load failure?
        │   • Memory issue?
        │       │
        │       └─► Log error
        │           Continue with next chunk
        │
        ├─► ChromaDB persistence error
        │       │
        │       ▼
        │   • Disk full?
        │   • Permission denied?
        │   • File locked?
        │       │
        │       └─► Show "Cannot save DB"
        │           Exit with error code
        │
        └─► Tesseract OCR error
                │
                ▼
            • Image corrupted?
            • Tesseract not installed?
                │
                └─► Log "OCR failed"
                    Skip image
                    Continue


DURING QUERY PROCESSING:
────────────────────────

ask() called
    │
    ├─► ChromaDB connection error
    │       │
    │       └─► Return: "Database connection failed"
    │
    ├─► Groq API error
    │       │
    │       ├─► "API key invalid"?
    │       │       └─► Return: "Auth failed"
    │       │
    │       ├─► "Rate limited"?
    │       │       └─► Return: "Too many requests"
    │       │
    │       ├─► "Timeout"?
    │       │       └─► Return: "Request timed out"
    │       │
    │       └─► "Server error (500)"?
    │               └─► Return: "Service unavailable"
    │
    ├─► No results from retrieval
    │       │
    │       └─► Return: "No relevant info found"
    │
    ├─► Citation metadata missing
    │       │
    │       └─► Use default: ("Unknown", "N/A")
    │
    └─► Output parsing error
            │
            └─► Return: "Error processing response"


DURING FILE UPLOAD:
───────────────────

User uploads file
        │
        ├─► File type not supported
        │       │
        │       └─► Show: "File type not supported"
        │
        ├─► File size too large
        │       │
        │       └─► Show: "File too large"
        │
        ├─► Corrupt file
        │       │
        │       └─► Show: "Cannot process file"
        │
        ├─► Processing error (OCR, PDF, etc)
        │       │
        │       └─► Show: "Error processing file"
        │
        └─► Chunk generation failed
                │
                └─► Show: "Cannot add to KB"


DURING STREAMLIT SESSION:
──────────────────────────

Session starts
        │
        ├─► .env file missing
        │       │
        │       └─► Show: "API key not configured"
        │
        ├─► ChromaDB folder missing
        │       │
        │       └─► Show: "Run build_kb.py first"
        │
        ├─► Memory leak
        │       │
        │       └─► Monitor history size
        │           Clear old entries
        │
        └─► Long response time
                │
                └─► Show loading spinner
                    Display progress updates
```

---

## Summary Visual

### System Architecture at a Glance

```
┌───────────────────────────────────────────────────────────────────┐
│                     CHATBOTPRO ARCHITECTURE                       │
├───────────────────────────────────────────────────────────────────┤
│                                                                    │
│  INPUT LAYER                                                       │
│  ├─ Documents: PDF, Images, PowerPoint                            │
│  ├─ Questions: Natural language user input                        │
│  └─ Files: Real-time upload support                               │
│                                                                    │
│  PROCESSING LAYERS                                                 │
│  ├─ Document Processing                                            │
│  │  ├─ PyMuPDF (PDFs)                                             │
│  │  ├─ Tesseract (Images)                                         │
│  │  └─ python-pptx (PowerPoints)                                  │
│  │                                                                 │
│  ├─ Text Chunking (800 chars, 150 overlap)                        │
│  │                                                                 │
│  ├─ Vectorization (FastEmbed - 384 dims)                          │
│  │                                                                 │
│  └─ Storage & Indexing (ChromaDB + HNSW)                          │
│                                                                    │
│  RETRIEVAL & GENERATION                                            │
│  ├─ Query Embedding (same model)                                  │
│  ├─ Similarity Search (top-20)                                    │
│  ├─ Context Assembly                                              │
│  ├─ LLM Generation (Groq Llama)                                   │
│  └─ Citation Extraction                                           │
│                                                                    │
│  OUTPUT LAYER                                                      │
│  ├─ Generated Answer                                              │
│  ├─ Source Citations                                              │
│  ├─ System Metrics                                                │
│  └─ Conversation History                                          │
│                                                                    │
└───────────────────────────────────────────────────────────────────┘

OPERATION MODES:
├─ RAG Mode: Knowledge base only (strict, no hallucination)
└─ General Mode: Open-ended (creative, may hallucinate)

KEY FEATURES:
├─ Multi-modal document support
├─ Citation with page numbers
├─ Conversation history (max 5 pairs)
├─ Real-time file upload processing
└─ Performance metrics
```

---

**Created**: 2025-12-16
**Document Version**: 1.0 Complete
**Total Diagrams**: 15+
**Last Updated**: 2025-12-16
