"use server";

import { prisma } from "@/lib/prisma";
import { revalidatePath } from "next/cache";

export async function handleReviewAction(
  taskId: string,
  action: "approve" | "reject",
  note?: string
) {
  try {
    if (action === "reject" && (!note || note.trim().length === 0)) {
      return { success: false, error: "A note is required for rejections." };
    }

    const task = await prisma.iCTask.findUnique({
      where: { id: taskId },
      include: { ic: true, enrollment: { include: { user: true } } },
    });

    if (!task) {
        return { success: false, error: "Task not found." };
    }

    if (task.status !== "UNDER_REVIEW") {
       return { success: false, error: "Task is not currently under review." }
    }

    if (action === "approve") {
      await prisma.iCTask.update({
          where: { id: taskId },
          data: { status: "COMPLETED", completedAt: new Date() },
      });
    } else {
      await prisma.iCTask.update({
        where: { id: taskId },
        data: {
          status: "IN_PROGRESS",
          mentorNote: note,
        },
      });
    }

    revalidatePath("/admin/review");
    revalidatePath("/admin/dashboard");
    revalidatePath(`/admin/interns/${task.enrollment.user.id}`);
    return { success: true };
  } catch (error) {
    console.error("Error processing review action:", error);
    return { success: false, error: "Failed to process review action. Please try again." };
  }
}
