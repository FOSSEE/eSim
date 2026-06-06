"use client";

import { useState } from "react";
import { ICCategory, Technology } from "@prisma/client";
import { updateICMetadata, addICAlias, deleteICAlias } from "@/app/actions/catalog-actions";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { toast } from "sonner";
import { Loader2, Plus, Trash2 } from "lucide-react";

export function ICMetadataManager({
  ic
}: {
  ic: {
    id: string;
    description: string | null;
    category: ICCategory;
    technology: Technology;
    datasheetUrl: string | null;
    aliases: { id: string; name: string }[];
  }
}) {
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [formData, setFormData] = useState({
    description: ic.description || "",
    category: ic.category,
    technology: ic.technology,
    datasheetUrl: ic.datasheetUrl || "",
  });

  const [newAlias, setNewAlias] = useState("");
  const [isAddingAlias, setIsAddingAlias] = useState(false);
  const [deletingAliasId, setDeletingAliasId] = useState<string | null>(null);

  const categories = Object.values(ICCategory);
  const technologies = Object.values(Technology);

  const handleSave = async () => {
    setIsSaving(true);
    const result = await updateICMetadata(ic.id, formData);
    setIsSaving(false);

    if (result.error) {
      toast.error(result.error);
    } else {
      toast.success(result.success);
      setIsEditing(false);
    }
  };

  const handleAddAlias = async () => {
    if (!newAlias.trim()) return;
    setIsAddingAlias(true);
    const result = await addICAlias(ic.id, newAlias);
    setIsAddingAlias(false);

    if (result.error) {
      toast.error(result.error);
    } else {
      toast.success(result.success);
      setNewAlias("");
    }
  };

  const handleDeleteAlias = async (aliasId: string) => {
    if (!confirm("Are you sure you want to delete this alias?")) return;
    
    setDeletingAliasId(aliasId);
    const result = await deleteICAlias(aliasId, ic.id);
    setDeletingAliasId(null);

    if (result.error) {
      toast.error(result.error);
    } else {
      toast.success(result.success);
    }
  };

  return (
    <div className="grid gap-6 md:grid-cols-2">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Metadata</CardTitle>
          {!isEditing && (
            <Button variant="outline" size="sm" onClick={() => setIsEditing(true)}>
              Edit
            </Button>
          )}
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Description</Label>
            {isEditing ? (
              <Textarea 
                value={formData.description} 
                onChange={e => setFormData({ ...formData, description: e.target.value })} 
              />
            ) : (
              <p className="text-sm text-balance">{ic.description || <span className="italic text-muted-foreground">No description provided.</span>}</p>
            )}
          </div>
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Category</Label>
              {isEditing ? (
                <Select value={formData.category} onValueChange={(val) => val && setFormData({ ...formData, category: val as ICCategory })}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {categories.map(c => <SelectItem key={c} value={c}>{c}</SelectItem>)}
                  </SelectContent>
                </Select>
              ) : (
                <div><Badge variant="outline">{ic.category}</Badge></div>
              )}
            </div>
            <div className="space-y-2">
              <Label>Technology</Label>
              {isEditing ? (
                <Select value={formData.technology} onValueChange={(val) => val && setFormData({ ...formData, technology: val as Technology })}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    {technologies.map(t => <SelectItem key={t} value={t}>{t}</SelectItem>)}
                  </SelectContent>
                </Select>
              ) : (
                <div><Badge variant="secondary">{ic.technology}</Badge></div>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label>Datasheet URL</Label>
            {isEditing ? (
              <Input 
                value={formData.datasheetUrl} 
                onChange={e => setFormData({ ...formData, datasheetUrl: e.target.value })} 
                placeholder="https://..."
              />
            ) : (
              <p className="text-sm truncate">
                {ic.datasheetUrl ? (
                  <a href={ic.datasheetUrl} target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">
                    {ic.datasheetUrl}
                  </a>
                ) : (
                  <span className="italic text-muted-foreground">None</span>
                )}
              </p>
            )}
          </div>

          {isEditing && (
            <div className="flex justify-end gap-2 pt-4">
              <Button variant="ghost" onClick={() => {
                setIsEditing(false);
                setFormData({
                  description: ic.description || "",
                  category: ic.category,
                  technology: ic.technology,
                  datasheetUrl: ic.datasheetUrl || "",
                });
              }} disabled={isSaving}>Cancel</Button>
              <Button onClick={handleSave} disabled={isSaving}>
                {isSaving && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                Save Changes
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Alias Manager</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex gap-2">
            <Input 
              placeholder="Add new alias name..." 
              value={newAlias} 
              onChange={e => setNewAlias(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleAddAlias()}
            />
            <Button onClick={handleAddAlias} disabled={!newAlias.trim() || isAddingAlias}>
              {isAddingAlias ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />}
            </Button>
          </div>

          <div className="space-y-2">
            {ic.aliases.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-4">No aliases exist for this IC.</p>
            ) : (
              <div className="flex flex-wrap gap-2">
                {ic.aliases.map(alias => (
                  <Badge key={alias.id} variant="secondary" className="flex items-center gap-1 pr-1.5 py-1">
                    {alias.name}
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="h-4 w-4 rounded-full hover:bg-destructive/20 hover:text-destructive text-muted-foreground"
                      onClick={() => handleDeleteAlias(alias.id)}
                      disabled={deletingAliasId === alias.id}
                    >
                      {deletingAliasId === alias.id ? <Loader2 className="h-3 w-3 animate-spin" /> : <Trash2 className="h-3 w-3" />}
                    </Button>
                  </Badge>
                ))}
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
