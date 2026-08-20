export function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

export function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${String(value)}`);
}
