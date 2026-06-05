import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import Link from "next/link";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDistanceToNow } from "date-fns";
import { InternsFilter } from "@/components/admin/interns-filter";

export default async function AdminInternsPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  await requireRole(["ADMIN", "MENTOR"]);

  const params = await searchParams;

  const search = typeof params.search === "string" ? params.search : "";
  const page = typeof params.page === "string" ? parseInt(params.page, 10) : 1;
  const pageSize = 25;
  const sort = typeof params.sort === "string" ? params.sort : "name";
  const order = typeof params.order === "string" ? params.order : "asc";

  const interns = await prisma.batchEnrollment.findMany({
    where: {
      user: search ? { name: { contains: search, mode: "insensitive" } } : undefined,
    },
    include: {
      user: true,
      batch: true,
      tasks: { select: { status: true, updatedAt: true } },
    },
    skip: (page - 1) * pageSize,
    take: pageSize,
    orderBy: { user: { name: (order as any) } }, // Simplified sort for now
  });

  const totalInterns = await prisma.batchEnrollment.count({
    where: {
      user: search ? { name: { contains: search, mode: "insensitive" } } : undefined,
    },
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Admin Interns Table</h1>
      </div>

      <InternsFilter />

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Batch</TableHead>
              <TableHead>Active Tasks</TableHead>
              <TableHead>Completed</TableHead>
              <TableHead>Failed</TableHead>
              <TableHead>Last Activity</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {interns.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center h-24 text-muted-foreground">
                  No interns found.
                </TableCell>
              </TableRow>
            ) : (
              interns.map((enrollment) => {
                const activeTasks = enrollment.tasks.filter(t => ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"].includes(t.status)).length;
                const completedTasks = enrollment.tasks.filter(t => t.status === "COMPLETED").length;
                const failedTasks = enrollment.tasks.filter(t => t.status === "FAILED").length;
                
                const lastActivity = enrollment.tasks.length > 0 
                  ? new Date(Math.max(...enrollment.tasks.map(t => new Date(t.updatedAt).getTime())))
                  : null;

                return (
                  <TableRow key={enrollment.id}>
                    <TableCell className="font-medium">
                      <Link href={`/admin/interns/${enrollment.id}`} className="hover:underline text-primary">
                        {enrollment.user.name || enrollment.user.email}
                      </Link>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{enrollment.batch.season} {enrollment.batch.year}</Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant={activeTasks >= 3 ? "destructive" : "secondary"}>
                        {activeTasks}/3
                      </Badge>
                    </TableCell>
                    <TableCell>{completedTasks}</TableCell>
                    <TableCell className={failedTasks > 0 ? "text-destructive font-medium" : ""}>
                      {failedTasks}
                    </TableCell>
                    <TableCell className="text-muted-foreground">
                      {lastActivity ? formatDistanceToNow(lastActivity, { addSuffix: true }) : "No activity"}
                    </TableCell>
                    <TableCell>
                      <Link href={`/admin/interns/${enrollment.id}`}>
                        <Button variant="ghost" size="sm">View</Button>
                      </Link>
                    </TableCell>
                  </TableRow>
                )
              })
            )}
          </TableBody>
        </Table>
      </div>
      
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <div>
          Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, totalInterns)} of {totalInterns} interns.
        </div>
        <div className="space-x-2">
          <Link href={`?page=${page - 1}&search=${search}`} className={page <= 1 ? "pointer-events-none opacity-50" : ""}>
            <Button variant="outline" size="sm" disabled={page <= 1}>Previous</Button>
          </Link>
          <Link href={`?page=${page + 1}&search=${search}`} className={page * pageSize >= totalInterns ? "pointer-events-none opacity-50" : ""}>
            <Button variant="outline" size="sm" disabled={page * pageSize >= totalInterns}>Next</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
