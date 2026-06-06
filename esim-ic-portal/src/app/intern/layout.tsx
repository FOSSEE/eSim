import { requireRole } from "@/lib/auth";

import Link from "next/link";
import { LogoutButton } from "@/components/auth/logout-button";

export default async function InternLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const user = await requireRole("INTERN");

  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b bg-background">
        <div className="flex h-16 items-center px-4 max-w-7xl mx-auto w-full">
          <div className="flex items-center gap-6">
            <Link href="/intern/dashboard" className="font-bold text-lg">
              eSim IC Portal
            </Link>
            <nav className="flex items-center gap-4 text-sm whitespace-nowrap">
              <Link
                href="/intern/dashboard"
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/intern/browse"
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                Browse ICs
              </Link>
            </nav>
          </div>
          <div className="ml-auto flex items-center space-x-4">
            <span className="text-sm font-medium">{user.name}</span>
            <LogoutButton />
          </div>
        </div>
      </header>
      <main className="flex-1 w-full max-w-7xl mx-auto p-4 md:p-8">
        {children}
      </main>
    </div>
  );
}
