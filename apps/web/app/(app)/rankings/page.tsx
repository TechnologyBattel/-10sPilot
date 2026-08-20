import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';

export default function RankingsPage() {
  return (
    <>
      <PageHeader
        title="Rankings"
        description="Positions from Serper.dev plus clicks and impressions from Search Console."
      />
      <EmptyState title="No ranking data yet" hint="Connect SERPER_API_KEY and a GSC property." />
    </>
  );
}
