"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { ChevronLeft, ChevronRight, Clock, Loader2 } from "lucide-react";
import { submitQuiz } from "@/lib/api";

export default function QuizScreen() {
  const router = useRouter();
  const { activeQuiz, setQuizResult } = useStudy();
  const totalQuestions = activeQuiz?.questions.length ?? 0;

  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<(number | null)[]>(() =>
    activeQuiz ? new Array(activeQuiz.questions.length).fill(null) : []
  );
  const [timeLeft, setTimeLeft] = useState(() =>
    activeQuiz?.timer_enabled ? activeQuiz.timer_minutes * 60 : 0
  );
  const [submitted, setSubmitted] = useState(false);
  const submittingRef = useRef(false);

  const handleSubmit = useCallback(
    async (finalAnswers: (number | null)[], elapsedSeconds: number) => {
      if (!activeQuiz || submittingRef.current) return;
      submittingRef.current = true;
      setSubmitted(true);
      try {
        const result = await submitQuiz(
          activeQuiz.id,
          finalAnswers,
          elapsedSeconds
        );
        setQuizResult(result);
        if (result.generated_by === "mock") {
          toast.info(
            "Using sample questions (add your Gemini API key for AI-generated ones)."
          );
        }
        router.push("/quiz/results");
      } catch (err) {
        toast.error(err instanceof Error ? err.message : "Failed to submit quiz.");
        setSubmitted(false);
      } finally {
        submittingRef.current = false;
      }
    },
    [activeQuiz, setQuizResult, router]
  );

  useEffect(() => {
    if (!activeQuiz) {
      router.replace("/quiz/setup");
    }
  }, [activeQuiz, router]);

  // Countdown timer
  useEffect(() => {
    if (!activeQuiz?.timer_enabled || submitted) return;
    if (timeLeft <= 0) {
      const timer = setTimeout(() => {
        const elapsed = activeQuiz.timer_minutes * 60;
        void handleSubmit(answers, elapsed);
      }, 0);
      return () => clearTimeout(timer);
    }
    const timer = setTimeout(
      () => setTimeLeft((prev) => Math.max(0, prev - 1)),
      1000
    );
    return () => clearTimeout(timer);
  }, [timeLeft, activeQuiz, submitted, answers, handleSubmit]);

  if (!activeQuiz) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Redirecting...</p>
      </div>
    );
  }

  const quiz = activeQuiz;
  const q = quiz.questions[current];
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const selected = answers[current];
  const progress = ((current + 1) / totalQuestions) * 100;
  const elapsed =
    quiz.timer_enabled
      ? quiz.timer_minutes * 60 - timeLeft
      : 0;

  function selectOption(idx: number) {
    if (submitted) return;
    setAnswers((prev) => {
      const next = [...prev];
      next[current] = idx;
      return next;
    });
  }

  function goNext() {
    if (current < totalQuestions - 1) setCurrent(current + 1);
  }

  function goPrev() {
    if (current > 0) setCurrent(current - 1);
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Badge variant="secondary">
            {current + 1} / {totalQuestions}
          </Badge>
          <Badge variant="outline" className="capitalize">
            {quiz.difficulty}
          </Badge>
        </div>
        {quiz.timer_enabled && (
          <div
            className={`flex items-center gap-1.5 font-mono text-sm font-medium ${
              timeLeft < 60 ? "text-destructive" : "text-muted-foreground"
            }`}
          >
            <Clock className="size-4" />
            {String(minutes).padStart(2, "0")}:{String(seconds).padStart(2, "0")}
          </div>
        )}
      </div>

      {/* Progress */}
      <Progress value={progress} className="mb-8" />

      {/* Question */}
      <Card className="mb-8">
        <CardContent className="pt-6">
          <p className="mb-1 text-xs font-medium uppercase tracking-wider text-muted-foreground">
            Question {current + 1}
          </p>
          <h2 className="mb-6 text-lg font-semibold">{q.question}</h2>

          <div className="space-y-3">
            {q.options.map((opt, idx) => (
              <button
                key={idx}
                onClick={() => selectOption(idx)}
                className={`flex w-full items-center gap-3 rounded-lg border-2 px-4 py-3 text-left text-sm font-medium transition-colors cursor-pointer ${
                  selected === idx
                    ? "border-primary bg-primary/5 text-foreground"
                    : "border-transparent bg-muted/50 hover:bg-muted"
                }`}
              >
                <span
                  className={`flex size-7 shrink-0 items-center justify-center rounded-full border text-xs font-medium ${
                    selected === idx
                      ? "border-primary bg-primary text-primary-foreground"
                      : "border-border"
                  }`}
                >
                  {String.fromCharCode(65 + idx)}
                </span>
                {opt}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={goPrev}
          disabled={current === 0 || submitted}
          className="gap-1"
        >
          <ChevronLeft className="size-4" />
          Previous
        </Button>

        {current === totalQuestions - 1 ? (
          <Button
            onClick={() => handleSubmit(answers, elapsed)}
            disabled={submitted}
            className="gap-1"
          >
            {submitted ? (
              <>
                <Loader2 className="size-4 animate-spin" />
                Submitting...
              </>
            ) : (
              "Finish Quiz"
            )}
          </Button>
        ) : (
          <Button onClick={goNext} className="gap-1">
            Next
            <ChevronRight className="size-4" />
          </Button>
        )}
      </div>

      {/* Question dots */}
      <div className="mt-8 flex flex-wrap justify-center gap-2">
        {quiz.questions.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrent(idx)}
            className={`size-3 rounded-full transition-colors cursor-pointer ${
              idx === current
                ? "bg-primary"
                : answers[idx] !== null
                  ? "bg-primary/40"
                  : "bg-muted"
            }`}
          />
        ))}
      </div>
    </div>
  );
}