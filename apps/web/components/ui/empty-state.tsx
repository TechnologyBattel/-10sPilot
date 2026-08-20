export function EmptyState({ title, hint }: { title: string; hint: string }) {
  return (
    <div className="rounded-lg border border-dashed border-black/15 p-10 text-center dark:border-white/25">
      <p className="font-medium">{title}</p>
      <p className="mt-1 text-sm text-black/60 dark:text-white/60">{hint}</p>
    </div>
  );
}
