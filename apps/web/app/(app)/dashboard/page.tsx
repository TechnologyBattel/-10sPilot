'use client'

import { useEffect, useState } from 'react'
import {
  getAEOCheck,
  getApiHealth,
  type AEOResult,
} from '@/lib/api-client'

export default function Dashboard() {
  const [apiLive, setApiLive] = useState(false)
  const [aeo, setAeo] = useState<AEOResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function loadDashboard() {
      try {
        setLoading(true)
        setError(null)

        await getApiHealth()

        if (!cancelled) {
          setApiLive(true)
        }

        const results = await getAEOCheck(
          '10sPilot',
          'Best SEO tools',
          ['openai'],
        )

        if (!cancelled) {
          setAeo(results[0] ?? null)
        }
      } catch (err) {
        if (!cancelled) {
          setApiLive(false)
          setError(
            err instanceof Error
              ? err.message
              : 'Unable to connect to API',
          )
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadDashboard()

    return () => {
      cancelled = true
    }
  }, [])

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-8">
      <div className="max-w-6xl mx-auto">

        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">
            10sPilot Dashboard
          </h1>

          <div className="flex items-center gap-2 bg-[#111] border border-[#222] px-4 py-2 rounded-full">
            <div
              className={`w-2 h-2 rounded-full ${
                apiLive
                  ? 'bg-green-500 animate-pulse'
                  : 'bg-red-500'
              }`}
            />

            <span className="text-sm">
              {apiLive ? 'API LIVE' : 'API OFFLINE'}
            </span>
          </div>
        </div>

        {error && (
          <div className="mb-6 rounded-xl border border-red-900 bg-red-950/30 p-4 text-red-300">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">

          <div className="bg-[#111] border border-[#222] rounded-xl p-6">
            <div className="text-[#888] text-sm">
              AEO Visibility
            </div>

            <div className="text-3xl font-bold mt-2">
              {loading
                ? '…'
                : aeo?.mentioned
                  ? 'YES'
                  : 'NO'}
            </div>

            <div className="text-[#888] text-sm mt-1">
              Live provider check
            </div>
          </div>

          <div className="bg-[#111] border border-[#222] rounded-xl p-6">
            <div className="text-[#888] text-sm">
              AEO Position
            </div>

            <div className="text-3xl font-bold mt-2">
              {loading
                ? '…'
                : aeo?.position != null
                  ? `#${aeo.position}`
                  : '—'}
            </div>

            <div className="text-[#888] text-sm mt-1">
              Answer position
            </div>
          </div>

          <div className="bg-[#111] border border-[#222] rounded-xl p-6">
            <div className="text-[#888] text-sm">
              Provider
            </div>

            <div className="text-3xl font-bold mt-2">
              {loading
                ? '…'
                : aeo?.provider ?? '—'}
            </div>

            <div className="text-[#888] text-sm mt-1">
              Current AEO check
            </div>
          </div>

        </div>

        <div className="bg-[#111] border border-[#222] rounded-xl p-6">
          <div className="flex justify-between items-center mb-5">
            <div>
              <h2 className="font-bold text-lg">
                Live AEO Check
              </h2>

              <p className="text-sm text-[#888] mt-1">
                Real data returned by the AEO API
              </p>
            </div>
          </div>

          {loading ? (
            <div className="text-[#888]">
              Running AEO check…
            </div>
          ) : aeo ? (
            <div className="space-y-4">

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                <div className="bg-black rounded-lg p-4">
                  <div className="text-[#666] text-xs uppercase">
                    Query
                  </div>
                  <div className="mt-1">
                    {aeo.query}
                  </div>
                </div>

                <div className="bg-black rounded-lg p-4">
                  <div className="text-[#666] text-xs uppercase">
                    Brand
                  </div>
                  <div className="mt-1 text-green-400">
                    {aeo.brand}
                  </div>
                </div>

                <div className="bg-black rounded-lg p-4">
                  <div className="text-[#666] text-xs uppercase">
                    Mentioned
                  </div>
                  <div
                    className={`mt-1 ${
                      aeo.mentioned
                        ? 'text-green-400'
                        : 'text-red-400'
                    }`}
                  >
                    {aeo.mentioned ? 'Yes' : 'No'}
                  </div>
                </div>

                <div className="bg-black rounded-lg p-4">
                  <div className="text-[#666] text-xs uppercase">
                    Position
                  </div>
                  <div className="mt-1">
                    {aeo.position != null
                      ? `#${aeo.position}`
                      : 'Not ranked'}
                  </div>
                </div>

              </div>

              <div className="bg-black rounded-lg p-4">
                <div className="text-[#666] text-xs uppercase mb-2">
                  Context
                </div>

                <p className="text-sm text-[#aaa] leading-6">
                  {aeo.context ?? 'No context returned.'}
                </p>
              </div>

            </div>
          ) : (
            <div className="text-[#888]">
              No AEO result available.
            </div>
          )}
        </div>

      </div>
    </div>
  )
}
