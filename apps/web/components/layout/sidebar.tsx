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
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              'rounded-md px-3 py-2 text-sm',
              pathname.startsWith(item.href)
                ? 'bg-black/5 font-medium dark:bg-white/10'
                : 'text-black/70 hover:bg-black/5 dark:text-white/70 dark:hover:bg-white/10',
            )}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
