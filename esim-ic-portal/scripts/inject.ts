import "dotenv/config";
import {
  ICCategory,
  ICStatus,
  InternshipSeason,
  Role,
  Technology,
} from "@prisma/client";
import { prisma } from "../src/lib/prisma";
import fs from "fs";
import path from "path";

function parseBatchLabel(label: string): { season: InternshipSeason; year: number; finalLabel: string } {
    const l = label.toLowerCase();
    if (l.includes("summer")) return { season: InternshipSeason.SUMMER, year: 2026, finalLabel: "Summer 2026" };
    if (l.includes("winter")) return { season: InternshipSeason.WINTER, year: 2026, finalLabel: "Winter 2026" };
    if (l.includes("sli")) return { season: InternshipSeason.SLI, year: 2026, finalLabel: "SLI 2026" };
    return { season: InternshipSeason.OTHER, year: 2026, finalLabel: label };
}

async function main() {
  const jsonPath = path.join(__dirname, "../deepseek_json_20260410_f96bb7.json");
  const data = JSON.parse(fs.readFileSync(jsonPath, "utf-8"));

  // Delete everything
  console.log("Cleaning database...");
  await prisma.addRequest.deleteMany();
  await prisma.iCTask.deleteMany();
  await prisma.iCAlias.deleteMany();
  await prisma.iC.deleteMany();
  await prisma.batchEnrollment.deleteMany();
  await prisma.batch.deleteMany();
  await prisma.user.deleteMany();

  console.log("Creating default admin and mentor...");
  await prisma.user.create({ data: { name: "Admin User", email: "admin@esim.fossee.in", role: Role.ADMIN } });
  await prisma.user.create({ data: { name: "Mentor User", email: "mentor@esim.fossee.in", role: Role.MENTOR } });

  const internNames = new Set<string>();
  const batchLabels = new Set<string>();

  for (const ic of data) {
    if (ic.assignments) {
      for (const a of ic.assignments) {
        internNames.add(a.internName);
        batchLabels.add(a.batchLabel);
      }
    }
  }

  console.log("Creating Interns...");
  const userRecords = new Map<string, string>();
  const seenEmails = new Set<string>();
  
  for (const name of internNames) {
    let email = `${name.replace(/[^a-zA-Z0-9]+/g, '.').toLowerCase()}@intern.esim.in`;
    let counter = 1;
    while (seenEmails.has(email)) {
      email = `${name.replace(/[^a-zA-Z0-9]+/g, '.').toLowerCase()}${counter}@intern.esim.in`;
      counter++;
    }
    seenEmails.add(email);
    
    const u = await prisma.user.create({
      data: { name, email, role: Role.INTERN }
    });
    userRecords.set(name, u.id);
  }

  console.log("Creating Batches...");
  const batchRecords = new Map<string, string>();
  // We may have multiple labels mapping to the same season/year using parseBatchLabel.
  // We should create unique batch for each season/year combination.
  const createdBatches = new Set<string>();
  for (const label of batchLabels) {
    const info = parseBatchLabel(label);
    const key = `${info.year}-${info.season}`;
    let batchId;
    if (createdBatches.has(key)) {
      const b = await prisma.batch.findUnique({ where: { year_season: { year: info.year, season: info.season } } });
      if (b) batchId = b.id;
    } else {
      const b = await prisma.batch.create({
          data: { year: info.year, season: info.season, label: info.finalLabel }
      });
      batchId = b.id;
      createdBatches.add(key);
    }
    batchRecords.set(label, batchId!);
  }

  console.log("Creating Batch Enrollments...");
  const enrollmentRecords = new Map<string, string>(); // key: internName-batchLabel -> enrollmentId
  for (const ic of data) {
    if (!ic.assignments) continue;
    for (const a of ic.assignments) {
      const userId = userRecords.get(a.internName);
      const batchId = batchRecords.get(a.batchLabel);
      if (!userId || !batchId) continue;

      const key = `${userId}-${batchId}`;
      if (!enrollmentRecords.has(key)) {
        const e = await prisma.batchEnrollment.create({
          data: { userId, batchId }
        });
        enrollmentRecords.set(key, e.id);
      }
    }
  }

  console.log(`Injecting ${data.length} ICs and tasks...`);
  let count = 0;
  const chunkSize = 20;

  const seenAliases = new Set<string>();
  const seenCanonical = new Set<string>();

  for (let i = 0; i < data.length; i += chunkSize) {
    const chunk = data.slice(i, i + chunkSize);
    await Promise.all(
      chunk.map(async (row: any) => {
        try {
          if (seenCanonical.has(row.canonicalName)) {
             console.log(`Skipping duplicate canonicalName: ${row.canonicalName}`);
             return;
          }
          seenCanonical.add(row.canonicalName);
          seenAliases.add(row.canonicalName); // canonical name often shouldn't clash with alias either

          const finalAliases: { name: string }[] = [];
          if (row.aliases && row.aliases.length > 0) {
            for (let name of row.aliases) {
              name = name.trim();
              if (!seenAliases.has(name)) {
                seenAliases.add(name);
                finalAliases.push({ name });
              }
            }
          }

          const ic = await prisma.iC.create({
            data: {
              canonicalName: row.canonicalName,
              description: row.description || null,
              category: (row.category || "OTHER") as ICCategory,
              technology: (row.technology || "UNSPECIFIED") as Technology,
              aliases: finalAliases.length > 0 ? { create: finalAliases } : undefined,
            },
          });

          if (row.assignments && row.assignments.length > 0) {
            for (const a of row.assignments) {
              const userId = userRecords.get(a.internName);
              const batchId = batchRecords.get(a.batchLabel);
              const enrollmentId = enrollmentRecords.get(`${userId}-${batchId}`);
              if (!enrollmentId) continue;

              let finalStatus = a.status as ICStatus;
              if ((finalStatus as any) === "Under review by mentor") {
                finalStatus = ICStatus.UNDER_REVIEW;
              }

              let completedAt = null;
              if (finalStatus === ICStatus.COMPLETED) {
                completedAt = new Date();
              }

              await prisma.iCTask.create({
                data: {
                  enrollmentId,
                  icId: ic.id,
                  status: finalStatus,
                  completedAt: completedAt,
                },
              });
            }
          }
        } catch (e) {
          console.error(`Failed on row ${row.canonicalName}: ${e}`);
        }
      })
    );
    count += chunk.length;
    console.log(`Inserted ${count} / ${data.length}...`);
  }

  console.log("Data injection complete!");
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
