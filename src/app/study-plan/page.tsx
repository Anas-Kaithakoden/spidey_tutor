"use client";

import { useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Calendar, Clock, Loader2, Sparkles, BookOpen, RotateCcw, FileUp, X } from "lucide-react";
import { useStudy } from "@/lib/context";
import { generateStudyPlan, generateStudyPlanFromPdf, type StudyPlan } from "@/lib/api";
import { ModelSelect } from "@/components/model-select";

export default function StudyPlanPage() {
  const { material, model } = useStudy();
  const [syllabus, setSyllabus] = useState("");
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [examDate, setExamDate] = useState("");
  const [dailyHours, setDailyHours] = useState(3);
  const [language, setLanguage] = useState<"en" | "ml">("en");
  const [plan, setPlan] = useState<StudyPlan | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    if (!examDate) {
      toast.error("Pick an exam date.");
      return;
    }
    if (new Date(examDate) < new Date(new Date().setHours(0, 0, 0, 0))) {
      toast.error("Exam date cannot be in the past. Pick a future date.");
      return;
    }
    const extra = syllabus.trim();
    if (!pdfFile && !extra && !material?.content) {
      toast.error("Upload a syllabus PDF, paste a syllabus, or add material on the Add page first.");
      return;
    }
    setLoading(true);
    try {
      const res = pdfFile
        ? await generateStudyPlanFromPdf(pdfFile, {
            exam_date: examDate,
            daily_hours: dailyHours,
            provider: model.provider,
            model_name: model.name,
            language,
            syllabus: extra || undefined,
          })
        : await generateStudyPlan({
            syllabus: extra || material?.content || "",
            material_id: material?.id,
            exam_date: examDate,
            daily_hours: dailyHours,
            provider: model.provider,
            model_name: model.name,
            language,
          });
      setPlan(res);
      if (res.generated_by === "mock") toast("Plan from mock data");
      else if (res.generated_by === "quick") toast("Quick plan (deterministic)");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Failed to generate plan");
    } finally {
      setLoading(false);
    }
  }

  const tomorrow = (() => {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${day}`;
  })();
  const daysLeft = examDate ? Math.ceil((new Date(examDate).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24)) : 0;
  const isPast = examDate ? new Date(examDate) < new Date(new Date().setHours(0, 0, 0, 0)) : false;

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="mb-2 flex items-center gap-2 text-2xl font-bold">
        <Calendar className="size-6 text-primary" /> Study Plan
      </h1>
      <p className="mb-8 text-muted-foreground">
        Paste your syllabus and pick your exam date — get a day-by-day plan with focus, tasks, and revision.
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
            <Label htmlFor="syllabus-pdf">Syllabus PDF <span className="text-xs text-muted-foreground">(optional — upload instead of pasting)</span></Label>
            <div className="mt-2 flex items-center gap-2 rounded-lg border border-dashed px-3 py-2.5">
              <FileUp className="size-4 shrink-0 text-muted-foreground" />
              <input
                id="syllabus-pdf"
                type="file"
                accept="application/pdf,.pdf"
                onChange={(e) => {
                  const f = e.target.files?.[0] ?? null;
                  setPdfFile(f);
                  if (f) toast(`Using "${f.name}" as your syllabus`);
                }}
                className="flex-1 text-sm text-muted-foreground file:mr-3 file:cursor-pointer file:rounded-md file:border-0 file:bg-primary/10 file:px-3 file:py-1.5 file:text-sm file:font-medium file:text-primary hover:file:bg-primary/20"
              />
              {pdfFile && (
                <>
                  <Badge variant="secondary" className="max-w-[45%] truncate px-2 py-1 text-xs">
                    {pdfFile.name} ({(pdfFile.size / 1024).toFixed(0)} KB)
                  </Badge>
                  <Button size="sm" variant="ghost" className="h-7 w-7 p-0" onClick={() => setPdfFile(null)} aria-label="Remove PDF">
                    <X className="size-4" />
                  </Button>
                </>
              )}
            </div>
          </div>

          <div>
            <Label htmlFor="syllabus">
              Syllabus {material ? <span className="text-xs text-muted-foreground">— prefilled from “{material.title}”</span> : null}
              {pdfFile && <span className="text-xs text-muted-foreground"> — optional extra topics on top of the PDF</span>}
            </Label>
            <Textarea
              id="syllabus"
              placeholder="Paste syllabus topics, e.g. Module 1: Search, Module 2: Heuristics... Or leave empty to use current material or PDF."
              value={syllabus}
              onChange={(e) => setSyllabus(e.target.value)}
              className="mt-2 min-h-[140px]"
            />
            <p className="mt-1 text-xs text-muted-foreground">{(syllabus || material?.content || "").split(/\s+/).filter(Boolean).length} words</p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <Label htmlFor="exam-date">Exam date</Label>
              <Input
                id="exam-date"
                type="date"
                value={examDate}
                onChange={(e) => setExamDate(e.target.value)}
                className="mt-2"
                min={tomorrow}
              />
              {isPast && <p className="mt-1 text-xs text-destructive">Cannot pick a past date</p>}
              {daysLeft > 0 && !isPast && <p className="mt-1 text-xs text-muted-foreground">{daysLeft} days left</p>}
            </div>
            <div>
              <Label>Daily hours: {dailyHours}h</Label>
              <div className="mt-3 flex items-center gap-3">
                <Clock className="size-4 text-muted-foreground" />
                <input type="range" min={1} max={8} step={1} value={dailyHours} onChange={(e) => setDailyHours(Number(e.target.value))} className="h-1 w-full accent-primary" />
                <Badge variant="secondary">{dailyHours}h</Badge>
              </div>
            </div>
          </div>

          <div className="flex justify-end">
            <Button onClick={handleGenerate} disabled={loading} className="gap-2">
              {loading ? <Loader2 className="size-4 animate-spin" /> : <Sparkles className="size-4" />}
              {loading ? "Generating..." : "Generate Plan"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {plan && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="size-4 text-primary" /> {plan.total_topics} Days → Exam {plan.exam_date} ({plan.days_left} days left, {plan.daily_hours}h/day)
                <Badge variant="outline" className="ml-auto">{plan.generated_by}</Badge>
              </CardTitle>
            </CardHeader>
          </Card>

          <div className="grid gap-3">
            {plan.plan.map((d) => (
              <Card key={d.day} className={d.revision ? "border-primary/40 bg-primary/5" : ""}>
                <CardContent className="pt-4">
                  <div className="mb-2 flex flex-wrap items-center gap-2">
                    <Badge>Day {d.day}</Badge>
                    <span className="text-xs text-muted-foreground">{d.date}</span>
                    <Badge variant={d.revision ? "secondary" : "outline"} className="ml-auto gap-1">
                      {d.revision && <RotateCcw className="size-3" />} {d.focus} • {d.duration_hours}h {d.revision && "• Revision"}
                    </Badge>
                  </div>
                  <h3 className="font-medium">{d.topic}</h3>
                  <ul className="mt-2 list-disc space-y-1 pl-5 text-sm text-muted-foreground">
                    {d.tasks.map((t, i) => (
                      <li key={i}>{t}</li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>

          {plan.tips.length > 0 && (
            <Card>
              <CardHeader><CardTitle className="text-base">Tips</CardTitle></CardHeader>
              <CardContent>
                <ul className="list-disc space-y-1 pl-5 text-sm text-muted-foreground">
                  {plan.tips.map((tip, i) => (
                    <li key={i}>{tip}</li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
