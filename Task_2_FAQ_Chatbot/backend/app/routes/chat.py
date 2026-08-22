from fastapi import APIRouter, HTTPException, status
from ..models import ChatRequest, ChatResponse, ErrorResponse
from ..services import FAQMatcher
from ..config import settings
import os

router = APIRouter()

faq_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faqs.json')
faq_matcher = None


def get_faq_matcher():
    global faq_matcher
    if faq_matcher is None:
        faq_matcher = FAQMatcher(faq_data_path)
    return faq_matcher


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest):
    try:
        if len(request.question) > settings.max_question_length:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question exceeds maximum length of {settings.max_question_length} characters"
            )
        
        matcher = get_faq_matcher()
        result = matcher.match_question(request.question)
        
        return ChatResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )
