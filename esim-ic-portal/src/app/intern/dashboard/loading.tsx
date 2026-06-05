import { Skeleton } from "@/components/ui/skeleton";

export default function InternDashboardLoading() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <Skeleton className="h-9 w-64" />
          <Skeleton className="h-5 w-80" />
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-6">
          {/* Active Tasks Skeleton */}
          <div className="rounded-xl border bg-card text-card-foreground shadow">
            <div className="p-6 flex flex-row items-center justify-between pb-2 space-y-0">
              <Skeleton className="h-6 w-32" />
              <Skeleton className="h-4 w-4 rounded-full" />
            </div>
            <div className="p-6 pt-4 space-y-4">
              {Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="flex items-center justify-between border-b pb-4 last:border-0 last:pb-0">
                  <div className="space-y-1">
                    <Skeleton className="h-5 w-48" />
                    <Skeleton className="h-4 w-64" />
                  </div>
                  <Skeleton className="h-9 w-24" />
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-6">
          {/* Recent Activity / Progress Skeleton */}
          <div className="rounded-xl border bg-card text-card-foreground shadow">
            <div className="p-6 flex flex-row items-center justify-between pb-2 space-y-0">
              <Skeleton className="h-6 w-32" />
              <Skeleton className="h-4 w-4 rounded-full" />
            </div>
            <div className="p-6 pt-4 space-y-4">
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="flex items-center border-b pb-4 last:border-0 last:pb-0">
                  <Skeleton className="h-10 w-10 rounded-full mr-4" />
                  <div className="space-y-1 w-full">
                    <div className="flex justify-between w-full">
                      <Skeleton className="h-4 w-32" />
                      <Skeleton className="h-4 w-20" />
                    </div>
                    <Skeleton className="h-4 w-48" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
