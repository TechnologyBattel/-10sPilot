export type ChatRole = 'system' | 'user' | 'assistant';

export type ChatMessage = {
  role: ChatRole;
  content: string;
};

export type CompletionOptions = {
  model?: string;
  temperature?: number;
  maxTokens?: number;
};

export type CompletionResult = {
  text: string;
  model: string;
};

export interface AiProvider {
  readonly name: string;
  complete(messages: ChatMessage[], options?: CompletionOptions): Promise<CompletionResult>;
}
