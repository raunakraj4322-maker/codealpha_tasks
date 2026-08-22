import axios from 'axios';
import { TranslationResult } from './mymemoryProvider.js';

export async function translateWithAzure(
  text: string,
  sourceLang: string,
  targetLang: string,
  apiKey: string,
  region: string = 'global'
): Promise<TranslationResult> {
  if (!apiKey) {
    throw new Error('Azure Translator key is missing in environment variables.');
  }

  let url = `https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=${encodeURIComponent(targetLang)}`;
  if (sourceLang !== 'auto') {
    url += `&from=${encodeURIComponent(sourceLang)}`;
  }

  const response = await axios.post(
    url,
    [{ Text: text }],
    {
      headers: {
        'Ocp-Apim-Subscription-Key': apiKey,
        'Ocp-Apim-Subscription-Region': region,
        'Content-Type': 'application/json',
      },
      timeout: 10000,
    }
  );

  if (Array.isArray(response.data) && response.data.length > 0) {
    const item = response.data[0];
    const translation = item.translations?.[0]?.text;
    const detectedLang = item.detectedLanguage?.language;

    return {
      translatedText: translation || text,
      detectedSourceLanguage: detectedLang || sourceLang,
      provider: 'Microsoft Azure Translator',
    };
  }

  throw new Error('Unexpected response structure from Azure Translator API.');
}
