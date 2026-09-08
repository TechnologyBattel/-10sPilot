import Link from 'next/link'

import { SiteFooter } from '@/components/layout/site-footer'

function AeoIcon() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="32"
      height="32"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      strokeLinecap="round"
      strokeLinejoin="round"
      className="text-purple-400"
      aria-hidden="true"
    >
      <circle cx="11" cy="11" r="8" />
      <path d="m21 21-4.35-4.35" />
      <path d="M11 8v6M8 11h6" />
    </svg>
  )
}

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-black text-white">
      {/* Hero */}
      <section className="px-4 py-16 sm:px-6 sm:py-24">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-4xl font-bold leading-tight sm:text-6xl mb-6">
            Is Your Brand Visible in{' '}
            <span className="text-purple-400">AI Search?</span>
          </h1>
          <p className="text-lg text-gray-400 mb-8 max-w-3xl mx-auto sm:text-xl">
            Diagnose your brand&apos;s visibility in AI search, AI answer engines, and AI overviews.
          </p>
          <div className="flex gap-4 justify-center mb-12">
            <Link
              href="/dashboard"
              className="px-8 py-4 bg-white text-black rounded-full font-bold"
            >
              Open AEO Diagnostic
            </Link>
          </div>

          {/* AEO Engine Feature Card */}
          <div className="flex justify-center mt-20">
            <div className="p-8 bg-white/5 rounded-2xl border border-white/10 max-w-md w-full text-left">
              <div className="mb-4">
                <AeoIcon />
              </div>
              <h3 className="text-xl font-bold mb-2">
                AEO Engine — Answer Engine Optimization
              </h3>
              <p className="text-gray-400 text-sm">
                Review brand mention status, answer position when available, and response context.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="px-4 py-16 border-t border-white/10 sm:px-6 sm:py-24">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl font-bold mb-12 sm:text-4xl sm:mb-16">How It Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-400 font-bold text-lg">
                1
              </div>
              <h3 className="font-semibold text-lg">Open the diagnostic</h3>
              <p className="text-gray-400 text-sm">Start a live AEO visibility check from your dashboard.</p>
            </div>
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-400 font-bold text-lg">
                2
              </div>
              <h3 className="font-semibold text-lg">We evaluate visibility</h3>
              <p className="text-gray-400 text-sm">
                The engine checks whether your brand is mentioned in an AI answer.
              </p>
            </div>
            <div className="flex flex-col items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-purple-500/20 border border-purple-500/40 flex items-center justify-center text-purple-400 font-bold text-lg">
                3
              </div>
              <h3 className="font-semibold text-lg">Review the result</h3>
              <p className="text-gray-400 text-sm">
                See mention status, answer position when available, and response context.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="px-4 py-16 border-t border-white/10 sm:px-6 sm:py-24">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold mb-12 text-center sm:text-4xl">
            Frequently Asked Questions
          </h2>
          <div className="space-y-8">
            <div>
              <h3 className="text-lg font-semibold mb-2">What does the AEO diagnostic check?</h3>
              <p className="text-gray-400">
                It checks whether an AI answer mentions your brand and returns answer position
                and context when available.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">
                How is this different from regular SEO?
              </h3>
              <p className="text-gray-400">
                No. It adds a focused view of brand visibility in AI search alongside your
                existing search strategy.
              </p>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-2">What results will I see?</h3>
              <p className="text-gray-400">
                The diagnostic shows mention status, reported answer position, and response context.
              </p>
            </div>
          </div>
        </div>
      </section>

      <SiteFooter />
    </main>
  )
}
