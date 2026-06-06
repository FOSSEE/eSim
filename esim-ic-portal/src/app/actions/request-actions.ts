"use server";

import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { revalidatePath } from "next/cache";

export async function processAddRequest(
  requestId: string,
  action: "APPROVE_AS_NEW" | "MERGE" | "REJECT",
  payload: {
    mergeWithIcId?: string;
    reviewNote?: string;
    finalName?: string;
    finalAliases?: string[];
  }
) {
  const user = await requireRole(["ADMIN", "MENTOR"]);

  try {
    const request = await prisma.addRequest.findUnique({
      where: { id: requestId },
    });

    if (!request) return { error: "Request not found" };
    if (request.status !== "PENDING") return { error: "Request is already resolved" };

    if (action === "REJECT") {
      if (!payload.reviewNote || !payload.reviewNote.trim()) {
        return { error: "A note is required for rejections." };
      }
      await prisma.addRequest.update({
        where: { id: requestId },
        data: {
          status: "REJECTED",
          reviewerId: user.id,
          reviewNote: payload.reviewNote,
          reviewedAt: new Date(),
        },
      });
      revalidatePath("/admin/requests");
      return { success: "Request rejected successfully." };
    }

    if (action === "APPROVE_AS_NEW") {
      const canonicalName = payload.finalName || request.normalizedName!;
      const aliases = payload.finalAliases || [];
      const normalizedAliases = aliases.map(a => a.toUpperCase().replace(/\s+/g, ""));

      const existingIc = await prisma.iC.findUnique({
        where: { canonicalName },
      });
      
      if (existingIc) {
        return { error: "An IC with this canonical name already exists. Please merge it instead." };
      }

      if (normalizedAliases.length > 0) {
        const existingAliases = await prisma.iCAlias.findMany({
          where: { name: { in: normalizedAliases } }
        });
        if (existingAliases.length > 0) {
          return { error: `These aliases already exist: ${existingAliases.map(a => a.name).join(", ")}` };
        }

        const conflictingCanonical = await prisma.iC.findMany({
          where: { canonicalName: { in: normalizedAliases } }
        });
        if (conflictingCanonical.length > 0) {
           return { error: `These aliases conflict with existing ICs: ${conflictingCanonical.map(c => c.canonicalName).join(", ")}` };
        }
      }

      await prisma.$transaction(async (tx) => {
        const newIc = await tx.iC.create({
          data: {
            canonicalName,
            category: "OTHER",
            technology: "UNSPECIFIED",
            aliases: normalizedAliases.length > 0 ? {
              create: normalizedAliases.map(name => ({
                name,
                note: "Added during IC request approval"
              }))
            } : undefined
          },
        });

        await tx.addRequest.update({
          where: { id: requestId },
          data: {
            status: "APPROVED_AS_NEW",
            reviewerId: user.id,
            createdIcId: newIc.id,
            reviewedAt: new Date(),
          },
        });
      });

      revalidatePath("/admin/requests");
      revalidatePath("/admin/catalog");
      return { success: "Request approved and new IC created." };
    }

    if (action === "MERGE") {
      if (!payload.mergeWithIcId) return { error: "You must specify a target IC to merge into." };
      
      const targetIc = await prisma.iC.findUnique({
        where: { id: payload.mergeWithIcId },
      });

      if (!targetIc) return { error: "Target IC not found." };

      await prisma.$transaction(async (tx) => {
        // Optional: Create alias if the normalized name is different from the target canonical name
        if (targetIc.canonicalName !== request.normalizedName) {
           const existingAlias = await tx.iCAlias.findUnique({
             where: { name: request.normalizedName! },
           });
           if (!existingAlias) {
             await tx.iCAlias.create({
               data: {
                 name: request.normalizedName!,
                 icId: targetIc.id,
                 note: "Auto-generated from AddRequest merge"
               }
             });
           }
        }

        await tx.addRequest.update({
          where: { id: requestId },
          data: {
            status: "MERGED",
            reviewerId: user.id,
            mergeWithIcId: targetIc.id,
            reviewedAt: new Date(),
          },
        });
      });

      revalidatePath("/admin/requests");
      revalidatePath("/admin/catalog");
      return { success: "Request successfully merged into existing IC." };
    }

    return { error: "Invalid action." };
  } catch (error) {
    console.error("Error processing request:", error);
    return { error: "An error occurred while processing the request." };
  }
}

export async function searchICsForMerge(query: string) {
  await requireRole(["ADMIN", "MENTOR"]);
  if (!query) return [];
  const ics = await prisma.iC.findMany({
    where: { canonicalName: { contains: query, mode: "insensitive" } },
    select: { id: true, canonicalName: true },
    take: 15,
  });
  return ics;
}
