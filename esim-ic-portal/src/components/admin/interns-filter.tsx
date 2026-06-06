"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Input } from "@/components/ui/input";
import { useState, useEffect } from "react";
// Ensure use-debounce is available, otherwise implement simple timeout. For simplicity I will just use setTimeout.

export function InternsFilter() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [search, setSearch] = useState(searchParams.get("search") || "");

  useEffect(() => {
    const timer = setTimeout(() => {
      const params = new URLSearchParams(searchParams.toString());
      if (search) {
        params.set("search", search);
        params.set("page", "1");
      } else {
        params.delete("search");
      }
      router.replace(`/admin/interns?${params.toString()}`);
    }, 500);

    return () => clearTimeout(timer);
  }, [search, router]); // omitted searchParams to avoid loop

  return (
    <div className="flex items-center gap-4 mb-4">
      <Input
        placeholder="Search interns by name..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="max-w-sm"
      />
    </div>
  );
}
