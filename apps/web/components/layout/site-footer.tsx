import Link from 'next/link'

export function SiteFooter() {
  return (
    <footer className="border-t border-white/10 px-4 py-8 text-sm text-gray-400 sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-7xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <p>10sPilot</p>
        <nav aria-label="Legal" className="flex gap-6">
          <Link className="transition-colors hover:text-white" href="/privacy">
            Privacy Policy
          </Link>
          <Link className="transition-colors hover:text-white" href="/terms">
            Terms of Service
          </Link>
        </nav>
      </div>
    </footer>
  )
}
