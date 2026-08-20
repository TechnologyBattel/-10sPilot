import Link from 'next/link';

export function SiteHeader() {
  return (
    <header className="flex items-center justify-between border-b border-black/10 px-6 py-4 dark:border-white/20">
      <Link href="/" className="font-semibold">
        10sPilot
      </Link>
      <nav className="flex gap-4 text-sm">
        <Link href="/dashboard">Dashboard</Link>
        <a href="https://github.com/TechnologyBattel/-10sPilot/tree/main/docs">Docs</a>
      </nav>
    </header>
  );
}
