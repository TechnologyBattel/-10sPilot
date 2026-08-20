import { loadAiConfig, type AiConfig } from './config';
import { GeminiProvider } from './providers/gemini';
import { GroqProvider } from './providers/groq';
import type { AiProvider } from './types';

export function createAiProvider(config: AiConfig = loadAiConfig()): AiProvider {
  if (config.provider === 'gemini') {
    if (!config.googleApiKey) {
      throw new Error('GOOGLE_API_KEY is not set');
    }
    return new GeminiProvider(config.googleApiKey, config.googleModel);
  }

  if (!config.groqApiKey) {
    throw new Error('GROQ_API_KEY is not set');
  }
  return new GroqProvider(config.groqApiKey, config.groqModel);
}
