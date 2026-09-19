"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { ArrowRight, Clock, Loader2 } from "lucide-react";
import { createQuiz, getMaterial } from "@/lib/api";
import { ModelSelect } from "@/components/model-select";

const difficulties = [
  { value: "easy", label: "Easy", desc: "Basic recall questions" },
  { value: "medium", label: "Medium", desc: "Understanding & application" },
  { value: "hard", label: "Hard", desc: "Analysis & problem solving" },
] as const;

const questionCounts = [5, 10, 15, 20];

const timerOptions = [5, 10, 15, 20];

export default function QuizSetup() {
  const router = useRouter();
  const { material, setMaterial, quizConfig, setQuizConfig, setActiveQuiz, model } = useStudy();
  const [difficulty, setDifficulty] = useState(quizConfig.difficulty);
  const [questionCount, setQuestionCount] = useState(quizConfig.questionCount);
  const [timerEnabled, setTimerEnabled] = useState(quizConfig.timerEnabled);
  const [timerMinutes, setTimerMinutes] = useState(quizConfig.timerMinutes);
  const [generating, setGenerating] = useState(false);

  async function handleStart() {
    const params = new URLSearchParams(window.location.search);
    const materialId = Number(params.get("material_id"));

    let currentMaterial = material;
    if (materialId && (!currentMaterial || currentMaterial.id !== materialId)) {
      setGenerating(true);
      try {
        currentMaterial = await getMaterial(materialId);
        setMaterial(currentMaterial);
      } catch (err) {
        toast.error(
          err instanceof Error ? err.message : "Failed to load material."
        );
        setGenerating(false);
        return;
      }
    }

    if (!currentMaterial) {
      toast.error("Add study material first.");
      router.push("/add");
      return;
    }

    setGenerating(true);
    try {
      const config = { difficulty, questionCount, timerEnabled, timerMinutes };
      setQuizConfig(config);
      const quiz = await createQuiz({
        material_id: currentMaterial.id,
        difficulty: config.difficulty,
        question_count: config.questionCount,
        timer_enabled: config.timerEnabled,
        timer_minutes: config.timerMinutes,
        provider: model.provider,
        model_name: model.name,
      });
      setActiveQuiz(quiz);
      if (quiz.generated_by === "mock") {
        toast.info(
          quiz.warning ??
            `Showing sample questions — AI generation via ${model.provider} failed. Check the backend .env.`
        );
      } else if (quiz.generated_by === "quick") {
        toast.info("Quick Mode: questions generated deterministically, no AI call.");
      }
      router.push("/quiz");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to create quiz.");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Quiz Setup</h1>
      <p className="mb-8 text-muted-foreground">
        Configure your quiz before you begin.
      </p>

      <div className="space-y-8">
        {/* Model */}
        <ModelSelect />

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

        {/* Timer */}
        <section>
          <div className="mb-3 flex items-center justify-between">
            <Label className="text-base font-medium" htmlFor="timer-toggle">
              <span className="flex items-center gap-2">
                <Clock className="size-4" />
                Timer
              </span>
            </Label>
            <Switch
              id="timer-toggle"
              checked={timerEnabled}
              onCheckedChange={setTimerEnabled}
            />
          </div>

          {timerEnabled && (
            <div className="grid grid-cols-4 gap-3">
              {timerOptions.map((mins) => (
                <button
                  key={mins}
                  onClick={() => setTimerMinutes(mins)}
                  disabled={generating}
                  className={`rounded-xl border-2 px-4 py-3 text-center font-medium transition-colors cursor-pointer disabled:opacity-50 ${
                    timerMinutes === mins
                      ? "border-primary bg-primary/5"
                      : "border-transparent bg-muted/50 hover:bg-muted"
                  }`}
                >
                  {mins} min
                </button>
              ))}
            </div>
          )}
        </section>
      </div>

      <div className="mt-10 flex justify-end">
        <Button
          onClick={handleStart}
          disabled={generating}
          className="gap-2 px-8"
        >
          {generating ? (
            <>
              <Loader2 className="size-4 animate-spin" />
              Generating questions...
            </>
          ) : (
            <>
              Start Quiz
              <ArrowRight className="size-4" />
            </>
          )}
        </Button>
      </div>
    </div>
  );
}