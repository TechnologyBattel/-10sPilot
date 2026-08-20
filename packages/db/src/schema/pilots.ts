import { pgTable, text, timestamp, uuid } from 'drizzle-orm/pg-core';

import { users } from './users';

export const pilots = pgTable('pilots', {
  id: uuid('id').defaultRandom().primaryKey(),
  userId: uuid('user_id')
    .references(() => users.id, { onDelete: 'cascade' })
    .notNull(),
  name: text('name').notNull(),
  prompt: text('prompt').notNull(),
  status: text('status').default('draft').notNull(),
  createdAt: timestamp('created_at', { withTimezone: true }).defaultNow().notNull(),
  updatedAt: timestamp('updated_at', { withTimezone: true }).defaultNow().notNull(),
});

export type Pilot = typeof pilots.$inferSelect;
export type NewPilot = typeof pilots.$inferInsert;
