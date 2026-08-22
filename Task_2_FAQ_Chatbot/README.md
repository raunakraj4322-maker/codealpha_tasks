# AI Learning Platform FAQ Chatbot

**CodeAlpha Artificial Intelligence Internship - Task 2**

A production-style FAQ chatbot that uses Natural Language Processing (NLP) to provide intelligent responses to user questions about a fictional AI Learning Platform. The system employs TF-IDF vectorization and cosine similarity to match user queries with the most relevant FAQ entries.

## 🎯 Project Overview

This project demonstrates practical NLP techniques for building an intelligent FAQ chatbot without relying on paid LLM APIs. The chatbot preprocesses text, vectorizes questions using TF-IDF, and calculates cosine similarity to find the best matching FAQ answers. It includes a modern React frontend and a FastAPI backend with proper error handling and security measures.

## ✨ Features

- **NLP-Powered Matching**: Uses TF-IDF vectorization and cosine similarity for intelligent FAQ matching
- **Confidence Thresholding**: Returns fallback responses when similarity scores are below threshold
- **Modern Chat UI**: Professional, responsive chat interface with message bubbles and loading states
- **Suggested Questions**: Quick-start suggested questions for common queries
- **Real-time Feedback**: Shows confidence scores and matched questions for transparency
- **Input Validation**: Comprehensive validation and error handling
- **CORS Configuration**: Proper cross-origin resource sharing setup
- **Security Best Practices**: Input sanitization, rate limiting considerations, and no exposed secrets

## 🧠 NLP Approach

### Text Preprocessing Pipeline

1. **Lowercase Conversion**: Normalizes text to lowercase
2. **Punctuation Removal**: Removes unnecessary punctuation and special characters
3. **Number Removal**: Eliminates digits to focus on semantic content
4. **Tokenization**: Splits text into individual words using NLTK
5. **Stopword Removal**: Removes common words (the, a, an, etc.) using NLTK's English stopwords
6. **Lemmatization**: Reduces words to their base form using WordNet lemmatizer
7. **Text Normalization**: Cleans whitespace and standardizes format

### TF-IDF Vectorization

- **Term Frequency-Inverse Document Frequency (TF-IDF)**: Converts text to numerical vectors
- **N-gram Range**: Uses both unigrams and bigrams (1-2 grams) for better context
- **Max Features**: Limits to 1000 most important features to reduce dimensionality
- **Stopword Filtering**: Additional English stopword filtering during vectorization
- **Min/Max Document Frequency**: Filters out very rare and very common terms

### Cosine Similarity

- Calculates similarity between user question vector and FAQ question vectors
- Returns values between 0 (no similarity) and 1 (identical)
- Selects the FAQ with highest similarity score
- Applies configurable confidence threshold (default: 0.25)

### Confidence Threshold

The system uses a configurable similarity threshold (`SIMILARITY_THRESHOLD=0.25`):

- **Above threshold**: Returns the matched FAQ with confidence score
- **Below threshold**: Returns a friendly fallback response suggesting rephrasing
- Prevents returning irrelevant or random answers

## 📊 Dataset Information

- **Total FAQ Entries**: 55 comprehensive questions
- **Categories**: Courses, Enrollment, Pricing, Certificates, Payments, Account, Technical Support, Assignments, Projects, Career, Internship
- **Format**: Structured JSON with id, question, answer, and category fields
- **Location**: `backend/app/data/faqs.json`
- **Content**: Realistic questions about AI Learning Platform services

Example FAQ structure:
```json
{
  "id": 1,
  "question": "What courses are available on the platform?",
  "answer": "We offer a wide range of courses including...",
  "category": "Courses"
}
```

## 🛠 Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **FastAPI**: Modern, fast web framework for building APIs
- **NLTK**: Natural language processing library for text preprocessing
- **scikit-learn**: Machine learning library for TF-IDF and cosine similarity
- **NumPy**: Numerical computing for vector operations
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI

### Frontend
- **React 18**: UI library for building user interfaces
- **TypeScript**: Type-safe JavaScript for better code quality
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework for styling
- **Lucide React**: Beautiful icon library

## 🏗 Architecture

```
Task_2_FAQ_Chatbot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py            # Configuration settings
│   │   ├── routes/              # API route handlers
│   │   │   ├── chat.py          # Chat endpoint
│   │   │   ├── health.py        # Health check endpoint
│   │   │   └── faqs.py          # FAQ listing endpoint
│   │   ├── services/            # Business logic
│   │   │   ├── nlp_processor.py # Text preprocessing
│   │   │   └── faq_matcher.py   # FAQ matching logic
│   │   ├── models/              # Pydantic models
│   │   │   └── __init__.py      # Request/response models
│   │   └── data/                # Data files
│   │       └── faqs.json        # FAQ dataset
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Chat.tsx         # Main chat interface
│   │   │   ├── ChatMessage.tsx  # Message bubble component
│   │   │   ├── ChatInput.tsx    # Input component
│   │   │   └── SuggestedQuestions.tsx
│   │   ├── services/            # API service layer
│   │   │   └── api.ts           # API calls
│   │   ├── types/               # TypeScript types
│   │   │   └── index.ts         # Type definitions
│   │   ├── App.tsx              # Root component
│   │   ├── main.tsx             # Entry point
│   │   └── index.css            # Global styles
│   ├── public/                  # Static assets
│   ├── package.json             # Node dependencies
│   ├── vite.config.ts           # Vite configuration
│   ├── tsconfig.json            # TypeScript config
│   └── tailwind.config.js       # Tailwind CSS config
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. The NLTK data will be downloaded automatically on first run.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## 🏃 Running the Project

### Start Backend

1. With virtual environment activated:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. The backend will start at `http://localhost:8000`

### Start Frontend

1. In a new terminal:
```bash
cd frontend
npm run dev
```

2. The frontend will start at `http://localhost:5173`

### Access the Application

Open your browser and navigate to `http://localhost:5173`

## 📡 API Endpoints

### Health Check
- **Endpoint**: `GET /api/health`
- **Description**: Check if the API is running
- **Response**:
```json
{
  "status": "healthy",
  "app_name": "AI Learning Platform FAQ Chatbot",
  "version": "1.0.0"
}
```

### Get All FAQs
- **Endpoint**: `GET /api/faqs`
- **Description**: Retrieve all FAQ entries
- **Response**: Array of FAQ objects with id, question, answer, and category

### Chat
- **Endpoint**: `POST /api/chat`
- **Description**: Send a question and get a matched FAQ answer
- **Request Body**:
```json
{
  "question": "How long does a course take?"
}
```
- **Response**:
```json
{
  "answer": "Course duration depends on the selected course...",
  "matched_question": "How long do courses take?",
  "confidence": 0.82,
  "category": "Courses",
  "faq_id": 5
}
```

## 🧪 Testing

### Backend API Testing

Test the health endpoint:
```bash
curl http://localhost:8000/api/health
```

Test the chat endpoint:
```bash
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"question\": \"How long do courses take?\"}"
```

Test with empty question (should return error):
```bash
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" -d "{\"question\": \"\"}"
```

### Frontend Testing

1. Open the application at `http://localhost:5173`
2. Try suggested questions
3. Type custom questions
4. Test edge cases (empty input, very long questions)
5. Verify confidence scores display correctly
6. Check fallback responses for unrelated questions

## 🔒 Security Considerations

- **Input Validation**: All inputs are validated for length and content
- **Request Size Limits**: Maximum question length enforced (500 characters)
- **CORS Configuration**: Restricts cross-origin requests to approved origins
- **Safe JSON Parsing**: Proper error handling for malformed JSON
- **No Arbitrary Code Execution**: User input never executed as code
- **No Shell Command Execution**: No system calls from user input
- **No Secrets in Source Code**: No API keys or credentials in code
- **Proper Exception Handling**: Errors caught and handled gracefully
- **No Stack Trace Exposure**: Internal errors not exposed to users
- **No Filesystem Path Exposure**: Internal paths not revealed
- **Privacy Focused**: No personal information collection

## ⚠️ Limitations

- **Local NLP Only**: Uses TF-IDF similarity, not generative AI
- **Fixed FAQ Database**: Can only answer questions present in the FAQ dataset
- **No Context Memory**: Each question is processed independently
- **English Only**: Currently optimized for English language
- **Similarity-Based**: May not handle complex multi-part questions well
- **Threshold Dependent**: Quality depends on similarity threshold tuning

## 🚀 Future Improvements

- **Word Embeddings**: Use Word2Vec or BERT for better semantic understanding
- **Context Awareness**: Implement conversation context and memory
- **Multi-language Support**: Add support for other languages
- **Machine Learning**: Train custom models for better matching
- **Database Integration**: Store FAQs in a database for dynamic updates
- **User Analytics**: Track common questions for FAQ improvement
- **Admin Dashboard**: Interface for managing FAQ content
- **Advanced NLP**: Add named entity recognition and intent classification
- **A/B Testing**: Test different similarity thresholds and approaches

## 📄 License

This project is created as part of the CodeAlpha Artificial Intelligence Internship and is intended for educational purposes.

## 🙏 Acknowledgments

- **CodeAlpha**: For the internship opportunity and project guidance
- **NLTK Team**: For the excellent NLP library
- **scikit-learn Team**: For the machine learning tools
- **FastAPI Team**: For the modern web framework
- **React Community**: For the amazing UI library

---

**Note**: This is a fictional AI Learning Platform created for educational purposes as part of the CodeAlpha internship. It is not associated with any real company or service.
