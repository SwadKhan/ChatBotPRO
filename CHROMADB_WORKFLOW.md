# ChromaDB Workflow - Detailed Technical Guide

## Table of Contents

1. [ChromaDB Overview](#chromadb-overview)
2. [Architecture & Components](#architecture--components)
3. [Detailed Workflow](#detailed-workflow)
4. [Data Storage Structure](#data-storage-structure)
5. [Retrieval Process](#retrieval-process)
6. [Complete System Flow](#complete-system-flow)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting & Best Practices](#troubleshooting--best-practices)

---

## ChromaDB Overview

### What is ChromaDB?

ChromaDB is a vector database designed for AI applications. It stores embeddings (high-dimensional vectors) and their associated metadata, enabling fast semantic similarity searches.

### Why ChromaDB for ChatBotPRO?

- **Efficient Search**: Find relevant documents in milliseconds
- **Persistent Storage**: Data survives application restarts
- **Metadata Support**: Store and filter by source, page, etc.
- **Scalability**: Handle thousands of document chunks
- **Easy Integration**: Works seamlessly with LangChain
- **Local First**: No cloud dependency, full data privacy

### Key Concepts

| Concept        | Definition                                           |
| -------------- | ---------------------------------------------------- |
| **Vector**     | High-dimensional representation of text (embeddings) |
| **Embedding**  | Mathematical representation capturing text meaning   |
| **Chunk**      | Fixed-size piece of document text (~800 chars)       |
| **Metadata**   | Associated information (source, page, slide)         |
| **Collection** | Database containing vectors and metadata             |
| **Query**      | User question converted to embedding                 |
| **Similarity** | How close two embeddings are (0-1 scale)             |

---

## Architecture & Components

### Physical Storage Structure

```
chroma_db/
├── chroma.sqlite3                    # Main database file
│   ├── Collections table
│   ├── Embeddings table
│   └── Metadata table
│
└── 5eb532d7-d910-474b-8762-b368a46fed1f/  # Collection folder
    ├── data/
    │   ├── embeddings/               # Vector storage
    │   ├── documents/                # Document chunks
    │   └── metadata/                 # Metadata storage
    │
    └── index/                        # Similarity search index
        └── Vector Index (HNSW)       # Fast search structure
```

### ChromaDB Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CHROMADB ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          VECTOR STORAGE LAYER                       │   │
│  │ ┌──────────────┐  ┌──────────────┐                 │   │
│  │ │  Embeddings  │  │   Metadata   │                 │   │
│  │ │  (Dense)     │  │  (Tags/Info) │                 │   │
│  │ └──────────────┘  └──────────────┘                 │   │
│  └────────────┬───────────────────────────────────────┘   │
│               ▼                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │      SIMILARITY SEARCH INDEX LAYER                  │   │
│  │  (Hierarchical Navigable Small World - HNSW)       │   │
│  │  - Enables fast k-nearest neighbor search           │   │
│  │  - Configurable k value (default: 20)              │   │
│  └────────────┬───────────────────────────────────────┘   │
│               ▼                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │        PERSISTENCE LAYER                            │   │
│  │  SQLite3 Backend for durability                     │   │
│  └────────────┬───────────────────────────────────────┘   │
│               │                                              │
│               └─► chroma_db/ folder storage                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Model

```
┌────────────────────────────────────┐
│          CHUNK OBJECT              │
├────────────────────────────────────┤
│                                    │
│  page_content (required)           │
│  └─ String: Text content (≤800)   │
│                                    │
│  metadata (required)               │
│  ├─ source: Document filename     │
│  ├─ page: Page number             │
│  ├─ slide: Slide number           │
│  └─ other: Custom fields          │
│                                    │
│  embedding (auto-generated)        │
│  └─ Vector: 384-dim FastEmbed     │
│                                    │
└────────────────────────────────────┘
```

---

## Detailed Workflow

### Phase 1: Knowledge Base Building (build_kb.py)

```
STEP-BY-STEP KNOWLEDGE BASE CONSTRUCTION
═══════════════════════════════════════════════════════════════

1. INITIALIZATION
   │
   ├─ Import FastEmbedEmbeddings (384-dimension embedder)
   ├─ Initialize ChromaDB client
   └─ Set persist_directory="chroma_db"

2. DOCUMENT DISCOVERY
   │
   ├─ Scan data/*.pdf
   ├─ Scan data/*.jpg, data/*.png, data/*.jpeg
   ├─ Scan data/*.pptx, data/*.ppt
   └─ Scan data/*.mp4, data/*.avi, data/*.mov

3. PARALLEL DOCUMENT LOADING
   │
   ├─ PDF PROCESSING
   │  ├─ Use PyPDFLoader
   │  ├─ Extract text + page metadata
   │  └─ Return: List[Document] with page info
   │
   ├─ IMAGE PROCESSING
   │  ├─ Use PIL to load image
   │  ├─ Apply Tesseract OCR
   │  ├─ Extract text from image
   │  └─ Return: List[Document] with source metadata
   │
   ├─ POWERPOINT PROCESSING
   │  ├─ Use python-pptx library
   │  ├─ Iterate through slides
   │  ├─ Extract text from shapes
   │  └─ Return: List[Document] with slide metadata
   │
   └─ VIDEO PROCESSING (optional)
      ├─ Use OpenCV to capture frames
      ├─ Extract every N frames (based on FPS)
      ├─ Apply OCR to frames
      └─ Return: List[Document] with frame metadata

4. TEXT CHUNKING
   │
   ├─ Create RecursiveCharacterTextSplitter:
   │  ├─ chunk_size = 800 characters
   │  └─ chunk_overlap = 150 characters
   │
   └─ Split each document into chunks:
      Example:
      Document: "The system processes documents in chunks.
                  Each chunk contains up to 800 characters.
                  Overlapping ensures context continuity..."

      Result:
      Chunk 1: "The system processes documents in chunks.
                Each chunk contains up to 800 characters."

      Chunk 2: "Each chunk contains up to 800 characters.
                Overlapping ensures context continuity..."

5. METADATA ENHANCEMENT
   │
   └─ For each chunk, preserve:
      ├─ source: Filename (e.g., "document.pdf")
      ├─ page: Page number (PDFs only)
      ├─ slide: Slide number (PowerPoints only)
      ├─ frame: Frame number (videos only)
      └─ Other fields from original document

6. EMBEDDING GENERATION
   │
   ├─ For each chunk:
   │  ├─ Extract page_content (text)
   │  └─ Pass to FastEmbedEmbeddings
   │
   ├─ FastEmbed Model:
   │  ├─ Uses ONNX runtime (fast inference)
   │  ├─ Generates 384-dimensional vectors
   │  └─ All texts in same vector space
   │
   └─ Result: Chunk + Embedding pair

7. CHROMADB STORAGE
   │
   ├─ Initialize ChromaDB collection
   │
   ├─ For each chunk:
   │  ├─ Pass page_content to embeddings
   │  ├─ Store embedding vector
   │  ├─ Store metadata
   │  └─ Create collection entry
   │
   ├─ Build Similarity Index (HNSW)
   │  ├─ Index embeddings for fast search
   │  ├─ Create hierarchical graph
   │  └─ Enable k-nearest neighbor queries
   │
   └─ Persist to Disk:
      ├─ Save chroma.sqlite3
      ├─ Write embedding vectors
      ├─ Write metadata
      └─ Save index structures

8. COMPLETION
   │
   └─ Knowledge base ready for queries!
```

### Phase 2: Query Processing (RAG Mode)

```
QUERY-TO-ANSWER FLOW
═══════════════════════════════════════════════════════════════

1. USER INPUT
   │
   └─ Question: "What is mantrap in cybersecurity?"

2. QUESTION EMBEDDING
   │
   ├─ Receive question string
   ├─ Pass to FastEmbedEmbeddings (same model as build)
   ├─ Generate 384-dimensional vector
   └─ Result: question_embedding vector

3. CHROMADB SIMILARITY SEARCH
   │
   ├─ Query Configuration:
   │  ├─ search_kwargs = {"k": 20}
   │  └─ Retrieve top 20 similar chunks
   │
   ├─ HNSW Index Search:
   │  ├─ Start from random node in graph
   │  ├─ Use greedy layer-wise search
   │  ├─ Calculate cosine similarity to neighbors
   │  ├─ Move to closer neighbors
   │  └─ Repeat until optimal k found
   │
   ├─ Similarity Calculation:
   │  ├─ Formula: cos(v1, v2) = (v1·v2) / (|v1||v2|)
   │  ├─ Range: -1 (opposite) to 1 (identical)
   │  └─ High score = high relevance
   │
   └─ Result: List[20 Document chunks with similarity scores]

4. CONTEXT ASSEMBLY
   │
   ├─ Retrieved chunks example:
   │  Chunk 1 (score: 0.95): "A mantrap is a device designed..."
   │  Chunk 2 (score: 0.92): "Common types of mantraps include..."
   │  Chunk 3 (score: 0.89): "Mantraps are used in..."
   │  ...
   │  Chunk 20 (score: 0.71): "..."
   │
   └─ Combine into context string:
      context = """
      A mantrap is a device designed...
      Common types of mantraps include...
      Mantraps are used in...
      ...
      """

5. RAG PROMPT CREATION
   │
   └─ Template:
      """
      You are a strict RAG assistant.

      RULES:
      1. Use ONLY the information from the context below.
      2. DO NOT generate your own citations.
      3. If context doesn't have info, say "I don't have
         information on that topic" and nothing else.

      Context:
      {context}

      Question: {question}

      Answer:
      """

6. LLM INFERENCE (Groq)
   │
   ├─ Send to Groq API:
   │  ├─ Model: llama-3.1-8b-instant
   │  ├─ Temperature: 0 (deterministic)
   │  └─ Prompt: Formatted RAG prompt
   │
   ├─ LLM Processing:
   │  ├─ Parse context (20 chunks)
   │  ├─ Understand question
   │  ├─ Generate answer using only context
   │  └─ Enforce RAG rules
   │
   └─ Result: Generated answer text

7. CITATION EXTRACTION
   │
   ├─ From retrieved documents, extract metadata:
   │  └─ For each of 20 chunks:
   │     ├─ source: "document.pdf"
   │     ├─ page: 42
   │     └─ Add to citations list
   │
   ├─ Result: List[(source, page_number)]
   │  Example:
   │  [
   │    ("document.pdf", 42),
   │    ("document.pdf", 43),
   │    ("Chapter_1.pdf", 15),
   │    ...
   │  ]
   │
   └─ Total: Up to 20 citation entries

8. CITATION FILTERING
   │
   ├─ Filter 1: Source location
   │  ├─ Keep only citations where source starts with "data/"
   │  ├─ This excludes uploaded files (uploaded during session)
   │  └─ Ensures only pre-built KB sources shown
   │
   ├─ Filter 2: Duplicate removal
   │  ├─ Same file, different pages: Keep
   │  ├─ Exact duplicate entry: Remove
   │  └─ Result: Unique citation list
   │
   └─ Result: Filtered, unique citations

9. RESPONSE FORMATTING
   │
   ├─ Compile response object:
   │  ├─ answer: Generated text
   │  ├─ citations: Filtered list
   │  ├─ latency: Response time (seconds)
   │  └─ citation_accuracy: Percent of relevant citations
   │
   └─ Format for display:
      Answer: "A mantrap is a security device..."

      Citations:
      - document.pdf, page 42
      - Chapter_1.pdf, page 15

10. DISPLAY TO USER
    │
    └─ Show formatted response in Streamlit UI
```

### Phase 3: ChromaDB Update (File Upload)

```
INCREMENTAL UPDATE FLOW
═══════════════════════════════════════════════════════════════

1. USER UPLOADS FILE
   │
   └─ Supports: PDF, JPG, PNG, PPTX

2. TEMPORARY PROCESSING
   │
   ├─ Save to temporary location
   ├─ Process same as during build:
   │  ├─ Extract text (OCR for images)
   │  ├─ Create chunks (800 chars, 150 overlap)
   │  └─ Add metadata (source = filename)
   │
   └─ Result: List of chunks

3. EMBEDDING GENERATION
   │
   ├─ Use same FastEmbedEmbeddings model
   ├─ Generate embeddings for all chunks
   └─ Result: Embeddings + metadata

4. CHROMADB ADD_DOCUMENTS
   │
   ├─ Use: vectordb.add_documents(chunks)
   │
   ├─ Process:
   │  ├─ Create embeddings for chunks
   │  ├─ Add to existing collection
   │  ├─ Update HNSW index
   │  └─ Merge with existing vectors
   │
   └─ Result: Uploaded content searchable

5. CITATION FILTERING
   │
   ├─ Uploaded files NOT shown in citations
   ├─ Reason: Filter checks source.startswith("data/")
   ├─ Uploaded files don't start with "data/"
   └─ Result: Clean citations from pre-built KB only

6. SESSION PERSISTENCE
   │
   ├─ Upload additions stay for session only
   ├─ When app restarts: Revert to original DB
   ├─ To make permanent: Run build_kb.py
   └─ Reason: Add_documents() not persisted by default
```

---

## Data Storage Structure

### SQLite Database Format

```
chroma.sqlite3
├── collections
│   ├── id (Primary Key)
│   ├── name (Collection name)
│   ├── metadata (JSON field)
│   └── timestamp
│
├── embeddings
│   ├── id (Primary Key)
│   ├── collection_id (Foreign Key)
│   ├── embedding (Binary BLOB - 384*4 bytes)
│   ├── document (Text content)
│   └── metadata (JSON - source, page, etc.)
│
└── indices
    ├── collection_id
    └── HNSW Index Structure (binary)
```

### Collection Folder Structure

```
5eb532d7-d910-474b-8762-b368a46fed1f/
├── data/
│   ├── embeddings.parquet  # Vector storage (Parquet format)
│   ├── documents.parquet   # Document chunks
│   └── metadata.parquet    # Metadata JSON
│
└── index/
    ├── index_metadata.json # Index configuration
    └── hnswlib.index      # HNSW binary index
```

### Sample Metadata JSON

```json
{
  "source": "data/document.pdf",
  "page": 42,
  "chunk_id": "doc_42_chunk_3"
}
```

---

## Retrieval Process

### Detailed Retrieval Algorithm

```
SIMILARITY SEARCH PROCESS
═══════════════════════════════════════════════════════════════

Input: Query question
       k = 20 (number of results)

Step 1: EMBEDDING CONVERSION
        ├─ Question: "What is XYZ?"
        ├─ Embed to vector: [0.234, -0.512, 0.891, ...]
        └─ Dimension: 384

Step 2: INDEX LOOKUP
        ├─ Load HNSW index from disk
        ├─ Start from entry point
        ├─ Perform greedy search through layers
        └─ Log distances to all explored nodes

Step 3: CANDIDATE SELECTION
        ├─ Visit approximately 2k candidates
        ├─ Calculate similarity:
        │  similarity = dot_product(query_embedding, candidate_embedding)
        └─ Sort by similarity descending

Step 4: TOP-K SELECTION
        ├─ Select top 20 candidates
        ├─ Results ranked by similarity:
        │  1. similarity=0.954, distance=0.046
        │  2. similarity=0.932, distance=0.068
        │  3. similarity=0.891, distance=0.109
        │  ...
        │  20. similarity=0.712, distance=0.288
        └─ Retrieve full documents for these 20

Step 5: METADATA RECONSTRUCTION
        ├─ For each result:
        │  ├─ Get embedding vector
        │  ├─ Get page_content (text)
        │  ├─ Get metadata JSON
        │  └─ Construct Document object
        │
        └─ Return List[Document]

Output: 20 most similar documents with metadata
```

### Performance Characteristics

```
COMPLEXITY ANALYSIS
═══════════════════════════════════════════════════════════════

Operation        Time Complexity    Space Complexity
─────────────────────────────────────────────────────────────
Embedding Gen    O(n)              O(1)  [384-dim fixed]
─────────────────────────────────────────────────────────────
HNSW Search      O(log N)          O(N)  [N = total chunks]
─────────────────────────────────────────────────────────────
Get Top-k        O(log N)          O(k)  [k = 20]
─────────────────────────────────────────────────────────────
Metadata Load    O(k)              O(k)
─────────────────────────────────────────────────────────────

Typical Performance (with 10,000 chunks):
├─ Embedding generation: ~50ms
├─ HNSW search: ~5-10ms
├─ Total latency: ~100-200ms (including LLM)
└─ Memory: ~100MB (embeddings) + 50MB (index)
```

---

## Complete System Flow

### End-to-End Question Answering Flow

```
                    CHATBOTPRO COMPLETE FLOW
════════════════════════════════════════════════════════════════════

USER INTERFACE (Streamlit app.py)
│
├─ User enters: "What is network security?"
│
└─► QUESTION PROCESSING
    │
    ├─ Validate input (not empty)
    │
    ├─► MODE CHECK
    │   │
    │   ├─ RAG MODE → Proceed to retrieval
    │   └─ GENERAL MODE → Skip to LLM only
    │
    └─► RAG MODE PATH (Main flow)
        │
        ├─ STEP 1: EMBEDDING CONVERSION
        │   ├─ Load FastEmbedEmbeddings model
        │   ├─ Convert question to vector
        │   └─ Result: 384-dim embedding
        │
        ├─ STEP 2: CHROMADB RETRIEVAL
        │   ├─ Query ChromaDB collection
        │   ├─ Using HNSW index search
        │   ├─ Retrieve top 20 similar chunks
        │   └─ Result: List[Document] with metadata
        │
        ├─ STEP 3: CONTEXT ASSEMBLY
        │   ├─ Extract text from 20 documents
        │   ├─ Combine into single context string
        │   └─ Limit to reasonable size
        │
        ├─ STEP 4: PROMPT BUILDING
        │   ├─ Create RAG prompt template
        │   ├─ Insert context and question
        │   └─ Result: Full prompt text
        │
        ├─ STEP 5: LLM GENERATION
        │   ├─ Send to Groq API
        │   ├─ Model: llama-3.1-8b-instant
        │   ├─ Temperature: 0 (deterministic)
        │   └─ Result: Generated answer
        │
        ├─ STEP 6: CITATION EXTRACTION
        │   ├─ Get metadata from 20 documents
        │   ├─ Extract source and page info
        │   └─ Result: List[(source, page)]
        │
        ├─ STEP 7: CITATION FILTERING
        │   ├─ Filter by source path (data/*)
        │   ├─ Remove duplicates
        │   └─ Result: Unique filtered citations
        │
        ├─ STEP 8: METRICS CALCULATION
        │   ├─ Calculate latency (response time)
        │   ├─ Calculate citation accuracy
        │   └─ Result: Performance metrics
        │
        └─ STEP 9: RESPONSE COMPILATION
            ├─ Combine:
            │  ├─ Answer text
            │  ├─ Citations
            │  └─ Metrics
            │
            └─ Return to UI

USER INTERFACE (Display Results)
│
├─ Show answer text
│
├─ Show citations:
│   ├─ source.pdf, page 42
│   └─ source.pdf, page 43
│
├─ Show metrics:
│   ├─ Latency: 1.23 seconds
│   └─ Citation Accuracy: 95%
│
├─ ADD TO HISTORY
│   ├─ Store Q/A pair in session state
│   ├─ Keep only last 5 pairs
│   └─ Display conversation history
│
└─ READY FOR NEXT QUESTION
    └─► Loop back to question input
```

---

## Performance Optimization

### Indexing Optimization

```
HNSW (Hierarchical Navigable Small World) Index
═══════════════════════════════════════════════════════════════

Benefits:
├─ Logarithmic time complexity: O(log N)
├─ No need to read all vectors
├─ Hierarchical structure speeds up search
└─ Configurable parameters

Default Configuration:
├─ M: 16 (connections per node)
├─ ef_construction: 200 (search parameter during indexing)
└─ ef: 20 (search parameter during querying)

Tuning Tips:
├─ Increase M → Better recall, more memory
├─ Increase ef → Better accuracy, slower speed
└─ Decrease ef → Faster speed, lower accuracy
```

### Query Optimization

```
OPTIMIZATION STRATEGIES
═══════════════════════════════════════════════════════════════

1. K VALUE ADJUSTMENT
   Current: k=20
   ├─ Increase to 30-50 → Better recall, slower
   └─ Decrease to 10-15 → Faster, may miss context

2. CHUNK SIZE OPTIMIZATION
   Current: 800 characters
   ├─ Smaller chunks (500) → More granular, more chunks
   └─ Larger chunks (1200) → Better context, fewer chunks

3. SIMILARITY THRESHOLD
   Could add threshold filtering:
   ├─ Keep only chunks with similarity > 0.7
   └─ Improves precision, may lose recall

4. RERANKING
   Two-stage retrieval:
   ├─ Stage 1: BM25 keyword search (fast)
   ├─ Stage 2: Semantic reranking (accurate)
   └─ Result: Better quality + faster

5. CACHING
   Cache frequently asked questions:
   ├─ Store (question, answer) pairs
   ├─ Return cached answer immediately
   └─ Reduce API calls and latency
```

---

## Troubleshooting & Best Practices

### Common Issues

| Issue           | Cause                      | Solution                                           |
| --------------- | -------------------------- | -------------------------------------------------- |
| Empty results   | No matching chunks         | Check document content, lower similarity threshold |
| Slow queries    | Large k value, many chunks | Reduce k, optimize chunk size, rebuild index       |
| Memory issues   | Too many embeddings        | Reduce document count, use smaller k               |
| Wrong answers   | Poor chunk relevance       | Improve documents, adjust chunk overlap            |
| Citation errors | Metadata missing           | Rebuild KB, verify document sources                |

### Best Practices

```
KNOWLEDGE BASE BUILDING
═══════════════════════════════════════════════════════════════

1. Document Quality
   ├─ Use clear, well-structured documents
   ├─ Remove formatting artifacts
   └─ Ensure OCR quality for images

2. Chunking Strategy
   ├─ Chunk size: 800-1000 chars (balanced)
   ├─ Overlap: 150-200 chars (context continuity)
   └─ Preserve complete sentences across chunks

3. Metadata Management
   ├─ Always include source file path
   ├─ Add page/slide numbers
   └─ Include document type indicators

4. Regular Maintenance
   ├─ Rebuild KB when adding new documents
   ├─ Archive old versions of DB
   └─ Monitor collection size

QUERY OPTIMIZATION
═══════════════════════════════════════════════════════════════

1. Question Formulation
   ├─ Use specific, clear language
   ├─ Include domain-relevant keywords
   └─ Avoid ambiguous pronouns

2. Mode Selection
   ├─ RAG mode: For domain-specific questions
   ├─ General mode: For open-ended questions
   └─ Use metadata filters when possible

3. Result Evaluation
   ├─ Check citation relevance
   ├─ Verify answer accuracy
   └─ Provide feedback for improvement
```

### Health Check Commands

```bash
# Inspect database contents
python inspect_db.py

# Check collection statistics
python -c "from rag_chatbot import vectordb; print(vectordb._collection.count())"

# Test retrieval directly
python -c "
from rag_chatbot import retriever
docs = retriever.invoke('Your test question')
for doc in docs[:3]:
    print(doc.metadata, doc.page_content[:100])
"

# Verify embeddings
python -c "
from rag_chatbot import embeddings
embed = embeddings.embed_query('test')
print(f'Embedding dimension: {len(embed)}')
print(f'Sample values: {embed[:5]}')
"
```

---

## Summary

### ChromaDB's Role in ChatBotPRO

**ChromaDB is the intelligent backbone** that:

1. **Stores** text embeddings and metadata from all documents
2. **Indexes** embeddings for fast similarity search using HNSW
3. **Retrieves** the most relevant chunks for each question
4. **Preserves** source information for citations
5. **Persists** data across sessions

### The RAG Pipeline

```
Documents → Embeddings → Storage (ChromaDB) → Search → LLM → Answer
   ↓           ↓               ↓                  ↓       ↓
 build_kb   FastEmbed    chroma_db/         retriever  groq
```

### Performance Characteristics

- **Indexing**: One-time cost (build_kb.py)
- **Query**: <100ms for similarity search + embedding
- **LLM**: 500-2000ms for answer generation
- **Total latency**: ~1-2 seconds per question

### Scalability

- **Supported**: 10,000+ document chunks
- **Memory**: ~100-200MB per 10,000 chunks
- **Disk**: ~1GB per 100,000 chunks
- **Performance**: Linear degradation with size

---

**Document Created**: 2025-12-16
**ChromaDB Version**: Latest (compatible with LangChain)
**FastEmbed Model**: Default (384-dimensional)
**HNSW Algorithm**: Standard configuration
