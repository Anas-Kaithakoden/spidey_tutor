"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { ArrowRight, Loader2 } from "lucide-react";
import {
  createExam,
  getMaterial,
  listMaterials,
  type Material,
} from "@/lib/api";
import { ModelSelect } from "@/components/model-select";

const difficulties = [
  { value: "easy", label: "Easy", desc: "Basic recall questions" },
  { value: "medium", label: "Medium", desc: "Understanding & application" },
  { value: "hard", label: "Hard", desc: "Analysis & problem solving" },
] as const;

const questionCounts = [5, 8, 10, 15];

const durationOptions = [10, 15, 20, 30];

export default function ExamSetup() {
  const router = useRouter();
  const {
    material,
    setMaterial,
    examConfig,
    setExamConfig,
    setActiveExam,
    model,
  } = useStudy();
  const [difficulty, setDifficulty] = useState(examConfig.difficulty);
  const [questionCount, setQuestionCount] = useState(examConfig.questionCount);
  const [durationMinutes, setDurationMinutes] = useState(
    examConfig.durationMinutes
  );
  const [title, setTitle] = useState(examConfig.title);
  const [materials, setMaterials] = useState<Material[]>([]);
  const [materialId, setMaterialId] = useState<number | null>(() => {
    if (typeof window === "undefined") return null;
    const id = Number(
      new URLSearchParams(window.location.search).get("material_id")
    );
    return Number.isFinite(id) && id > 0 ? id : null;
  });
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (materialId !== null) return;
    listMaterials()
      .then((mats) => {
        setMaterials(mats);
        setMaterialId(material ? material.id : (mats[0]?.id ?? null));
      })
      .catch(() => toast.error("Failed to load study materials."));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [materialId]);

  async function handleStart() {
    if (!materialId) {
      toast.error("Add study material first.");
      router.push("/add");
      return;
    }

    setGenerating(true);
    try {
      let currentMaterial = material;
      if (!currentMaterial || currentMaterial.id !== materialId) {
        currentMaterial = await getMaterial(materialId);
        setMaterial(currentMaterial);
      }

      const config = { difficulty, questionCount, durationMinutes, title };
      setExamConfig(config);
      const exam = await createExam({
        material_id: currentMaterial.id,
        title: title || undefined,
        difficulty: config.difficulty,
        question_count: config.questionCount,
        duration_minutes: config.durationMinutes,
        provider: model.provider,
        model_name: model.name,
      });
      setActiveExam(exam);
      if (exam.generated_by === "mock") {
        toast.info(
          exam.warning ??
            `Showing sample questions — AI generation via ${model.provider} failed. Check the backend .env.`
        );
      } else if (exam.generated_by === "quick") {
        toast.info("Quick Mode: questions generated deterministically, no AI call.");
      }
      router.push("/exam");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to create exam.");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Exam Setup</h1>
      <p className="mb-8 text-muted-foreground">
        Timed exam with mixed question types and AI-graded answers.
      </p>

      <div className="space-y-8">
        {/* Model */}
        <ModelSelect />

        {/* Material */}
        {materials.length > 0 && (
          <section>
            <Label className="mb-3 block text-base font-medium">Study Material</Label>
            <select
              value={materialId ?? ""}
              disabled={generating}
              onChange={(e) => setMaterialId(Number(e.target.value))}
              className="flex h-9 w-full rounded-md border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
            >
              {materials.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.title}
                </option>
              ))}
            </select>
          </section>
        )}

        {/* Title */}
        <section>
          <Label className="mb-3 block text-base font-medium">
            Exam Title <span className="text-xs text-muted-foreground">(optional)</span>
          </Label>
          <Input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Unit 2 Practice Exam"
            disabled={generating}
          />
        </section>

        {/* Difficulty */}
        <section>
          <Label className="mb-3 block text-base font-medium">Difficulty</Label>
          <div className="grid grid-cols-3 gap-3">
            {difficulties.map((d) => (
              <button
                key={d.value}
                onClick={() => setDifficulty(d.value)}
                disabled={generating}
                className={`flex flex-col items-center gap-1 rounded-xl border-2 p-4 text-center transition-colors cursor-pointer disabled:opacity-50 ${
                  difficulty === d.value
                    ? "border-primary bg-primary/5"
                    : "border-transparent bg-muted/50 hover:bg-muted"
                }`}
              >
                <span className="font-medium">{d.label}</span>
                <span className="text-xs text-muted-foreground">{d.desc}</span>
              </button>
            ))}
          </div>
        </section>

        {/* Number of Questions */}
        <section>
          <Label className="mb-3 block text-base font-medium">
            Number of Questions
          </Label>
          <div className="grid grid-cols-4 gap-3">
            {questionCounts.map((count) => (
              <button
                key={count}
                onClick={() => setQuestionCount(count)}
                disabled={generating}
                className={`rounded-xl border-2 px-4 py-3 text-center font-medium transition-colors cursor-pointer disabled:opacity-50 ${
                  questionCount === count
                    ? "border-primary bg-primary/5"
                    : "border-transparent bg-muted/50 hover:bg-muted"
                }`}
              >
                {count}
              </button>
            ))}
          </div>
        </section>

        {/* Duration */}
        <section>
          <Label className="mb-3 block text-base font-medium">
            Duration <span className="text-xs text-muted-foreground">(auto-submits at 0:00)</span>
          </Label>
          <div className="grid grid-cols-4 gap-3">
            {durationOptions.map((mins) => (
              <button
                key={mins}
                onClick={() => setDurationMinutes(mins)}
                disabled={generating}
                className={`rounded-xl border-2 px-4 py-3 text-center font-medium transition-colors cursor-pointer disabled:opacity-50 ${
                  durationMinutes === mins
                    ? "border-primary bg-primary/5"
                    : "border-transparent bg-muted/50 hover:bg-muted"
                }`}
              >
                {mins} min
              </button>
            ))}
          </div>
        </section>
      </div>

      <div className="mt-10 flex justify-end">
        <Button
          onClick={handleStart}
          disabled={generating || materials.length === 0}
          className="gap-2 px-8"
        >
          {generating ? (
            <>
              <Loader2 className="size-4 animate-spin" />
              Generating questions...
            </>
          ) : (
            <>
              Start Exam
              <ArrowRight className="size-4" />
            </>
          )}
        </Button>
      </div>
    </div>
  );
}