import rateLimit from 'express-rate-limit';

export const translationRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: {
      message: 'Too many translation requests from this IP. Please try again in 15 minutes.',
      status: 429
    }
  }
});
