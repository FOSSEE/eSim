"use client";

import { useRouter } from "next/navigation";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function BatchSelector({
  batches,
  currentBatchId,
}: {
  batches: { id: string; label: string; year: number; season: string }[];
  currentBatchId: string;
}) {
  const router = useRouter();

  return (
    <Select
      value={currentBatchId}
      onValueChange={(val) => {
        router.push(`/admin/batches?batchId=${val}`);
      }}
    >
      <SelectTrigger className="w-[240px]">
        <SelectValue placeholder="Select a batch..." />
      </SelectTrigger>
      <SelectContent>
        {batches.map((b) => (
          <SelectItem key={b.id} value={b.id}>
            {b.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
