import { pgTable, text, timestamp, uuid } from 'drizzle-orm/pg-core';

import { pilots } from './pilots';

export const runs = pgTable('runs', {
  id: uuid('id').defaultRandom().primaryKey(),
  pilotId: uuid('pilot_id')
    .references(() => pilots.id, { onDelete: 'cascade' })
    .notNull(),
  status: text('status').default('running').notNull(),
  output: text('output'),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow().notNull(),
});

export type Run = typeof runs.$inferSelect;
export type NewRun = typeof runs.$inferInsert;
