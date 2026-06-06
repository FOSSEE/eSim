# Project Summary: eSim IC Management Portal

## Overview
The eSim IC Management Portal is a comprehensive web application designed to manage, assign, and track Integrated Circuit (IC) tasks for interns and administrators. It features a robust role-based access control system, an intuitive task claiming mechanism, and an extensive admin dashboard for reviewing submitted work and cataloging ICs.

## Tech Stack
- **Framework**: Next.js 15.5 (App Router)
- **Language**: TypeScript
- **Database**: Prisma ORM with Neon Postgres (Serverless PostgreSQL)
- **Authentication**: Auth.js v5 (NextAuth) with Google OAuth provider
- **Styling**: Tailwind CSS v4, shadcn/ui, `next-themes` for dark/light mode support
- **Data Tables**: TanStack Table v8
- **UI Primitives**: `@base-ui/react`, Radix primitives (via shadcn), Lucide React (icons)
- **Deployment**: Configured for Vercel

## Architecture
- **Data Fetching & State**: Driven primarily by React Server Components (RSC) and URL search parameters. This eliminates the need for thick client-side state management, enabling highly shareable URLs and thin client bundles.
- **Mutations**: Next.js Server Actions (`use server`) handle all form submissions and direct database mutations securely.
- **Database Operations**: Prisma transactions (`prisma.$transaction()`) are used to ensure atomicity, particularly when merging IC aliases, resolving naming conflicts, or batch-inserting records.
- **Authentication Flow**: Managed via Auth.js v5 and Google OAuth. Access control is enforced through an email whitelist system mapped to `ADMIN` and `INTERN` roles in the database.

## Key Features
- **Intern Dashboard**: Features task tracking, a claiming system, and IC request forms with server-side validation to prevent duplicate entries.
- **Admin Dashboard**: Provides comprehensive system statistics, intern task history, and a paginated global IC catalog.
- **Review Queue**: A structured approval/rejection workflow allowing admins to provide mandatory feedback on intern submissions.
- **Batch Management**: Bulk-add UI (Admin Batches UI) to efficiently manage and enroll new intern cohorts.
- **Search & Filter**: Optimized server-side search querying across interns and the IC catalog with debounced input handlers.

## Recent Updates
- Successfully transitioned from mock authentication to a secure, production-ready Auth.js Google OAuth implementation.
- Completed the Admin Batch Management UI.
- Stabilized environment configurations (`.env`, `.env.local`) and deployment build scripts.
