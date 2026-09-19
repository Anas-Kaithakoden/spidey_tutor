"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { getExamResult } from "@/lib/api";
import {
  AlertTriangle,
  Award,
  BookOpenCheck,
  CheckCircle2,
  ListChecks,
  Lightbulb,
  Loader2,
  RotateCcw,
  Target,
  XCircle,
} from "lucide-react";

const STATUS_META = {
  correct: { label: "Correct", icon: <CheckCircle2 className="size-4 text-green-500" /> },
  partial: { label: "Partial", icon: <Target className="size-4 text-amber-500" /> },
  incorrect: { label: "Incorrect", icon: <XCircle className="size-4 text-red-500" /> },
  unanswered: { label: "Unanswered", icon: <AlertTriangle className="size-4 text-muted-foreground" /> },
} as const;

const TYPE_LABELS: Record<string, string> = {
  mcq: "Multiple Choice",
  short_answer: "Short Answer",
  fill_blank: "Fill in the Blank",
  paragraph: "Paragraph",
  essay: "Essay",
};

export default function ExamResults() {
  const router = useRouter();
  const { examResult, setExamResult } = useStudy();
  const [restoring, setRestoring] = useState(() => {
    if (typeof window === "undefined") return false;
    const params = new URLSearchParams(window.location.search);
    const queryId = Number(params.get("exam_id"));
    const lastId = Number(sessionStorage.getItem("spidey-exam-last"));
    const examId = Number.isFinite(queryId) && queryId > 0 ? queryId : lastId;
    return Number.isFinite(examId) && examId > 0;
  });

  useEffect(() => {
    if (examResult) return;
    let cancelled = false;
    const params = new URLSearchParams(window.location.search);
    const queryId = Number(params.get("exam_id"));
    const lastId = Number(sessionStorage.getItem("spidey-exam-last"));
    const examId = Number.isFinite(queryId) && queryId > 0 ? queryId : lastId;
    if (!Number.isFinite(examId) || examId <= 0) return;
    getExamResult(examId)
      .then((r) => {
        if (!cancelled) setExamResult(r);
      })
      .catch((err) => {
        if (!cancelled) {
          toast.error(
            err instanceof Error ? err.message : "Failed to load exam result."
          );
        }
      })
      .finally(() => {
        if (!cancelled) setRestoring(false);
      });
    return () => {
      cancelled = true;
    };
  }, [examResult, setExamResult]);

  if (!examResult && restoring) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Loading result...</p>
      </div>
    );
  }

  if (!examResult) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <p className="mb-4 text-muted-foreground">No exam results found.</p>
        <Button onClick={() => router.push("/exam/setup")}>Take an Exam</Button>
      </div>
    );
  }

  const r = examResult;
  const isAiGraded = r.grading_method === "hybrid";
  const isQuick = r.generated_by === "quick";

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      {/* Score */}
      <div className="mb-10 text-center">
        <h1 className="mb-2 text-2xl font-bold">Exam Complete!</h1>
        <div className="mb-4 flex flex-wrap items-center justify-center gap-2">
          {isQuick && (
            <Badge variant="secondary">Quick Mode — no AI call</Badge>
          )}
          {isAiGraded && (
            <Badge variant="outline">AI-graded subjective answers</Badge>
          )}
          {r.grading_method === "fallback" && (
            <Badge variant="outline">
              <AlertTriangle className="mr-1 size-3" />
              Keyword-graded (AI grading unavailable)
            </Badge>
          )}
        </div>
        <div className="mb-4 inline-flex size-32 flex-col items-center justify-center rounded-full border-4 border-primary">
          <span className="text-4xl font-bold">{r.percentage}%</span>
          <span className="text-xs text-muted-foreground">
            {r.total_score} / {r.max_score} pts
          </span>
        </div>
        <p className="mx-auto max-w-md text-sm text-muted-foreground">{r.summary}</p>
      </div>

      {/* Insights */}
      <div className="mb-8 grid gap-3 sm:grid-cols-2">
        {r.strengths.length > 0 && (
          <Card>
            <CardContent className="pt-6">
              <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold">
                <Award className="size-4 text-green-500" />
                Strengths
              </h3>
              <ul className="space-y-1 text-sm text-muted-foreground">
                {r.strengths.map((s, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="text-green-500">•</span>
                    {s}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
        {r.weak_areas.length > 0 && (
          <Card>
            <CardContent className="pt-6">
              <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold">
                <Target className="size-4 text-red-500" />
                Weak Areas
              </h3>
              <ul className="space-y-1 text-sm text-muted-foreground">
                {r.weak_areas.map((w, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="text-red-500">•</span>
                    {w}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
        {r.recommendations.length > 0 && (
          <Card>
            <CardContent className="pt-6">
              <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold">
                <BookOpenCheck className="size-4 text-primary" />
                Recommendations
              </h3>
              <ul className="space-y-1 text-sm text-muted-foreground">
                {r.recommendations.map((rec, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="text-primary">•</span>
                    {rec}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        )}
      </div>

      {r.generated_by === "mock" && (
        <p className="mb-8 text-center text-xs text-muted-foreground">
          These were sample questions — AI generation via the selected provider
          failed, so answers were graded against a keyword fallback.
        </p>
      )}

      {/* Review */}
      <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold">
        <ListChecks className="size-5 text-primary" />
        Review Answers
      </h2>
      <div className="mb-8 space-y-4">
        {r.reviews.map((rv, idx) => {
          const meta = STATUS_META[rv.status] ?? STATUS_META.unanswered;
          const pointsBadge =
            rv.status === "unanswered"
              ? "—"
              : `${rv.score} / ${rv.max_score}`;
          return (
            <Card key={rv.question_id}>
              <CardContent className="pt-6">
                <div className="mb-3 flex flex-wrap items-start justify-between gap-2">
                  <p className="text-sm font-medium">
                    {idx + 1}. {rv.question}
                    <span className="ml-2 text-xs font-normal capitalize text-muted-foreground">
                      {TYPE_LABELS[rv.question_type]} · {rv.max_score} pts
                    </span>
                  </p>
                  <div className="flex items-center gap-3">
                    <Badge
                      variant={
                        rv.status === "correct"
                          ? "secondary"
                          : rv.status === "unanswered"
                            ? "outline"
                            : "destructive"
                      }
                      className="shrink-0"
                    >
                      <span className="mr-1">{meta.icon}</span>
                      {meta.label}
                    </Badge>
                    <span className="text-xs font-medium tabular-nums">
                      {pointsBadge}
                    </span>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <div>
                    <span className="text-xs font-medium text-muted-foreground">
                      YOUR ANSWER:
                    </span>{" "}
                    <span className={rv.status === "unanswered" ? "italic text-muted-foreground" : ""}>
                      {rv.user_answer && rv.user_answer.trim().length > 0
                        ? rv.user_answer
                        : "—"}
                    </span>
                  </div>
                  <div>
                    <span className="text-xs font-medium text-muted-foreground">
                      EXPECTED:
                    </span>{" "}
                    {rv.expected_answer}
                  </div>
                  {rv.feedback && (
                    <p className="mt-1 rounded-md bg-muted/50 px-3 py-2 text-xs">
                      {rv.feedback}
                    </p>
                  )}
                  {rv.improved_answer && (
                    <p className="flex items-start gap-1.5 rounded-md bg-primary/5 px-3 py-2 text-xs">
                      <Lightbulb className="mt-0.5 size-3.5 shrink-0 text-primary" />
                      <span>{rv.improved_answer}</span>
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-3">
        <Button
          variant="outline"
          onClick={() => router.push("/exam/setup")}
          className="gap-2"
        >
          <RotateCcw className="size-4" />
          Retake Exam
        </Button>
        <Button onClick={() => router.push("/progress")} className="gap-2">
          View Progress
        </Button>
      </div>
    </div>
  );
}