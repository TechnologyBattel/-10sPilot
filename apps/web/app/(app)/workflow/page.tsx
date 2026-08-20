import { Card } from '@/components/ui/card';
import { PageHeader } from '@/components/ui/page-header';

const STEPS = [
  'research_keywords',
  'cluster_keywords',
  'get_rankings',
  'audit_page',
  'generate_content',
  'suggest_links',
  'check_citations',
];

export default function WorkflowPage() {
  return (
    <>
      <PageHeader
        title="Workflow"
        description="The autonomous agent chains every MCP tool into one run."
      />
      <Card title="Default pipeline" description="POST /api/v1/workflow/run to execute it.">
        <ol className="list-decimal space-y-1 pl-4 font-mono text-xs">
          {STEPS.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ol>
      </Card>
    </>
  );
}
