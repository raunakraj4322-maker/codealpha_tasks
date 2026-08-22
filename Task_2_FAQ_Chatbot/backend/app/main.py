from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import chat_router, health_router, faqs_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="FAQ Chatbot API using NLP and TF-IDF similarity matching"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])
app.include_router(faqs_router, prefix="/api", tags=["FAQs"])


@app.get("/")
async def root():
    return {
        "message": "AI Learning Platform FAQ Chatbot API",
        "version": settings.app_version,
        "endpoints": {
            "health": "/api/health",
            "chat": "/api/chat",
            "faqs": "/api/faqs"
        }
    }
