"use server";

import { requireRole } from "@/lib/auth";
import { prisma } from "@/lib/prisma";
import { revalidatePath } from "next/cache";

export async function updateTaskStatus(formData: FormData) {
  const user = await requireRole("INTERN");
  const taskId = formData.get("taskId") as string;
  const status = formData.get("status") as string;

  if (!taskId || !status) return;

  const task = await prisma.iCTask.findUnique({
    where: { id: taskId },
    include: { enrollment: true }
  });

  if (!task || task.enrollment.userId !== user.id) {
    throw new Error("Unauthorized");
  }

  // Ensure status flow is logical
  if (task.status === "CLAIMED" && status !== "IN_PROGRESS") return;
  if (task.status === "IN_PROGRESS" && status !== "UNDER_REVIEW") return;

  await prisma.iCTask.update({
    where: { id: taskId },
    data: { status: status as any }
  });

  revalidatePath("/intern/dashboard");
}

export async function claimTaskAction(icId: string) {
  const user = await requireRole("INTERN");

  const enrollment = await prisma.batchEnrollment.findFirst({
    where: { userId: user.id },
    include: { tasks: true }
  });

  if (!enrollment) {
    return { error: "No active enrollment found" };
  }

  const activeTaskCount = enrollment.tasks.filter(t => ["CLAIMED", "IN_PROGRESS"].includes(t.status)).length;
  
  if (activeTaskCount >= 3) {
    return { error: "You have reached the 3-task limit. Complete or submit a task to claim more." };
  }

  const ic = await prisma.iC.findUnique({
    where: { id: icId },
    include: { aliases: true }
  });

  if (!ic) {
    return { error: "IC not found" };
  }

  const aliasNames = ic.aliases.map(a => a.name);
  
  // check collision
  const collision = await prisma.iCTask.findFirst({
    where: {
      enrollment: { batchId: enrollment.batchId },
      status: { in: ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"] },
      ic: {
        OR: [
          { id: icId },
          { aliases: { some: { name: { in: aliasNames } } } }
        ]
      }
    }
  });

  if (collision) {
    return { error: "This IC (or its alias) is already claimed by someone else in your batch." };
  }

  await prisma.$transaction([
    prisma.iCTask.create({
      data: {
        icId: ic.id,
        enrollmentId: enrollment.id,
        status: "CLAIMED",
      }
    })
  ]);

  revalidatePath("/intern/dashboard");
  revalidatePath("/intern/browse");
  
  return { success: true };
}
