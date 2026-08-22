export interface Language {
  code: string;
  name: string;
  nativeName?: string;
  flag?: string;
  bcp47?: string; // Language tag for Web Speech API
}

export interface TranslationRequest {
  text: string;
  sourceLanguage: string;
  targetLanguage: string;
}

export interface TranslationResponse {
  translatedText: string;
  sourceLanguage: string;
  targetLanguage: string;
  provider: string;
  timestamp: string;
}

export interface HistoryItem {
  id: string;
  sourceText: string;
  translatedText: string;
  sourceLanguage: string;
  targetLanguage: string;
  timestamp: number;
}

export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'info';
  message: string;
}

export interface ServerHealth {
  status: string;
  service: string;
  activeProvider: string;
  timestamp: string;
}
