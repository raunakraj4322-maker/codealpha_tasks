import { Request, Response, NextFunction } from 'express';

export interface CustomError extends Error {
  statusCode?: number;
  details?: any;
}

export const errorHandler = (
  err: CustomError,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const statusCode = err.statusCode || 500;
  
  // Safe user-friendly error message, suppressing internal secrets or raw stack traces
  let message = err.message || 'An unexpected translation error occurred.';
  
  // Prevent leaking API keys or internal path details in error message
  if (message.includes('API_KEY') || message.includes('key=') || message.includes('Bearer')) {
    message = 'Translation API request authorization failed. Please check backend server credentials.';
  }

  console.error(`[Error ${statusCode}] ${req.method} ${req.path}: ${err.message}`);

  res.status(statusCode).json({
    error: {
      message,
      status: statusCode,
      timestamp: new Date().toISOString()
    }
  });
};
