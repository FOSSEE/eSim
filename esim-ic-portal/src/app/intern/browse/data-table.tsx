"use client";

import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useRouter, usePathname, useSearchParams } from "next/navigation";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useDebouncedCallback } from "use-debounce";

export function DataTable<TData, TValue>({
  columns,
  data,
  total,
}: {
  columns: any[];
  data: TData[];
  total: number;
}) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const pathname = usePathname();

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const page = parseInt(searchParams.get("page") || "1", 10);
  const pageSize = 50;
  const maxPage = Math.ceil(total / pageSize);

  const handleSearch = useDebouncedCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const params = new URLSearchParams(searchParams);
    if (e.target.value) {
      params.set("search", e.target.value);
    } else {
      params.delete("search");
    }
    params.set("page", "1");
    router.replace(`${pathname}?${params.toString()}`);
  }, 300);

  const handleDescriptionSearch = useDebouncedCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const params = new URLSearchParams(searchParams);
    if (e.target.value) {
      params.set("description", e.target.value);
    } else {
      params.delete("description");
    }
    params.set("page", "1");
    router.replace(`${pathname}?${params.toString()}`);
  }, 300);

  const handleCategoryChange = (value: string | null) => {
    const params = new URLSearchParams(searchParams);
    if (value && value !== "ALL") {
      params.set("category", value);
    } else {
      params.delete("category");
    }
    params.set("page", "1");
    router.replace(`${pathname}?${params.toString()}`);
  }

  const handleTechnologyChange = (value: string | null) => {
    const params = new URLSearchParams(searchParams);
    if (value && value !== "ALL") {
      params.set("technology", value);
    } else {
      params.delete("technology");
    }
    params.set("page", "1");
    router.replace(`${pathname}?${params.toString()}`);
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-4 py-4 md:flex-row md:items-center">
        <Input
          placeholder="Search by name or alias..."
          defaultValue={searchParams.get("search") || ""}
          onChange={handleSearch}
          className="max-w-[200px]"
        />
        <Input
          placeholder="Search in description..."
          defaultValue={searchParams.get("description") || ""}
          onChange={handleDescriptionSearch}
          className="max-w-[250px]"
        />
        
        <Select value={searchParams.get("category") || "ALL"} onValueChange={handleCategoryChange}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Categories</SelectItem>
            <SelectItem value="DIGITAL_LOGIC">Digital Logic</SelectItem>
            <SelectItem value="OP_AMP">Op-Amp</SelectItem>
            <SelectItem value="COMPARATOR">Comparator</SelectItem>
            <SelectItem value="VOLTAGE_REGULATOR">Voltage Regulator</SelectItem>
            <SelectItem value="MIXED_SIGNAL">Mixed Signal</SelectItem>
            <SelectItem value="DEVICE_MODEL">Device Model</SelectItem>
            <SelectItem value="IP_BLOCK">IP Block</SelectItem>
            <SelectItem value="OTHER">Other</SelectItem>
          </SelectContent>
        </Select>

        <Select value={searchParams.get("technology") || "ALL"} onValueChange={handleTechnologyChange}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder="Technology" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="ALL">All Technologies</SelectItem>
            <SelectItem value="TTL">TTL</SelectItem>
            <SelectItem value="CMOS">CMOS</SelectItem>
            <SelectItem value="BICMOS">BiCMOS</SelectItem>
            <SelectItem value="ANALOG">Analog</SelectItem>
            <SelectItem value="MIXED">Mixed</SelectItem>
            <SelectItem value="UNSPECIFIED">Unspecified</SelectItem>
          </SelectContent>
        </Select>
        
      </div>
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder
                      ? null
                      : flexRender(
                          header.column.columnDef.header,
                          header.getContext()
                        )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">
          Showing {data.length} of {total} results
        </div>
        <div className="flex items-center space-x-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              const params = new URLSearchParams(searchParams);
              params.set("page", (page - 1).toString());
              router.replace(`${pathname}?${params.toString()}`);
            }}
            disabled={page <= 1}
          >
            Previous
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              const params = new URLSearchParams(searchParams);
              params.set("page", (page + 1).toString());
              router.replace(`${pathname}?${params.toString()}`);
            }}
            disabled={page >= maxPage}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
