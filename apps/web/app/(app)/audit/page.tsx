import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';

export default function AuditPage() {
  return (
    <>
      <PageHeader
        title="Audit"
        description="Technical SEO checks: titles, headings, canonicals, structured data and thin content."
      />
      <EmptyState title="No audits yet" hint="Run one against a URL via /api/v1/audit." />
    </>
  );
}
