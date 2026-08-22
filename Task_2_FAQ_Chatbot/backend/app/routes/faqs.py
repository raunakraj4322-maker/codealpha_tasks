from fastapi import APIRouter
from typing import List
from ..models import FAQItem
from ..services import FAQMatcher
import os

router = APIRouter()

faq_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'faqs.json')
faq_matcher = None


def get_faq_matcher():
    global faq_matcher
    if faq_matcher is None:
        faq_matcher = FAQMatcher(faq_data_path)
    return faq_matcher


@router.get("/faqs", response_model=List[FAQItem])
async def get_faqs():
    matcher = get_faq_matcher()
    return matcher.get_all_faqs()
