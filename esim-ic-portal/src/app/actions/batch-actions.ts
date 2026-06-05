"use server";

import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { revalidatePath } from "next/cache";

export async function bulkAddInternsAction(batchId: string, emailsRaw: string) {
  await requireRole("ADMIN");

  const emails = emailsRaw
    .split(/[\n,]+/)
    .map((e) => e.trim().toLowerCase())
    .filter((e) => e.length > 0 && e.includes("@"));

  if (emails.length === 0) {
    throw new Error("No valid emails provided");
  }

  const batch = await prisma.batch.findUnique({ where: { id: batchId } });
  if (!batch) throw new Error("Batch not found");

  let addedCount = 0;

  for (const email of emails) {
    let user = await prisma.user.findUnique({ where: { email } });
    if (!user) {
      user = await prisma.user.create({
        data: {
          email,
          name: "Pending",
          role: "INTERN",
        },
      });
    }

    const existingEnrollment = await prisma.batchEnrollment.findUnique({
      where: {
        userId_batchId: {
          userId: user.id,
          batchId: batch.id,
        },
      },
    });

    if (!existingEnrollment) {
      await prisma.batchEnrollment.create({
        data: {
          userId: user.id,
          batchId: batch.id,
        },
      });
      addedCount++;
    }
  }

  revalidatePath("/admin/batches");
  return { success: true, count: addedCount, total: emails.length };
}

export async function removeBatchEnrollmentAction(enrollmentId: string) {
  await requireRole("ADMIN");

  const enrollment = await prisma.batchEnrollment.findUnique({
    where: { id: enrollmentId },
    include: { tasks: true },
  });

  if (!enrollment) throw new Error("Enrollment not found");

  if (enrollment.tasks.length > 0) {
    throw new Error(
      `Cannot remove enrollment: User has ${enrollment.tasks.length} tasks in this batch. Reassign or delete tasks first.`
    );
  }

  await prisma.batchEnrollment.delete({
    where: { id: enrollmentId },
  });

  revalidatePath("/admin/batches");
  return { success: true };
}
