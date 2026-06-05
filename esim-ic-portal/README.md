# eSim IC Management Portal

A robust, full-stack Next.js web application designed to help interns, mentors, and administrators manage the cataloging and mapping of Integrated Circuits (ICs) into the eSim database environment. 

## Features

* **Role-Based Workflows**: Segregated interfaces for Interns, Mentors, and Admins.
* **Intern Portal**: 
  * Browse and claim unused ICs from an extensive pre-seeded database.
  * Track progress of active IC datasheet mapping tasks.
  * Request new ICs to be added to the catalog if unlisted.
* **Admin / Mentor Portal**:
  * **Catalog Manager**: Comprehensive search, filter, and inline-edit interface for global IC records and aliases.
  * **Review Queue**: Approve or reject intern task submissions with mandatory feedback loops.
  * **Naming Requests**: Handle intern-submitted IC requests by either generating them as new canonical parts or merging them into existing parts via a smart search combobox.
* **Resilient State Management**: Relies heavily on URL Query Parameters for routing state (pagination, filters, search), allowing fully shareable states without bulky client-side stores.

## Architecture & Tech Stack

* **Framework**: [Next.js 14 App Router](https://nextjs.org/) (React Server Components + Server Actions)
* **Database / ORM**: [Neon Serverless Postgres](https://neon.tech/) + [Prisma ORM](https://www.prisma.io/)
* **UI & Styling**: [Tailwind CSS](https://tailwindcss.com/) + [shadcn/ui](https://ui.shadcn.com/)
* **Tables**: [TanStack Table v8](https://tanstack.com/table/v8) - Server-side pagination & filtering

## Local Setup

1. **Clone & Install Dependencies**
   ```bash
   npm install
   ```

2. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL="postgres://[user]:[password]@[neon-host]/[db]?sslmode=require"
   ```

3. **Database Scaffolding**
   ```bash
   npx prisma generate
   npx prisma db push
   npx tsx prisma/seed.ts
   ```

4. **Run Development Server**
   ```bash
   npm run dev
   ```

## Development Decisions & Tradeoffs

* **Data Fetching Paradigm**: Most page load data is fetched directly at the RSC (React Server Component) level. Loading states are managed natively by Next.js routers, offloading the browser.
* **Authentication**: Currently utilizing a development-only mock cookie swapper (`dev-user-switcher.tsx`) to rapidly test Admin/Intern scopes without requiring an OAuth provider (like Auth.js) setup until production environments require it.
* **Atomic Operations**: Core actions (like merging a part, where multiple tables must mutually agree) are strictly bound in `prisma.$transaction()` pipelines to prevent orphaned data states in the Postgres cloud due to momentary disconnects.
