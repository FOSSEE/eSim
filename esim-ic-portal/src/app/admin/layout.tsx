import { requireRole } from "@/lib/auth";

import Link from "next/link";
import { LogoutButton } from "@/components/auth/logout-button";

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const user = await requireRole(["ADMIN", "MENTOR"]);

  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b bg-background">
        <div className="flex h-16 items-center px-4 max-w-screen-2xl mx-auto w-full">
          <div className="flex items-center gap-6">
            <Link href="/admin/dashboard" className="font-bold text-lg">
              eSim IC Portal Admin
            </Link>
            <nav className="flex items-center gap-4 text-sm whitespace-nowrap">
              <Link
                href="/admin/dashboard"
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/admin/interns"
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                Interns
              </Link>
              <Link
                href="/admin/catalog"
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                Catalog
              </Link>
              {user.role === "ADMIN" && (
                <>
                  <Link
                    href="/admin/review"
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    Reviews
                  </Link>
                  <Link
                    href="/admin/requests"
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    Requests
                  </Link>
                  <Link
                    href="/admin/batches"
                    className="text-muted-foreground hover:text-primary transition-colors"
                  >
                    Batches
                  </Link>
                </>
              )}
            </nav>
          </div>
          <div className="ml-auto flex items-center space-x-4">
            <span className="text-sm font-medium">{user.name}</span>
            <LogoutButton />
          </div>
        </div>
      </header>
      <main className="flex-1 w-full max-w-screen-2xl mx-auto p-4 md:p-8">
        {children}
      </main>
    </div>
  );
}
