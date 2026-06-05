"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { useState, useEffect } from "react";

export function CatalogFilter() {
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
      router.replace(`/admin/catalog?${params.toString()}`);
    }, 500);

    return () => clearTimeout(timer);
  }, [search, router]); // omitted searchParams to avoid loop

  const updateParam = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());
    if (value && value !== "all") {
      params.set(key, value);
      params.set("page", "1");
    } else {
      params.delete(key);
    }
    router.replace(`/admin/catalog?${params.toString()}`);
  };

  return (
    <div className="flex flex-col sm:flex-row items-center gap-4 mb-4">
      <Input
        placeholder="Search name, aliases, or description..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="max-w-sm"
      />
      <Select value={searchParams.get("quality") || "all"} onValueChange={(val: string | null) => updateParam("quality", val || "")}>
        <SelectTrigger className="w-[180px]">
          <SelectValue placeholder="Data Quality" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All ICs</SelectItem>
          <SelectItem value="unspecified_tech">UNSPECIFIED Tech</SelectItem>
          <SelectItem value="no_datasheet">No Datasheet</SelectItem>
          <SelectItem value="no_aliases">No Aliases</SelectItem>
        </SelectContent>
      </Select>
    </div>
  );
}
