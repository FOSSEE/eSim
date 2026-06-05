"use server"

import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { revalidatePath } from "next/cache";
import { z } from "zod";

const AddRequestSchema = z.object({
  icName: z
    .string()
    .min(1, "Please provide a valid IC name.")
    .transform((val) => val.toUpperCase().replace(/\s+/g, ""))
    .pipe(
      z.string().regex(/^[A-Z0-9\-\_\/\+]{2,40}$/, {
        message:
          "Invalid format. Only letters, numbers, hyphens, slashes, and underscores are allowed (2-40 characters).",
      })
    ),
  icAliases: z.string().optional(),
});

export async function requestIcAction(formData: FormData) {
  const user = await requireRole("INTERN");
  
  const parsed = AddRequestSchema.safeParse({
    icName: formData.get("icName")?.toString() || "",
    icAliases: formData.get("icAliases")?.toString(),
  });

  if (!parsed.success) {
    return { error: parsed.error.issues[0].message };
  }

  const { icName: normalizedName, icAliases } = parsed.data;

  // We still need the original "raw" name to satisfy the database model,
  // but we can just use the user's un-transformed input for that.
  const rawName = formData.get("icName")?.toString() || "";

  const suggestedAliases = icAliases 
    ? icAliases.split(",").map(s => s.trim()).filter(s => s.length > 0)
    : [];

  // Step 2: Check if canonicalName already exists
  const existingIc = await prisma.iC.findFirst({
    where: { canonicalName: { equals: normalizedName, mode: "insensitive" } }
  });

  if (existingIc) {
    return { error: `Already exists. Search for ${existingIc.canonicalName} and claim it.` };
  }

  // Step 3: Check if name matches any ICAlias
  const existingAlias = await prisma.iCAlias.findFirst({
    where: { name: { equals: normalizedName, mode: "insensitive" } },
    include: { ic: true }
  });

  if (existingAlias) {
    return { error: `This is an alias of ${existingAlias.ic.canonicalName}. Search and claim that instead.` };
  }

  // Step 4: Check if AddRequest already exists for this intern
  const existingRequest = await prisma.addRequest.findFirst({
    where: { 
      normalizedName, 
      requesterId: user.id,
      status: "PENDING"
    }
  });

  if (existingRequest) {
    return { error: "You already have a pending request for this IC." };
  }

  // Per Architectural Core Rule 'SPICE Fidelity', do NOT auto-create a canonical IC without admin categories.
  // Instead, create an AddRequest indicating they want a new IC.
  await prisma.addRequest.create({
    data: {
      rawName: rawName.trim(),
      normalizedName,
      suggestedAliases,
      requesterId: user.id,
      status: "PENDING"
    }
  });

  revalidatePath("/intern/browse");
  return { success: `Request for ${normalizedName} has been sent to an admin for review.` };
}
