import axios from 'axios';
import { TranslationResult } from './mymemoryProvider.js';

export async function translateWithLibre(
  text: string,
  sourceLang: string,
  targetLang: string,
  baseUrl: string,
  apiKey?: string
): Promise<TranslationResult> {
  const url = `${baseUrl.replace(/\/$/, '')}/translate`;

  const body: Record<string, any> = {
    q: text,
    source: sourceLang === 'auto' ? 'auto' : sourceLang,
    target: targetLang,
    format: 'text',
  };

  if (apiKey) {
    body.api_key = apiKey;
  }

  const response = await axios.post(url, body, {
    headers: { 'Content-Type': 'application/json' },
    timeout: 10000,
  });

  if (response.data && response.data.translatedText) {
    return {
      translatedText: response.data.translatedText,
      detectedSourceLanguage: response.data.detectedLanguage?.language || sourceLang,
      provider: 'LibreTranslate',
    };
  }

  throw new Error('Unexpected response from LibreTranslate API.');
}
