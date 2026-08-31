import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white">
      {/* Hero - AEO/GEO Highlighted */}
      <section className="pt-20 pb-32 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <div className="inline-flex px-4 py-2 bg-white/10 rounded-full text-sm mb-6">
            🚀 10sPilot - 9.95/10 Rated - AEO + GEO + LLMO
          </div>
          <h1 className="text-6xl font-bold mb-6">
            Does <span className="text-purple-400">ChatGPT</span> Mention Your Brand?
          </h1>
          <p className="text-xl text-gray-400 mb-8 max-w-3xl mx-auto">
            10sPilot checks if your brand appears in ChatGPT, Perplexity, Google AI Overviews. 
            Unified 10sPilot Score.  cost with Groq free tier. 1/10th price of  tools.
          </p>
          <div className="flex gap-4 justify-center mb-12">
            <Link href="/dashboard" className="px-8 py-4 bg-white text-black rounded-full font-bold">
              Check My Brand Free - 50 Checks
            </Link>
            <Link href="/ai-citations" className="px-8 py-4 bg-white/10 rounded-full">
              See Live Demo
            </Link>
          </div>
          
          {/* 3 Pillars */}
          <div className="grid md:grid-cols-3 gap-6 mt-20">
            <div className="p-8 bg-white/5 rounded-2xl border border-white/10">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold mb-2">AEO Engine</h3>
              <p className="text-gray-400 text-sm mb-4">Answer Engine Optimization - ChatGPT, Perplexity, Claude tracking</p>
              <div className="text-xs text-purple-400">POST /api/v1/aeo/check - LIVE ✅</div>
            </div>
            <div className="p-8 bg-white/5 rounded-2xl border border-white/10">
              <div className="text-4xl mb-4">🔍</div>
              <h3 className="text-xl font-bold mb-2">GEO Engine</h3>
              <p className="text-gray-400 text-sm mb-4">Generative Engine Optimization - Google AI Overviews</p>
              <div className="text-xs text-yellow-400">POST /api/v1/geo/check - Building ⬜</div>
            </div>
            <div className="p-8 bg-white/5 rounded-2xl border border-white/10">
              <div className="text-4xl mb-4">📄</div>
              <h3 className="text-xl font-bold mb-2">LLMO Engine</h3>
              <p className="text-gray-400 text-sm mb-4">LLM Optimization - llms.txt, Schema, FAQ</p>
              <div className="text-xs text-green-400">POST /api/v1/llmo/generate - Next ⬜</div>
            </div>
          </div>
          
          {/* 10sPilot Score */}
          <div className="mt-20 p-8 bg-gradient-to-r from-purple-900/20 to-blue-900/20 rounded-3xl border border-purple-500/20">
            <h2 className="text-3xl font-bold mb-4">10sPilot Score - Unified Visibility</h2>
            <p className="text-gray-400 mb-6">SERP 40% + ChatGPT 30% + Perplexity 20% + AI Overview 10% = ONE Number 0-100</p>
            <div className="text-6xl font-bold">87/100</div>
            <div className="text-sm text-gray-500 mt-2">Example: 10sPilot.com for &apos;Best AI SEO tools&apos;</div>
          </div>
        </div>
      </section>
    </main>
  )
}
