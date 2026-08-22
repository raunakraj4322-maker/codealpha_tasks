import { Router, Request, Response, NextFunction } from 'express';
import { validateTranslationRequest, SUPPORTED_LANGUAGES } from '../middleware/validator.js';
import { translationRateLimiter } from '../middleware/rateLimiter.js';
import { translateText } from '../services/translationService.js';
import { config } from '../config/index.js';

const router = Router();

// POST /api/translate
router.post(
  '/translate',
  translationRateLimiter,
  validateTranslationRequest,
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { text, sourceLanguage, targetLanguage } = req.body;
      const result = await translateText(text, sourceLanguage, targetLanguage);

      res.status(200).json({
        translatedText: result.translatedText,
        sourceLanguage: result.detectedSourceLanguage || sourceLanguage,
        targetLanguage,
        provider: result.provider,
        timestamp: new Date().toISOString(),
      });
    } catch (err) {
      next(err);
    }
  }
);

// GET /api/languages
router.get('/languages', (req: Request, res: Response) => {
  const languagesList = Object.entries(SUPPORTED_LANGUAGES).map(([code, name]) => ({
    code,
    name,
  }));

  res.status(200).json({
    languages: languagesList,
    total: languagesList.length,
  });
});

// GET /api/health
router.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    status: 'ok',
    service: 'CodeAlpha Language Translation Tool API',
    activeProvider: config.translationProvider,
    timestamp: new Date().toISOString(),
  });
});

export default router;
