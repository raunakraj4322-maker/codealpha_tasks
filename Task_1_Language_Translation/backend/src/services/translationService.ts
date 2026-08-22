import { config } from '../config/index.js';
import { translateWithMyMemory, TranslationResult } from './mymemoryProvider.js';
import { translateWithGoogle } from './googleProvider.js';
import { translateWithAzure } from './azureProvider.js';
import { translateWithLibre } from './libreProvider.js';

export async function translateText(
  text: string,
  sourceLanguage: string,
  targetLanguage: string
): Promise<TranslationResult> {
  // If source and target language are the same, return the text directly
  if (sourceLanguage === targetLanguage && sourceLanguage !== 'auto') {
    return {
      translatedText: text,
      detectedSourceLanguage: sourceLanguage,
      provider: 'Direct Pass-through (Languages Match)',
    };
  }

  const provider = config.translationProvider.toLowerCase();

  try {
    if (provider === 'google') {
      if (!config.googleApiKey) {
        console.warn('Google API key not set. Falling back to MyMemory provider.');
        return await translateWithMyMemory(text, sourceLanguage, targetLanguage);
      }
      return await translateWithGoogle(text, sourceLanguage, targetLanguage, config.googleApiKey);
    }

    if (provider === 'azure') {
      if (!config.azureKey) {
        console.warn('Azure key not set. Falling back to MyMemory provider.');
        return await translateWithMyMemory(text, sourceLanguage, targetLanguage);
      }
      return await translateWithAzure(
        text,
        sourceLanguage,
        targetLanguage,
        config.azureKey,
        config.azureRegion
      );
    }

    if (provider === 'libretranslate') {
      return await translateWithLibre(
        text,
        sourceLanguage,
        targetLanguage,
        config.libreTranslateUrl,
        config.libreTranslateKey
      );
    }

    // Default provider: MyMemory
    return await translateWithMyMemory(text, sourceLanguage, targetLanguage);
  } catch (error: any) {
    console.error(`Primary provider "${provider}" failed: ${error?.message}`);

    // Fallback attempt to MyMemory if primary non-mymemory provider failed
    if (provider !== 'mymemory') {
      console.log('Attempting fallback translation with MyMemory...');
      try {
        return await translateWithMyMemory(text, sourceLanguage, targetLanguage);
      } catch (fallbackError: any) {
        console.error(`Fallback translation also failed: ${fallbackError?.message}`);
      }
    }

    throw new Error(
      error?.message || 'Translation service failed to process request. Please try again later.'
    );
  }
}
