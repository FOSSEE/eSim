"use client";

import { useState } from "react";
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
import { handleReviewAction } from "@/app/actions/review-actions";
import { toast } from "sonner";

interface ReviewActionModalProps {
  taskId: string;
  icName: string;
  internName: string;
  action: "approve" | "reject";
}

export function ReviewActionModal({ taskId, icName, internName, action }: ReviewActionModalProps) {
  const [open, setOpen] = useState(false);
  const [note, setNote] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const isReject = action === "reject";
  const title = isReject ? "Reject Task" : "Approve Task";
  const buttonVariant = isReject ? "destructive" : "default";

  const onConfirm = async () => {
    if (isReject && !note.trim()) {
      toast.error("Feedback note is required when rejecting a task.");
      return;
    }

    setIsLoading(true);
    try {
      const result = await handleReviewAction(taskId, action, note);
      if (result.success) {
        toast.success(`Task ${isReject ? "rejected" : "approved"} successfully.`);
        setOpen(false);
        setNote("");
      } else {
        toast.error(result.error || "An error occurred.");
      }
    } catch (error) {
      toast.error("Failed to perform action.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={
        <Button variant={buttonVariant} size="sm">
          {action === "approve" ? "Approve" : "Reject"}
        </Button>
      } />
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title} - {icName}</DialogTitle>
          <DialogDescription>
             You are about to {action} the work submitted by <strong>{internName}</strong> for IC <strong>{icName}</strong>. 
             {action === 'approve' 
                 ? " This will mark the task as COMPLETED." 
                 : " This will revert the task to IN_PROGRESS. You MUST provide feedback below."}
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          <label htmlFor="note" className="block text-sm font-medium mb-2">
            Feedback Note {isReject && <span className="text-destructive">*</span>}
          </label>
          <Textarea
            id="note"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder={isReject ? "Explain what needs to be fixed..." : "Optional positive feedback..."}
            rows={4}
          />
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)} disabled={isLoading}>
            Cancel
          </Button>
          <Button 
            variant={buttonVariant} 
            onClick={onConfirm} 
            disabled={isLoading || (isReject && note.trim().length === 0)}
          >
            {isLoading ? "Processing..." : `Confirm ${action === "approve" ? "Approval" : "Rejection"}`}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
