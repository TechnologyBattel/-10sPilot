import { z } from 'zod';

export const pilotStatusSchema = z.enum(['draft', 'running', 'completed', 'failed']);

export const pilotSchema = z.object({
  id: z.string(),
  name: z.string().min(1).max(120),
  prompt: z.string().min(1),
  status: pilotStatusSchema,
  createdAt: z.string(),
  updatedAt: z.string(),
});

export const createPilotSchema = pilotSchema.pick({ name: true, prompt: true });

export const runSchema = z.object({
  id: z.string(),
  pilotId: z.string(),
  status: pilotStatusSchema,
  output: z.string().nullable(),
  createdAt: z.string(),
  updatedAt: z.string(),
});

export type CreatePilotInput = z.infer<typeof createPilotSchema>;
