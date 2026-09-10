'use client';

import { useState } from 'react';

import {
  ApiError,
  getAEOCheck,
  runAudit,
  type AEOResult,
  type AuditReport,
} from '@/lib/api-client';

type EngineState<T> =
  | { status: 'ok'; data: T }
  | { status: 'error'; message: string };

type Overview = {
  domain: string;
  brand: string;
  query: string;
  audit: EngineState<AuditReport>;
  aeo: EngineState<AEOResult[]>;
};

function normalizeDomain(raw: string): { host: string; url: string } | null {
  const trimmed = raw.trim();
  if (!trimmed) return null;
  const withScheme = /^https?:\/\//i.test(trimmed) ? trimmed : `https://${trimmed}`;
  try {
    const parsed = new URL(withScheme);
    if (!parsed.hostname.includes('.')) return null;
    return { host: parsed.hostname.replace(/^www\./, ''), url: parsed.toString() };
  } catch {
    return null;
  }
}

function brandFromHost(host: string): string {
  const label = host.replace(/^www\./, '').split('.')[0] ?? host;
  return label.charAt(0).toUpperCase() + label.slice(1);
}

/** AEO visibility (0-100) derived from live mention + reported position. */
function aeoScore(results: AEOResult[]): number | null {
  if (results.length === 0) return null;
  const per = results.map((r) => {
    if (!r.mentioned) return 0;
    if (r.position == null) return 70;
    return Math.max(40, 100 - (r.position - 1) * 15);
  });
  return Math.round(per.reduce((a, b) => a + b, 0) / per.length);
}

function scoreTone(score: number): string {
  if (score >= 80) return 'text-success';
  if (score >= 50) return 'text-warning';
  return 'text-danger';
}

function severityStyles(severity: string): string {
  switch (severity.toLowerCase()) {
    case 'error':
    case 'critical':
      return 'bg-danger/10 text-danger border-danger/20';
    case 'warning':
      return 'bg-warning/10 text-warning border-warning/20';
    default:
      return 'bg-muted text-muted-foreground border-border';
  }
}

function engineMessage(err: unknown): string {
  if (err instanceof ApiError) {
    if (err.status === 429) return 'Rate limit reached. Please wait a minute and try again.';
    if (err.status === 400) return 'This domain could not be fetched safely (blocked or invalid).';
    if (err.status >= 500)
      return 'This engine is unavailable — its AI provider may not be configured on the server yet.';
    return `Engine request failed (HTTP ${err.status}).`;
  }
  return 'Could not reach the analysis API. Is the backend running?';
}

export function OverviewSearch() {
  const [value, setValue] = useState('');
  const [inputError, setInputError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [overview, setOverview] = useState<Overview | null>(null);

  async function analyze(rawDomain: string) {
    const normalized = normalizeDomain(rawDomain);
    if (!normalized) {
      setInputError('Enter a valid domain, e.g. example.com');
      return;
    }
    setInputError(null);
    setLoading(true);

    const brand = brandFromHost(normalized.host);
    const query = `What is ${brand}?`;

    const [auditResult, aeoResult] = await Promise.allSettled([
      runAudit(normalized.url),
      getAEOCheck(brand, query, ['groq']),
    ]);

    setOverview({
      domain: normalized.host,
      brand,
      query,
      audit:
        auditResult.status === 'fulfilled'
          ? { status: 'ok', data: auditResult.value }
          : { status: 'error', message: engineMessage(auditResult.reason) },
      aeo:
        aeoResult.status === 'fulfilled'
          ? { status: 'ok', data: aeoResult.value }
          : { status: 'error', message: engineMessage(aeoResult.reason) },
    });
    setLoading(false);
  }

  function onSubmit(event: React.FormEvent) {
    event.preventDefault();
    if (loading) return;
    void analyze(value);
  }

  return (
    <div className="w-full">
      <form onSubmit={onSubmit} className="mx-auto w-full max-w-xl">
        <div className="flex items-center gap-2 rounded-full border border-input bg-card px-5 py-2.5 shadow-sm transition focus-within:border-primary focus-within:ring-2 focus-within:ring-ring/30">
          <SearchIcon />
          <input
            type="text"
            inputMode="url"
            autoCapitalize="off"
            autoCorrect="off"
            spellCheck={false}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Enter your domain, e.g. vercel.com"
            aria-label="Domain to analyze"
            className="min-w-0 flex-1 bg-transparent text-base text-foreground outline-none placeholder:text-muted-foreground"
          />
          {value && (
            <button
              type="button"
              onClick={() => {
                setValue('');
                setInputError(null);
              }}
              aria-label="Clear"
              className="rounded-full p-1 text-muted-foreground hover:bg-muted"
            >
              <ClearIcon />
            </button>
          )}
        </div>

        <div className="mt-6 flex items-center justify-center gap-3">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center gap-2 rounded-lg bg-primary px-6 py-2.5 text-sm font-semibold text-primary-foreground shadow-sm transition hover:opacity-90 disabled:opacity-60"
          >
            {loading ? 'Analyzing…' : 'Get full overview'}
          </button>
          <button
            type="button"
            disabled={loading}
            onClick={() => {
              setValue('vercel.com');
              void analyze('vercel.com');
            }}
            className="rounded-lg border border-border bg-card px-6 py-2.5 text-sm font-medium text-foreground transition hover:bg-muted disabled:opacity-60"
          >
            Try an example
          </button>
        </div>
        {inputError && (
          <p className="mt-3 text-center text-sm text-danger" role="alert">
            {inputError}
          </p>
        )}
      </form>

      {loading && <LoadingReport />}
      {!loading && overview && <ReportView overview={overview} />}
    </div>
  );
}

function ReportView({ overview }: { overview: Overview }) {
  const auditScore = overview.audit.status === 'ok' ? overview.audit.data.score : null;
  const aeoVisibility =
    overview.aeo.status === 'ok' ? aeoScore(overview.aeo.data) : null;

  const parts: { weight: number; value: number }[] = [];
  if (auditScore != null) parts.push({ weight: 0.6, value: auditScore });
  if (aeoVisibility != null) parts.push({ weight: 0.4, value: aeoVisibility });
  const totalWeight = parts.reduce((a, p) => a + p.weight, 0);
  const unified =
    totalWeight > 0
      ? Math.round(parts.reduce((a, p) => a + p.value * p.weight, 0) / totalWeight)
      : null;

  return (
    <section className="mx-auto mt-12 w-full max-w-3xl text-left" aria-label="Overview report">
      <div className="mb-6 flex flex-wrap items-end justify-between gap-4 border-b border-border pb-6">
        <div>
          <p className="text-sm text-muted-foreground">Overview for</p>
          <h2 className="text-2xl font-semibold text-foreground">{overview.domain}</h2>
        </div>
        {unified != null && (
          <div className="text-right">
            <p className="text-sm text-muted-foreground">10sPilot Score</p>
            <p className={`text-4xl font-bold ${scoreTone(unified)}`}>{unified}</p>
          </div>
        )}
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <AuditCard state={overview.audit} />
        <AeoCard state={overview.aeo} query={overview.query} score={aeoVisibility} />
      </div>

      <div className="mt-5 rounded-lg border border-dashed border-border bg-muted/50 p-5">
        <h3 className="text-sm font-semibold text-foreground">More engines coming</h3>
        <p className="mt-1 text-sm text-muted-foreground">
          GEO (Google AI Overviews) and LLMO (llms.txt) are on the roadmap and are not part of this
          live overview yet. The score above is derived only from the engines that ran: Technical
          Audit (60%) and AEO visibility (40%).
        </p>
      </div>
    </section>
  );
}

function CardShell({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-lg border border-border bg-card p-5 shadow-sm">
      <h3 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
        {title}
      </h3>
      {children}
    </div>
  );
}

function AuditCard({ state }: { state: EngineState<AuditReport> }) {
  if (state.status === 'error') {
    return (
      <CardShell title="Technical Audit">
        <p className="text-sm text-danger">{state.message}</p>
      </CardShell>
    );
  }
  const audit = state.data;
  return (
    <CardShell title="Technical Audit">
      <div className="mb-4 flex items-baseline gap-2">
        <span className={`text-3xl font-bold ${scoreTone(audit.score)}`}>
          {Math.round(audit.score)}
        </span>
        <span className="text-sm text-muted-foreground">/ 100</span>
      </div>
      <dl className="space-y-2 text-sm">
        <Row label="HTTP status" value={String(audit.status_code)} />
        <Row label="Title" value={audit.title || '—'} />
        <Row label="Meta description" value={audit.meta_description ? 'Present' : 'Missing'} />
        <Row label="Word count" value={String(audit.word_count)} />
      </dl>
      {audit.issues.length > 0 && (
        <ul className="mt-4 space-y-2">
          {audit.issues.map((issue, i) => (
            <li
              key={`${issue.check}-${i}`}
              className={`rounded-md border px-3 py-2 text-sm ${severityStyles(issue.severity)}`}
            >
              <span className="font-medium capitalize">{issue.severity}:</span> {issue.message}
            </li>
          ))}
        </ul>
      )}
    </CardShell>
  );
}

function AeoCard({
  state,
  query,
  score,
}: {
  state: EngineState<AEOResult[]>;
  query: string;
  score: number | null;
}) {
  if (state.status === 'error') {
    return (
      <CardShell title="AI Visibility (AEO)">
        <p className="text-sm text-danger">{state.message}</p>
      </CardShell>
    );
  }
  const results = state.data;
  return (
    <CardShell title="AI Visibility (AEO)">
      {score != null && (
        <div className="mb-4 flex items-baseline gap-2">
          <span className={`text-3xl font-bold ${scoreTone(score)}`}>{score}</span>
          <span className="text-sm text-muted-foreground">/ 100</span>
        </div>
      )}
      <p className="mb-3 text-sm text-muted-foreground">
        Query: <span className="text-foreground">{query}</span>
      </p>
      {results.length === 0 ? (
        <p className="text-sm text-muted-foreground">No provider returned a result.</p>
      ) : (
        <ul className="space-y-2">
          {results.map((r, i) => (
            <li
              key={`${r.provider}-${i}`}
              className="rounded-md border border-border px-3 py-2 text-sm"
            >
              <div className="flex items-center justify-between">
                <span className="font-medium capitalize">{r.provider}</span>
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                    r.mentioned
                      ? 'bg-success/10 text-success'
                      : 'bg-muted text-muted-foreground'
                  }`}
                >
                  {r.mentioned ? 'Mentioned' : 'Not mentioned'}
                </span>
              </div>
              {r.position != null && (
                <p className="mt-1 text-xs text-muted-foreground">Position: {r.position}</p>
              )}
              {r.context && (
                <p className="mt-1 line-clamp-3 text-xs text-muted-foreground">{r.context}</p>
              )}
            </li>
          ))}
        </ul>
      )}
    </CardShell>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-start justify-between gap-4">
      <dt className="shrink-0 text-muted-foreground">{label}</dt>
      <dd className="truncate text-right font-medium text-foreground">{value}</dd>
    </div>
  );
}

function LoadingReport() {
  return (
    <section className="mx-auto mt-12 w-full max-w-3xl" aria-hidden="true">
      <div className="mb-6 h-16 animate-pulse rounded-lg bg-muted" />
      <div className="grid gap-5 sm:grid-cols-2">
        <div className="h-64 animate-pulse rounded-lg bg-muted" />
        <div className="h-64 animate-pulse rounded-lg bg-muted" />
      </div>
    </section>
  );
}

function SearchIcon() {
  return (
    <svg
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="shrink-0 text-muted-foreground"
      aria-hidden="true"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.3-4.3" />
    </svg>
  );
}

function ClearIcon() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M18 6 6 18M6 6l12 12" />
    </svg>
  );
}
