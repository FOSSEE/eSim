import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import Link from "next/link";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CatalogFilter } from "@/components/admin/catalog-filter";
import { ExternalLink, TriangleAlert } from "lucide-react";
import { Prisma, ICCategory, Technology } from "@prisma/client";

export default async function AdminCatalogPage({
  searchParams,
}: {
  searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
}) {
  await requireRole(["ADMIN", "MENTOR"]);

  const params = await searchParams;

  const search = typeof params.search === "string" ? params.search : "";
  const category = typeof params.category === "string" ? params.category as ICCategory : undefined;
  const technology = typeof params.technology === "string" ? params.technology as Technology : undefined;
  const quality = typeof params.quality === "string" ? params.quality : "all";
  
  const page = typeof params.page === "string" ? parseInt(params.page, 10) : 1;
  const pageSize = 50;
  const sort = typeof params.sort === "string" ? params.sort : "canonicalName";
  const order = typeof params.order === "string" ? params.order : "asc";

  const getWhereClause = (): Prisma.ICWhereInput => {
    return {
      AND: [
        search ? {
          OR: [
            { canonicalName: { contains: search, mode: "insensitive" } },
            { aliases: { some: { name: { contains: search, mode: "insensitive" } } } },
            { description: { contains: search, mode: "insensitive" } },
          ],
        } : {},
        category ? { category } : {},
        technology ? { technology } : {},
        quality === "no_datasheet" ? { datasheetUrl: null } : {},
        quality === "unspecified_tech" ? { technology: "UNSPECIFIED" } : {},
        quality === "no_aliases" ? { aliases: { none: {} } } : {},
      ],
    };
  };

  const where = getWhereClause();

  const [items, total] = await Promise.all([
    prisma.iC.findMany({
      where,
      include: {
        aliases: true,
        _count: { select: { tasks: true, aliases: true } },
        tasks: { 
          select: { status: true, enrollment: { include: { user: true } } }, 
          orderBy: { claimedAt: "desc" }, 
          take: 1 
        },
      },
      skip: (page - 1) * pageSize,
      take: pageSize,
      orderBy: { [sort]: order as any },
    }),
    prisma.iC.count({ where }),
  ]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">IC Catalog</h1>
        {/* Placeholder for Add New IC Modal */}
        <Button>Add New IC</Button>
      </div>

      <CatalogFilter />

      <div className="border rounded-md">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Canonical Name</TableHead>
              <TableHead>Aliases</TableHead>
              <TableHead>Category</TableHead>
              <TableHead>Technology</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Datasheet</TableHead>
              <TableHead>Assignment</TableHead>
              <TableHead>Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items.length === 0 ? (
              <TableRow>
                <TableCell colSpan={8} className="text-center h-24 text-muted-foreground">
                  No ICs found matching constraints.
                </TableCell>
              </TableRow>
            ) : (
              items.map((ic) => {
                const latestTask = ic.tasks[0];
                let assignmentLabel: React.ReactNode = <span className="text-green-600 font-medium text-xs">Available</span>;
                
                if (latestTask) {
                  if (latestTask.status === "COMPLETED") {
                    assignmentLabel = <span className="text-blue-600 font-medium text-xs">Completed</span>;
                  } else if (["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"].includes(latestTask.status)) {
                     assignmentLabel = <span className="text-yellow-600 font-medium text-xs truncate max-w-[120px] block" title={latestTask.enrollment.user.name || "Intern"}>In Progress — {latestTask.enrollment.user.name?.split(" ")[0]}</span>;
                  }
                }

                return (
                  <TableRow key={ic.id}>
                    <TableCell className="font-mono font-medium">
                      <Link href={`/admin/catalog/${ic.id}`} className="hover:underline text-primary">
                        {ic.canonicalName}
                      </Link>
                    </TableCell>
                    <TableCell>
                      {ic.aliases.length > 0 ? (
                        <Badge variant="secondary" className="cursor-help" title={ic.aliases.map(a => a.name).join(", ")}>
                          {ic.aliases.length} aliases
                        </Badge>
                      ) : (
                        <span className="text-muted-foreground text-xs">-</span>
                      )}
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className="text-[10px] uppercase tracking-wider">{ic.category.replace('_', ' ')}</Badge>
                    </TableCell>
                    <TableCell>
                      {ic.technology === "UNSPECIFIED" ? (
                        <Badge variant="destructive" className="bg-orange-500 hover:bg-orange-600 text-[10px]">Unspec</Badge>
                      ) : (
                        <Badge variant="secondary" className="text-[10px]">{ic.technology}</Badge>
                      )}
                    </TableCell>
                    <TableCell className="max-w-[200px] truncate text-xs" title={ic.description || ""}>
                      {ic.description || <span className="text-muted-foreground italic">None</span>}
                    </TableCell>
                    <TableCell className="text-center">
                      {ic.datasheetUrl ? (
                        <a href={ic.datasheetUrl} target="_blank" rel="noopener noreferrer" className="text-primary hover:text-primary/80 inline-block">
                           <ExternalLink className="h-4 w-4" />
                        </a>
                      ) : (
                        <TriangleAlert className="h-4 w-4 text-orange-500 inline-block"  />
                      )}
                    </TableCell>
                    <TableCell>{assignmentLabel}</TableCell>
                    <TableCell>
                       <Link href={`/admin/catalog/${ic.id}`}>
                         <Button variant="ghost" size="sm">Edit</Button>
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
          Showing {(page - 1) * pageSize + 1} to {Math.min(page * pageSize, total)} of {total} ICs.
        </div>
        <div className="space-x-2">
          <Link href={`?page=${page - 1}`} className={page <= 1 ? "pointer-events-none opacity-50" : ""}>
            <Button variant="outline" size="sm" disabled={page <= 1}>Previous</Button>
          </Link>
          <Link href={`?page=${page + 1}`} className={page * pageSize >= total ? "pointer-events-none opacity-50" : ""}>
            <Button variant="outline" size="sm" disabled={page * pageSize >= total}>Next</Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
