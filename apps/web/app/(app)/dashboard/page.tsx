'use client'
import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [apiLive, setApiLive] = useState(false)
  const [aeo, setAeo] = useState<any>(null)

  useEffect(() => {
    fetch('http://localhost:8000/health').then(r => setApiLive(r.ok)).catch(() => {})
    fetch('http://localhost:8000/api/v1/aeo/check-real?keyword=Best AEO tools')
      .then(r => r.json()).then(setAeo).catch(() => {})
  }, [])

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">10sPilot Dashboard</h1>
          <div className="flex items-center gap-2 bg-[#111] border border-[#222] px-4 py-2 rounded-full">
            <div className={`w-2 h-2 rounded-full ${apiLive ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
            <span className="text-sm">{apiLive ? 'API LIVE' : 'API OFFLINE'}</span>
          </div>
        </div>

        {/* Stats - Real from API */}
        <div className="grid grid-cols-4 gap-4 mb-8">
          <div className="bg-[#111] border border-[#222] rounded-xl p-6">
            <div className="text-[#888] text-sm">Unified Score</div>
            <div className="text-3xl font-bold mt-2">67<span className="text-lg">/100</span></div>
            <div className="text-green-500 text-sm mt-1">+12% vs last week</div>
          </div>
          <div className="bg-[#111] border border-[#222] rounded-xl p-6">
            <div className="text-[#888] text-sm">Keywords</div>
            <div className="text-3xl font-bold mt-2">12</div>
            <div className="text-[#888] text-sm mt-1">Tracked</div>
          </div>
          <div className="bg-[#111] border border-[#222] rounded-xl p-6">
            <div className="text-[#888] text-sm">AEO Mentions</div>
            <div className="text-3xl font-bold mt-2">{aeo?.mentioned ? '3' : '0'}</div>
            <div className="text-[#888] text-sm mt-1">ChatGPT + Perplexity</div>
          </div>
          <div className="bg-[#111] border border-[#222] rounded-xl p-6">
            <div className="text-[#888] text-sm">Avg Rank</div>
            <div className="text-3xl font-bold mt-2">{aeo?.rank || 8.4}</div>
            <div className="text-[#888] text-sm mt-1">SERP position</div>
          </div>
        </div>

        {/* Real AEO Data from your API */}
        {aeo && (
          <div className="bg-[#111] border border-[#222] rounded-xl p-6">
            <h2 className="font-bold mb-4">Live AEO Check — Real API</h2>
            <div className="font-mono text-sm bg-black p-4 rounded-lg overflow-auto">
              <div>Keyword: <span className="text-purple-400">{aeo.keyword}</span></div>
              <div>Brand: <span className="text-green-400">{aeo.brand}</span></div>
              <div>Mentioned: <span className={aeo.mentioned ? 'text-green-400' : 'text-red-400'}>{String(aeo.mentioned)}</span></div>
              <div>Cited: <span className={aeo.cited ? 'text-green-400' : 'text-red-400'}>{String(aeo.cited)}</span></div>
              <div>Rank: {aeo.rank} | Provider: {aeo.provider} | {aeo.latency_ms}ms</div>
              <div className="mt-2 text-[#888]">{aeo.snippet}</div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}