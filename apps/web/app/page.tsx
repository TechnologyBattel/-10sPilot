import { OverviewSearch } from '@/components/overview-search'
import { SiteFooter } from '@/components/layout/site-footer'

const PILLARS = [
  {
    label: 'Technical Audit',
    status: 'Live',
    description: 'Titles, meta, headings and thin-content checks for any URL.',
  },
  {
    label: 'AEO Visibility',
    status: 'Live',
    description: 'Whether AI answer engines mention your brand, and where.',
  },
  {
    label: 'GEO / LLMO',
    status: 'Coming soon',
    description: 'Google AI Overviews and llms.txt coverage.',
  },
]

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-background text-foreground">
      <section className="flex flex-1 flex-col items-center justify-center px-4 py-20 sm:px-6">
        <div className="w-full max-w-3xl text-center">
          <h1 className="text-5xl font-bold tracking-tight sm:text-6xl">
            <span className="text-primary">10s</span>Pilot
          </h1>
          <p className="mx-auto mt-4 max-w-xl text-balance text-lg text-muted-foreground">
            Enter your domain to get a full visibility overview across technical SEO and AI answer
            engines — powered by live checks.
          </p>

          <div className="mt-10">
            <OverviewSearch />
          </div>
        </div>

        <div className="mt-20 grid w-full max-w-3xl gap-4 sm:grid-cols-3">
          {PILLARS.map((pillar) => (
            <div
              key={pillar.label}
              className="rounded-lg border border-border bg-card p-5 text-left"
            >
              <div className="mb-2 flex items-center justify-between gap-2">
                <h2 className="text-sm font-semibold text-foreground">{pillar.label}</h2>
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                    pillar.status === 'Live'
                      ? 'bg-success/10 text-success'
                      : 'bg-muted text-muted-foreground'
                  }`}
                >
                  {pillar.status}
                </span>
              </div>
              <p className="text-sm text-muted-foreground">{pillar.description}</p>
            </div>
          ))}
        </div>
      </section>

      <SiteFooter />
    </main>
  )
}
