import axios from 'axios';

export interface TranslationResult {
  translatedText: string;
  detectedSourceLanguage?: string;
  provider: string;
}

export async function translateWithMyMemory(
  text: string,
  sourceLang: string,
  targetLang: string
): Promise<TranslationResult> {
  const langPair = sourceLang === 'auto' ? `autodetect|${targetLang}` : `${sourceLang}|${targetLang}`;
  
  const url = 'https://api.mymemory.translated.net/get';

  const response = await axios.get(url, {
    params: {
      q: text,
      langpair: langPair,
    },
    timeout: 10000,
  });

  if (response.data && response.data.responseData) {
    const translatedText = response.data.responseData.translatedText;
    const detectedLang = response.data.responseData.detectedLanguage;

    if (response.data.responseStatus === 403 || response.data.responseStatus === 429) {
      throw new Error('MyMemory API quota or rate limit exceeded.');
    }

    return {
      translatedText: translatedText || text,
      detectedSourceLanguage: detectedLang || (sourceLang !== 'auto' ? sourceLang : 'en'),
      provider: 'MyMemory Translate',
    };
  }

  throw new Error('Invalid response structure from MyMemory Translation API.');
}
