"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Download, Loader2, Sparkles, Beaker } from "lucide-react";
import { useStudy } from "@/lib/context";
import { generateFormulaSheet, downloadFormulaSheetPdf, type FormulaSheet } from "@/lib/api";
import { ModelSelect } from "@/components/model-select";

export default function FormulaSheetPage() {
  const { material, model } = useStudy();
  const [syllabus, setSyllabus] = useState("");
  const [language, setLanguage] = useState<"en" | "ml">("en");
  const [sheet, setSheet] = useState<FormulaSheet | null>(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);

  async function handleGenerate() {
    const text = syllabus.trim() || material?.content || "";
    if (!text || text.length < 10) {
      toast.error("Paste syllabus or upload material first (add page).");
      return;
    }
    setLoading(true);
    try {
      const res = await generateFormulaSheet({
        syllabus: text,
        material_id: material?.id,
        provider: model.provider,
        model_name: model.name,
        language,
      });
      setSheet(res);
      if (res.generated_by === "mock") toast("Formula sheet from mock data");
      else if (res.generated_by === "quick") toast("Quick sheet (deterministic)");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to generate");
    } finally {
      setLoading(false);
    }
  }

  async function handleDownload() {
    const text = syllabus.trim() || material?.content || "";
    if (!text) {
      toast.error("No content to download");
      return;
    }
    setDownloading(true);
    try {
      const blob = await downloadFormulaSheetPdf({
        syllabus: text,
        material_id: material?.id,
        provider: model.provider,
        model_name: model.name,
        language,
      });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "formula-sheet.pdf";
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      toast.success("PDF downloaded");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "PDF download failed");
    } finally {
      setDownloading(false);
    }
  }

  // group by category
  const grouped = sheet
    ? sheet.formulas.reduce<Record<string, typeof sheet.formulas>>((acc, f) => {
        const cat = f.category || "General";
        if (!acc[cat]) acc[cat] = [];
        acc[cat].push(f);
        return acc;
      }, {})
    : {};

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="mb-2 flex items-center gap-2 text-2xl font-bold">
        <Beaker className="size-6 text-primary" /> Formula Sheet
      </h1>
      <p className="mb-8 text-muted-foreground">
        Extract key formulas, equations, and definitions from your material — download as a clean PDF.
      </p>

      <Card className="mb-6">
        <CardContent className="pt-6 space-y-4">
          <div className="flex items-center gap-2">
            <ModelSelect />
            <div className="ml-auto flex items-center gap-2 rounded-lg border bg-card px-2 py-1">
              <Button size="sm" variant={language === "en" ? "secondary" : "ghost"} onClick={() => setLanguage("en")} className="h-7 px-2 text-xs">English</Button>
              <Button size="sm" variant={language === "ml" ? "secondary" : "ghost"} onClick={() => setLanguage("ml")} className="h-7 px-2 text-xs">മലയാളം</Button>
            </div>
          </div>

          <div>
            <Label htmlFor="syllabus">Syllabus / Material {material ? <span className="text-xs text-muted-foreground">— prefilled from “{material.title}”</span> : null}</Label>
            <Textarea
              id="syllabus"
              placeholder="Paste syllabus or leave empty to use current material. E.g. Ohm's Law, Quadratic Formula, Pythagorean..."
              value={syllabus}
              onChange={(e) => setSyllabus(e.target.value)}
              className="mt-2 min-h-[120px]"
            />
            <p className="mt-1 text-xs text-muted-foreground">{(syllabus || material?.content || "").split(/\s+/).filter(Boolean).length} words</p>
          </div>

          <div className="flex flex-wrap gap-3 justify-end">
            <Button onClick={handleGenerate} disabled={loading} className="gap-2">
              {loading ? <Loader2 className="size-4 animate-spin" /> : <Sparkles className="size-4" />}
              {loading ? "Generating..." : "Generate Sheet"}
            </Button>
            {sheet && (
              <Button onClick={handleDownload} disabled={downloading} variant="outline" className="gap-2">
                {downloading ? <Loader2 className="size-4 animate-spin" /> : <Download className="size-4" />}
                {downloading ? "Downloading..." : "Download PDF"}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {sheet && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {sheet.title} <Badge variant="outline" className="ml-auto">{sheet.generated_by}</Badge>
              </CardTitle>
              <p className="text-sm text-muted-foreground">{sheet.description} • {sheet.formulas.length} formulas • {sheet.language}</p>
            </CardHeader>
          </Card>

          {Object.entries(grouped).map(([cat, items]) => (
            <Card key={cat}>
              <CardHeader><CardTitle className="text-base">{cat}</CardTitle></CardHeader>
              <CardContent className="space-y-3">
                {items.map((f, idx) => (
                  <div key={idx} className="rounded-lg border bg-muted/30 p-3">
                    <div className="flex items-start justify-between gap-2">
                      <h4 className="font-medium text-sm">{f.title}</h4>
                      <Badge variant="secondary" className="text-xs">{f.category}</Badge>
                    </div>
                    <div className="mt-1 font-mono text-sm bg-background rounded px-2 py-1 border">{f.formula}</div>
                    <p className="mt-1 text-xs text-muted-foreground">{f.description}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
