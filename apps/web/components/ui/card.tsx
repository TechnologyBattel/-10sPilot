import type { ReactNode } from 'react';

import { cn } from '@/lib/utils';

export function Card({
  title,
  description,
  children,
  className,
}: {
  title?: string;
  description?: string;
  children?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn('rounded-lg border border-black/10 p-5 dark:border-white/20', className)}>
      {title ? <h2 className="text-base font-semibold">{title}</h2> : null}
      {description ? (
        <p className="mt-1 text-sm text-black/60 dark:text-white/60">{description}</p>
      ) : null}
      {children ? <div className="mt-3 text-sm">{children}</div> : null}
    </div>
  );
}
