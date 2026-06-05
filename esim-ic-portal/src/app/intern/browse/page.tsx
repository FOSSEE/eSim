import { requireRole } from "@/lib/auth";
import { getIcsForLobby } from "@/lib/queries";
import { prisma } from "@/lib/prisma";
import { DataTable } from "./data-table";
import { columns } from "./columns";
import { RequestIcModal } from "@/components/intern/request-ic-modal";

export default async function BrowsePage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>
}) {
  const user = await requireRole("INTERN");
  const params = await searchParams;
  
  const search = typeof params.search === 'string' ? params.search : undefined;
  const description = typeof params.description === 'string' ? params.description : undefined;
  const category = typeof params.category === 'string' ? params.category : undefined;
  const technology = typeof params.technology === 'string' ? params.technology : undefined;
  const showAll = params.showAll === 'true';
  const page = typeof params.page === 'string' ? parseInt(params.page, 10) : 1;
  const pageSize = 50;

  const activeEnrollment = await prisma.batchEnrollment.findFirst({
    where: { userId: user.id },
    include: { batch: true, tasks: true }
  });

  if (!activeEnrollment) {
    return <div>No active enrollment found.</div>;
  }

  const { items, total } = await getIcsForLobby({
    search,
    description,
    category,
    technology,
    showAll,
    page,
    pageSize,
    batchId: activeEnrollment.batchId
  });

  const activeTaskCount = activeEnrollment.tasks.filter(t => ["CLAIMED", "IN_PROGRESS"].includes(t.status)).length;
  const canClaim = activeTaskCount < 3;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-bold tracking-tight">Browse ICs</h1>
          <p className="text-muted-foreground">Find and claim ICs for your project. You can claim up to 3 ICs at a time.</p>
        </div>
        <div className="flex flex-col items-end gap-1">
          <RequestIcModal />
          <div className="px-2 py-1 bg-amber-50 dark:bg-amber-950/30 text-amber-800 dark:text-amber-400 border border-amber-200 dark:border-amber-900/50 rounded flex items-center gap-1 shadow-sm mt-1">
            <span className="text-[10px] uppercase font-bold tracking-wider">Note</span>
            <span className="text-[11px] font-medium text-amber-900/80 dark:text-amber-300">Search aliases thoroughly!</span>
          </div>
        </div>
      </div>
      
      <DataTable 
        columns={columns} 
        data={items.map(ic => ({ ...ic, canClaim, activeTaskId: ic.tasks.find(t => ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"].includes(t.status) && t.enrollment.batchId === activeEnrollment.batchId)?.id }))}
        total={total}
      />
    </div>
  );
}
