import { Card } from '@/components/ui/card';
import { PageHeader } from '@/components/ui/page-header';
import { Stat } from '@/components/ui/stat';

export default function DashboardPage() {
  return (
    <>
      <PageHeader
        title="Dashboard"
        description="Search, answer engine and generative engine performance at a glance."
      />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Stat label="Tracked keywords" value="0" />
        <Stat label="Avg. position" value="—" />
        <Stat label="AI citations" value="0" />
        <Stat label="Audit score" value="—" />
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <Card
          title="Latest workflow run"
          description="The autonomous agent chains research, audit, content and citation checks."
        >
          No runs yet — start one from the Workflow page.
        </Card>
        <Card title="Engines" description="Every module exposed by the API.">
          <ul className="list-disc pl-4">
            <li>SERP · Keyword · Content</li>
            <li>Audit · AEO · GEO</li>
            <li>Citation monitor · Internal links · Workflow</li>
          </ul>
        </Card>
      </div>
    </>
  );
}
