import { requireRole } from "@/lib/auth";
import { getInternDashboardData } from "@/lib/queries";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatDistanceToNow } from "date-fns";
import { updateTaskStatus } from "@/app/actions/intern-actions";
import { AlertTriangle, ExternalLink, CalendarDays } from "lucide-react";
import Link from 'next/link';

export default async function InternDashboardPage() {
  const user = await requireRole("INTERN");
  const data = await getInternDashboardData(user.id);

  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center">
        <AlertTriangle className="h-10 w-10 text-yellow-500 mb-4" />
        <h2 className="text-xl font-semibold">No Active Enrollment</h2>
        <p className="text-muted-foreground mt-2">You are not currently enrolled in any batch.</p>
      </div>
    );
  }

  const activeTasks = data.tasks.filter(t => ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"].includes(t.status));
  const activeTaskCountForLimit = data.tasks.filter(t => ["CLAIMED", "IN_PROGRESS"].includes(t.status)).length;
  const completedCount = data.tasks.filter(t => t.status === "COMPLETED").length;
  const failedCount = data.tasks.filter(t => t.status === "FAILED").length;
  const hasReachedLimit = activeTaskCountForLimit >= 3;

  function StatusBadge({ status }: { status: string }) {
    switch(status) {
      case "CLAIMED": return <Badge className="bg-blue-500">Claimed</Badge>;
      case "IN_PROGRESS": return <Badge className="bg-yellow-500">In Progress</Badge>;
      case "UNDER_REVIEW": return <Badge className="bg-purple-500">Under Review</Badge>;
      case "COMPLETED": return <Badge className="bg-green-500">Completed</Badge>;
      case "FAILED": return <Badge variant="destructive">Failed</Badge>;
      default: return <Badge variant="outline">{status}</Badge>;
    }
  }

  return (
    <div className="space-y-8">
      <Card className="border-l-4 border-l-primary">
        <CardHeader className="pb-3">
          <div className="flex justify-between items-start">
            <div>
              <CardDescription className="flex items-center gap-1.5 mb-1">
                <CalendarDays className="h-3.5 w-3.5" />
                {data.batch.label} Batch
              </CardDescription>
              <CardTitle className="text-3xl">{user.name}</CardTitle>
            </div>
            <Badge variant="secondary" className="text-sm px-3 py-1">
              Active: {activeTaskCountForLimit}/3
            </Badge>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-6 text-sm">
            <div className="flex flex-col">
              <span className="text-muted-foreground mb-1">Total Completed</span>
              <span className="font-semibold text-lg">{completedCount}</span>
            </div>
            <div className="flex flex-col">
              <span className="text-muted-foreground mb-1">Failed Attempts</span>
              <span className="font-semibold text-lg">{failedCount}</span>
            </div>
          </div>
          
          {hasReachedLimit && (
            <div className="mt-6 bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200 p-3.5 rounded-lg flex items-start gap-3 border border-yellow-200 dark:border-yellow-800/30">
              <AlertTriangle className="h-5 w-5 mt-0.5 shrink-0" />
              <div className="text-sm font-medium">
                You have reached the 3-task limit. Complete or submit a task to claim more.
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold tracking-tight">Active Tasks</h2>
          {!hasReachedLimit && (
             <Button variant="outline" size="sm">
               <Link href="/intern/browse">Claim New IC</Link>
             </Button>
          )}
        </div>
        
        {activeTasks.length === 0 ? (
          <div className="text-center p-8 border rounded-lg bg-muted/40 border-dashed">
            <div className="text-muted-foreground mb-4">No active tasks currently.</div>
            <Button>
               <Link href="/intern/browse">Browse Catalog to Claim</Link>
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {activeTasks.map(task => (
              <Card key={task.id} className="flex flex-col">
                <CardHeader className="pb-3">
                  <div className="flex justify-between items-start mb-2">
                    <StatusBadge status={task.status} />
                    {task.ic.datasheetUrl && (
                      <a href={task.ic.datasheetUrl} target="_blank" rel="noreferrer" className="text-muted-foreground hover:text-primary transition-colors">
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    )}
                  </div>
                  <CardTitle className="font-mono text-2xl truncate" title={task.ic.canonicalName}>
                    {task.ic.canonicalName}
                  </CardTitle>
                  <CardDescription className="line-clamp-2 min-h-10 mt-1">
                    {task.ic.description || "No description provided."}
                  </CardDescription>
                </CardHeader>
                <CardContent className="flex-1">
                  <div className="flex flex-wrap gap-1.5 mb-4">
                    <Badge variant="outline" className="bg-muted/50">{task.ic.category.replace(/_/g, ' ')}</Badge>
                    <Badge variant="outline" className="bg-muted/50 text-xs">{task.ic.technology}</Badge>
                  </div>
                  
                  {task.ic.aliases.length > 0 && (
                    <div className="space-y-1.5 mb-4">
                      <div className="text-xs text-muted-foreground font-medium">Aliases</div>
                      <div className="flex flex-wrap gap-1">
                        {task.ic.aliases.map(a => (
                          <Badge key={a.id} variant="secondary" className="text-xs py-0 h-5 font-mono">{a.name}</Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {task.status === "FAILED" && task.mentorNote && (
                    <div className="bg-destructive/10 text-destructive text-xs p-3 rounded-md border border-destructive/20 mt-4">
                      <strong>Mentor Note:</strong> {task.mentorNote}
                    </div>
                  )}
                  {task.status === "CLAIMED" && task.mentorNote && (
                    <div className="bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200 text-xs p-3 rounded-md border border-yellow-200 dark:border-yellow-800/30 mt-4">
                      <strong>Returned Note:</strong> {task.mentorNote}
                    </div>
                  )}
                </CardContent>
                <CardFooter className="pt-0 border-t bg-muted/20 flex-col items-stretch gap-3 pb-3 mt-auto">
                  <div className="text-[10px] text-muted-foreground w-full py-2">
                    Claimed {formatDistanceToNow(new Date(task.claimedAt), { addSuffix: true })}
                  </div>
                  
                  <div className="w-full">
                  {task.status === "CLAIMED" && (
                    <form action={updateTaskStatus}>
                      <input type="hidden" name="taskId" value={task.id} />
                      <input type="hidden" name="status" value="IN_PROGRESS" />
                      <Button type="submit" className="w-full" size="sm">Mark In Progress</Button>
                    </form>
                  )}
                  {task.status === "IN_PROGRESS" && (
                    <form action={updateTaskStatus}>
                      <input type="hidden" name="taskId" value={task.id} />
                      <input type="hidden" name="status" value="UNDER_REVIEW" />
                      <Button type="submit" className="w-full bg-yellow-600 hover:bg-yellow-700" size="sm">Submit for Review</Button>
                    </form>
                  )}
                  {task.status === "UNDER_REVIEW" && (
                    <Button disabled className="w-full" size="sm" variant="secondary">Awaiting Mentor Review</Button>
                  )}
                  </div>
                </CardFooter>
              </Card>
            ))}
          </div>
        )}
      </div>

      {data.tasks.filter(t => !["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"].includes(t.status)).length > 0 && (
        <div className="mt-12">
          <h2 className="text-xl font-bold tracking-tight mb-4">Task History</h2>
          <div className="border rounded-md">
            <div className="grid grid-cols-4 whitespace-nowrap overflow-x-auto gap-4 p-4 border-b font-medium text-sm text-muted-foreground bg-muted/50">
              <div>IC Name</div>
              <div>Category</div>
              <div>Status</div>
              <div>Last Updated</div>
            </div>
            <div className="divide-y">
              {data.tasks.filter(t => !["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"].includes(t.status)).map(task => (
                <div key={task.id} className="grid grid-cols-4 whitespace-nowrap overflow-x-auto gap-4 p-4 items-center text-sm">
                  <div className="font-mono font-medium">{task.ic.canonicalName}</div>
                  <div className="text-muted-foreground truncate">{task.ic.category.replace(/_/g, ' ')}</div>
                  <div><StatusBadge status={task.status} /></div>
                  <div className="text-muted-foreground">{new Date(task.updatedAt).toLocaleDateString()}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
