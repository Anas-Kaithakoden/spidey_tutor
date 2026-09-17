"use client";

import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { CheckCircle, XCircle, RotateCcw, CreditCard, Loader2 } from "lucide-react";
import { generateFlashcards } from "@/lib/api";
import { useState } from "react";

export default function QuizResults() {
  const router = useRouter();
  const { material, quizResult, model } = useStudy();
  const [creatingCards, setCreatingCards] = useState(false);

  if (!quizResult) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <p className="mb-4 text-muted-foreground">No quiz results found.</p>
        <Button onClick={() => router.push("/add")}>Take a Quiz</Button>
      </div>
    );
  }

  const generatedBy = quizResult.generated_by;
  const reviews = quizResult.reviews;
  const correct = quizResult.score;
  const total = quizResult.total;
  const percentage = quizResult.percentage;

  async function handleCreateFlashcards() {
    if (!material) {
      toast.error("Add study material first.");
      router.push("/add");
      return;
    }
    setCreatingCards(true);
    try {
      await generateFlashcards(material.id, model.provider, model.name);
      if (generatedBy === "mock") {
        toast.info(
          "Using sample flashcards (add your Gemini API key for AI-generated ones)."
        );
      }
      router.push(`/flashcards?material_id=${material.id}&generated=1`);
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to create flashcards.");
    } finally {
      setCreatingCards(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      {/* Score */}
      <div className="mb-10 text-center">
        <h1 className="mb-2 text-2xl font-bold">Quiz Complete!</h1>
        <div className="mb-4 inline-flex size-28 items-center justify-center rounded-full border-4 border-primary">
          <span className="text-3xl font-bold">{percentage}%</span>
        </div>
        <div className="flex items-center justify-center gap-6">
          <div className="flex items-center gap-1.5 text-sm">
            <CheckCircle className="size-4 text-green-500" />
            <span className="font-medium">{correct}</span>
            <span className="text-muted-foreground">correct</span>
          </div>
          <div className="flex items-center gap-1.5 text-sm">
            <XCircle className="size-4 text-red-500" />
            <span className="font-medium">{total - correct}</span>
            <span className="text-muted-foreground">incorrect</span>
          </div>
        </div>
        <p className="mt-2 text-muted-foreground">
          You scored {correct} out of {total}
        </p>
      </div>

      {/* Review */}
      <h2 className="mb-4 text-lg font-semibold">Review Answers</h2>
      <div className="mb-8 space-y-4">
        {reviews.map((rv, idx) => {
          const userAnswer = rv.user_answer;
          const isCorrect = rv.is_correct;

          return (
            <Card key={idx}>
              <CardContent className="pt-6">
                <div className="mb-3 flex items-start justify-between gap-3">
                  <p className="text-sm font-medium">
                    {idx + 1}. {rv.question}
                  </p>
                  {isCorrect ? (
                    <CheckCircle className="size-5 shrink-0 text-green-500" />
                  ) : (
                    <XCircle className="size-5 shrink-0 text-red-500" />
                  )}
                </div>

                <div className="mb-3 space-y-1.5">
                  {rv.options.map((opt, optIdx) => (
                    <div
                      key={optIdx}
                      className={`flex items-center gap-2 rounded-md px-3 py-1.5 text-sm ${
                        optIdx === rv.correct_answer
                          ? "bg-green-500/10 text-green-600 dark:text-green-400"
                          : optIdx === userAnswer
                            ? "bg-red-500/10 text-red-600 dark:text-red-400"
                            : "text-muted-foreground"
                      }`}
                    >
                      <span className="font-medium">
                        {String.fromCharCode(65 + optIdx)}.
                      </span>
                      {opt}
                    </div>
                  ))}
                </div>

                <p className="text-xs text-muted-foreground">{rv.explanation}</p>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3">
        <Button
          variant="outline"
          onClick={() => router.push("/quiz/setup")}
          className="gap-2"
        >
          <RotateCcw className="size-4" />
          Retry Quiz
        </Button>
        <Button
          onClick={handleCreateFlashcards}
          disabled={creatingCards}
          className="gap-2"
        >
          {creatingCards ? (
            <>
              <Loader2 className="size-4 animate-spin" />
              Creating...
            </>
          ) : (
            <>
              <CreditCard className="size-4" />
              Create Flashcards
            </>
          )}
        </Button>
      </div>
    </div>
  );
}