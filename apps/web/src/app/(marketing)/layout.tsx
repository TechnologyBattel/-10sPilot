import { SiteHeader } from '@/components/layout/site-header';

export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <SiteHeader />
      <main className="mx-auto max-w-4xl px-6 py-16">{children}</main>
    </div>
  );
}
