export function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-black/10 p-5 dark:border-white/20">
      <p className="text-xs uppercase tracking-wide text-black/50 dark:text-white/50">{label}</p>
      <p className="mt-2 text-2xl font-semibold">{value}</p>
    </div>
  );
}
