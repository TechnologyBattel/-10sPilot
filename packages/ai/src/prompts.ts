import { APP_NAME } from '@10spilot/core';

export const SYSTEM_PROMPT = `You are ${APP_NAME}, an assistant that turns short prompts into shippable plans.
Answer concisely and prefer actionable steps.`;

export function pilotPrompt(prompt: string): string {
  return `Produce a concise, ordered plan for the following request:\n\n${prompt}`;
}
