import type { ReactNode } from 'react';

import { cn } from '@/lib/utils';

export function Card({ title, children, className }: { title?: string; children: ReactNode; className?: string }) {
  return (
    <div className={cn('rounded-lg border border-black/10 p-6 dark:border-white/20', className)}>
      {title ? <h2 className="mb-2 text-lg font-semibold">{title}</h2> : null}
      {children}
    </div>
  );
}
