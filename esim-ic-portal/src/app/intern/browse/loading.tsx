import { Skeleton } from "@/components/ui/skeleton";

export default function BrowseLoading() {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <Skeleton className="h-9 w-48" />
          <Skeleton className="h-5 w-96" />
        </div>
        <div className="flex flex-col items-end gap-2">
          <Skeleton className="h-10 w-32" />
          <Skeleton className="h-6 w-40" />
        </div>
      </div>
      
      <div className="space-y-4">
        <div className="flex flex-col gap-4 py-4 md:flex-row md:items-center">
          <Skeleton className="h-10 w-[200px]" />
          <Skeleton className="h-10 w-[250px]" />
          <Skeleton className="h-10 w-[180px]" />
          <Skeleton className="h-10 w-[180px]" />
        </div>
        <div className="rounded-md border">
          <div className="p-4 border-b">
            <div className="flex items-center justify-between">
              <Skeleton className="h-6 w-full max-w-[1200px]" />
            </div>
          </div>
          {Array.from({ length: 15 }).map((_, i) => (
            <div key={i} className="p-4 border-b flex justify-between">
              <Skeleton className="h-6 w-1/4" />
              <Skeleton className="h-6 w-1/4" />
              <Skeleton className="h-6 w-1/4" />
              <Skeleton className="h-8 w-24" />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
