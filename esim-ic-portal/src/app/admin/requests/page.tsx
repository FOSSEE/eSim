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
import Link from "next/link";
import { RequestReviewModal } from "@/components/admin/request-review-modal";
import { AddRequestStatus } from "@prisma/client";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default async function AdminRequestsPage({
  searchParams,
}: {
  searchParams: Promise<{ status?: string; page?: string }>;
}) {
  const params = await searchParams;
  const status = (params.status as AddRequestStatus) || "PENDING";
  const page = parseInt(params.page || "1");
  const pageSize = 25;

  const [requests, total] = await Promise.all([
    prisma.addRequest.findMany({
      where: { status },
      include: {
        requester: true,
        reviewer: true,
        suggestedMergeWith: true,
        createdIc: true,
      },
      skip: (page - 1) * pageSize,
      take: pageSize,
      orderBy: { createdAt: "asc" },
    }),
    prisma.addRequest.count({ where: { status } }),
  ]);

  const [pendingCount, approvedCount, mergedCount, rejectedCount] = await Promise.all([
    prisma.addRequest.count({ where: { status: "PENDING" } }),
    prisma.addRequest.count({ where: { status: "APPROVED_AS_NEW" } }),
    prisma.addRequest.count({ where: { status: "MERGED" } }),
    prisma.addRequest.count({ where: { status: "REJECTED" } }),
  ]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">IC Add Requests</h1>
        <p className="text-muted-foreground mt-2">
          Manage IC requests submitted by interns. Merge them with existing ICs or approve as new.
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        <Link
          href={`/admin/requests?status=PENDING`}
          className={cn(
            buttonVariants({ variant: status === "PENDING" ? "default" : "outline" })
          )}
        >
          Pending ({pendingCount})
        </Link>
        <Link
          href={`/admin/requests?status=APPROVED_AS_NEW`}
          className={cn(
            buttonVariants({ variant: status === "APPROVED_AS_NEW" ? "default" : "outline" })
          )}
        >
          Approved ({approvedCount})
        </Link>
        <Link
          href={`/admin/requests?status=MERGED`}
          className={cn(
            buttonVariants({ variant: status === "MERGED" ? "default" : "outline" })
          )}
        >
          Merged ({mergedCount})
        </Link>
        <Link
          href={`/admin/requests?status=REJECTED`}
          className={cn(
            buttonVariants({ variant: status === "REJECTED" ? "default" : "outline" })
          )}
        >
          Rejected ({rejectedCount})
        </Link>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Requested Name</TableHead>
              <TableHead>Requested By</TableHead>
              <TableHead>Date</TableHead>
              <TableHead>Status / Details</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {requests.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                  No {status.toLowerCase()} requests found.
                </TableCell>
              </TableRow>
            ) : (
              requests.map((req) => (
                <TableRow key={req.id}>
                  <TableCell>
                    <div className="font-medium">{req.rawName}</div>
                    <div className="text-xs text-muted-foreground font-mono">
                      Norm: {req.normalizedName}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Link href={`/admin/interns/${req.requesterId}`} className="hover:underline">
                      {req.requester.name}
                    </Link>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="font-mono">
                      {formatDistanceToNow(req.createdAt, { addSuffix: true })}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant={status === "PENDING" ? "secondary" : "default"}>
                      {req.status}
                    </Badge>
                    {req.status === "APPROVED_AS_NEW" && req.createdIc && (
                      <div className="text-xs text-muted-foreground mt-1">
                        Created: <Link href={`/admin/catalog/${req.createdIc.id}`} className="hover:underline text-blue-600">{req.createdIc.canonicalName}</Link>
                      </div>
                    )}
                    {req.status === "MERGED" && req.suggestedMergeWith && (
                      <div className="text-xs text-muted-foreground mt-1">
                        Merged: <Link href={`/admin/catalog/${req.suggestedMergeWith.id}`} className="hover:underline text-blue-600">{req.suggestedMergeWith.canonicalName}</Link>
                      </div>
                    )}
                    {req.status === "REJECTED" && req.reviewNote && (
                      <div className="text-xs text-muted-foreground mt-1 truncate max-w-xs" title={req.reviewNote}>
                        Note: {req.reviewNote}
                      </div>
                    )}
                  </TableCell>
                  <TableCell className="text-right">
                    {status === "PENDING" ? (
                      <RequestReviewModal
                        requestId={req.id}
                        rawName={req.rawName}
                        normalizedName={req.normalizedName || ""}
                        suggestedAliases={req.suggestedAliases || []}
                        internName={req.requester.name}
                      />
                    ) : (
                      <span className="text-sm text-muted-foreground">
                        Reviewed by {req.reviewer?.name}
                      </span>
                    )}
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
