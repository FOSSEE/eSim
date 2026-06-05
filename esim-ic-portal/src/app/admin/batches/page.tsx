import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { BatchSelector } from "@/components/admin/batch-selector";
import { BulkAddDialog } from "@/components/admin/bulk-add-dialog";
import { BatchesTable } from "@/components/admin/batches-table";

export default async function AdminBatchesPage({
  searchParams,
}: {
  searchParams: Promise<{ batchId?: string }>;
}) {
  await requireRole("ADMIN");
  
  const params = await searchParams;

  const batches = await prisma.batch.findMany({
    orderBy: [{ year: "desc" }, { season: "desc" }],
  });

  if (batches.length === 0) {
    return (
      <div className="p-8 text-center text-muted-foreground">
        No batches found in the database. Please run the seed script.
      </div>
    );
  }

  const selectedBatchId = params.batchId || batches[0].id;
  const activeBatch = batches.find((b) => b.id === selectedBatchId) || batches[0];

  const enrollments = await prisma.batchEnrollment.findMany({
    where: { batchId: activeBatch.id },
    include: {
      user: true,
    },
    orderBy: {
      user: {
        createdAt: "desc",
      },
    },
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Batch Management</h1>
        <p className="text-muted-foreground">
          Manage intern rosters and pre-authorized email whitelists.
        </p>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <BatchSelector batches={batches} currentBatchId={activeBatch.id} />
          <div className="text-sm text-muted-foreground">
            {enrollments.length} intern{enrollments.length !== 1 ? "s" : ""} enrolled
          </div>
        </div>
        <BulkAddDialog batchId={activeBatch.id} />
      </div>

      <BatchesTable data={enrollments} />
    </div>
  );
}
