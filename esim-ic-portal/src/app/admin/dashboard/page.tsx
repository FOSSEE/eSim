import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { ArrowRight, Activity, Users, FileQuestion, CheckCircle2 } from "lucide-react";
import { formatDistanceToNow } from "date-fns";

export default async function AdminDashboardPage() {
  const user = await requireRole(["ADMIN", "MENTOR"]);

  const [
    totalICs,
    unclaimedICs,
    inProgressICs,
    completedICs,
    activeInterns,
    pendingReviews,
    pendingRequests,
    recentActivity,
    awaitingReview,
  ] = await Promise.all([
    prisma.iC.count(),
    prisma.iC.count({
      where: {
        tasks: {
          none: {
            status: {
              in: ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW", "COMPLETED"],
            },
          },
        },
      },
    }),
    prisma.iC.count({
      where: {
        tasks: {
          some: {
            status: {
              in: ["CLAIMED", "IN_PROGRESS"],
            },
          },
        },
      },
    }),
    prisma.iC.count({
      where: {
        tasks: {
          some: {
            status: "COMPLETED",
          },
        },
      },
    }),
    prisma.batchEnrollment.count({
      where: {
        batch: {
          year: 2026,
        },
      },
    }),
    prisma.iCTask.count({
      where: {
        status: "UNDER_REVIEW",
      },
    }),
    prisma.addRequest.count({
      where: {
        status: "PENDING",
      },
    }),
    prisma.iCTask.findMany({
      where: {
        updatedAt: { gte: new Date(Date.now() - 48 * 60 * 60 * 1000) },
      },
      include: {
        ic: true,
        enrollment: {
          include: {
            user: true,
          },
        },
      },
      orderBy: {
        updatedAt: "desc",
      },
      take: 10,
    }),
    prisma.iCTask.findMany({
      where: {
        status: "UNDER_REVIEW",
      },
      include: {
        ic: true,
        enrollment: {
          include: {
            user: true,
          },
        },
      },
      orderBy: {
        updatedAt: "asc",
      },
      take: 10,
    }),
  ]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Admin Dashboard</h1>
          <p className="text-muted-foreground">Welcome back, {user.name}!</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total ICs</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalICs}</div>
            <p className="text-xs text-muted-foreground mt-1 text-balance">
              {unclaimedICs} Unclaimed &middot; {inProgressICs} In Progress &middot; {completedICs} Completed
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Interns (2026)</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{activeInterns}</div>
            <p className="text-xs text-muted-foreground mt-1">Currently enrolled</p>
          </CardContent>
        </Card>
        <Link href="/admin/review" className="block outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-lg">
          <Card className="hover:bg-muted/50 transition-colors h-full cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Pending Reviews</CardTitle>
              <CheckCircle2 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{pendingReviews}</div>
              <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                Needs attention <ArrowRight className="h-3 w-3" />
              </p>
            </CardContent>
          </Card>
        </Link>
        <Link href="/admin/requests" className="block outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-lg">
          <Card className="hover:bg-muted/50 transition-colors h-full cursor-pointer">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Name Requests</CardTitle>
              <FileQuestion className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{pendingRequests}</div>
              <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                New IC additions <ArrowRight className="h-3 w-3" />
              </p>
            </CardContent>
          </Card>
        </Link>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card className="flex flex-col">
          <CardHeader>
            <CardTitle className="text-xl">Awaiting Review</CardTitle>
          </CardHeader>
          <CardContent className="flex-1">
            {awaitingReview.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-6">No tasks require review.</p>
            ) : (
              <div className="border rounded-md">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>IC</TableHead>
                      <TableHead>Intern</TableHead>
                      <TableHead className="text-right">Waited</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {awaitingReview.map((task) => (
                      <TableRow key={task.id}>
                        <TableCell className="font-medium truncate max-w-[150px]" title={task.ic.canonicalName}>
                          {task.ic.canonicalName}
                        </TableCell>
                        <TableCell>{task.enrollment.user.name || task.enrollment.user.email.split('@')[0]}</TableCell>
                        <TableCell className="text-right text-muted-foreground whitespace-nowrap">
                          {formatDistanceToNow(new Date(task.updatedAt), { addSuffix: true })}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
            {pendingReviews > 10 && (
              <div className="mt-4 text-center">
                <Link href="/admin/review" className="text-sm text-primary hover:underline">
                  View all {pendingReviews} pending
                </Link>
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="flex flex-col">
          <CardHeader>
            <CardTitle className="text-xl">Recent Activity (48h)</CardTitle>
          </CardHeader>
          <CardContent className="flex-1">
             {recentActivity.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-6">No activity in the last 48 hours.</p>
            ) : (
              <div className="border rounded-md">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>IC</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="text-right">Time</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {recentActivity.map((task) => (
                      <TableRow key={task.id}>
                        <TableCell className="font-medium truncate max-w-[150px]" title={task.ic.canonicalName}>
                          {task.ic.canonicalName}
                        </TableCell>
                        <TableCell>
                          <Badge variant={task.status === "COMPLETED" ? "default" : task.status === "UNDER_REVIEW" ? "secondary" : "outline"} className="text-[10px] px-1.5 py-0 h-5">
                            {task.status.replace('_', ' ')}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-right text-muted-foreground whitespace-nowrap">
                          {formatDistanceToNow(new Date(task.updatedAt), { addSuffix: true })}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
