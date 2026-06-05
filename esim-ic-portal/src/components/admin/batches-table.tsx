"use client";

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Trash2 } from "lucide-react";
import { removeBatchEnrollmentAction } from "@/app/actions/batch-actions";
import { toast } from "sonner";
import { useRouter } from "next/navigation";

export function BatchesTable({ data }: { data: any[] }) {
  const router = useRouter();

  const handleRemove = async (enrollmentId: string) => {
    if (!confirm("Are you sure you want to remove this intern from the batch?")) return;
    try {
      await removeBatchEnrollmentAction(enrollmentId);
      toast.success("Enrollment removed");
      router.refresh();
    } catch (error: any) {
      toast.error(error.message || "Failed to remove enrollment");
    }
  };

  const columns = [
    {
      accessorKey: "user.email",
      header: "Email",
    },
    {
      accessorKey: "user.name",
      header: "Name",
      cell: ({ row }: any) => {
        const name = row.original.user.name;
        return name === "Pending" ? (
          <span className="text-muted-foreground italic">Pending Login</span>
        ) : (
          name
        );
      },
    },
    {
      accessorKey: "createdAt",
      header: "Joined Date",
      cell: ({ row }: any) => {
        return new Date(row.original.user.createdAt).toLocaleDateString();
      },
    },
    {
      id: "actions",
      header: "Actions",
      cell: ({ row }: any) => {
        return (
          <Button
            variant="ghost"
            size="icon"
            className="text-red-500 hover:text-red-700 hover:bg-red-50"
            onClick={() => handleRemove(row.original.id)}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        );
      },
    },
  ];

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map((headerGroup) => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map((header) => {
                return (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                );
              })}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows?.length ? (
            table.getRowModel().rows.map((row) => (
              <TableRow key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <TableCell key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </TableCell>
                ))}
              </TableRow>
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={columns.length} className="h-24 text-center text-muted-foreground">
                No interns found in this batch.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </div>
  );
}
