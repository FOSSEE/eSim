import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { notFound } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { formatDistanceToNow, format } from "date-fns";

export default async function AdminInternsDetailPage(props: { params: Promise<{ id: string }> }) {
  const params = await props.params;

  await requireRole(["ADMIN", "MENTOR"]);

  const enrollment = await prisma.batchEnrollment.findUnique({
    where: { id: params.id },
    include: {
      user: true,
      batch: true,
      tasks: {
        include: { ic: { include: { aliases: true } } },
        orderBy: { claimedAt: "desc" },
      },
    },
  });

  if (!enrollment) {
    notFound();
  }

  const activeTasks = enrollment.tasks.filter(t => ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"].includes(t.status));
  const completedTasks = enrollment.tasks.filter(t => t.status === "COMPLETED");
  const failedTasks = enrollment.tasks.filter(t => t.status === "FAILED");
  const totalTasks = enrollment.tasks.length;
  const completionRate = totalTasks > 0 ? Math.round((completedTasks.length / totalTasks) * 100) : 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">{enrollment.user.name || enrollment.user.email}</h1>
        <div className="text-muted-foreground flex gap-4 text-sm items-center">
          <span>{enrollment.user.email}</span>
          <span>&middot;</span>
          <Badge variant="outline">{enrollment.batch.season} {enrollment.batch.year}</Badge>
          <span>&middot;</span>
          <span>Enrolled {format(new Date(enrollment.user.createdAt), "MMM d, yyyy")}</span>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              <span className={activeTasks.length >= 3 ? "text-destructive" : ""}>{activeTasks.length}</span>
              <span className="text-muted-foreground text-lg">/3</span>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{completedTasks.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Failed</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-destructive">{failedTasks.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completion Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{completionRate}%</div>
          </CardContent>
        </Card>
      </div>

      <div className="border rounded-md mt-8">
        <div className="p-4 bg-muted/30 border-b flex justify-between items-center">
          <h2 className="font-semibold text-lg">Task History ({totalTasks})</h2>
        </div>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>IC Name</TableHead>
              <TableHead>Aliases</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Claimed Date</TableHead>
              <TableHead>Completed Date</TableHead>
              <TableHead>Days Taken</TableHead>
              <TableHead>Mentor Note</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {enrollment.tasks.length === 0 ? (
              <TableRow>
                <TableCell colSpan={8} className="text-center h-24 text-muted-foreground">
                  No tasks found for this intern.
                </TableCell>
              </TableRow>
            ) : (
              enrollment.tasks.map((task) => {
                const daysTaken = task.completedAt 
                  ? Math.max(1, Math.round((new Date(task.completedAt).getTime() - new Date(task.claimedAt).getTime()) / (1000 * 60 * 60 * 24)))
                  : null;

                return (
                  <TableRow key={task.id}>
                    <TableCell className="font-mono text-sm">{task.ic.canonicalName}</TableCell>
                    <TableCell className="max-w-[200px] truncate text-xs text-muted-foreground" title={task.ic.aliases.map(a => a.name).join(", ")}>
                      {task.ic.aliases.map(a => a.name).join(", ") || "-"}
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
                    <TableCell>
                      {task.status === "UNDER_REVIEW" ? (
                        <div className="flex gap-2">
                           <Badge variant="default" className="cursor-pointer">Approve</Badge>
                           <Badge variant="destructive" className="cursor-pointer">Reject</Badge>
                        </div>
                      ) : (
                         <span className="text-xs text-muted-foreground">-</span>
                      )}
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
