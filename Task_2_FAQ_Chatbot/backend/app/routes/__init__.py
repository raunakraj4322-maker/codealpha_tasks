from .chat import router as chat_router
from .health import router as health_router
from .faqs import router as faqs_router

__all__ = ['chat_router', 'health_router', 'faqs_router']
