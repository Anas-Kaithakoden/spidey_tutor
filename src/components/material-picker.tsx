"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { listMaterials, type Material } from "@/lib/api";
import { useStudy } from "@/lib/context";
import { EmptyState } from "@/components/ui/empty-state";
import { Button } from "@/components/ui/button";
import {
  FileText,
  File,
  Image as ImageIcon,
  Plus,
  ArrowRight,
  Sparkles,
} from "lucide-react";

interface MaterialPickerProps {
  title?: string;
  description?: string;
  onSelect?: (material: Material) => void;
}

export function MaterialPicker({
  title = "Select a Study Set",
  description = "Choose which uploaded lecture slides or notes you want to study.",
  onSelect,
}: MaterialPickerProps) {
  const { setMaterial } = useStudy();
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    listMaterials()
      .then((res) => {
        if (!cancelled) setMaterials(res);
      })
      .catch(() => {
        if (!cancelled) setMaterials([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  function handlePick(m: Material) {
    setMaterial(m);
    onSelect?.(m);
  }

  function getSourceIcon(type: string) {
    if (type === "pdf") return <FileText className="size-5 text-[#8e7fff]" />;
    if (type === "image") return <ImageIcon className="size-5 text-[#ffb3b6]" />;
    return <File className="size-5 text-[#e3c464]" />;
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-center">
        <div className="size-8 rounded-full border-2 border-[#8e7fff] border-t-transparent animate-spin mb-3" />
        <p className="text-sm text-[#c8c4d6]">Loading your study sets...</p>
      </div>
    );
  }

  if (materials.length === 0) {
    return (
      <EmptyState
        mascotMood="idle"
        title="No study material selected"
        description="Upload a PDF, lecture deck, or paste your notes to begin studying."
        action={
          <Button
            render={<Link href="/add" />}
            nativeButton={false}
            size="lg"
            className="rounded-xl bg-[#8e7fff] hover:bg-[#8e7fff]/90 text-white font-bold shadow-md shadow-[#8e7fff]/25"
          >
            <Plus className="size-4 mr-2" />
            <span>Add Study Material</span>
          </Button>
        }
      />
    );
  }

  return (
    <div className="flex flex-col gap-6 max-w-2xl mx-auto p-6 rounded-3xl bg-[#1d1a25] border border-white/5 shadow-xl">
      <div className="flex items-center justify-between">
        <div>
          <div className="inline-flex items-center gap-1.5 text-xs font-bold text-[#8e7fff] uppercase tracking-wider mb-1">
            <Sparkles className="size-3.5" />
            <span>Available Study Sets</span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">{title}</h2>
          <p className="text-xs text-[#c8c4d6] mt-0.5">{description}</p>
        </div>

        <Button
          render={<Link href="/add" />}
          nativeButton={false}
          variant="outline"
          size="sm"
          className="rounded-xl border-white/10 hover:bg-[#2c2834] text-xs font-semibold"
        >
          <Plus className="size-3.5 mr-1" />
          <span>Upload New</span>
        </Button>
      </div>

      <div className="grid gap-3">
        {materials.map((m) => (
          <div
            key={m.id}
            onClick={() => handlePick(m)}
            className="group flex items-center justify-between p-4 rounded-2xl bg-[#211e2a] hover:bg-[#2c2834] border border-white/5 hover:border-[#8e7fff]/40 transition-all cursor-pointer shadow-sm hover:-translate-y-0.5"
          >
            <div className="flex items-center gap-3.5 min-w-0">
              <div className="size-10 rounded-xl bg-[#1d1a25] flex items-center justify-center border border-white/5 shrink-0">
                {getSourceIcon(m.source_type)}
              </div>
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-white truncate group-hover:text-[#8e7fff] transition-colors">
                    {m.title}
                  </h3>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-[#1d1a25] text-[#c8c4d6] border border-white/5 shrink-0">
                    {m.source_type}
                  </span>
                </div>
                <p className="text-xs text-[#c8c4d6] mt-0.5">
                  {m.word_count || Math.round(m.char_count / 5)} words indexed
                </p>
              </div>
            </div>

            <Button
              type="button"
              size="sm"
              className="rounded-xl bg-[#8e7fff]/15 text-[#8e7fff] group-hover:bg-[#8e7fff] group-hover:text-white transition-all font-semibold text-xs shrink-0 ml-3"
            >
              <span>Study Set</span>
              <ArrowRight className="size-3.5 ml-1 transition-transform group-hover:translate-x-0.5" />
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
}
