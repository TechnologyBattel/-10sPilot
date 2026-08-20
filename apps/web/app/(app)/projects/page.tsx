import { EmptyState } from '@/components/ui/empty-state';
import { PageHeader } from '@/components/ui/page-header';

export default function ProjectsPage() {
  return (
    <>
      <PageHeader title="Projects" description="One project per domain you are optimizing." />
      <EmptyState
        title="No projects yet"
        hint="Create a project with a domain to start tracking keywords, rankings and citations."
      />
    </>
  );
}
