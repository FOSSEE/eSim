import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { formatDistanceToNow, format } from "date-fns";
import { ICMetadataManager } from "@/components/admin/ic-metadata-manager";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ExternalLink } from "lucide-react";

export default async function AdminICDetailPage(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;

  await requireRole(["ADMIN", "MENTOR"]);

  const ic = await prisma.iC.findUnique({
    where: { id: params.id },
    include: {
      aliases: true,
      tasks: {
        include: { enrollment: { include: { user: true, batch: true } } },
        orderBy: { claimedAt: "desc" },
      },
      createdFromRequest: { include: { requester: true } },
    },
  });

  if (!ic) {
    notFound();
  }

  return (
    <div className="space-y-8">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-4xl font-mono font-bold tracking-tight">{ic.canonicalName}</h1>
          <div className="flex gap-2">
            {/* Merge function placeholder */}
            <Button variant="outline">Merge into another IC</Button>
          </div>
        </div>
        
        {ic.createdFromRequest && (
          <div className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
            Added from request by
            <Link href={`/admin/interns/${ic.createdFromRequest.requesterId}`} className="font-medium hover:underline text-primary">
              {ic.createdFromRequest.requester.name || ic.createdFromRequest.requester.email.split('@')[0]}
            </Link>
          </div>
        )}
      </div>

      <ICMetadataManager ic={{
        id: ic.id,
        description: ic.description,
        category: ic.category,
        technology: ic.technology,
        datasheetUrl: ic.datasheetUrl,
        aliases: ic.aliases.map(a => ({ id: a.id, name: a.name })),
      }} />

      <div className="border rounded-md mt-12 bg-card">
        <div className="p-4 bg-muted/30 border-b flex justify-between items-center">
          <h2 className="font-semibold text-lg">Assignment History ({ic.tasks.length})</h2>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Intern Name</TableHead>
              <TableHead>Batch</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Claimed Date</TableHead>
              <TableHead>Completed Date</TableHead>
              <TableHead>Days Taken</TableHead>
              <TableHead>Mentor Note</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {ic.tasks.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center h-24 text-muted-foreground">
                  This IC has never been assigned.
                </TableCell>
              </TableRow>
            ) : (
              ic.tasks.map((task) => {
                const daysTaken = task.completedAt 
                  ? Math.max(1, Math.round((new Date(task.completedAt).getTime() - new Date(task.claimedAt).getTime()) / (1000 * 60 * 60 * 24)))
                  : null;

                return (
                  <TableRow key={task.id}>
                    <TableCell className="font-medium">
                      <Link href={`/admin/interns/${task.enrollment.id}`} className="hover:underline text-primary">
                        {task.enrollment.user.name || task.enrollment.user.email}
                      </Link>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{task.enrollment.batch.season} {task.enrollment.batch.year}</Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant={
                        task.status === "COMPLETED" ? "default" : 
                        task.status === "FAILED" ? "destructive" : 
                        "secondary"
                      } className="text-xs">
                        {task.status.replace("_", " ")}
                      </Badge>
                    </TableCell>
                    <TableCell className="whitespace-nowrap">{format(new Date(task.claimedAt), "MMM d, yyyy")}</TableCell>
                    <TableCell className="whitespace-nowrap">
                      {task.completedAt ? format(new Date(task.completedAt), "MMM d, yyyy") : "-"}
                    </TableCell>
                    <TableCell>{daysTaken ? `${daysTaken} days` : "-"}</TableCell>
                    <TableCell className="text-sm max-w-[200px] truncate" title={task.mentorNote || ""}>
                      {task.mentorNote || "-"}
                    </TableCell>
                  </TableRow>
                )
              })
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
