import { TranslationRequest, TranslationResponse, ServerHealth } from '../types';

const API_BASE_URL = '/api';

export async function requestTranslation(
  payload: TranslationRequest
): Promise<TranslationResponse> {
  const response = await fetch(`${API_BASE_URL}/translate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  if (!response.ok) {
    const errorMessage = data?.error?.message || 'Translation request failed.';
    throw new Error(errorMessage);
  }

  return data as TranslationResponse;
}

export async function checkServerHealth(): Promise<ServerHealth> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return await response.json();
  } catch (error) {
    return {
      status: 'offline',
      service: 'Offline / Disconnected',
      activeProvider: 'none',
      timestamp: new Date().toISOString(),
    };
  }
}
