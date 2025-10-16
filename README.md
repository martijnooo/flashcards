# 🧠 Flashcard Genius

**AI-Powered Learning • Smart Flashcards • Instant Knowledge**

Flashcard Genius is an intelligent study companion that transforms your documents into smart flashcards using advanced AI. Say goodbye to manual note-taking and hello to efficient, organized learning!

## 🚀 Features

### 🤖 AI-Powered Flashcard Generation
- **Instant Creation**: Upload any document and get flashcards in seconds
- **Smart Content Understanding**: AI identifies key concepts and creates structured Q&A pairs
- **Batch Processing**: Handles multiple documents with parallel processing
- **Structured Output**: Clean JSON format with categories and metadata

### 🔍 Intelligent Duplicate Detection
- **Vector Similarity Search**: Advanced AI compares new cards with existing ones
- **Smart Warnings**: Visual alerts for potential duplicates
- **Similarity Scoring**: Make informed decisions about what to save
- **Clean Knowledge Base**: Maintain an organized, non-redundant collection

### 📊 Advanced Analytics & Organization
- **Category Analysis**: Automatic organization by topics and subjects
- **K-means Clustering**: AI-powered grouping of related concepts
- **Learning Insights**: Visualize your knowledge distribution
- **Progress Tracking**: Monitor your learning journey

### ⚡ Smart Search & Retrieval
- **Semantic Search**: Find cards by meaning, not just keywords
- **Instant Results**: Lightning-fast vector similarity search
- **Context Understanding**: AI understands the intent behind your queries

## 🏗️ How It Works

### Technical Pipeline
'1. Upload → 2. Generate → 3. Compare → 4. Search


1. **📄 Upload** - Simple document upload interface
2. **⚡ Generate** - AI processes document chunks using LLM + Parallel Processing
3. **🔍 Compare** - Vector similarity search against existing cards using Pinecone
4. **🎯 Search** - Semantic search across your entire knowledge base

### Core Technology Stack

- **Frontend**: Streamlit for responsive web interface
- **AI/ML**: OpenAI GPT, LangChain for intelligent processing
- **Vector Database**: Pinecone for similarity search and storage
- **Backend**: Python with parallel processing capabilities
- **Embeddings**: Advanced text embedding models for semantic understanding

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- Pinecone API key

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flashcard-genius.git
   cd flashcard-genius

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt

3. **Set up environment variables**
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    PINECONE_API_KEY=your_pinecone_api_key

4. **Run the application**
streamlit run Home.py

### Project structure
```bash
    flashcard-genius/
    ├── Home.py                 # Main homepage and entry point
    ├── styles.css              # Comprehensive styling
    ├── pages/
    │   ├── 1_📤_Create_Flashcards.py    # Document upload & generation
    │   ├── 2_🔍_Search_Flashcards.py    # Smart search functionality
    │   └── 3_📊_Categorise.py           # Analytics & clustering
    ├── utils/
    │   ├── pinecone_utils.py   # Vector database operations
    │   ├── llm_utils.py        # AI model interactions
    │   ├── text_utils.py       # Text processing utilities
    │   └── __init__.py
    ├── dummy_data/database_population.py # Sample data for database
    └── requirements.txt        # Python dependencies
````

## 🎯 Usage Guide

### Creating Flashcards

1. **Navigate to Create Flashcards** from the homepage
2. **Upload a Word document** (.docx or .doc) with your study material
3. **Click Generate** and watch AI create flashcards in seconds
4. **Review each card** with answers and metadata
5. **Check for duplicates** using the smart detection system
6. **Save unique cards** to your personal knowledge base

### Searching Your Collection

1. **Go to Search Flashcards**
2. **Enter any query** - the AI understands semantic meaning
3. **Get instant results** with relevant flashcards
4. **Review answers** in the expandable sections

### Analyzing Your Knowledge

1. **Visit the Categorize page**
2. **View category distributions** and statistics
3. **Explore AI clustering** of your flashcards
4. **Discover learning patterns** and focus areas

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `PINECONE_API_KEY` | Your Pinecone API key | Yes |

## 🎓 Use Cases

### Perfect For:
- **Students** preparing for exams and courses
- **Professionals** learning new skills and technologies
- **Researchers** organizing knowledge and literature reviews
- **Lifelong Learners** building personal knowledge systems
- **Educators** creating teaching materials

### Supported Document Types:
- Microsoft Word (.docx, .doc)
