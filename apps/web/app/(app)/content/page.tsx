import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';

export default function ContentPage() {
  return (
    <>
      <PageHeader
        title="Content"
        description="Briefs and drafts scored for answer engines (AEO) and generative engines (GEO)."
      />
      <EmptyState
        title="No drafts yet"
        hint="Generate one from a keyword via /api/v1/content/generate."
      />
    </>
  );
}
