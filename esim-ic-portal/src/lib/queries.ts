import { prisma } from "@/lib/prisma";

export async function getInternDashboardData(userId: string) {
  return prisma.batchEnrollment.findFirst({
    where: { userId },
    include: {
      batch: true,
      tasks: {
        include: { ic: { include: { aliases: true } } },
        orderBy: { claimedAt: "desc" },
      },
    },
  });
}

export type LobbyParams = {
  search?: string;
  description?: string;
  category?: string;
  technology?: string;
  showAll?: boolean;
  page: number;
  pageSize: number;
  batchId: string;
};

export async function getIcsForLobby({
  search, description, category, technology, showAll, page, pageSize, batchId
}: LobbyParams) {
  const where: any = {
    AND: [
      search ? {
        OR: [
          { canonicalName: { contains: search, mode: "insensitive" } },
          { aliases: { some: { name: { contains: search, mode: "insensitive" } } } },
        ],
      } : {},
      description ? { description: { contains: description, mode: "insensitive" } } : {},
      category ? { category } : {},
      technology ? { technology } : {},
      !showAll ? {
        NOT: {
          tasks: {
            some: {
              status: { in: ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"] },
              enrollment: { batchId: batchId },
            },
          },
        },
      } : {},
    ],
  };
  const [items, total] = await Promise.all([
    prisma.iC.findMany({
      where,
      include: { aliases: true, tasks: { include: { enrollment: { include: { user: true } } } } },
      skip: (page - 1) * pageSize,
      take: pageSize,
      orderBy: { canonicalName: "asc" },
    }),
    prisma.iC.count({ where }),
  ]);
  
  return { items, total };
}
