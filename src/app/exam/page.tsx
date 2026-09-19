"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import {
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  Clock,
  Loader2,
} from "lucide-react";
import {
  getExam,
  submitExam,
  type ExamQuestionType,
} from "@/lib/api";

const storageKey = (examId: number) => `spidey-exam-${examId}`;

interface StoredAnswers {
  examId: number;
  answers: { option: number | null; text: string }[];
  startedAt: number;
}

interface AnswerState {
  option: number | null;
  text: string;
}

const TYPE_LABELS: Record<ExamQuestionType, string> = {
  mcq: "Multiple Choice",
  short_answer: "Short Answer",
  fill_blank: "Fill in the Blank",
  paragraph: "Paragraph",
  essay: "Essay",
};

function readStored(examId: number): StoredAnswers | null {
  try {
    const raw = sessionStorage.getItem(storageKey(examId));
    if (!raw) return null;
    const parsed = JSON.parse(raw) as StoredAnswers;
    if (!parsed || parsed.examId !== examId) return null;
    if (!Array.isArray(parsed.answers)) return null;
    return parsed;
  } catch {
    return null;
  }
}

function mapAnswers(
  count: number,
  stored?: StoredAnswers["answers"]
): AnswerState[] {
  const out: AnswerState[] = Array.from({ length: count }, () => ({
    option: null,
    text: "",
  }));
  if (!stored) return out;
  stored.forEach((a, i) => {
    if (i >= count) return;
    out[i] = {
      option: typeof a?.option === "number" ? a.option : null,
      text: typeof a?.text === "string" ? a.text : "",
    };
  });
  return out;
}

export default function ExamScreen() {
  const router = useRouter();
  const { activeExam, setActiveExam, setExamResult, model } = useStudy();
  const totalQuestions = activeExam?.questions.length ?? 0;
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<AnswerState[]>(() =>
    activeExam
      ? mapAnswers(activeExam.questions.length)
      : []
  );
  const [timeLeft, setTimeLeft] = useState(() =>
    activeExam ? activeExam.duration_minutes * 60 : 0
  );
  const [submitting, setSubmitting] = useState(false);
  const submittingRef = useRef(false);
  const startedAtRef = useRef<number>(0);

  useEffect(() => {
    let cancelled = false;
    // Fresh navigation (exam was just created): start a new attempt.
    if (activeExam) {
      startedAtRef.current = Date.now();
      return;
    }
    // Hard refresh: rehydrate the exam, answers and remaining time.
    const params = new URLSearchParams(window.location.search);
    const examId = Number(params.get("exam_id"));
    if (!Number.isFinite(examId) || examId <= 0) {
      router.replace("/exam/setup");
      return;
    }
    const stored = readStored(examId);
    const timer = setTimeout(() => {
      if (cancelled) return;
      getExam(examId)
        .then((exam) => {
          if (cancelled) return;
          const startedAt = stored?.startedAt ?? Date.now();
          startedAtRef.current = startedAt;
          setActiveExam(exam);
          setAnswers(mapAnswers(exam.questions.length, stored?.answers));
          const elapsed = Math.round((Date.now() - startedAt) / 1000);
          setTimeLeft(Math.max(0, exam.duration_minutes * 60 - elapsed));
        })
        .catch(() => {
          if (!cancelled) router.replace("/exam/setup");
        });
    }, 0);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeExam, router]);

  const persist = useCallback((next: AnswerState[]) => {
    if (!activeExam) return;
    try {
      sessionStorage.setItem(
        storageKey(activeExam.id),
        JSON.stringify({
          examId: activeExam.id,
          answers: next,
          startedAt: startedAtRef.current,
        } satisfies StoredAnswers)
      );
    } catch {
      // ignore
    }
  }, [activeExam]);

  const handleSubmit = useCallback(
    async (finalAnswers: AnswerState[], forceAuto: boolean) => {
      if (!activeExam || submittingRef.current) return;
      const answered = finalAnswers.filter(
        (a) => a.option !== null || a.text.trim().length > 0
      ).length;
      if (!forceAuto && answered < totalQuestions) {
        const confirmed = window.confirm(
          `${totalQuestions - answered} question(s) are still unanswered. Submit anyway?`
        );
        if (!confirmed) return;
      }

      submittingRef.current = true;
      setSubmitting(true);
      try {
        const elapsed = Math.min(
          Math.max(0, Math.round((Date.now() - startedAtRef.current) / 1000)),
          activeExam.duration_minutes * 60
        );
        const result = await submitExam(
          activeExam.id,
          activeExam.questions.map((q, idx) => {
            const a = finalAnswers[idx];
            if (q.question_type === "mcq")
              return { question_id: q.id, option: a.option, text: null };
            return { question_id: q.id, text: a.text.trim() || null, option: null };
          }),
          elapsed,
          model.provider,
          model.name
        );
        setExamResult(result);
        sessionStorage.setItem("spidey-exam-last", String(activeExam.id));
        sessionStorage.removeItem(storageKey(activeExam.id));
        if (forceAuto) toast.info("Time's up — exam submitted automatically.");
        router.push("/exam/results");
      } catch (err) {
        toast.error(err instanceof Error ? err.message : "Failed to submit exam.");
        setSubmitting(false);
      } finally {
        submittingRef.current = false;
      }
    },
    [activeExam, totalQuestions, setExamResult, model, router]
  );

  // Countdown timer + auto-submit at zero
  useEffect(() => {
    if (!activeExam || submitting) return;
    if (timeLeft <= 0) {
      const timer = setTimeout(() => {
        void handleSubmit(answers, true);
      }, 0);
      return () => clearTimeout(timer);
    }
    const timer = setTimeout(() => setTimeLeft((prev) => Math.max(0, prev - 1)), 1000);
    return () => clearTimeout(timer);
  }, [timeLeft, activeExam, submitting, answers, handleSubmit]);

  if (!activeExam) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Loading exam...</p>
      </div>
    );
  }

  const exam = activeExam;
  const q = exam.questions[current];
  const a = answers[current];
  const totalSec = exam.duration_minutes * 60;
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;
  const progress = ((current + 1) / totalQuestions) * 100;
  const answered = answers.filter(
    (x) => x.option !== null || x.text.trim().length > 0
  ).length;
  const timeFraction = totalSec > 0 ? (timeLeft / totalSec) * 100 : 0;

  function setOption(idx: number) {
    if (submitting) return;
    const next = answers.map((x, i) => (i === current ? { ...x, option: idx } : x));
    setAnswers(next);
    persist(next);
  }

  function setText(value: string) {
    if (submitting) return;
    const next = answers.map((x, i) => (i === current ? { ...x, text: value } : x));
    setAnswers(next);
    persist(next);
  }

  function goNext() {
    if (current < totalQuestions - 1) setCurrent(current + 1);
  }

  function goPrev() {
    if (current > 0) setCurrent(current - 1);
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      {/* Header */}
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-3">
          <Badge variant="secondary">
            {current + 1} / {totalQuestions}
          </Badge>
          <Badge variant="outline" className="capitalize">
            {exam.difficulty}
          </Badge>
          <Badge variant="outline">
            {answered} / {totalQuestions} answered
          </Badge>
        </div>
        <div
          className={`flex items-center gap-1.5 font-mono text-sm font-medium ${
            timeLeft < 60 ? "text-destructive" : "text-muted-foreground"
          }`}
          title="Time remaining"
        >
          <Clock className="size-4" />
          {String(minutes).padStart(2, "0")}:{String(seconds).padStart(2, "0")}
        </div>
      </div>

      {/* Progress */}
      <div className="mb-2 flex items-center justify-between text-xs text-muted-foreground">
        <span>Progress</span>
        <span>Time remaining</span>
      </div>
      <div className="mb-8 flex gap-3">
        <Progress value={progress} className="flex-1" />
        <Progress value={timeFraction} className="w-24 [&>div]:bg-primary/40" />
      </div>

      {/* Question */}
      <Card className="mb-8">
        <CardContent className="pt-6">
          <p className="mb-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">
            Question {current + 1} · {TYPE_LABELS[q.question_type]} ·{" "}
            {q.max_score} pts
          </p>
          <h2 className="mb-6 text-lg font-semibold">{q.question}</h2>

          {q.question_type === "mcq" && (
            <div className="space-y-3">
              {(q.options ?? []).map((opt, idx) => (
                <button
                  key={idx}
                  onClick={() => setOption(idx)}
                  className={`flex w-full items-center gap-3 rounded-lg border-2 px-4 py-3 text-left text-sm font-medium transition-colors cursor-pointer ${
                    a.option === idx
                      ? "border-primary bg-primary/5 text-foreground"
                      : "border-transparent bg-muted/50 hover:bg-muted"
                  }`}
                >
                  <span
                    className={`flex size-7 shrink-0 items-center justify-center rounded-full border text-xs font-medium ${
                      a.option === idx
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
          )}

          {(q.question_type === "short_answer" ||
            q.question_type === "fill_blank") && (
            <Input
              value={a.text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Type your answer..."
              disabled={submitting}
            />
          )}

          {(q.question_type === "paragraph" ||
            q.question_type === "essay") && (
            <Textarea
              value={a.text}
              onChange={(e) => setText(e.target.value)}
              placeholder={
                q.question_type === "essay"
                  ? "Write your essay response..."
                  : "Write your paragraph response..."
              }
              disabled={submitting}
              className="min-h-40"
            />
          )}
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={goPrev}
          disabled={current === 0 || submitting}
          className="gap-1"
        >
          <ChevronLeft className="size-4" />
          Previous
        </Button>

        {current === totalQuestions - 1 ? (
          <Button
            onClick={() => handleSubmit(answers, false)}
            disabled={submitting}
            className="gap-1"
          >
            {submitting ? (
              <>
                <Loader2 className="size-4 animate-spin" />
                Submitting...
              </>
            ) : (
              <>
                <ClipboardCheck className="size-4" />
                Submit Exam
              </>
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
        {exam.questions.map((_, idx) => {
          const isAnswered =
            answers[idx].option !== null || answers[idx].text.trim().length > 0;
          return (
            <button
              key={idx}
              onClick={() => setCurrent(idx)}
              className={`size-3 rounded-full transition-colors cursor-pointer ${
                idx === current
                  ? "bg-primary"
                  : isAnswered
                    ? "bg-primary/40"
                    : "bg-muted"
              }`}
            />
          );
        })}
      </div>
    </div>
  );
}