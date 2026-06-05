# 📋 Product Requirements Document (PRD)
# eSim IC Management Portal — FOSSEE, IIT Bombay

**Version:** 1.0 (MVP)
**Stack:** Next.js 14 (App Router) · Prisma · PostgreSQL · Tailwind CSS · shadcn/ui · TanStack Table
**Prepared for:** AI Coding Agent (Cursor / Windsurf)

---

## 🚨 AGENT INSTRUCTIONS (READ FIRST — NON-NEGOTIABLE)

1. You are building a **completely NEW Next.js 14 App Router project from scratch**. Do not reference any previous codebase.
2. Execute **ONE phase at a time**. After completing each phase, **stop and wait for explicit confirmation** before proceeding to the next.
3. After any Prisma schema change, always run `npx prisma generate`.
4. **Do not install any npm package** without first listing it and receiving approval.
5. Use **Tailwind CSS + shadcn/ui** for all styling. No other CSS frameworks.
6. Use **TanStack Table (via shadcn data-table)** for every list that requires search, sort, or filter.
7. All data tables must use **server-side pagination, search, and sort** via URL search params. Never fetch all 804 rows to the client.
8. The "Switch User" dev toolbar must **only render when `process.env.NODE_ENV === 'development'`**.
9. Delete any legacy in-memory mock state or `app-context.tsx` files from previous generations before writing new code.
10. Every Prisma write that involves claiming an IC **must use `$transaction`**.

---

## 🎯 Architectural Core Rules

| Rule | Detail |
|---|---|
| **RSC First** | Fetch all initial data in React Server Components using Prisma directly. Pass serialized data down to Client Components for interactivity. |
| **Server-Side Tables** | All TanStack tables are driven by URL search params (`?page`, `?search`, `?sort`, `?order`, `?category`, `?technology`). The RSC reads these params and passes filtered, paginated data to the table. |
| **Atomic Claims** | The IC claim Server Action must use `prisma.$transaction` to check the 3-task limit and create the `ICTask` atomically. No race conditions. |
| **3-IC Limit** | An intern can never hold more than 3 tasks with status `CLAIMED`, `IN_PROGRESS`, or `UNDER_REVIEW` simultaneously within a single `BatchEnrollment`. |
| **Alias-First Search** | Every search input that queries ICs must search both `IC.canonicalName` AND `ICAlias.name` simultaneously using a Prisma `OR` clause. |
| **SPICE Fidelity** | Never auto-create a new canonical IC without an Admin explicitly selecting `Category` and `Technology`. No defaults allowed on new IC creation. |
| **Collision Prevention** | When an intern claims an IC, the system must check whether any alias of that IC is already in an active task (`CLAIMED`, `IN_PROGRESS`, `UNDER_REVIEW`) by another intern in the same batch. If so, block the claim. |

---

## 🗄️ THE FINAL SCHEMA (Source of Truth — Do Not Alter)

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

enum Role              { INTERN MENTOR ADMIN }
enum ICStatus          { UNCLAIMED CLAIMED IN_PROGRESS UNDER_REVIEW COMPLETED FAILED }
enum ICCategory        { DIGITAL_LOGIC OP_AMP COMPARATOR VOLTAGE_REGULATOR MIXED_SIGNAL DEVICE_MODEL IP_BLOCK OTHER }
enum Technology        { TTL CMOS BICMOS ANALOG MIXED UNSPECIFIED }
enum AddRequestStatus  { PENDING APPROVED_AS_NEW MERGED REJECTED }
enum InternshipSeason  { SUMMER WINTER SLI OTHER }

model User {
  id               String           @id @default(cuid())
  email            String           @unique
  name             String
  role             Role             @default(INTERN)
  createdAt        DateTime         @default(now())
  batchEnrollments BatchEnrollment[]
  addRequests      AddRequest[]     @relation("RequestedBy")
  reviews          AddRequest[]     @relation("ReviewedBy")
}

model Batch {
  id          String            @id @default(cuid())
  year        Int
  season      InternshipSeason
  label       String
  startDate   DateTime?
  endDate     DateTime?
  enrollments BatchEnrollment[]
  @@unique([year, season])
}

model BatchEnrollment {
  id      String    @id @default(cuid())
  user    User      @relation(fields: [userId], references: [id])
  userId  String
  batch   Batch     @relation(fields: [batchId], references: [id])
  batchId String
  tasks   ICTask[]
  @@unique([userId, batchId])
}

model IC {
  id                 String       @id @default(cuid())
  canonicalName      String       @unique
  description        String?
  category           ICCategory
  technology         Technology   @default(UNSPECIFIED)
  datasheetUrl       String?
  aliases            ICAlias[]
  tasks              ICTask[]
  mergeRequests      AddRequest[] @relation("MergeCandidate")
  createdFromRequest AddRequest?  @relation("CreatedFromRequest")
  createdAt          DateTime     @default(now())
  seededFrom         String?
}

model ICAlias {
  id   String  @id @default(cuid())
  name String  @unique
  ic   IC      @relation(fields: [icId], references: [id])
  icId String
  note String?
}

model ICTask {
  id           String          @id @default(cuid())
  ic           IC              @relation(fields: [icId], references: [id])
  icId         String
  enrollment   BatchEnrollment @relation(fields: [enrollmentId], references: [id])
  enrollmentId String
  status       ICStatus        @default(CLAIMED)
  claimedAt    DateTime        @default(now())
  updatedAt    DateTime        @updatedAt
  completedAt  DateTime?
  mentorNote   String?
  @@index([enrollmentId])
  @@index([icId])
  @@index([status])
}

model AddRequest {
  id              String           @id @default(cuid())
  rawName         String
  normalizedName  String?
  requester       User             @relation("RequestedBy", fields: [requesterId], references: [id])
  requesterId     String
  status          AddRequestStatus @default(PENDING)
  suggestedMergeWith IC?           @relation("MergeCandidate", fields: [mergeWithIcId], references: [id])
  mergeWithIcId   String?
  reviewer        User?            @relation("ReviewedBy", fields: [reviewerId], references: [id])
  reviewerId      String?
  reviewNote      String?
  createdIc       IC?              @relation("CreatedFromRequest", fields: [createdIcId], references: [id])
  createdIcId     String?          @unique
  createdAt       DateTime         @default(now())
  reviewedAt      DateTime?
  @@index([status])
  @@index([requesterId])
}
```

---

## 🗂️ URL & Route Structure

```
/                            → Redirect to /intern/dashboard or /admin/dashboard based on role cookie
/intern/dashboard            → Intern home: active task cards + history table
/intern/browse               → IC lobby: full searchable/filterable 804-row table
/admin/dashboard             → Admin home: stats cards + quick-action tables
/admin/interns               → All enrolled interns (searchable, sortable table)
/admin/interns/[id]          → Individual intern detail: full task history
/admin/catalog               → Master IC database (searchable, filterable)
/admin/catalog/[id]          → Individual IC detail: edit metadata, manage aliases
/admin/review                → UNDER_REVIEW task queue (approve / reject)
/admin/requests              → AddRequest queue: merge, approve-as-new, or reject
```

---

## 🚀 EXECUTION PHASES

---

### PHASE 0 — Project Scaffolding & Database Sync

**Goal:** Working Next.js project with Prisma connected to PostgreSQL and shadcn/ui installed.

**Steps:**

1. Initialize a clean Next.js 14 project:
   ```bash
   npx create-next-app@latest esim-ic-portal \
     --typescript --tailwind --eslint --app --src-dir=false
   ```

2. Install and initialize shadcn/ui. Install these components:
   `button` `input` `table` `dialog` `select` `toast` `dropdown-menu` `command` `popover` `badge` `card` `separator` `textarea` `label` `sonner`

3. Install Prisma:
   ```bash
   npm install prisma @prisma/client
   npx prisma init
   ```

4. Replace the generated `schema.prisma` with the **Final Schema** above verbatim.

5. Run:
   ```bash
   npx prisma db push
   npx prisma generate
   ```

6. Create `lib/prisma.ts` — the singleton Prisma client:
   ```typescript
   import { PrismaClient } from "@prisma/client";
   const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };
   export const prisma =
     globalForPrisma.prisma ?? new PrismaClient({ log: ["query"] });
   if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
   ```

7. Create `lib/queries.ts` — reusable Prisma query helpers (to be expanded in later phases):
   ```typescript
   // Placeholder: all shared query functions go here.
   // Never write raw Prisma queries inline in RSC page files.
   ```

**Stop. Confirm database connection works before proceeding.**

---

### PHASE 1 — Seed Script (`prisma/seed.ts`)

**Goal:** Populate the database with realistic test data that mirrors the real eSim dataset.

**Seed the following data exactly:**

**Users:**

| Name | Email | Role |
|---|---|---|
| Admin User | admin@esim.fossee.in | ADMIN |
| Mentor User | mentor@esim.fossee.in | MENTOR |
| Arjun Sharma | arjun@intern.esim.in | INTERN |
| Priya Nair | priya@intern.esim.in | INTERN |
| Rohan Mehta | rohan@intern.esim.in | INTERN |

**Batches:**

| Year | Season | Label |
|---|---|---|
| 2026 | SUMMER | Summer 2026 |
| 2026 | WINTER | Winter 2026 |

**Enrollments:**
- Arjun → SUMMER 2026
- Priya → SUMMER 2026
- Rohan → SUMMER 2026 and WINTER 2026

**Canonical ICs to seed (minimum — use this exact data):**

```typescript
const ics = [
  { canonicalName: "LM741",     description: "General purpose op-amp",          category: "OP_AMP",           technology: "ANALOG",      aliases: ["UA741", "µA741", "LM741CN"] },
  { canonicalName: "LM324",     description: "Quad op-amp",                      category: "OP_AMP",           technology: "ANALOG",      aliases: ["LM324N", "LM324D"] },
  { canonicalName: "LM358",     description: "Dual op-amp",                      category: "OP_AMP",           technology: "ANALOG",      aliases: ["LM358N", "LM358P"] },
  { canonicalName: "LM339",     description: "Quad comparator",                  category: "COMPARATOR",       technology: "ANALOG",      aliases: ["LM339N"] },
  { canonicalName: "LM7805",    description: "5V linear voltage regulator",      category: "VOLTAGE_REGULATOR",technology: "ANALOG",      aliases: ["UA7805", "MC7805"] },
  { canonicalName: "LM317",     description: "Adjustable voltage regulator",     category: "VOLTAGE_REGULATOR",technology: "ANALOG",      aliases: ["LM317T"] },
  { canonicalName: "74LS138",   description: "3-to-8 line decoder",             category: "DIGITAL_LOGIC",    technology: "TTL",         aliases: ["SN74LS138", "DM74LS138"] },
  { canonicalName: "74HC244",   description: "Octal buffer/line driver",        category: "DIGITAL_LOGIC",    technology: "CMOS",        aliases: ["SN74HC244", "74HC244N"] },
  { canonicalName: "74HC595",   description: "8-bit shift register",            category: "DIGITAL_LOGIC",    technology: "CMOS",        aliases: ["SN74HC595", "74HC595N"] },
  { canonicalName: "74LS04",    description: "Hex inverter",                    category: "DIGITAL_LOGIC",    technology: "TTL",         aliases: ["SN74LS04", "DM74LS04"] },
  { canonicalName: "IDT72V201", description: "FIFO memory",                     category: "MIXED_SIGNAL",     technology: "CMOS",        aliases: ["72V201"] },
  { canonicalName: "DS90CR285", description: "Channel link serializer",         category: "MIXED_SIGNAL",     technology: "CMOS",        aliases: ["DS90CR285A"] },
  { canonicalName: "AD633",     description: "Low cost analog multiplier",      category: "MIXED_SIGNAL",     technology: "ANALOG",      aliases: ["AD633JN"] },
  { canonicalName: "NE555",     description: "Timer IC",                        category: "OTHER",            technology: "BICMOS",      aliases: ["LM555", "NE555P", "SA555"] },
  { canonicalName: "CD4051B",   description: "8-channel analog multiplexer",   category: "MIXED_SIGNAL",     technology: "CMOS",        aliases: ["HCF4051B"] },
];
```

**ICTask assignments to seed:**

| Intern | IC | Status | Notes |
|---|---|---|---|
| Arjun | LM741 | IN_PROGRESS | Active task |
| Arjun | LM324 | UNDER_REVIEW | Submitted for review |
| Arjun | LM7805 | CLAIMED | Just claimed |
| Arjun | 74LS138 | COMPLETED | Historical |
| Arjun | NE555 | FAILED | mentorNote: "Simulation output does not match datasheet at Vcc=5V" |
| Priya | LM358 | CLAIMED | Active |
| Priya | LM339 | IN_PROGRESS | Active |
| Priya | 74HC595 | COMPLETED | Historical |
| Rohan | AD633 | IN_PROGRESS | Active (SUMMER enrollment) |

**Seed execution:**
```typescript
// package.json
"prisma": {
  "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seed.ts"
}
```
Run: `npx prisma db seed`

**Stop. Verify seed by running `npx prisma studio` and confirming all records exist.**

---

### PHASE 2 — Auth Context, Layout & Navigation

**Goal:** Role-based routing and persistent layouts for both portals. Mock auth for development.

#### 2a — Auth Cookie & Context

Create `lib/auth.ts`:
- Store active `userId` and `role` in a cookie named `esim_user`.
- Export `getCurrentUser(): Promise<User | null>` — reads cookie, queries `prisma.user.findUnique`.
- Export `requireRole(role: Role)` — throws redirect to `/` if role doesn't match.

Create `components/dev-user-switcher.tsx`:
- Renders **only when `process.env.NODE_ENV === 'development'`**.
- A `<Select>` dropdown listing all seeded users by name and role.
- On change: calls a Server Action that sets the `esim_user` cookie and redirects to the appropriate portal root.
- Render this component in the shared top navbar.

#### 2b — Root Layout & Routing

`app/layout.tsx` — Root layout with Toaster (sonner) and font setup only.

`app/page.tsx` — Server Component that reads the auth cookie and redirects:
```typescript
// If role === INTERN → redirect('/intern/dashboard')
// If role === ADMIN || MENTOR → redirect('/admin/dashboard')
// If no cookie → redirect('/intern/dashboard') with first intern as default (dev only)
```

#### 2c — Intern Layout (`app/intern/layout.tsx`)

- Server Component. Calls `requireRole('INTERN')`.
- Top navbar with: eSim logo · "IC Portal" label · Links: `Dashboard` · `Browse ICs` · Dev switcher (dev only) · User name display (right side).
- No sidebar — interns only have 2 navigation destinations.

#### 2d — Admin Layout (`app/admin/layout.tsx`)

- Server Component. Calls `requireRole` for `ADMIN` or `MENTOR`.
- **Persistent left sidebar** (fixed width: 240px) containing:
  - eSim / FOSSEE logo at top
  - Nav links:
    - 📊 Dashboard → `/admin/dashboard`
    - 👥 Interns → `/admin/interns`
    - 🗂️ IC Catalog → `/admin/catalog`
    - ✅ Review Queue → `/admin/review` (show pending count badge)
    - 📨 Name Requests → `/admin/requests` (show pending count badge)
  - User name + role badge at bottom of sidebar
- Top header bar: breadcrumb (current page) · Dev switcher (dev only, right side)

**Stop. Confirm layout renders for both roles before proceeding.**

---

### PHASE 3 — Intern Portal

#### 3a — `/intern/dashboard`

**Data fetching (RSC):**
```typescript
// lib/queries.ts
export async function getInternDashboardData(userId: string) {
  return prisma.batchEnrollment.findFirst({
    where: { userId },
    include: {
      batch: true,
      tasks: {
        include: { ic: { include: { aliases: true } } },
        orderBy: { claimedAt: "desc" },
      },
    },
  });
}
```

**UI — Enrollment Card:**
- Intern name (large heading)
- Batch label badge: `SUMMER 2026`
- Stats row: `Active: N/3` · `Completed: N` · `Failed: N`
- If `active === 3`: show a yellow warning banner: "You have reached the 3-task limit. Complete or submit a task to claim more."

**UI — Active Task Cards (max 3, rendered from active task filter):**

Active = status in `[CLAIMED, IN_PROGRESS, UNDER_REVIEW]`

Each card contains:
- IC canonical name (large, font-mono)
- Alias pills (grey badges) — all aliases
- Category badge (colored) + Technology badge
- Status badge (color-coded: CLAIMED=blue, IN_PROGRESS=yellow, UNDER_REVIEW=purple)
- "Claimed N days ago" (relative time)
- Datasheet link button (if `datasheetUrl` is not null)
- If `mentorNote` exists and status is `FAILED`: red callout box with note text
- Status update button:
  - `CLAIMED` → **"Mark In Progress"** button → Server Action sets status to `IN_PROGRESS`
  - `IN_PROGRESS` → **"Submit for Review"** button → Server Action sets status to `UNDER_REVIEW`
  - `UNDER_REVIEW` → Disabled grey button: "Awaiting Mentor Review"

**UI — Task History Table (bottom of page):**

Shows all tasks with status `COMPLETED` or `FAILED`. Client Component using TanStack Table.

Columns: IC Name · Status · Claimed Date · Completed Date · Mentor Note

Sortable by all date columns. Default sort: `completedAt` descending. No pagination (history is per-intern, bounded).

---

#### 3b — `/intern/browse` — IC Lobby

**URL params:** `?search=&category=&technology=&status=available&page=1&pageSize=50`

**RSC data fetch (`lib/queries.ts`):**
```typescript
export async function getIcsForLobby({
  search, category, technology, showAll, page, pageSize, enrollmentId
}: LobbyParams) {
  const where = {
    AND: [
      search ? {
        OR: [
          { canonicalName: { contains: search, mode: "insensitive" } },
          { aliases: { some: { name: { contains: search, mode: "insensitive" } } } },
        ],
      } : {},
      category ? { category: category as ICCategory } : {},
      technology ? { technology: technology as Technology } : {},
      !showAll ? {
        NOT: {
          tasks: {
            some: {
              status: { in: ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"] },
              enrollment: { batchId: currentBatchId },
            },
          },
        },
      } : {},
    ],
  };
  const [items, total] = await Promise.all([
    prisma.iC.findMany({
      where,
      include: { aliases: true, tasks: { include: { enrollment: { include: { user: true } } } } },
      skip: (page - 1) * pageSize,
      take: pageSize,
      orderBy: { canonicalName: "asc" },
    }),
    prisma.iC.count({ where }),
  ]);
  return { items, total, page, pageSize };
}
```

**UI — Filter Bar (Client Component):**
- Global search input (debounced 300ms, updates URL param)
- Category `<Select>` — options with counts: `OP_AMP (124)`
- Technology `<Select>` — options with counts
- Status toggle: `Available Only` (default) | `Show All`
- "Request New IC" button → opens modal (see 3c)
- Result count display: "Showing 50 of 312 available ICs"

**UI — Data Table (TanStack Table, server-side):**

| Column | Sortable | Detail |
|---|---|---|
| Canonical Name | ✓ | font-mono, bold |
| Aliases | — | Up to 3 grey badge pills, then `+N more` tooltip |
| Category | ✓ | Colored badge |
| Technology | ✓ | Badge |
| Description | — | Truncated at 60 chars, full text on hover tooltip |
| Status | ✓ | `AVAILABLE` (green) · `TAKEN` (grey, shows assignee name) · `COMPLETED` (blue) |
| Actions | — | Claim button |

**Claim button rules:**
- If IC status is not AVAILABLE → button disabled, tooltip: "Currently claimed by [Name]"
- If intern is at 3 active tasks → button disabled, tooltip: "Release a task to claim more"
- If IC available and intern under limit → active green **"Claim"** button

**On Claim button click:**
- Opens confirmation `<Dialog>`:
  - Title: "Claim [IC Name]?"
  - Body: Shows all aliases, category, technology
  - Footer: Cancel · **"Confirm Claim"** (triggers Server Action)

**Claim Server Action (`app/actions/claim-ic.ts`):**
```typescript
"use server"
// Must use prisma.$transaction:
// 1. Count intern's active tasks in this enrollment. If >= 3, throw error.
// 2. Check if any ICAlias of this IC has an active task in the same batch. If yes, throw collision error.
// 3. Create ICTask with status CLAIMED.
// All three steps in a single $transaction.
```

On success: `revalidatePath('/intern/browse')` and `revalidatePath('/intern/dashboard')`.

On collision error: show toast: "This IC (or its alias [alias name]) is already claimed by [Intern Name] in your batch."

---

#### 3c — Request New IC Modal

Trigger: "Request New IC" button on `/intern/browse`.

**Modal contents:**
- Input: "IC Name or Part Number" (e.g., `UA741`, `LM386`)
- Submit button: **"Check & Request"**

**Server Action logic (`app/actions/request-ic.ts`):**

```typescript
"use server"
// Step 1: Normalize input (uppercase, strip spaces).
// Step 2: Check if canonicalName already exists → toast "Already exists, search for [name]"
// Step 3: Check if name matches any ICAlias → toast "This is an alias of [canonical]. Claim that IC instead."
// Step 4: Regex whitelist check:
//   Known prefixes: /^(74|54|LM|LT|AD|TL|NE|SA|MC|UA|CD|HCF|SN|DS|IDT|MAX|ICL|OP|CA|RC)/i
//   If matches → auto-create IC with UNCLAIMED status, category=OTHER, technology=UNSPECIFIED.
//     Show toast: "[Name] added to catalog. You can now claim it."
//     Revalidate /intern/browse.
//   If does not match → create AddRequest with status PENDING.
//     Show toast: "Request for [Name] sent to admin for review."
```

---

### PHASE 4 — Admin Portal

#### 4a — `/admin/dashboard`

**Data fetching (RSC — all in parallel with `Promise.all`):**

```typescript
const [
  totalICs, unclaimedICs, inProgressICs, completedICs,
  activeInterns, pendingReviews, pendingRequests,
  recentActivity, awaitingReview
] = await Promise.all([
  prisma.iC.count(),
  prisma.iC.count({ where: { tasks: { none: { status: { in: ["CLAIMED","IN_PROGRESS","UNDER_REVIEW","COMPLETED"] } } } } }),
  prisma.iC.count({ where: { tasks: { some: { status: { in: ["CLAIMED","IN_PROGRESS"] } } } } }),
  prisma.iC.count({ where: { tasks: { some: { status: "COMPLETED" } } } }),
  prisma.batchEnrollment.count({ where: { batch: { year: 2026 } } }),
  prisma.iCTask.count({ where: { status: "UNDER_REVIEW" } }),
  prisma.addRequest.count({ where: { status: "PENDING" } }),
  // last 10 task updates in 48h
  prisma.iCTask.findMany({ where: { updatedAt: { gte: new Date(Date.now() - 48*60*60*1000) } }, include: { ic: true, enrollment: { include: { user: true } } }, orderBy: { updatedAt: "desc" }, take: 10 }),
  // oldest 10 UNDER_REVIEW tasks
  prisma.iCTask.findMany({ where: { status: "UNDER_REVIEW" }, include: { ic: true, enrollment: { include: { user: true } } }, orderBy: { updatedAt: "asc" }, take: 10 }),
]);
```

**UI Layout:**

Stats Cards Row (4 cards):
- **Total ICs:** `804` (with breakdown: Unclaimed · In Progress · Completed)
- **Active Interns (2026):** `N`
- **Pending Reviews:** `N` — clicking navigates to `/admin/review`
- **Name Requests:** `N` — clicking navigates to `/admin/requests`

Side-by-side compact tables below:

Left — **"Awaiting Review (oldest first)":**
- Columns: IC Name · Intern · Days Waiting · Quick Actions (Approve / Reject buttons)
- Days waiting > 7: highlight row in amber

Right — **"Recent Activity (last 48h)":**
- Columns: Intern Name · Action (e.g., "Claimed LM741") · Time Ago

---

#### 4b — `/admin/interns`

**URL params:** `?search=&batch=&status=&page=1&pageSize=25&sort=name&order=asc`

**RSC data fetch:**
```typescript
export async function getAdminInternsList({ search, batchId, statusFilter, page, pageSize, sort, order }) {
  return prisma.batchEnrollment.findMany({
    where: {
      batch: batchId ? { id: batchId } : undefined,
      user: search ? { name: { contains: search, mode: "insensitive" } } : undefined,
    },
    include: {
      user: true,
      batch: true,
      tasks: { select: { status: true, updatedAt: true } },
    },
    skip: (page - 1) * pageSize,
    take: pageSize,
    orderBy: sort === "name" ? { user: { name: order } } : { [sort]: order },
  });
}
```

**Filter Bar:**
- Search by intern name
- Batch `<Select>` — "All Batches" · "Summer 2026" · "Winter 2026"
- Status filter `<Select>`: "All" · "Has Active Tasks" · "Has Failed Tasks" · "All Completed"

**Table Columns:**

| Column | Sortable | Detail |
|---|---|---|
| Name | ✓ | Clickable → `/admin/interns/[id]` |
| Batch | ✓ | Badge |
| Active Tasks | ✓ | `2/3` — red badge if at limit (3/3) |
| Completed | ✓ | Count |
| Failed | ✓ | Count — red text if > 0 |
| Last Activity | ✓ | Relative time from most recent `updatedAt` |
| Actions | — | "View" button |

---

#### 4c — `/admin/interns/[id]`

**RSC data fetch:**
```typescript
export async function getInternDetail(enrollmentId: string) {
  return prisma.batchEnrollment.findUnique({
    where: { id: enrollmentId },
    include: {
      user: true,
      batch: true,
      tasks: {
        include: { ic: { include: { aliases: true } } },
        orderBy: { claimedAt: "desc" },
      },
    },
  });
}
```

**UI:**
- Header: Intern name · Email · Batch label · Enrolled date
- Stats row: Active `N/3` · Completed `N` · Failed `N` · Completion rate `N%`
- Full task history TanStack Table:
  - Columns: IC Name (mono) · Aliases · Status · Claimed Date · Completed Date · Days Taken · Mentor Note
  - Filter by status (All · Active · Completed · Failed)
  - Sortable by all date and status columns
- For any task with status `UNDER_REVIEW`: show inline **Approve** and **Reject** buttons in the Actions column (same Server Actions as `/admin/review`)

---

#### 4d — `/admin/catalog`

**URL params:** `?search=&category=&technology=&quality=&page=1&pageSize=50&sort=canonicalName&order=asc`

**RSC data fetch:**
```typescript
export async function getAdminCatalog({ search, category, technology, quality, page, pageSize, sort, order }) {
  const where = {
    AND: [
      search ? {
        OR: [
          { canonicalName: { contains: search, mode: "insensitive" } },
          { aliases: { some: { name: { contains: search, mode: "insensitive" } } } },
        ],
      } : {},
      category ? { category } : {},
      technology ? { technology } : {},
      quality === "no_datasheet" ? { datasheetUrl: null } : {},
      quality === "unspecified_tech" ? { technology: "UNSPECIFIED" } : {},
      quality === "no_aliases" ? { aliases: { none: {} } } : {},
    ],
  };
  const [items, total] = await Promise.all([
    prisma.iC.findMany({
      where,
      include: {
        aliases: true,
        _count: { select: { tasks: true, aliases: true } },
        tasks: { select: { status: true }, orderBy: { claimedAt: "desc" }, take: 1 },
      },
      skip: (page - 1) * pageSize,
      take: pageSize,
      orderBy: { [sort]: order },
    }),
    prisma.iC.count({ where }),
  ]);
  return { items, total };
}
```

**Filter Bar:**
- Global search (canonical name + aliases)
- Category multiselect (checkboxes in a popover)
- Technology multiselect (checkboxes in a popover)
- Data Quality filter `<Select>`: "All" · "UNSPECIFIED Technology" · "No Datasheet" · "No Aliases"
- "Add New IC" button (top right) → opens Add IC Dialog

**Table Columns:**

| Column | Sortable | Detail |
|---|---|---|
| Canonical Name | ✓ | font-mono · links to `/admin/catalog/[id]` |
| Aliases | — | Count badge: `3 aliases` — hover shows list |
| Category | ✓ | Colored badge |
| Technology | ✓ | Badge — `UNSPECIFIED` renders as orange warning badge |
| Description | — | Truncated at 60 chars |
| Datasheet | — | Link icon if URL exists, warning icon if null |
| Assignment | ✓ | `Available` (green) · `In Progress — [Name]` (yellow) · `Completed` (blue) |
| Actions | — | Edit button |

**Add New IC Dialog:**
- Fields: Canonical Name · Description · Category (required, no default) · Technology (required, no default) · Datasheet URL (optional)
- Canonical Name uniqueness check on submit
- Server Action creates IC with explicit category and technology (SPICE fidelity enforcement)

---

#### 4e — `/admin/catalog/[id]`

**RSC data fetch:**
```typescript
export async function getICDetail(icId: string) {
  return prisma.iC.findUnique({
    where: { id: icId },
    include: {
      aliases: true,
      tasks: {
        include: { enrollment: { include: { user: true, batch: true } } },
        orderBy: { claimedAt: "desc" },
      },
      createdFromRequest: { include: { requester: true } },
    },
  });
}
```

**UI:**
- Header: Canonical name (large, mono) · Category badge · Technology badge
- Edit inline form for: Description · Category · Technology · Datasheet URL
  - "Save Changes" Server Action: `prisma.iC.update(...)`

- **Alias Manager section:**
  - List of all aliases with individual delete buttons
  - On delete: checks no active task depends on this alias, then deletes
  - "Add Alias" input + button
  - Server Action: checks `prisma.iCAlias.findUnique({ where: { name } })` first — if exists, show error: "This name already exists as an alias for [other IC name]"

- **Full Assignment History table (all batches):**
  - Columns: Intern Name · Batch · Status · Claimed Date · Completed Date · Days Taken · Mentor Note
  - Sortable by status and date

- **"Merge into another IC" button** → opens same Combobox Merge Dialog as in `/admin/requests`

---

### PHASE 5 — Admin Review & Requests

#### 5a — `/admin/review` — Task Review Queue

**URL params:** `?search=&batch=&page=1&pageSize=25&sort=updatedAt&order=asc`

**RSC data fetch:**
```typescript
export async function getReviewQueue({ search, batchId, page, pageSize }) {
  return prisma.iCTask.findMany({
    where: {
      status: "UNDER_REVIEW",
      enrollment: {
        batchId: batchId || undefined,
        user: search ? { name: { contains: search, mode: "insensitive" } } : undefined,
      },
    },
    include: {
      ic: { include: { aliases: true } },
      enrollment: { include: { user: true, batch: true } },
    },
    skip: (page - 1) * pageSize,
    take: pageSize,
    orderBy: { updatedAt: "asc" }, // oldest first by default
  });
}
```

**Filter Bar:**
- Search by intern name or IC name
- Batch `<Select>`
- Sort toggle: "Oldest First" (default) | "Newest First"

**Table Columns:**

| Column | Sortable | Detail |
|---|---|---|
| IC Name | ✓ | font-mono |
| Aliases | — | Grey pills |
| Intern | ✓ | Name + batch badge |
| Submitted | ✓ | Relative time |
| Days Waiting | ✓ | Number — red if > 7 days |
| Actions | — | Approve · Reject buttons |

**Approve Server Action:**
- Sets `status = COMPLETED`, `completedAt = new Date()`
- `revalidatePath('/admin/review')`, `revalidatePath('/admin/dashboard')`

**Reject flow:**
- Reject button opens `<Dialog>`:
  - Title: "Reject Task — [IC Name]"
  - Mandatory `<Textarea>` labeled "Reason for rejection (intern will see this)"
  - Submit is disabled if textarea is empty
  - Server Action: sets `status = FAILED`, saves `mentorNote`

---

#### 5b — `/admin/requests` — Naming Request Queue

**URL params:** `?status=PENDING&page=1&pageSize=25`

**RSC data fetch:**
```typescript
export async function getAddRequests({ status, page, pageSize }) {
  return prisma.addRequest.findMany({
    where: { status: status || "PENDING" },
    include: { requester: true, reviewer: true, suggestedMergeWith: true, createdIc: true },
    skip: (page - 1) * pageSize,
    take: pageSize,
    orderBy: { createdAt: "asc" },
  });
}
```

**Filter Bar:**
- Status tabs: `Pending (N)` · `Approved (N)` · `Merged (N)` · `Rejected (N)`

**Table Columns:**

| Column | Detail |
|---|---|
| Requested Name | Raw string intern typed — e.g., `ua 741` |
| Normalized | Auto-uppercased, stripped — e.g., `UA741` |
| Requested By | Intern name |
| Date | Relative time |
| Status | Badge |
| Actions | "Review" button (opens Review Dialog) |

**Review Dialog (The Smart Merge UI):**

This is a single `<Dialog>` with a mode toggle inside it.

Header: "Review IC Request — [Raw Name]"
Requested by: [Intern Name] · [Date]

**Two action paths inside the dialog:**

**Path A — Merge with Existing IC:**
- Searchable `<Command>` combobox (shadcn Command component)
- Label: "Search existing ICs by canonical name or alias..."
- On keystroke: Server Action queries:
  ```typescript
  prisma.iC.findMany({
    where: {
      OR: [
        { canonicalName: { contains: query, mode: "insensitive" } },
        { aliases: { some: { name: { contains: query, mode: "insensitive" } } } },
      ],
    },
    include: { aliases: true },
    take: 10,
  })
  ```
- Results display: `LM741` · `[µA741, UA741, LM741CN]` (show aliases beneath)
- Admin selects target IC
- Optional "Reviewer Note" textarea
- **"Approve & Merge"** button → Server Action:
  1. Check `prisma.iCAlias.findUnique({ where: { name: normalizedName } })` — if exists, abort with error "This alias already exists"
  2. `prisma.iCAlias.create({ data: { name: normalizedName, icId: selectedIcId, note: reviewNote } })`
  3. `prisma.addRequest.update({ where: { id }, data: { status: "MERGED", reviewerId, reviewNote, reviewedAt } })`

**Path B — Approve as New Canonical IC:**
- Toggle/tab: "Create New IC"
- Fields (ALL required, no defaults):
  - Category `<Select>` — explicitly required
  - Technology `<Select>` — explicitly required
  - Description `<Textarea>` (optional but shown)
  - Datasheet URL `<Input>` (optional)
- **"Approve as New IC"** button → Server Action:
  1. `prisma.iC.create({ data: { canonicalName: normalizedName, category, technology, description, datasheetUrl } })`
  2. `prisma.addRequest.update({ status: "APPROVED_AS_NEW", createdIcId: newIc.id, reviewerId, reviewedAt })`

**Path C — Reject:**
- "Reject" text button (subtle, bottom left of dialog)
- Opens confirmation with mandatory note
- Server Action: `prisma.addRequest.update({ status: "REJECTED", reviewNote, reviewedAt })`

---

## 📁 Final File Structure

```
esim-ic-portal/
├── app/
│   ├── layout.tsx                    # Root layout (Toaster only)
│   ├── page.tsx                      # Role-based redirect
│   ├── intern/
│   │   ├── layout.tsx                # Intern top navbar layout
│   │   ├── dashboard/
│   │   │   └── page.tsx              # RSC: task cards + history
│   │   └── browse/
│   │       └── page.tsx              # RSC: IC lobby table
│   └── admin/
│       ├── layout.tsx                # Admin sidebar layout
│       ├── dashboard/
│       │   └── page.tsx              # RSC: stats + quick tables
│       ├── interns/
│       │   ├── page.tsx              # RSC: intern list table
│       │   └── [id]/
│       │       └── page.tsx          # RSC: intern detail
│       ├── catalog/
│       │   ├── page.tsx              # RSC: IC catalog table
│       │   └── [id]/
│       │       └── page.tsx          # RSC: IC detail + alias mgr
│       ├── review/
│       │   └── page.tsx              # RSC: review queue table
│       └── requests/
│           └── page.tsx              # RSC: add request queue
├── components/
│   ├── dev-user-switcher.tsx         # Dev-only user switcher
│   ├── intern/
│   │   ├── task-card.tsx             # Active task card (Client)
│   │   ├── task-history-table.tsx    # History TanStack table (Client)
│   │   ├── lobby-table.tsx           # IC lobby TanStack table (Client)
│   │   ├── lobby-filters.tsx         # Filter bar (Client)
│   │   └── request-ic-modal.tsx      # Request IC dialog (Client)
│   └── admin/
│       ├── intern-table.tsx          # Interns TanStack table (Client)
│       ├── catalog-table.tsx         # IC catalog TanStack table (Client)
│       ├── review-table.tsx          # Review queue TanStack table (Client)
│       ├── requests-table.tsx        # AddRequest TanStack table (Client)
│       ├── reject-dialog.tsx         # Mandatory note reject dialog (Client)
│       ├── review-request-dialog.tsx # Smart merge dialog (Client)
│       └── add-ic-dialog.tsx         # New IC creation dialog (Client)
├── app/
│   └── actions/
│       ├── claim-ic.ts               # Atomic claim Server Action
│       ├── update-task-status.ts     # Status update Server Action
│       ├── request-ic.ts             # Request new IC Server Action
│       ├── approve-task.ts           # Review approve Server Action
│       ├── reject-task.ts            # Review reject Server Action
│       ├── merge-request.ts          # AddRequest merge Server Action
│       ├── approve-new-ic.ts         # AddRequest approve-as-new Server Action
│       ├── reject-request.ts         # AddRequest reject Server Action
│       ├── add-alias.ts              # Add IC alias Server Action
│       └── update-ic.ts              # Edit IC metadata Server Action
├── lib/
│   ├── prisma.ts                     # Singleton Prisma client
│   ├── auth.ts                       # Cookie auth helpers
│   └── queries.ts                    # All reusable Prisma query functions
└── prisma/
    ├── schema.prisma                 # Final schema (above)
    └── seed.ts                       # Full seed script
```

---

## ⚠️ Critical Implementation Notes

### Server-Side Table Pattern (Follow This Exactly)

Every table page follows this pattern — never deviate:

```typescript
// app/admin/catalog/page.tsx (RSC)
export default async function CatalogPage({ searchParams }) {
  const { search, category, technology, page } = searchParams;
  const { items, total } = await getAdminCatalog({ search, category, technology, page: Number(page) || 1, pageSize: 50 });
  return <CatalogTable data={items} total={total} />;
}

// components/admin/catalog-table.tsx ("use client")
"use client"
// TanStack Table with columns defined here.
// Filtering/sorting updates URL params via useRouter().push() — does NOT re-filter client-side.
// Pagination buttons do router.push(`?page=${newPage}`) — triggers RSC refetch.
```

### Naming Collision Check (Implement in `claim-ic.ts`)

```typescript
// Inside prisma.$transaction:
const icWithAliases = await tx.iC.findUnique({
  where: { id: icId },
  include: { aliases: true },
});
const allNames = [icWithAliases.canonicalName, ...icWithAliases.aliases.map(a => a.name)];
const collision = await tx.iCTask.findFirst({
  where: {
    status: { in: ["CLAIMED", "IN_PROGRESS", "UNDER_REVIEW"] },
    enrollment: { batchId: currentBatchId },
    ic: {
      OR: [
        { canonicalName: { in: allNames } },
        { aliases: { some: { name: { in: allNames } } } },
      ],
    },
  },
  include: { enrollment: { include: { user: true } } },
});
if (collision) throw new Error(`Collision: already claimed by ${collision.enrollment.user.name}`);
```

### Badge Color Mapping (Consistent Across All Tables)

```typescript
// Category → badge color
const categoryColors = {
  OP_AMP: "blue", COMPARATOR: "indigo", DIGITAL_LOGIC: "violet",
  VOLTAGE_REGULATOR: "green", MIXED_SIGNAL: "orange", DEVICE_MODEL: "cyan",
  IP_BLOCK: "pink", OTHER: "grey",
};
// Technology → badge color
const techColors = {
  TTL: "red", CMOS: "blue", BICMOS: "purple", ANALOG: "green", MIXED: "orange",
  UNSPECIFIED: "yellow", // Always render as a warning
};
// Status → badge color
const statusColors = {
  CLAIMED: "blue", IN_PROGRESS: "yellow", UNDER_REVIEW: "purple",
  COMPLETED: "green", FAILED: "red", UNCLAIMED: "grey",
};
```

---

## ✅ Phase Completion Checklist

| Phase | Deliverable | Done? |
|---|---|---|
| 0 | Next.js + Prisma + shadcn/ui scaffold, DB connected | ☒ |
| 1 | Seed script runs, all users/ICs/tasks in DB | ☒ |
| 2 | Role-based layouts, nav, dev switcher working | ☒ |
| 3a | Intern dashboard: task cards + history table | ☒ |
| 3b | Intern browse: server-side table with search/filter/claim | ☒ |
| 3c | Request New IC modal with regex + AddRequest fallback | ☒ |
| 4a | Admin dashboard: stats cards + quick tables | ☒ |
| 4b | Admin interns: searchable, sortable table | ☒ |
| 4c | Admin intern detail: full task history + inline review | ☒ |
| 4d | Admin catalog: filtered table + Add IC dialog | ☒ |
| 4e | Admin IC detail: edit metadata + alias manager | ☒ |
| 5a | Admin review queue: approve + mandatory-note reject | ☒ |
| 5b |approve-as-new | ☒ |

**Do not mark a phase done until the UI renders correctly with real seeded data and all Server Actions succeed without errors.**

---

### PHASE 7 — NextAuth & Editable Batch Management

**Step 1: NextAuth Implementation (The Security Gate)**
- Install `next-auth` and configure the Google Provider.
- `signIn` Callback: Only allow sign-in if the user's email already exists in the `User` table. If it does not exist, redirect to an error page: "Access Denied: Your email is not whitelisted. Please use the exact email you provided to FOSSEE."
- `session`/`jwt` Callback: Pass the `User.id` and `Role` into the NextAuth session so Server Components can use them.
- Name Capture: On their very first successful login, update the Prisma User record with the name provided by the Google profile.
- Remove all legacy Mock Auth code.

**Step 2: The Batch Management UI (`/admin/batches`)**
- Create a dedicated page for Admins to manage intern rosters.
- Dropdown/selector to choose the active Batch.
- Display a TanStack Table showing enrolled interns for the selected batch. Columns: Email, Name, Joined Date, Actions.
- Action 1 (Bulk Add): Button opens a Dialog with a Textarea for comma-separated emails. A Server Action parses these, upserts into the `User` table, and creates a `BatchEnrollment`.
- Action 2 (Remove): Trash icon to delete that specific `BatchEnrollment`.