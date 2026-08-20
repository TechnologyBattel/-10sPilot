export type ProviderName = 'groq' | 'gemini';

export type AiConfig = {
  provider: ProviderName;
  groqApiKey?: string;
  groqModel: string;
  googleApiKey?: string;
  googleModel: string;
};

export function loadAiConfig(env: NodeJS.ProcessEnv = process.env): AiConfig {
  const provider = (env.AI_PROVIDER as ProviderName | undefined) ?? 'groq';

  return {
    provider,
    groqApiKey: env.GROQ_API_KEY,
    groqModel: env.GROQ_MODEL ?? 'llama-3.3-70b-versatile',
    googleApiKey: env.GOOGLE_API_KEY,
    googleModel: env.GOOGLE_MODEL ?? 'gemini-2.0-flash',
  };
}
