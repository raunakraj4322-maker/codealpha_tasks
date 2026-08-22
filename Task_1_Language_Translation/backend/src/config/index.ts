import dotenv from 'dotenv';
import path from 'path';

// Load .env file from root or local backend folder
dotenv.config({ path: path.resolve(__dirname, '../../../.env') });
dotenv.config();

export interface AppConfig {
  port: number;
  nodeEnv: string;
  clientUrl: string;
  translationProvider: 'mymemory' | 'google' | 'azure' | 'libretranslate';
  googleApiKey: string;
  azureKey: string;
  azureRegion: string;
  libreTranslateUrl: string;
  libreTranslateKey: string;
}

export const config: AppConfig = {
  port: parseInt(process.env.PORT || '5000', 10),
  nodeEnv: process.env.NODE_ENV || 'development',
  clientUrl: process.env.CLIENT_URL || 'http://localhost:5173',
  translationProvider: (process.env.TRANSLATION_PROVIDER as AppConfig['translationProvider']) || 'mymemory',
  googleApiKey: process.env.GOOGLE_TRANSLATE_API_KEY || '',
  azureKey: process.env.AZURE_TRANSLATOR_KEY || '',
  azureRegion: process.env.AZURE_TRANSLATOR_REGION || 'global',
  libreTranslateUrl: process.env.LIBRETRANSLATE_API_URL || 'https://libretranslate.com',
  libreTranslateKey: process.env.LIBRETRANSLATE_API_KEY || '',
};
