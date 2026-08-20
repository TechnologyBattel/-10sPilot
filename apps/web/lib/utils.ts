export function cn(...classes: Array<string | false | null | undefined>): string {
  return classes.filter(Boolean).join(' ');
}

export function formatPercent(value: number): string {
  return `${Math.round(value)}%`;
}
