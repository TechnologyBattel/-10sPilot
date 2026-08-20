import { Card } from '@/components/ui/card';
import { PageHeader } from '@/components/ui/page-header';

const ENGINES = ['ChatGPT', 'Perplexity', 'Gemini'];

export default function AiCitationsPage() {
  return (
    <>
      <PageHeader
        title="AI Citations"
        description="Whether answer engines cite your domain for the prompts that matter."
      />
      <div className="grid gap-4 sm:grid-cols-3">
        {ENGINES.map((engine) => (
          <Card key={engine} title={engine} description="No checks recorded yet." />
        ))}
      </div>
    </>
  );
}
