import { Request, Response, NextFunction } from 'express';
import { CustomError } from './errorHandler.js';

export const SUPPORTED_LANGUAGES: Record<string, string> = {
  auto: 'Auto Detect',
  en: 'English',
  hi: 'Hindi',
  bn: 'Bengali',
  ta: 'Tamil',
  te: 'Telugu',
  mr: 'Marathi',
  gu: 'Gujarati',
  kn: 'Kannada',
  ml: 'Malayalam',
  pa: 'Punjabi',
  ur: 'Urdu',
  es: 'Spanish',
  fr: 'French',
  de: 'German',
  it: 'Italian',
  pt: 'Portuguese',
  ru: 'Russian',
  ja: 'Japanese',
  ko: 'Korean',
  zh: 'Chinese',
  ar: 'Arabic',
  nl: 'Dutch',
  tr: 'Turkish',
  pl: 'Polish',
  vi: 'Vietnamese',
  th: 'Thai',
  id: 'Indonesian',
  sv: 'Swedish',
  el: 'Greek'
};

export const validateTranslationRequest = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const { text, sourceLanguage, targetLanguage } = req.body;

  if (text === undefined || text === null || typeof text !== 'string') {
    const err: CustomError = new Error('Field "text" must be a valid string.');
    err.statusCode = 400;
    return next(err);
  }

  const trimmedText = text.trim();
  if (trimmedText.length === 0) {
    const err: CustomError = new Error('Translation text cannot be empty.');
    err.statusCode = 400;
    return next(err);
  }

  if (trimmedText.length > 5000) {
    const err: CustomError = new Error('Translation text exceeds maximum limit of 5000 characters.');
    err.statusCode = 400;
    return next(err);
  }

  if (!sourceLanguage || typeof sourceLanguage !== 'string') {
    const err: CustomError = new Error('Field "sourceLanguage" is required.');
    err.statusCode = 400;
    return next(err);
  }

  if (!targetLanguage || typeof targetLanguage !== 'string') {
    const err: CustomError = new Error('Field "targetLanguage" is required.');
    err.statusCode = 400;
    return next(err);
  }

  const normalizedSource = sourceLanguage.toLowerCase();
  const normalizedTarget = targetLanguage.toLowerCase();

  if (!SUPPORTED_LANGUAGES[normalizedSource]) {
    const err: CustomError = new Error(`Unsupported source language code: "${sourceLanguage}".`);
    err.statusCode = 400;
    return next(err);
  }

  if (!SUPPORTED_LANGUAGES[normalizedTarget] || normalizedTarget === 'auto') {
    const err: CustomError = new Error(`Invalid or unsupported target language code: "${targetLanguage}". Target cannot be "auto".`);
    err.statusCode = 400;
    return next(err);
  }

  req.body.text = trimmedText;
  req.body.sourceLanguage = normalizedSource;
  req.body.targetLanguage = normalizedTarget;

  next();
};
