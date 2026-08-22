class Settings:
    app_name: str = "AI Learning Platform FAQ Chatbot"
    app_version: str = "1.0.0"
    similarity_threshold: float = 0.25
    max_question_length: int = 500
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
