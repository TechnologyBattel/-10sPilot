'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

import { NAV_ITEMS } from '@/lib/nav';
import { cn } from '@/lib/utils';

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden w-56 shrink-0 border-r border-black/10 p-4 md:block dark:border-white/20">
      <Link href="/" className="mb-6 block text-lg font-semibold">
        10sPilot
      </Link>
      <nav className="flex flex-col gap-1">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname.startsWith(item.href);

          return (
            <Link
              key={item.href}
              href={item.href}
              aria-current={isActive ? 'page' : undefined}
              className={cn(
                'flex items-center justify-between gap-2 rounded-md px-3 py-2 text-sm',
                isActive
                  ? 'bg-black/5 font-medium dark:bg-white/10'
                  : 'text-black/70 hover:bg-black/5 dark:text-white/70 dark:hover:bg-white/10',
              )}
            >
              <span>{item.label}</span>
              {isActive ? (
                <span className="rounded-full bg-emerald-500/10 px-2 py-0.5 text-xs text-emerald-700 dark:text-emerald-300">
                  Live
                </span>
              ) : null}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
