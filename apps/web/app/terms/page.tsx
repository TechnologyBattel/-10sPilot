import Link from 'next/link'

export default function TermsPage() {
  return (
    <main className="min-h-screen bg-black px-4 py-16 text-white sm:px-6 sm:py-24 lg:px-8">
      <div className="mx-auto max-w-3xl">
        <Link className="text-sm font-medium text-purple-300 hover:text-white" href="/">
          Back to 10sPilot
        </Link>
        <h1 className="mt-8 text-3xl font-bold sm:text-4xl">Terms of Service</h1>
        <p className="mt-6 text-gray-400">
          Our terms of service are being prepared and will be published here.
        </p>
      </div>
    </main>
  )
}
