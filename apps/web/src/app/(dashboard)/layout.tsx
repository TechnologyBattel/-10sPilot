import { SiteHeader } from '@/components/layout/site-header';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <SiteHeader />
      <main className="mx-auto max-w-5xl px-6 py-10">{children}</main>
    </div>
  );
}
