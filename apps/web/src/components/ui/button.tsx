import type { ButtonHTMLAttributes } from 'react';

import { cn } from '@/lib/utils';

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'ghost';
};

export function Button({ variant = 'primary', className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex h-10 items-center justify-center rounded-md px-4 text-sm font-medium transition-colors',
        variant === 'primary'
          ? 'bg-foreground text-background hover:opacity-90'
          : 'border border-black/10 hover:bg-black/5 dark:border-white/20 dark:hover:bg-white/10',
        className,
      )}
      {...props}
    />
  );
}
