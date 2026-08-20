import { Sidebar } from '@/components/layout/sidebar';
import { SiteHeader } from '@/components/layout/site-header';

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <SiteHeader />
        <main className="flex-1 px-6 py-8">{children}</main>
      </div>
    </div>
  );
}
