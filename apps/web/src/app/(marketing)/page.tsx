import Link from 'next/link';

import { Button } from '@/components/ui/button';
import { APP_NAME, APP_TAGLINE } from '@10spilot/core';

export default function HomePage() {
  return (
    <section className="flex flex-col gap-6">
      <h1 className="text-4xl font-bold tracking-tight">{APP_NAME}</h1>
      <p className="text-lg text-black/70 dark:text-white/70">{APP_TAGLINE}</p>
      <Link href="/dashboard">
        <Button>Open dashboard</Button>
      </Link>
    </section>
  );
}
