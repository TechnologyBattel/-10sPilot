import { z } from 'zod'

const seoTypeSchema = z.object({
  id: z.string(),
  name: z.string(),
  priority: z.enum(['A','B','C']),
  description: z.string()
})

const requiredIds = ['aeo','geo','llmo','messaging-app-seo']

export function validateContentSchema(data: any) {
  const parsed = z.array(seoTypeSchema).parse(data)
  const ids = parsed.map(d => d.id)
  for (const req of requiredIds) {
    if (!ids.includes(req)) throw new Error(Missing required ID: )
  }
  const priorityA = parsed.filter(d => d.priority === 'A')
  if (priorityA.length < 4) throw new Error('Need at least 4 Priority A')
  return true
}
