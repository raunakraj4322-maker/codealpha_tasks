import { Language } from '../types';

export const POPULAR_LANGUAGES: Language[] = [
  { code: 'auto', name: 'Auto Detect', nativeName: 'Automatic', flag: '🌐', bcp47: 'en-US' },
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸', bcp47: 'en-US' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', flag: '🇮🇳', bcp47: 'hi-IN' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা', flag: '🇧🇩', bcp47: 'bn-IN' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்', flag: '🇮🇳', bcp47: 'ta-IN' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు', flag: '🇮🇳', bcp47: 'te-IN' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी', flag: '🇮🇳', bcp47: 'mr-IN' },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી', flag: '🇮🇳', bcp47: 'gu-IN' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ', flag: '🇮🇳', bcp47: 'kn-IN' },
  { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം', flag: '🇮🇳', bcp47: 'ml-IN' },
  { code: 'pa', name: 'Punjabi', nativeName: 'ਪੰਜਾਬੀ', flag: '🇮🇳', bcp47: 'pa-IN' },
  { code: 'ur', name: 'Urdu', nativeName: 'اردو', flag: '🇵🇰', bcp47: 'ur-PK' },
  { code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸', bcp47: 'es-ES' },
  { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷', bcp47: 'fr-FR' },
  { code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪', bcp47: 'de-DE' },
  { code: 'it', name: 'Italian', nativeName: 'Italiano', flag: '🇮🇹', bcp47: 'it-IT' },
  { code: 'pt', name: 'Portuguese', nativeName: 'Português', flag: '🇵🇹', bcp47: 'pt-PT' },
  { code: 'ru', name: 'Russian', nativeName: 'Русский', flag: '🇷🇺', bcp47: 'ru-RU' },
  { code: 'ja', name: 'Japanese', nativeName: '日本語', flag: '🇯🇵', bcp47: 'ja-JP' },
  { code: 'ko', name: 'Korean', nativeName: '한국어', flag: '🇰🇷', bcp47: 'ko-KR' },
  { code: 'zh', name: 'Chinese', nativeName: '中文', flag: '🇨🇳', bcp47: 'zh-CN' },
  { code: 'ar', name: 'Arabic', nativeName: 'العربية', flag: '🇸🇦', bcp47: 'ar-SA' },
  { code: 'nl', name: 'Dutch', nativeName: 'Nederlands', flag: '🇳🇱', bcp47: 'nl-NL' },
  { code: 'tr', name: 'Turkish', nativeName: 'Türkçe', flag: '🇹🇷', bcp47: 'tr-TR' },
  { code: 'pl', name: 'Polish', nativeName: 'Polski', flag: '🇵🇱', bcp47: 'pl-PL' },
  { code: 'vi', name: 'Vietnamese', nativeName: 'Tiếng Việt', flag: '🇻🇳', bcp47: 'vi-VN' },
  { code: 'th', name: 'Thai', nativeName: 'ไทย', flag: '🇹🇭', bcp47: 'th-TH' },
  { code: 'id', name: 'Indonesian', nativeName: 'Bahasa Indonesia', flag: '🇮🇩', bcp47: 'id-ID' },
  { code: 'sv', name: 'Swedish', nativeName: 'Svenska', flag: '🇸🇪', bcp47: 'sv-SE' },
  { code: 'el', name: 'Greek', nativeName: 'Ελληνικά', flag: '🇬🇷', bcp47: 'el-GR' },
];

export const getLanguageByCode = (code: string): Language => {
  const found = POPULAR_LANGUAGES.find((l) => l.code === code);
  return found || { code, name: code.toUpperCase(), nativeName: code.toUpperCase(), flag: '🌐', bcp47: 'en-US' };
};
