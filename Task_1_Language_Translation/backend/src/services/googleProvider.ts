import axios from 'axios';
import { TranslationResult } from './mymemoryProvider.js';

export async function translateWithGoogle(
  text: string,
  sourceLang: string,
  targetLang: string,
  apiKey: string
): Promise<TranslationResult> {
  if (!apiKey) {
    throw new Error('Google Translate API key is missing in environment variables.');
  }

  const url = `https://translation.googleapis.com/language/translate/v2?key=${encodeURIComponent(apiKey)}`;

  const body: Record<string, any> = {
    q: text,
    target: targetLang,
    format: 'text',
  };

  if (sourceLang !== 'auto') {
    body.source = sourceLang;
  }

  const response = await axios.post(url, body, {
    headers: { 'Content-Type': 'application/json' },
    timeout: 10000,
  });

  if (response.data && response.data.data && response.data.data.translations?.length > 0) {
    const item = response.data.data.translations[0];
    return {
      translatedText: item.translatedText,
      detectedSourceLanguage: item.detectedSourceLanguage || sourceLang,
      provider: 'Google Cloud Translate',
    };
  }

  throw new Error('Unexpected response format from Google Translate API.');
}
