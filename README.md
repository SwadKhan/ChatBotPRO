# ChatBotPRO - Multi-Modal Retrieval-Augmented Generation (RAG) System

## Overview

ChatBotPRO is an advanced Retrieval-Augmented Generation (RAG) system that allows users to query and get answers from various document types including PDFs, images, and PowerPoint presentations. The system uses optical character recognition (OCR) for images, processes PowerPoint slides, and provides accurate, context-aware answers with citations using a Large Language Model.

### Key Features

- **Multi-Modal Support**: Process PDFs, images (JPG/PNG), and PowerPoint files (PPTX/PPT)
- **OCR Integration**: Extract text from images using Tesseract OCR
- **Vector Database**: Uses ChromaDB with FastEmbed embeddings for efficient retrieval
- **Dual Mode Operation**: Choose between strict RAG (from knowledge base only) or general answers (may hallucinate)
- **Conversation History**: Stores last 5 Q/A pairs with citations
- **Citation Filtering**: Shows only sources from pre-processed data, not uploaded files
- **Web Interface**: User-friendly Streamlit app for uploading files and asking questions
- **Citations**: Provides source references for RAG answers

## Technologies Used

- **Python 3.11**
- **LangChain** - Framework for building LLM applications
- **ChromaDB** - Vector database for embeddings
- **FastEmbed** - High-performance embeddings
- **Groq LLM** - LLaMA 3.1 8B model for generation
- **Streamlit** - Web interface
- **Tesseract OCR** - Optical character recognition
- **python-pptx** - PowerPoint file processing
- **PyMuPDF** - PDF text extraction

All library versions are specified in `requirements.txt`.

## Project Structure

```
ChatBotPRO/
├── app.py                 # Streamlit web interface
├── build_kb.py           # Knowledge base builder
├── rag_chatbot.py        # RAG chatbot logic
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── .env                 # Environment variables (API keys)
├── data/                # Folder for document files
│   ├── *.pdf
│   ├── *.jpg/*.png
│   └── *.pptx/*.ppt
├── chroma_db/           # Vector database storage
└── __pycache__/         # Python cache
```

## Installation

### Prerequisites

1. **Python 3.11** or higher
2. **Tesseract OCR** (for image/video processing)

### Install Tesseract OCR

On Windows:

```bash
winget install UB-Mannheim.TesseractOCR
```

Or download from: https://github.com/UB-Mannheim/tesseract/wiki

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Set Up API Key

1. Create a `.env` file in the project root
2. Add your Groq API key:

```
GROQ_API_KEY=your_actual_groq_api_key_here
```

Get your API key from [Groq Console](https://console.groq.com/).

## Usage

### 1. Prepare Documents

Place your files in the `data/` folder:

- **PDFs**: Research papers, textbooks, documents
- **Images**: Screenshots, diagrams, scanned documents
- **PowerPoint**: Presentations, slides

### 2. Build Knowledge Base

After adding files, build the vector database:

```bash
python build_kb.py
```

This will process all files, extract text, create embeddings, and store them in ChromaDB.

### 3. Run the Chatbot

#### Command Line Interface

```bash
python rag_chatbot.py
```

#### Web Interface (Recommended)

```bash
streamlit run app.py
```

### 4. Using the Web App

1. Open the Streamlit app in your browser
2. Select mode: "RAG (strictly from knowledge base)" for answers from your documents, or "General (may hallucinate)" for broader responses
3. Upload additional files using the file uploader (supports PDFs, images, PowerPoint) - these are processed temporarily
4. Ask questions in the text box
5. Get answers with citations (RAG mode only, from pre-processed data)
6. View conversation history (last 5 interactions)
7. Use "Clear Conversation History" to reset history

## File Processing Details

### PDFs

- Text extraction using PyMuPDF
- Split into 800-character chunks with 150-character overlap

### Images

- OCR using Tesseract
- Supports JPG, PNG, JPEG formats
- Full image text extraction

### PowerPoint Files

- Extracts text from all slides
- Supports PPTX and PPT formats
- Citations include slide numbers

## How It Works

1. **Document Processing**: Files are loaded and text is extracted
2. **Chunking**: Text is split into manageable pieces
3. **Embedding**: FastEmbed creates vector representations
4. **Storage**: Vectors stored in ChromaDB
5. **Query Processing**: User questions are embedded and matched
6. **Retrieval**: Most relevant chunks retrieved using multi-query approach
7. **Generation**: LLM generates answers using retrieved context
8. **Citation**: Sources are tracked and displayed

## Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)

### Chunking Parameters (in build_kb.py)

- `chunk_size`: 800 characters
- `chunk_overlap`: 150 characters

### Video Processing (in build_kb.py)

- `frame_interval`: Sample every 30 seconds

## Troubleshooting

### Common Issues

**Tesseract not found**

- Ensure Tesseract is installed and in PATH
- Restart your terminal/IDE after installation

**Import errors**

- Run `pip install -r requirements.txt`
- Check Python version compatibility

**No answers from chatbot**

- Ensure `.env` file exists with valid API key
- Check internet connection for Groq API

**Video processing slow**

- Videos are processed frame-by-frame
- Consider shorter videos or adjust frame_interval

### Performance Tips

- Use smaller chunk sizes for more precise retrieval
- Limit video length for faster processing
- Clear chroma_db/ folder if rebuilding from scratch

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open-source. Please check individual library licenses for usage restrictions.

## Support

For issues or questions:

1. Check the troubleshooting section
2. Review error messages in terminal
3. Ensure all prerequisites are installed
4. Verify file formats are supported

---

**Built with ❤️ using LangChain, ChromaDB, and Groq**
