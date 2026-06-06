import { getCurrentUser } from "@/lib/auth";
import { redirect } from "next/navigation";
import { signIn } from "@/auth";

export default async function RootPage() {
  const user = await getCurrentUser();
  
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-zinc-50">
        <div className="max-w-md w-full space-y-8 p-8 bg-white shadow-xl rounded-2xl text-center border border-zinc-100">
          <div className="space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">eSim IC Portal</h1>
            <p className="text-sm text-muted-foreground">Please sign in to access your dashboard.</p>
          </div>
          <form
            action={async () => {
              "use server"
              await signIn("google")
            }}
          >
            <button
              type="submit"
              className="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-zinc-900 hover:bg-zinc-800 transition-colors"
            >
              Sign in with Google
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (user.role === "INTERN") {
    redirect("/intern/dashboard");
  }

  if (user.role === "ADMIN" || user.role === "MENTOR") {
    redirect("/admin/dashboard");
  }

  return <div>Unknown role</div>;
}
