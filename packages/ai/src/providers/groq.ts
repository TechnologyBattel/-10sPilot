import type { AiProvider, ChatMessage, CompletionOptions, CompletionResult } from '../types';

const GROQ_URL = 'https://api.groq.com/openai/v1/chat/completions';

type GroqResponse = {
  model: string;
  choices: Array<{ message: { content: string } }>;
};

export class GroqProvider implements AiProvider {
  readonly name = 'groq';

  constructor(
    private readonly apiKey: string,
    private readonly defaultModel = 'llama-3.3-70b-versatile',
  ) {}

  async complete(
    messages: ChatMessage[],
    options: CompletionOptions = {},
  ): Promise<CompletionResult> {
    const response = await fetch(GROQ_URL, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: options.model ?? this.defaultModel,
        messages,
        temperature: options.temperature ?? 0.2,
        max_tokens: options.maxTokens,
      }),
    });

    if (!response.ok) {
      throw new Error(`Groq request failed with status ${response.status}`);
    }

    const data = (await response.json()) as GroqResponse;
    return { text: data.choices[0]?.message.content ?? '', model: data.model };
  }
}
