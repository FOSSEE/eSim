"use client";

import { ColumnDef } from "@tanstack/react-table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { claimTaskAction } from "@/app/actions/intern-actions";
import { toast } from "sonner";
import { useTransition } from "react";

export const columns: ColumnDef<any>[] = [
  {
    accessorKey: "canonicalName",
    header: "IC Name",
    cell: ({ row }) => <div className="font-mono font-medium">{row.getValue("canonicalName")}</div>,
  },
  {
    accessorKey: "aliases",
    header: "Aliases",
    cell: ({ row }) => {
      const aliases = row.original.aliases || [];
      return (
        <div className="flex flex-wrap gap-1">
          {aliases.map((a: any) => (
            <Badge key={a.id} variant="secondary" className="text-xs font-mono py-0 h-5">
              {a.name}
            </Badge>
          ))}
        </div>
      );
    },
  },
  {
    accessorKey: "category",
    header: "Category",
    cell: ({ row }) => <div>{(row.getValue("category") as string).replace(/_/g, ' ')}</div>,
  },
  {
    accessorKey: "technology",
    header: "Tech",
  },
  {
    accessorKey: "description",
    header: "Description",
    cell: ({ row }) => {
      const desc = row.getValue("description") as string | undefined;
      return (
        <div className="max-w-[200px] truncate text-xs text-muted-foreground whitespace-nowrap" title={desc || ""}>
          {desc || "-"}
        </div>
      );
    }
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const ic = row.original;
      return <ClaimButton icId={ic.id} canClaim={ic.canClaim} activeTaskId={ic.activeTaskId} />;
    },
  },
];

function ClaimButton({ icId, canClaim, activeTaskId }: { icId: string, canClaim: boolean, activeTaskId?: string }) {
  const [isPending, startTransition] = useTransition();

  if (activeTaskId) {
    return <Button variant="secondary" disabled size="sm">Claimed</Button>;
  }

  if (!canClaim) {
    return null;
  }

  return (
    <Button 
      size="sm"
      disabled={isPending}
      onClick={() => {
        startTransition(async () => {
          try {
            const res = await claimTaskAction(icId);
            if (res?.error) {
              toast.error(res.error);
            } else {
              toast.success("IC claimed successfully!");
            }
          } catch (e: any) {
            toast.error(e.message || "Failed to claim IC");
          }
        });
      }}
    >
      {isPending ? "Claiming..." : "Claim"}
    </Button>
  );
}
