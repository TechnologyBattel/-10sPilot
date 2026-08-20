import Link from 'next/link';

import { ApiStatus } from '@/components/api-status';

export function SiteHeader() {
  return (
    <header className="flex items-center justify-between border-b border-black/10 px-6 py-3 dark:border-white/20">
      <Link href="/dashboard" className="text-sm font-medium md:hidden">
        10sPilot
      </Link>
      <div className="ml-auto">
        <ApiStatus />
      </div>
    </header>
  );
}
