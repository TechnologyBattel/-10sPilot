import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { APP_NAME, APP_TAGLINE } from '@10spilot/core';

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center gap-6 px-6">
      <h1 className="text-4xl font-bold tracking-tight">{APP_NAME}</h1>
      <p className="text-lg text-black/70 dark:text-white/70">{APP_TAGLINE}</p>
      <div>
        <Link href="/dashboard">
          <Button>Open dashboard</Button>
        </Link>
      </div>
    </main>
  );
}
