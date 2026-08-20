import { Card } from '@/components/ui/card';

export default function DashboardPage() {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <Card title="Pilots">No pilots yet.</Card>
      <Card title="Runs">No runs yet.</Card>
    </div>
  );
}
