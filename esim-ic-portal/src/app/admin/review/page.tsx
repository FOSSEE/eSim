import { prisma } from "@/lib/prisma";
import { formatDistanceToNow } from "date-fns";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { ReviewActionModal } from "@/components/admin/review-action-modal";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default async function AdminReviewQueuePage() {
  const tasks = await prisma.iCTask.findMany({
    where: { status: "UNDER_REVIEW" },
    include: {
      ic: true,
      enrollment: {
        include: { user: true }
      }
    },
    orderBy: { updatedAt: "asc" }, 
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Review Queue</h1>
        <p className="text-muted-foreground mt-2">
          Approve or reject mapped ICs submitted by interns. Oldest submissions are listed first.
        </p>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>IC Canonical Name</TableHead>
              <TableHead>Intern</TableHead>
              <TableHead>Waiting Time</TableHead>
              <TableHead>Category</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {tasks.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                  No tasks currently awaiting review.
                </TableCell>
              </TableRow>
            ) : (
              tasks.map((task: any) => (
                <TableRow key={task.id}>
                  <TableCell className="font-medium">
                    <Link href={`/admin/catalog/${task.ic.id}`} className="hover:underline text-blue-600">
                      {task.ic.canonicalName}
                    </Link>
                  </TableCell>
                  <TableCell>
                    <Link href={`/admin/interns/${task.enrollment.user.id}`} className="hover:underline">
                      {task.enrollment.user.name || "Unknown"}
                    </Link>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="font-mono">
                      {formatDistanceToNow(task.updatedAt, { addSuffix: true })}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge>{task.ic.category.replace(/_/g, " ")}</Badge>
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                     <ReviewActionModal 
                        taskId={task.id} 
                        icName={task.ic.canonicalName} 
                        internName={task.enrollment.user.name || "Unknown"} 
                        action="approve" 
                     />
                     <ReviewActionModal 
                        taskId={task.id} 
                        icName={task.ic.canonicalName} 
                        internName={task.enrollment.user.name || "Unknown"} 
                        action="reject" 
                     />
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
