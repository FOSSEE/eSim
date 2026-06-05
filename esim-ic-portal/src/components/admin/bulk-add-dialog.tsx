"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { bulkAddInternsAction } from "@/app/actions/batch-actions";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";

export function BulkAddDialog({ batchId }: { batchId: string }) {
  const [open, setOpen] = useState(false);
  const [emails, setEmails] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  async function onSubmit() {
    if (!emails.trim()) return;
    setLoading(true);
    try {
      const res = await bulkAddInternsAction(batchId, emails);
      toast.success(`Successfully enrolled ${res.count} interns out of ${res.total} provided.`);
      setOpen(false);
      setEmails("");
      router.refresh();
    } catch (error: any) {
      toast.error(error.message || "Failed to add interns");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={<Button />}>
        Bulk Add Interns
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add Interns by Email</DialogTitle>
        </DialogHeader>
        <div className="py-4">
          <p className="text-sm text-muted-foreground mb-4">
            Paste comma or newline separated email addresses. Users who do not
            exist will be automatically created and added to this batch.
          </p>
          <Textarea
            value={emails}
            onChange={(e) => setEmails(e.target.value)}
            placeholder="intern1@example.com, intern2@example.com"
            rows={10}
          />
        </div>
        <div className="flex justify-end gap-2">
          <Button variant="outline" onClick={() => setOpen(false)}>
            Cancel
          </Button>
          <Button onClick={onSubmit} disabled={loading}>
            {loading ? "Adding..." : "Add to Batch"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
