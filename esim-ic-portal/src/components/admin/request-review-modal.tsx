"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { processAddRequest, searchICsForMerge } from "@/app/actions/request-actions";
import { toast } from "sonner";
import { Search } from "lucide-react";

import { Label } from "@/components/ui/label";

interface RequestReviewModalProps {
  requestId: string;
  rawName: string;
  normalizedName: string;
  suggestedAliases: string[];
  internName: string;
}

export function RequestReviewModal({ requestId, rawName, normalizedName, suggestedAliases, internName }: RequestReviewModalProps) {
  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState<"MERGE" | "APPROVE_AS_NEW" | "REJECT">("MERGE");
  const [note, setNote] = useState("");
  const [canonicalName, setCanonicalName] = useState(normalizedName || "");
  const [aliases, setAliases] = useState(suggestedAliases?.join(", ") || "");
  const [search, setSearch] = useState("");
  const [options, setOptions] = useState<{id: string, canonicalName: string}[]>([]);
  const [selectedIcId, setSelectedIcId] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (mode === "MERGE" && open) {
      const delay = setTimeout(() => {
        if (search.trim().length >= 2) {
          searchICsForMerge(search).then(setOptions);
        } else {
          setOptions([]);
        }
      }, 300);
      return () => clearTimeout(delay);
    }
  }, [search, mode, open]);

  const onConfirm = async () => {
    if (mode === "REJECT" && !note.trim()) {
      toast.error("Feedback note is required when rejecting.");
      return;
    }
    if (mode === "MERGE" && !selectedIcId) {
      toast.error("Please select an IC to merge with.");
      return;
    }
    if (mode === "APPROVE_AS_NEW" && !canonicalName.trim()) {
      toast.error("Canonical Name is required.");
      return;
    }

    setIsLoading(true);
    try {
      const parsedAliases = aliases.split(",").map(a => a.trim()).filter(a => a.length > 0);
      const result = await processAddRequest(requestId, mode, {
        mergeWithIcId: mode === "MERGE" ? selectedIcId : undefined,
        reviewNote: note,
        finalName: mode === "APPROVE_AS_NEW" ? canonicalName.trim() : undefined,
        finalAliases: mode === "APPROVE_AS_NEW" ? parsedAliases : undefined,
      });

      if (result.success) {
        toast.success(result.success);
        setOpen(false);
      } else if (result.error) {
        toast.error(result.error);
      }
    } catch (error) {
      toast.error("Failed to process request.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={<Button variant="outline" size="sm">Review</Button>} />
      <DialogContent className="max-w-lg">
        <DialogHeader>
          <DialogTitle>Review Add Request</DialogTitle>
          <DialogDescription>
             Intern: <strong>{internName}</strong> <br/>
             Requested Name: <strong className="text-zinc-900 dark:text-zinc-100">{rawName}</strong> <br/>
             Normalized: <span className="font-mono">{normalizedName}</span>
          </DialogDescription>
        </DialogHeader>

        <div className="flex space-x-2 border-b pb-2 mb-2">
          <Button variant={mode === "MERGE" ? "default" : "ghost"} size="sm" onClick={() => setMode("MERGE")}>
            Merge
          </Button>
          <Button variant={mode === "APPROVE_AS_NEW" ? "default" : "ghost"} size="sm" onClick={() => setMode("APPROVE_AS_NEW")}>
            Approve as New
          </Button>
          <Button variant={mode === "REJECT" ? "destructive" : "ghost"} size="sm" onClick={() => setMode("REJECT")}>
            Reject
          </Button>
        </div>

        <div className="py-2 min-h-[200px]">
          {mode === "MERGE" && (
             <div className="space-y-4">
               <div className="relative">
                 <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                 <Input 
                   placeholder="Search existing IC..." 
                   className="pl-9" 
                   value={search}
                   onChange={(e) => setSearch(e.target.value)}
                 />
               </div>
               
               <div className="border rounded-md overflow-y-auto max-h-[200px] h-[200px] bg-muted/20">
                 {options.length === 0 ? (
                   <div className="p-4 text-center text-sm text-muted-foreground">
                      {search.length < 2 ? "Type at least 2 characters to search" : "No ICs found."}
                   </div>
                 ) : (
                   <div className="p-1 flex flex-col gap-1">
                     {options.map((ic) => (
                        <div 
                           key={ic.id}
                           onClick={() => setSelectedIcId(ic.id)}
                           className={`px-3 py-2 text-sm rounded cursor-pointer ${selectedIcId === ic.id ? 'bg-primary text-primary-foreground' : 'hover:bg-muted'}`}
                        >
                           {ic.canonicalName}
                        </div>
                     ))}
                   </div>
                 )}
               </div>
             </div>
          )}

          {mode === "APPROVE_AS_NEW" && (
             <div className="space-y-4">
               <p className="text-sm">
                 Create a new IC and link the intern's task to it.
               </p>
               <div className="grid gap-2">
                 <Label htmlFor="canonicalName">Canonical Name</Label>
                 <Input 
                   id="canonicalName"
                   value={canonicalName}
                   onChange={(e) => setCanonicalName(e.target.value.toUpperCase().replace(/\s+/g, ""))}
                 />
               </div>
               <div className="grid gap-2 mt-2">
                 <Label htmlFor="aliases" className="flex items-center justify-between">
                   <span>Aliases (Optional)</span>
                   <span className="text-xs text-muted-foreground font-normal">Comma-separated</span>
                 </Label>
                 <Input 
                   id="aliases"
                   value={aliases}
                   onChange={(e) => setAliases(e.target.value)}
                   placeholder="e.g. LM741, 741 Op-Amp"
                 />
                 <p className="text-xs text-muted-foreground">
                   Intern suggested: {suggestedAliases?.length ? suggestedAliases.join(", ") : "None"}
                 </p>
               </div>
             </div>
          )}

          {mode === "REJECT" && (
             <div className="space-y-2">
               <label htmlFor="note" className="block text-sm font-medium">
                 Feedback Note <span className="text-destructive">*</span>
               </label>
               <Textarea
                 id="note"
                 value={note}
                 onChange={(e) => setNote(e.target.value)}
                 placeholder="Explain why this IC request is rejected (e.g. Invalid part number)..."
                 rows={4}
               />
             </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button 
            variant={mode === "REJECT" ? "destructive" : "default"} 
            onClick={onConfirm} 
            disabled={
              isLoading || 
              (mode === "REJECT" && note.trim().length === 0) || 
              (mode === "MERGE" && !selectedIcId)
            }
          >
            {isLoading ? "Processing..." : "Confirm"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
