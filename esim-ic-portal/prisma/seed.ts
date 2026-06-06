import "dotenv/config";
import {
  ICCategory,
  ICStatus,
  InternshipSeason,
  Role,
  Technology,
} from "@prisma/client";

import { prisma } from "../src/lib/prisma";

const users = [
  { name: "Admin User", email: "admin@esim.fossee.in", role: Role.ADMIN },
  { name: "Mentor User", email: "mentor@esim.fossee.in", role: Role.MENTOR },
  { name: "Arjun Sharma", email: "arjun@intern.esim.in", role: Role.INTERN },
  { name: "Priya Nair", email: "priya@intern.esim.in", role: Role.INTERN },
  { name: "Rohan Mehta", email: "rohan@intern.esim.in", role: Role.INTERN },
] as const;

const batches = [
  {
    year: 2026,
    season: InternshipSeason.SUMMER,
    label: "Summer 2026",
  },
  {
    year: 2026,
    season: InternshipSeason.WINTER,
    label: "Winter 2026",
  },
] as const;

const ics = [
  {
    canonicalName: "LM741",
    description: "General purpose op-amp",
    category: ICCategory.OP_AMP,
    technology: Technology.ANALOG,
    aliases: ["UA741", "µA741", "LM741CN"],
  },
  {
    canonicalName: "LM324",
    description: "Quad op-amp",
    category: ICCategory.OP_AMP,
    technology: Technology.ANALOG,
    aliases: ["LM324N", "LM324D"],
  },
  {
    canonicalName: "LM358",
    description: "Dual op-amp",
    category: ICCategory.OP_AMP,
    technology: Technology.ANALOG,
    aliases: ["LM358N", "LM358P"],
  },
  {
    canonicalName: "LM339",
    description: "Quad comparator",
    category: ICCategory.COMPARATOR,
    technology: Technology.ANALOG,
    aliases: ["LM339N"],
  },
  {
    canonicalName: "LM7805",
    description: "5V linear voltage regulator",
    category: ICCategory.VOLTAGE_REGULATOR,
    technology: Technology.ANALOG,
    aliases: ["UA7805", "MC7805"],
  },
  {
    canonicalName: "LM317",
    description: "Adjustable voltage regulator",
    category: ICCategory.VOLTAGE_REGULATOR,
    technology: Technology.ANALOG,
    aliases: ["LM317T"],
  },
  {
    canonicalName: "74LS138",
    description: "3-to-8 line decoder",
    category: ICCategory.DIGITAL_LOGIC,
    technology: Technology.TTL,
    aliases: ["SN74LS138", "DM74LS138"],
  },
  {
    canonicalName: "74HC244",
    description: "Octal buffer/line driver",
    category: ICCategory.DIGITAL_LOGIC,
    technology: Technology.CMOS,
    aliases: ["SN74HC244", "74HC244N"],
  },
  {
    canonicalName: "74HC595",
    description: "8-bit shift register",
    category: ICCategory.DIGITAL_LOGIC,
    technology: Technology.CMOS,
    aliases: ["SN74HC595", "74HC595N"],
  },
  {
    canonicalName: "74LS04",
    description: "Hex inverter",
    category: ICCategory.DIGITAL_LOGIC,
    technology: Technology.TTL,
    aliases: ["SN74LS04", "DM74LS04"],
  },
  {
    canonicalName: "IDT72V201",
    description: "FIFO memory",
    category: ICCategory.MIXED_SIGNAL,
    technology: Technology.CMOS,
    aliases: ["72V201"],
  },
  {
    canonicalName: "DS90CR285",
    description: "Channel link serializer",
    category: ICCategory.MIXED_SIGNAL,
    technology: Technology.CMOS,
    aliases: ["DS90CR285A"],
  },
  {
    canonicalName: "AD633",
    description: "Low cost analog multiplier",
    category: ICCategory.MIXED_SIGNAL,
    technology: Technology.ANALOG,
    aliases: ["AD633JN"],
  },
  {
    canonicalName: "NE555",
    description: "Timer IC",
    category: ICCategory.OTHER,
    technology: Technology.BICMOS,
    aliases: ["LM555", "NE555P", "SA555"],
  },
  {
    canonicalName: "CD4051B",
    description: "8-channel analog multiplexer",
    category: ICCategory.MIXED_SIGNAL,
    technology: Technology.CMOS,
    aliases: ["HCF4051B"],
  },
] as const;

async function main() {
  await prisma.addRequest.deleteMany();
  await prisma.iCTask.deleteMany();
  await prisma.iCAlias.deleteMany();
  await prisma.iC.deleteMany();
  await prisma.batchEnrollment.deleteMany();
  await prisma.batch.deleteMany();
  await prisma.user.deleteMany();

  const userRecords = new Map<string, { id: string; name: string }>();
  for (const u of users) {
    const created = await prisma.user.create({ data: { ...u } });
    userRecords.set(u.email, { id: created.id, name: created.name });
  }

  const batchRecords = new Map<string, { id: string; label: string }>();
  for (const b of batches) {
    const created = await prisma.batch.create({ data: { ...b } });
    const key = `${b.year}-${b.season}`;
    batchRecords.set(key, { id: created.id, label: created.label });
  }

  const summerId = batchRecords.get("2026-SUMMER")!.id;
  const winterId = batchRecords.get("2026-WINTER")!.id;

  const arjunId = userRecords.get("arjun@intern.esim.in")!.id;
  const priyaId = userRecords.get("priya@intern.esim.in")!.id;
  const rohanId = userRecords.get("rohan@intern.esim.in")!.id;

  const enrollArjunSummer = await prisma.batchEnrollment.create({
    data: { userId: arjunId, batchId: summerId },
  });
  const enrollPriyaSummer = await prisma.batchEnrollment.create({
    data: { userId: priyaId, batchId: summerId },
  });
  const enrollRohanSummer = await prisma.batchEnrollment.create({
    data: { userId: rohanId, batchId: summerId },
  });
  await prisma.batchEnrollment.create({
    data: { userId: rohanId, batchId: winterId },
  });

  const icRecords = new Map<string, string>();
  for (const row of ics) {
    const { aliases, ...icData } = row;
    const ic = await prisma.iC.create({
      data: {
        ...icData,
        aliases: {
          create: aliases.map((name) => ({ name })),
        },
      },
    });
    icRecords.set(row.canonicalName, ic.id);
  }

  const taskDefs: {
    enrollmentId: string;
    canonical: string;
    status: ICStatus;
    mentorNote?: string;
    completedAt?: Date;
  }[] = [
    {
      enrollmentId: enrollArjunSummer.id,
      canonical: "LM741",
      status: ICStatus.IN_PROGRESS,
    },
    {
      enrollmentId: enrollArjunSummer.id,
      canonical: "LM324",
      status: ICStatus.UNDER_REVIEW,
    },
    {
      enrollmentId: enrollArjunSummer.id,
      canonical: "LM7805",
      status: ICStatus.CLAIMED,
    },
    {
      enrollmentId: enrollArjunSummer.id,
      canonical: "74LS138",
      status: ICStatus.COMPLETED,
      completedAt: new Date(),
    },
    {
      enrollmentId: enrollArjunSummer.id,
      canonical: "NE555",
      status: ICStatus.FAILED,
      mentorNote:
        "Simulation output does not match datasheet at Vcc=5V",
    },
    {
      enrollmentId: enrollPriyaSummer.id,
      canonical: "LM358",
      status: ICStatus.CLAIMED,
    },
    {
      enrollmentId: enrollPriyaSummer.id,
      canonical: "LM339",
      status: ICStatus.IN_PROGRESS,
    },
    {
      enrollmentId: enrollPriyaSummer.id,
      canonical: "74HC595",
      status: ICStatus.COMPLETED,
      completedAt: new Date(),
    },
    {
      enrollmentId: enrollRohanSummer.id,
      canonical: "AD633",
      status: ICStatus.IN_PROGRESS,
    },
  ];

  for (const t of taskDefs) {
    const icId = icRecords.get(t.canonical);
    if (!icId) throw new Error(`Missing IC: ${t.canonical}`);
    await prisma.iCTask.create({
      data: {
        enrollmentId: t.enrollmentId,
        icId,
        status: t.status,
        mentorNote: t.mentorNote,
        completedAt: t.completedAt,
      },
    });
  }
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error(e);
    await prisma.$disconnect();
    process.exit(1);
  });
