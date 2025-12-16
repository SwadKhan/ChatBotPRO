# ChatBotPRO - Quick Reference Guide

## 🚀 Quick Start (5 minutes)

### 1. Install & Setup

```bash
# Install Tesseract OCR (Windows)
winget install UB-Mannheim.TesseractOCR

# Install Python packages
pip install -r requirements.txt

# Create .env with API key
echo GROQ_API_KEY=your_key > .env
```

### 2. Build Knowledge Base

```bash
# Place documents in data/ folder
python build_kb.py
```

### 3. Run Application

```bash
streamlit run app.py
# Opens at http://localhost:8501
```

---

## 📋 File Guide

| File               | Purpose                     | Usage                             |
| ------------------ | --------------------------- | --------------------------------- |
| `app.py`           | Main web interface          | `streamlit run app.py`            |
| `build_kb.py`      | Build vector database       | `python build_kb.py`              |
| `rag_chatbot.py`   | RAG logic & LLM integration | Imported by app.py                |
| `inspect_db.py`    | Database inspection         | `python inspect_db.py`            |
| `requirements.txt` | Dependencies                | `pip install -r requirements.txt` |
| `.env`             | API keys (create it)        | Contains GROQ_API_KEY             |
| `data/`            | Document storage            | Place PDFs, images, PPT here      |
| `chroma_db/`       | Vector database             | Auto-created by build_kb.py       |

---

## 🎯 How It Works (Simple View)

```
Documents → Text Extraction → Chunking → Embeddings → ChromaDB
                                                           ↓
User Question → Embedding → Search → Context + LLM → Answer + Citations
```

### RAG Mode vs General Mode

| Aspect            | RAG Mode            | General Mode      |
| ----------------- | ------------------- | ----------------- |
| **Source**        | Only from documents | LLM training data |
| **Hallucination** | No (strict rules)   | Possible          |
| **Citations**     | Yes (with page #)   | No                |
| **Best for**      | Domain questions    | General knowledge |

---

## 🔧 Configuration

### Chunk Size & Overlap (in build_kb.py)

```python
chunk_size=800        # Larger = more context, fewer chunks
chunk_overlap=150     # Overlap ensures continuity
```

### Retrieval Count (in rag_chatbot.py)

```python
search_kwargs={"k": 20}  # 20 = balanced, increase for better recall
```

### LLM Settings (in rag_chatbot.py)

```python
temperature=0  # 0 = consistent, 1 = creative
model="llama-3.1-8b-instant"
```

---

## 📊 Key Concepts

### Embeddings

- **What**: Numbers representing text meaning
- **Size**: 384 dimensions (FastEmbed)
- **Use**: Find similar documents via vector math
- **Speed**: ~50ms to generate

### ChromaDB

- **What**: Vector database storing embeddings
- **Where**: `chroma_db/` folder
- **Contains**: 384-dim vectors + metadata (source, page)
- **Index**: HNSW (Hierarchical Navigable Small World)

### RAG (Retrieval-Augmented Generation)

- **Retrieval**: Find relevant document chunks
- **Augmentation**: Use as context for LLM
- **Generation**: LLM generates answer from context
- **Benefit**: No hallucination, answers from your data

### HNSW Index

- **What**: Algorithm for fast nearest neighbor search
- **Speed**: O(log N) instead of O(N)
- **Meaning**: Find top 20 similar chunks in milliseconds

---

## 🐛 Common Issues & Fixes

### "Tesseract not found"

```bash
# Windows: Install via winget
winget install UB-Mannheim.TesseractOCR

# Verify installation
tesseract --version
```

### "No module named 'langchain'"

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "GROQ_API_KEY not set"

```bash
# Create .env file
GROQ_API_KEY=sk_your_actual_key_here

# In code, verify:
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
```

### "chroma_db not found"

```bash
# Must build KB first
python build_kb.py

# Check folder was created
ls chroma_db/
```

### Empty answers in RAG mode

- **Check**: Knowledge base has documents
- **Check**: Documents are in `data/` folder
- **Check**: API key is valid
- **Try**: Rebuild KB with `python build_kb.py`

### Slow performance

- **Reduce**: k value from 20 to 10
- **Reduce**: chunk_size from 800 to 500
- **Limit**: Document count in data/
- **Monitor**: API latency to Groq

---

## 📚 Document Support

### Supported Formats

| Type           | Extension         | Processing                        |
| -------------- | ----------------- | --------------------------------- |
| **PDF**        | .pdf              | Text extraction + page numbers    |
| **Images**     | .jpg, .png, .jpeg | OCR (Tesseract) + text extraction |
| **PowerPoint** | .pptx, .ppt       | Slide parsing + text extraction   |
| **Videos**     | .mp4, .avi, .mov  | Frame extraction + OCR (optional) |

### How Each is Processed

**PDFs**:

- Use PyMuPDF to extract text with page metadata
- Chunk into 800-char pieces (preserve page info)
- Ready for retrieval with "page X" citations

**Images**:

- Use PIL to load image
- Use Tesseract to perform OCR
- Extract visible text from image
- Citations show "from image" (no page #)

**PowerPoint**:

- Use python-pptx to load presentation
- Iterate through slides
- Extract text from shapes
- Citations show "Slide X"

---

## 💾 Database Management

### Check Database Contents

```bash
python inspect_db.py
```

### Get Database Statistics

```python
from rag_chatbot import vectordb
count = vectordb._collection.count()
print(f"Total chunks: {count}")
```

### Clear Database (Start Fresh)

```bash
# Delete the folder
rm -r chroma_db/

# Rebuild
python build_kb.py
```

### Backup Database

```bash
# Copy folder to backup location
cp -r chroma_db/ backup_chroma_db_date/
```

---

## 🎨 Customization Examples

### Change Chunk Size (More detailed chunks)

```python
# In build_kb.py, line ~25
RecursiveCharacterTextSplitter(
    chunk_size=600,      # Smaller = more granular
    chunk_overlap=100    # Adjust accordingly
)
```

### Increase Retrieval Count (Better context)

```python
# In rag_chatbot.py, line ~20
retriever = vectordb.as_retriever(
    search_kwargs={"k": 30}  # More chunks = better recall
)
```

### Change Temperature (More creative)

```python
# In rag_chatbot.py, line ~26
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7  # 0.7 = more creative, less consistent
)
```

### Custom RAG Prompt

```python
# In rag_chatbot.py, line ~32
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""Your custom template here

    Context: {context}
    Question: {question}
    Answer:"""
)
```

---

## 📊 Performance Metrics

### Typical Latency Breakdown

```
Embedding generation:    ~50ms
ChromaDB retrieval:      ~10ms
Context assembly:        ~5ms
LLM inference:           ~1000ms
Response parsing:        ~50ms
─────────────────────────────
Total:                   ~1.1 seconds
```

### System Requirements

- **Python**: 3.11+
- **Memory**: 2GB RAM minimum (4GB+ recommended)
- **Disk**: 2GB for vector database (with 10K chunks)
- **Network**: Internet for Groq API calls

### Scalability

| Metric                | Capacity     |
| --------------------- | ------------ |
| Max chunks            | 100,000+     |
| Typical chunks        | 5,000-20,000 |
| Query time            | <2 seconds   |
| Memory per 10K chunks | ~100-200MB   |

---

## 🔐 Security & Privacy

### API Key Management

```bash
# .env file - NEVER commit to git
GROQ_API_KEY=sk_your_key_here

# .gitignore - add this line
.env

# Verify it's in .gitignore
cat .gitignore
```

### Data Privacy

- ✅ Documents stay local in `data/` folder
- ✅ Vector database stays local in `chroma_db/`
- ⚠️ Questions are sent to Groq API (read their privacy policy)
- ✅ No data shared with other services

### Best Practices

1. Use strong API key (never hardcode)
2. Keep `.env` in `.gitignore`
3. Rotate API keys periodically
4. Review Groq's data retention policy
5. Don't upload sensitive/private documents

---

## 🚦 Workflow Examples

### Example 1: Add New PDF and Query

```bash
# 1. Place PDF in data/
cp my_document.pdf data/

# 2. Rebuild knowledge base
python build_kb.py

# 3. Launch app (or already running)
streamlit run app.py

# 4. Ask question
# (App automatically searches new PDF)
```

### Example 2: Use General Mode

```
1. Open Streamlit app
2. Select "General (may hallucinate)" mode
3. Ask any question
4. Get answer from LLM training (no citations)
```

### Example 3: Upload Temporary Document

```
1. Open app (RAG mode)
2. Click "Upload PDF, JPG, PNG, PPTX"
3. Select file to upload
4. Wait for processing
5. Ask question - can reference uploaded content
6. Note: Uploaded file won't appear in citations (filtered)
```

### Example 4: Review Conversation History

```
1. Ask several questions
2. Scroll down to "Conversation History"
3. See last 5 Q/A pairs with citations
4. Click "Clear Conversation History" to reset
```

---

## 🔍 Debugging Tips

### Enable Verbose Logging

```python
# Add to app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test RAG Directly

```python
from rag_chatbot import ask
answer, citations = ask("Your question?", return_data=True)
print(f"Answer: {answer}")
print(f"Citations: {citations}")
```

### Check Retrieval Quality

```python
from rag_chatbot import retriever
docs = retriever.invoke("Your question?")
for i, doc in enumerate(docs[:5]):
    print(f"\n{i+1}. Source: {doc.metadata.get('source')}")
    print(f"   Content: {doc.page_content[:200]}...")
```

### Monitor Database Size

```bash
# Check folder size
du -sh chroma_db/

# Count files
find chroma_db/ -type f | wc -l
```

---

## 📝 Common Task Checklist

### Setting Up First Time

- [ ] Install Tesseract OCR
- [ ] Create virtual environment
- [ ] Install requirements.txt
- [ ] Create .env with API key
- [ ] Place documents in data/
- [ ] Run build_kb.py
- [ ] Run streamlit run app.py
- [ ] Test with sample question

### Adding New Documents

- [ ] Copy files to data/
- [ ] Run python build_kb.py
- [ ] (App already running) - will search new docs
- [ ] Or: Upload via UI (temporary)

### Regular Maintenance

- [ ] Backup chroma_db/ periodically
- [ ] Monitor API usage/costs
- [ ] Update dependencies monthly
- [ ] Clean old conversation history
- [ ] Archive old data/

### Troubleshooting

- [ ] Check .env file exists
- [ ] Check chroma_db/ exists
- [ ] Verify API key validity
- [ ] Run build_kb.py if errors
- [ ] Check error logs
- [ ] Test with simple question first

---

## 📞 Getting Help

### Check These First

1. **README.md** - User documentation
2. **PROJECT_OVERVIEW.md** - Architecture overview
3. **CHROMADB_WORKFLOW.md** - Detailed data flow
4. **FLOWCHARTS_AND_DIAGRAMS.md** - Visual guides
5. **This file** - Quick reference

### Common Documentation Links

- FastEmbed: https://qdrant.github.io/fastembed/
- ChromaDB: https://docs.trychroma.com/
- LangChain: https://python.langchain.com/
- Groq API: https://console.groq.com/

### Debug Process

1. Check error message in console
2. Verify prerequisites (Tesseract, Python version)
3. Check .env file exists and has valid key
4. Check data/ folder has documents
5. Check chroma_db/ folder exists
6. Try rebuilding KB: `python build_kb.py`
7. Restart Streamlit: Ctrl+C then `streamlit run app.py`

---

## 🎓 Learning Path

### Beginner (1-2 hours)

1. Read PROJECT_OVERVIEW.md (How it Works section)
2. Run through Quick Start
3. Try RAG mode with built-in documents
4. Explore conversation history

### Intermediate (2-4 hours)

1. Read CHROMADB_WORKFLOW.md
2. Add your own documents
3. Try both RAG and General modes
4. Monitor system metrics
5. Customize chunk size

### Advanced (4+ hours)

1. Study FLOWCHARTS_AND_DIAGRAMS.md
2. Understand vector embeddings
3. Learn HNSW algorithm
4. Modify LLM prompts
5. Implement caching strategies

---

## 🏁 Summary

**ChatBotPRO is**:

- A document-based question answering system
- Using vector similarity (embeddings) to find relevant info
- Using LLMs to generate natural language answers
- Showing source citations for verification
- Supporting PDFs, images, and PowerPoints

**Key files**:

- `build_kb.py` - Creates database
- `app.py` - User interface
- `rag_chatbot.py` - RAG logic
- `data/` - Your documents
- `chroma_db/` - Vector database

**Quick operations**:

- Build KB: `python build_kb.py`
- Run app: `streamlit run app.py`
- Fix issues: Check .env, rebuild KB, restart app

---

**Created**: 2025-12-16
**Version**: 1.0
**Last Updated**: 2025-12-16
