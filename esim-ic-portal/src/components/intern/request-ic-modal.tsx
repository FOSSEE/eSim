"use client"

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Textarea } from "@/components/ui/textarea";
import { requestIcAction } from "@/app/actions/request-ic";
import { toast } from "sonner";
import { Plus, Info } from "lucide-react";

export function RequestIcModal() {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  async function onSubmit(formData: FormData) {
    setLoading(true);
    try {
      const result = await requestIcAction(formData);
      if (result.error) {
        toast.error(result.error);
      } else if (result.success) {
        toast.success(result.success);
        setOpen(false);
      }
    } catch (e) {
      toast.error("Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={
        <Button variant="outline" className="gap-2">
          <Plus className="h-4 w-4" />
          Request New IC
        </Button>
      } />
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Request New IC</DialogTitle>
          <DialogDescription>
            Can't find an IC in the catalog? Enter its full name and part number here.
          </DialogDescription>
          <div className="mt-2 p-3 bg-blue-50 dark:bg-blue-950/40 text-blue-800 dark:text-blue-300 rounded-md text-xs border border-blue-200 dark:border-blue-900/50 flex flex-col gap-1">
            <span className="font-semibold">💡 Tip</span>
            <p>Always search the existing database before requesting a newly created entry to avoid duplicates.</p>
          </div>
        </DialogHeader>
        <form action={onSubmit} className="grid gap-4 py-4">
          <div className="grid gap-2">
            <div className="flex items-center gap-1">
              <Label htmlFor="icName">Full Manufacturer Part Number</Label>
              <TooltipProvider delay={300}>
                <Tooltip>
                  <TooltipTrigger className="inline-flex">
                    <Info className="h-4 w-4 text-muted-foreground cursor-help" />
                  </TooltipTrigger>
                  <TooltipContent className="max-w-xs">
                    <p>Look at the top of your component's datasheet. Include prefixes (e.g., SN, LM, CD) but ignore trailing packaging codes (e.g., -N, -SMD).</p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
            <Input
              id="icName"
              name="icName"
              placeholder="e.g., NE555P (Not just '555')"
              className="uppercase"
              required
            />
            <p className="text-xs text-muted-foreground">
              Provide the exact part number. This will be the main identifying name.
            </p>
          </div>
          <div className="grid gap-2 mt-2">
            <Label htmlFor="icAliases">Suggested Aliases (Optional)</Label>
            <Input
              id="icAliases"
              name="icAliases"
              placeholder="e.g., 555 timer, precision timer"
            />
            <p className="text-xs text-muted-foreground">
              Comma-separated list of common names or alternate part numbers to help others find this IC.
            </p>
          </div>
          <div className="grid gap-2 mt-2">
            <Label htmlFor="datasheetUrl">Datasheet URL (Optional)</Label>
            <Input
              id="datasheetUrl"
              name="datasheetUrl"
              placeholder="https://..."
              type="url"
            />
          </div>
          <div className="grid gap-2 mt-2">
            <Label htmlFor="additionalDetails">Additional Details (Optional)</Label>
            <Textarea
              id="additionalDetails"
              name="additionalDetails"
              placeholder="What type of component is this, or do you know any of its alternate names?"
              className="resize-none"
              rows={3}
            />
          </div>
          
          <p className="text-sm text-muted-foreground mt-2">
            Standard 74xx and CMOS chips will be added instantly. Specialized chips will be sent to the Admin queue for manual SPICE fidelity review.
          </p>

          <DialogFooter className="mt-4">
            <Button type="button" variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading}>
              {loading ? "Checking..." : "Check & Request"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
