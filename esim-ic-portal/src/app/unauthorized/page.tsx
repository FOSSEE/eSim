import Link from "next/link";

export default function UnauthorizedPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-zinc-50">
      <div className="max-w-md w-full space-y-6 p-8 bg-white shadow-xl rounded-2xl text-center border border-red-100">
        <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
          <svg
            className="h-6 w-6 text-red-600"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            aria-hidden="true"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
        </div>
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-zinc-900">
            Access Denied
          </h2>
          <p className="mt-2 text-sm text-zinc-600">
            Your email is not whitelisted. Please use the exact email you
            provided to FOSSEE.
          </p>
        </div>
        <div className="mt-6">
          <Link
            href="/"
            className="w-full flex justify-center py-2.5 px-4 border border-zinc-300 rounded-lg shadow-sm text-sm font-medium text-zinc-700 bg-white hover:bg-zinc-50 transition-colors"
          >
            Return to Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}
