# ChatBotPRO - Complete Project Overview & Architecture

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Key Components](#key-components)
6. [How It Works](#how-it-works)
7. [Data Flow Diagrams](#data-flow-diagrams)
8. [Installation & Setup](#installation--setup)
9. [Usage Guide](#usage-guide)
10. [Features & Capabilities](#features--capabilities)

---

## Executive Summary

**ChatBotPRO** is an intelligent Retrieval-Augmented Generation (RAG) system that transforms documents into a conversational knowledge base. It processes multiple document types (PDFs, images, PowerPoints) and allows users to ask natural language questions to retrieve accurate, cited answers.

### Key Value Propositions

- 📚 **Multi-Modal Support**: Process PDFs, images (with OCR), and PowerPoint presentations
- 🎯 **Accurate Answers**: RAG mode ensures answers come from your documents only
- 🔗 **Source Citations**: Every answer includes source references with page/slide numbers
- 💬 **Conversational Interface**: Easy-to-use Streamlit web interface
- 🚀 **Fast Processing**: Powered by ChromaDB vector database for quick retrieval
- 🔧 **Flexible Modes**: Choose between strict RAG (no hallucination) or general mode (creative answers)

---

## System Architecture

### High-Level Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CHATBOT PRO SYSTEM                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐      ┌──────────────────┐                    │
│  │   USER INTERFACE │      │  FILE UPLOAD     │                    │
│  │   (Streamlit)    │      │  (PDF/IMG/PPTX)  │                    │
│  └────────┬─────────┘      └────────┬─────────┘                    │
│           │                         │                              │
│           └─────────────┬───────────┘                              │
│                         ▼                                          │
│  ┌────────────────────────────────────────┐                       │
│  │   DOCUMENT PROCESSING LAYER            │                       │
│  │ • PDF Text Extraction (PyMuPDF)        │                       │
│  │ • Image OCR (Tesseract)                │                       │
│  │ • PowerPoint Parsing (python-pptx)     │                       │
│  └────────────┬─────────────────────────┘                        │
│               ▼                                                    │
│  ┌────────────────────────────────────────┐                       │
│  │   TEXT CHUNKING & PROCESSING           │                       │
│  │ • RecursiveCharacterTextSplitter       │                       │
│  │ • Chunk Size: 800 chars                │                       │
│  │ • Overlap: 150 chars                   │                       │
│  └────────────┬─────────────────────────┘                        │
│               ▼                                                    │
│  ┌────────────────────────────────────────┐                       │
│  │   EMBEDDING & VECTORIZATION            │                       │
│  │ • FastEmbed Model                      │                       │
│  │ • High-Performance Embeddings          │                       │
│  └────────────┬─────────────────────────┘                        │
│               ▼                                                    │
│  ┌────────────────────────────────────────┐                       │
│  │   VECTOR DATABASE (ChromaDB)           │                       │
│  │ • Persistent Storage in chroma_db/     │                       │
│  │ • Metadata Storage (source, page)      │                       │
│  │ • Similarity Search Capability         │                       │
│  └────────────┬─────────────────────────┘                        │
│               │                                                    │
│               └──────┬──────────┬──────────┐                      │
│                      ▼          ▼          ▼                      │
│              ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│              │RETRIEVER │  │  LLM     │  │ RESPONSE │            │
│              │ (Top 20) │  │ (Groq)   │  │FORMATTER │            │
│              └──────────┘  └──────────┘  └──────────┘            │
│                      │          │          │                      │
│                      └──────────┴──────────┘                      │
│                             ▼                                      │
│              ┌──────────────────────────────┐                     │
│              │ ANSWER + CITATIONS + METRICS│                     │
│              │ • Answer Text               │                     │
│              │ • Source References         │                     │
│              │ • Latency Information       │                     │
│              │ • Citation Accuracy Score   │                     │
│              └──────────────────────────────┘                     │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Backend Technologies

| Component            | Technology              | Purpose                       |
| -------------------- | ----------------------- | ----------------------------- |
| **Framework**        | LangChain               | RAG pipeline orchestration    |
| **Vector DB**        | ChromaDB                | Persistent vector storage     |
| **Embeddings**       | FastEmbed               | High-speed text vectorization |
| **LLM**              | Groq API (Llama 3.1 8B) | Answer generation             |
| **PDF Processing**   | PyMuPDF                 | Extract text from PDFs        |
| **Image Processing** | PIL + Tesseract         | OCR for image text extraction |
| **PowerPoint**       | python-pptx             | Extract text from slides      |
| **Text Splitting**   | LangChain               | Document chunking             |

### Frontend & User Interface

| Component              | Technology              | Purpose                             |
| ---------------------- | ----------------------- | ----------------------------------- |
| **Web Framework**      | Streamlit               | Interactive web interface           |
| **UI Elements**        | Streamlit Widgets       | Buttons, text inputs, radio buttons |
| **Session Management** | Streamlit Session State | Conversation history                |

### Supporting Tools

- **Python 3.11+** - Runtime environment
- **pip** - Package management
- **.env** - Environment variables (API keys)
- **Git** - Version control

---

## Project Structure

```
ChatBotPRO/
│
├── 📄 app.py                              # Main Streamlit application
├── 📄 build_kb.py                         # Knowledge base builder
├── 📄 rag_chatbot.py                      # RAG logic and LLM integration
├── 📄 inspect_db.py                       # Database inspection utility
│
├── 📄 requirements.txt                    # Python dependencies
├── 📄 README.md                           # User documentation
├── 📄 .env                                # API keys (not in git)
├── 📄 .gitignore                          # Git ignore rules
│
├── 📄 process_flow.txt                    # Process flow documentation
├── 📄 detailed_guide.txt                  # Comprehensive technical guide
├── 📄 storage_process_detailed_explanation.md  # Storage details
├── 📄 PROJECT_OVERVIEW.md                 # This file
├── 📄 CHROMADB_WORKFLOW.md               # ChromaDB detailed workflow
│
├── 📁 data/                               # Input documents directory
│   ├── *.pdf                              # PDF files
│   ├── *.jpg, *.png, *.jpeg              # Image files
│   └── *.pptx, *.ppt                      # PowerPoint files
│
├── 📁 chroma_db/                          # Vector database directory
│   ├── chroma.sqlite3                     # Database file
│   └── [collection folders]               # Vector data
│
└── 📁 __pycache__/                        # Python cache (auto-generated)
```

---

## Key Components

### 1. **build_kb.py** - Knowledge Base Builder

**Purpose**: Converts documents into a searchable vector database

**Process**:

```
Data Folder (PDFs, Images, PPTX)
         ↓
    File Discovery
         ↓
  ┌─────┴─────┬──────────┬──────────┐
  ▼           ▼          ▼          ▼
PDFs       Images    PowerPoint   Videos
  │           │          │          │
  ├─ Text ────┼─ OCR ────┼─ Parse ──┤
  │           │          │          │
  └─────┬─────┴──────────┴──────────┘
        ▼
  Text Chunking (800 chars, 150 overlap)
        ▼
  Add Metadata (source, page/slide)
        ▼
  Generate Embeddings (FastEmbed)
        ▼
  Store in ChromaDB
```

**Key Functions**:

- `load_all_pdfs()` - Extract text from PDF files
- `load_images()` - OCR text from images
- `load_slides()` - Extract text from PowerPoint
- `load_videos()` - Extract frames from videos
- `build_vector_db()` - Create and persist ChromaDB

---

### 2. **rag_chatbot.py** - RAG Logic Engine

**Purpose**: Implements the Retrieval-Augmented Generation pipeline

**Components**:

```
Question Input
      ↓
Convert to Embedding (FastEmbed)
      ↓
Search ChromaDB (Top 20 similar chunks)
      ↓
Format Retrieved Context
      ↓
Create RAG Prompt with Context + Question
      ↓
Send to Groq LLM (temperature=0)
      ↓
Parse Output as String
      ↓
Extract Citations from Retrieved Docs
      ↓
Return Answer + Citations
```

**Key Functions**:

- `ask(question)` - RAG-based query (strict, with citations)
- `general_ask(question)` - Direct LLM query (creative, may hallucinate)
- Embeddings setup with FastEmbedEmbeddings
- Vector store initialization with ChromaDB
- Retriever configuration (k=20 chunks)

---

### 3. **app.py** - Streamlit Web Interface

**Purpose**: User-friendly interactive interface

**Features**:

```
┌──────────────────────────────────────┐
│         STREAMLIT APP (app.py)       │
├──────────────────────────────────────┤
│                                      │
│  1. Mode Selection (Radio Button)   │
│     ├─ RAG Mode (knowledge base)    │
│     └─ General Mode (creative)      │
│                                      │
│  2. File Upload                      │
│     ├─ PDF Upload                   │
│     ├─ Image Upload (JPG/PNG)       │
│     └─ PowerPoint Upload            │
│                                      │
│  3. Question Input                   │
│     └─ Text Input Box               │
│                                      │
│  4. Processing & Display            │
│     ├─ Answer Display               │
│     ├─ Citations (if RAG)          │
│     └─ System Metrics               │
│         • Latency (response time)   │
│         • Citation Accuracy %       │
│                                      │
│  5. Conversation History            │
│     └─ Last 5 Q/A pairs            │
│                                      │
│  6. Clear History Button            │
│     └─ Reset conversation          │
│                                      │
└──────────────────────────────────────┘
```

**Key Features**:

- Real-time file upload processing
- Session state management for history
- Automatic citation filtering (data/ sources only)
- Performance metrics calculation
- FIFO history management (max 5 entries)

---

## How It Works

### Phase 1: Initial Knowledge Base Construction

1. **Document Discovery**: Scan `data/` folder for supported files
2. **Format-Specific Processing**:
   - **PDFs**: Extract text with page metadata
   - **Images**: Apply Tesseract OCR to extract text
   - **PowerPoints**: Parse slides for text content
3. **Text Chunking**: Split content into 800-character chunks with 150-character overlap
4. **Metadata Attachment**: Tag each chunk with source file and page/slide number
5. **Vectorization**: Convert chunks to dense vectors using FastEmbed
6. **Persistent Storage**: Save vectors and metadata in ChromaDB database

### Phase 2: Query Processing (RAG Mode)

1. **User Input**: User types a question in Streamlit
2. **Embedding Creation**: Convert question to vector using same FastEmbed model
3. **Similarity Search**: Query ChromaDB for top 20 most similar chunks
4. **Context Assembly**: Combine retrieved chunks into a context string
5. **LLM Prompt Creation**: Format prompt with context, question, and RAG rules
6. **Generation**: Send to Groq LLM for answer generation (temperature=0 for consistency)
7. **Citation Extraction**: Extract source metadata from retrieved chunks
8. **Filtering**: Remove duplicates and non-data/ sources
9. **Response Display**: Show answer, citations, and metrics

### Phase 3: Query Processing (General Mode)

1. **User Input**: User types a question
2. **Direct LLM Call**: Send question directly to Groq without retrieval
3. **Creative Response**: LLM generates answer using training knowledge
4. **Display**: Show answer without citations

### Phase 4: File Upload Processing

1. **File Reception**: User uploads a new document
2. **Format Detection**: Identify file type (PDF/image/PPTX)
3. **Content Extraction**: Parse content using appropriate method
4. **Chunking**: Split into 800-character chunks
5. **Vectorization**: Generate embeddings
6. **Database Addition**: Add new chunks to ChromaDB with metadata
7. **Citation Filtering**: Ensure new uploads don't appear in citations

### Phase 5: Session Management

1. **History Storage**: Q/A pairs stored in Streamlit session state
2. **FIFO Management**: Keep only last 5 interactions
3. **Manual Clear**: User can reset history with button
4. **Display**: Show conversation history below chat

---

## Data Flow Diagrams

### Complete System Data Flow

```
USER INTERACTION FLOW
════════════════════════════════════════════════════════════════════

                           USER ENTERS QUESTION
                                   │
                                   ▼
                          ┌────────────────┐
                          │ Question Input │
                          └────────┬───────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
            ┌──────────────┐            ┌──────────────┐
            │  RAG MODE    │            │ GENERAL MODE │
            └──────┬───────┘            └──────┬───────┘
                   │                           │
        ┌──────────┴──────────┐                │
        ▼                     ▼                │
  Generate Embedding   No Retrieval           │
        │                                     │
        ▼                                     │
  Search ChromaDB                             │
  (Top 20 chunks)                             │
        │                                     │
        ▼                                     │
  Format Context                              │
        │                                     │
        └──────────────┬──────────────────────┘
                       ▼
                Create RAG/General Prompt
                       │
                       ▼
                Send to Groq LLM
                (llama-3.1-8b-instant)
                       │
                       ▼
                Receive Generated Answer
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
    Extract Citations          No Citations
    (from retrieved docs)
        │
        ▼
    Filter Citations
    (data/ sources only)
        │
        ▼
    Remove Duplicates
        │
        └──────────────┬──────────────┐
                       ▼              ▼
                  Citations      No Citations
                       │
                       ▼
            DISPLAY ANSWER + CITATIONS
            + SYSTEM METRICS
                       │
                       ▼
            ADD TO CONVERSATION HISTORY
            (max 5 entries, FIFO)
                       │
                       ▼
                USER SEES RESULTS
```

### Knowledge Base Building Data Flow

```
DOCUMENT PROCESSING PIPELINE
════════════════════════════════════════════════════════════════════

DATA/ FOLDER
├── PDFs/
│   └── document.pdf
├── Images/
│   ├── screenshot.jpg
│   └── diagram.png
└── PowerPoint/
    └── presentation.pptx

        │
        ▼
    FILE DISCOVERY
        │
        ├─────────────┬────────────┬──────────┐
        ▼             ▼            ▼          ▼
      PDFs        Images      PowerPoint   Videos
        │             │            │          │
        ▼             ▼            ▼          ▼
    PyMuPDF      Tesseract    python-pptx  cv2
   (Text)          (OCR)       (Parse)     (Frames)
        │             │            │          │
        ▼             ▼            ▼          ▼
    Text +        Text +        Text +     Text +
    Metadata      Metadata      Metadata   Metadata
        │
        └────────────────┬──────────────────┘
                         ▼
            RECURSIVE TEXT SPLITTER
            • Chunk Size: 800 chars
            • Overlap: 150 chars
                         │
                         ▼
            CHUNKS WITH METADATA
            {
              page_content: "text...",
              metadata: {
                source: "document.pdf",
                page: 5
              }
            }
                         │
                         ▼
            FASTEMBED VECTORIZATION
            • Convert text to vectors
            • High-dimensional embeddings
                         │
                         ▼
            CHROMADB STORAGE
            • chroma_db/
            • Persistent storage
            • Indexing for fast retrieval
                         │
                         ▼
            READY FOR QUERIES
```

---

## Installation & Setup

### Prerequisites

```bash
# System Requirements
- Python 3.11+
- Tesseract OCR (for image processing)
- 2GB+ disk space (for ChromaDB)
- Internet connection (for Groq API)
```

### Step 1: Install Tesseract OCR

**Windows**:

```bash
winget install UB-Mannheim.TesseractOCR
# or download: https://github.com/UB-Mannheim/tesseract/wiki
```

**Linux**:

```bash
sudo apt-get install tesseract-ocr
```

**macOS**:

```bash
brew install tesseract
```

### Step 2: Clone/Setup Project

```bash
cd ChatbotPro
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Configure API Key

```bash
# Create .env file with:
GROQ_API_KEY=your_groq_api_key_here
```

Get API key from: https://console.groq.com/

### Step 6: Build Knowledge Base

```bash
# Place documents in data/ folder
python build_kb.py
# This creates chroma_db/ directory
```

### Step 7: Run Application

```bash
streamlit run app.py
# Opens at http://localhost:8501
```

---

## Usage Guide

### Basic Usage

1. **Place Documents**: Add PDF/image/PPTX files to `data/` folder
2. **Build KB**: Run `python build_kb.py`
3. **Launch App**: Run `streamlit run app.py`
4. **Ask Questions**: Type questions in the interface
5. **View Answers**: Read answers with citations and metrics

### RAG Mode (Recommended for Accuracy)

- Answers strictly from your documents
- Always shows source citations
- No hallucination
- Best for domain-specific questions

### General Mode (For Creative Answers)

- Uses LLM training knowledge
- May include external information
- No citations provided
- Best for general knowledge questions

### File Upload

- Upload additional PDFs, images, or PowerPoints
- Automatically processed and added to knowledge base
- Temporary processing (cleared after session)
- Not included in citations (optional feature)

---

## Features & Capabilities

### 🎯 Core Features

- ✅ Multi-modal document support (PDF, images, PowerPoint)
- ✅ Optical Character Recognition (OCR) for images
- ✅ Automatic text chunking with configurable overlap
- ✅ Vector-based semantic search (top-k retrieval)
- ✅ Dual operation modes (RAG and General)
- ✅ Source citations with page/slide references
- ✅ Conversation history tracking (last 5 Q/A)
- ✅ Real-time file upload processing
- ✅ Performance metrics (latency, citation accuracy)

### 📊 Advanced Features

- Multiple document format support
- Metadata preservation (page numbers, slide info)
- Duplicate citation filtering
- Session-based conversation history
- Citation accuracy scoring
- Configurable retrieval parameters
- Temperature control for LLM consistency

### 🔒 Safety Features

- Strict RAG mode prevents hallucination
- Source verification for all citations
- Filter to exclude uploaded file citations
- Configurable chunk size and overlap
- Error handling for file processing

### ⚡ Performance Features

- FastEmbed for high-speed vectorization
- ChromaDB for efficient similarity search
- Top-20 chunk retrieval (configurable)
- Groq API for fast LLM inference
- Streamlit for responsive UI
- Persistent database caching

---

## Configuration Options

### Chunking Parameters (in build_kb.py)

```python
RecursiveCharacterTextSplitter(
    chunk_size=800,      # Characters per chunk
    chunk_overlap=150    # Character overlap between chunks
)
```

### Retrieval Parameters (in rag_chatbot.py)

```python
retriever = vectordb.as_retriever(
    search_kwargs={"k": 20}  # Number of chunks to retrieve
)
```

### LLM Parameters (in rag_chatbot.py)

```python
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0  # 0 = deterministic, 1 = creative
)
```

---

## Troubleshooting

| Issue               | Solution                                              |
| ------------------- | ----------------------------------------------------- |
| Tesseract not found | Install Tesseract OCR and add to PATH                 |
| Module not found    | Run `pip install -r requirements.txt`                 |
| API key error       | Check `.env` file and Groq API key validity           |
| Empty answers       | Ensure knowledge base built with `python build_kb.py` |
| No citations        | Check that documents are in `data/` folder            |
| Slow performance    | Reduce retrieval k value or chunk size                |

---

## Summary

**ChatBotPRO** is a complete RAG system that:

1. 📚 Transforms documents into searchable knowledge base
2. 🔍 Uses vector similarity to find relevant information
3. 🧠 Leverages LLMs to generate natural language answers
4. 📝 Provides citations to verify answer sources
5. 💬 Offers interactive web interface for easy access

It combines the accuracy of document-based retrieval with the naturalness of LLM-generated responses, creating a powerful tool for document-based question answering.

---

**Created**: 2025-12-16
**Last Updated**: 2025-12-16
**Version**: 1.0
