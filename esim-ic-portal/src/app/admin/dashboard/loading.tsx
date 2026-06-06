import { Skeleton } from "@/components/ui/skeleton";

export default function AdminDashboardLoading() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <Skeleton className="h-9 w-64" />
        <Skeleton className="h-5 w-80" />
      </div>

      {/* Tabs list skeleton */}
      <div className="w-fit mb-4">
        <Skeleton className="h-10 w-[400px] rounded-lg" />
      </div>

      <div className="space-y-4">
        <div className="rounded-md border">
          <div className="p-4 border-b">
            <Skeleton className="h-6 w-full max-w-[1200px]" />
          </div>
          {Array.from({ length: 15 }).map((_, i) => (
            <div key={i} className="p-4 border-b flex justify-between">
              <Skeleton className="h-6 w-1/4" />
              <Skeleton className="h-6 w-1/4" />
              <Skeleton className="h-6 w-1/5" />
              <Skeleton className="h-8 w-24" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
