import { redirect } from "next/navigation";
import { cache } from "react";
import type { Role, User } from "@prisma/client";
import { prisma } from "@/lib/prisma";
import { auth } from "@/auth";

export const getCurrentUser = cache(async (): Promise<User | null> => {
  const session = await auth();
  if (!session?.user?.id) return null;
  
  const user = await prisma.user.findUnique({ where: { id: session.user.id } });
  return user;
});

export async function requireRole(allowed: Role | Role[]): Promise<User> {
  const user = await getCurrentUser();
  const roles = Array.isArray(allowed) ? allowed : [allowed];
  
  if (!user || !roles.includes(user.role)) {
    redirect("/");
  }
  return user;
}
