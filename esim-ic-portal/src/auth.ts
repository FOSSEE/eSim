import NextAuth, { type DefaultSession } from "next-auth";
import Google from "next-auth/providers/google";
import { prisma } from "@/lib/prisma";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      role: "INTERN" | "ADMIN" | "MENTOR";
    } & DefaultSession["user"];
  }
}

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [Google],
  callbacks: {
    async signIn({ user, profile }) {
      if (!user.email) return false;

      const dbUser = await prisma.user.findUnique({
        where: { email: user.email },
      });

      // User must exist in the whitelist
      if (!dbUser) {
        return "/unauthorized";
      }

      // Name capture logic: update if current name is placeholder
      if (
        profile?.name &&
        (!dbUser.name ||
          dbUser.name === "Unknown" ||
          dbUser.name === dbUser.email ||
          dbUser.name === "Pending")
      ) {
        await prisma.user.update({
          where: { email: user.email },
          data: { name: profile.name },
        });
      }

      return true;
    },
    async jwt({ token, user }) {
      if (user?.email) {
        const dbUser = await prisma.user.findUnique({
          where: { email: user.email },
        });
        if (dbUser) {
          token.id = dbUser.id;
          token.role = dbUser.role;
        }
      }
      return token;
    },
    async session({ session, token }) {
      if (token?.id) {
        session.user.id = token.id as string;
      }
      if (token?.role) {
        session.user.role = token.role as "INTERN" | "ADMIN" | "MENTOR";
      }
      return session;
    },
  },
  pages: {
    signIn: "/",
    error: "/unauthorized",
  },
});
