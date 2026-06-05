"use server";

import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { revalidatePath } from "next/cache";
import { ICCategory, Technology } from "@prisma/client";

export async function updateICMetadata(icId: string, data: {
  description: string;
  category: ICCategory;
  technology: Technology;
  datasheetUrl?: string;
}) {
  await requireRole(["ADMIN", "MENTOR"]);

  try {
    await prisma.iC.update({
      where: { id: icId },
      data: {
        description: data.description || null,
        category: data.category,
        technology: data.technology,
        datasheetUrl: data.datasheetUrl || null,
      },
    });

    revalidatePath(`/admin/catalog/${icId}`);
    return { success: "IC metadata updated successfully" };
  } catch (error) {
    console.error("Failed to update IC metadata:", error);
    return { error: "An error occurred while updating IC metadata" };
  }
}

export async function addICAlias(icId: string, newAliasName: string) {
  await requireRole(["ADMIN", "MENTOR"]);

  const cleanName = newAliasName.trim().toUpperCase().replace(/\s+/g, '');
  if (!cleanName) return { error: "Alias name cannot be empty" };

  try {
    // Check if canonical name matches anywhere
    const existingIC = await prisma.iC.findUnique({
      where: { canonicalName: cleanName },
    });
    if (existingIC) {
      return { error: `This name is already the canonical name for an IC.` };
    }

    const existingAlias = await prisma.iCAlias.findUnique({
      where: { name: cleanName },
      include: { ic: true },
    });

    if (existingAlias) {
      return { error: `This name already exists as an alias for ${existingAlias.ic.canonicalName}` };
    }

    await prisma.iCAlias.create({
      data: {
        name: cleanName,
        icId,
      },
    });

    revalidatePath(`/admin/catalog/${icId}`);
    return { success: "Alias added successfully" };
  } catch (error) {
    console.error("Failed to add alias:", error);
    return { error: "Failed to add alias." };
  }
}

export async function deleteICAlias(aliasId: string, icId: string) {
  await requireRole(["ADMIN", "MENTOR"]);

  try {
    // Check for active tasks
    const activeTasks = await prisma.iCTask.count({
      where: {
        icId,
        status: { in: ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"] },
      },
    });

    if (activeTasks > 0) {
      return { error: "Cannot delete aliases while there are active tasks assigned to this IC." };
    }

    await prisma.iCAlias.delete({
      where: { id: aliasId },
    });

    revalidatePath(`/admin/catalog/${icId}`);
    return { success: "Alias removed successfully" };
  } catch (error) {
    console.error("Failed to delete alias:", error);
    return { error: "Failed to remove alias." };
  }
}
