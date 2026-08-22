export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  confidence?: number;
  matchedQuestion?: string;
  category?: string;
}

export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
  matched_question?: string;
  confidence: number;
  category?: string;
  faq_id?: number;
}

export interface FAQItem {
  id: number;
  question: string;
  answer: string;
  category: string;
}

export interface HealthResponse {
  status: string;
  app_name: string;
  version: string;
}
