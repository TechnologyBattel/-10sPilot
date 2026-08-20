import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';

export default function KeywordsPage() {
  return (
    <>
      <PageHeader
        title="Keywords"
        description="Research from free SERP signals, then cluster by topic and intent."
      />
      <EmptyState
        title="No keywords yet"
        hint="POST a seed term to /api/v1/keywords/research to populate this view."
      />
    </>
  );
}
