import type { AiProvider, ChatMessage, CompletionOptions, CompletionResult } from '../types';

const GEMINI_BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models';

type GeminiResponse = {
  candidates?: Array<{ content: { parts: Array<{ text?: string }> } }>;
};

export class GeminiProvider implements AiProvider {
  readonly name = 'gemini';

  constructor(
    private readonly apiKey: string,
    private readonly defaultModel = 'gemini-2.0-flash',
  ) {}

  async complete(
    messages: ChatMessage[],
    options: CompletionOptions = {},
  ): Promise<CompletionResult> {
    const model = options.model ?? this.defaultModel;
    const response = await fetch(
      `${GEMINI_BASE_URL}/${model}:generateContent?key=${this.apiKey}`,
      {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          contents: messages.map((message) => ({
            role: message.role === 'assistant' ? 'model' : 'user',
            parts: [{ text: message.content }],
          })),
          generationConfig: {
            temperature: options.temperature ?? 0.2,
            maxOutputTokens: options.maxTokens,
          },
        }),
      },
    );

    if (!response.ok) {
      throw new Error(`Gemini request failed with status ${response.status}`);
    }

    const data = (await response.json()) as GeminiResponse;
    const text = data.candidates?.[0]?.content.parts.map((part) => part.text ?? '').join('') ?? '';
    return { text, model };
  }
}
