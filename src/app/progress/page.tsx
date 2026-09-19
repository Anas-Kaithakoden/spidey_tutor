"use client";

import { useEffect, useState, type ReactNode } from "react";
import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { getAnalytics, type Analytics } from "@/lib/api";
import {
  Activity,
  BarChart3,
  BookOpen,
  CalendarDays,
  CheckCircle2,
  CreditCard,
  FileText,
  GraduationCap,
  Layers,
  ListChecks,
  Loader2,
  NotebookPen,
  RotateCcw,
  Target,
  TrendingUp,
  Trophy,
  XCircle,
  Zap,
} from "lucide-react";

const TREND_POINTS = 14;

export default function ProgressDashboard() {
  const [data, setData] = useState<Analytics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    getAnalytics()
      .then((d) => {
        if (!cancelled) setData(d);
      })
      .catch((err) => {
        if (!cancelled) {
          setError(
            err instanceof Error ? err.message : "Failed to load progress."
          );
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Loading progress...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <p className="mb-4 text-muted-foreground">{error}</p>
        <Button onClick={() => window.location.reload()}>Retry</Button>
      </div>
    );
  }

  if (!data) return null;

  if (!data.has_activity) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12">
        <h1 className="mb-2 text-2xl font-bold">Progress Dashboard</h1>
        <p className="mb-8 text-muted-foreground">
          Track your study activity and performance over time.
        </p>
        <div className="flex flex-col items-center gap-4 rounded-xl border border-dashed p-12 text-center">
          <BarChart3 className="size-10 text-muted-foreground" />
          <div>
            <h2 className="font-semibold">No study activity yet</h2>
            <p className="mt-1 max-w-sm text-sm text-muted-foreground">
              Take a quiz or review some flashcards and your progress, scores,
              and stats will show up here.
            </p>
          </div>
          <Button render={<Link href="/add" />} className="gap-2" nativeButton={false}>
            <GraduationCap className="size-4" />
            Start Studying
          </Button>
        </div>
      </div>
    );
  }

  const overallAccuracy =
    data.questions_answered > 0
      ? Math.round((data.correct_answers / data.questions_answered) * 100)
      : 0;

  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Progress Dashboard</h1>
      <p className="mb-8 text-muted-foreground">
        Track your study activity and performance over time.
      </p>

      {/* Overall progress */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="size-4 text-primary" />
            Overall Progress
          </CardTitle>
          <CardDescription>
            Questions answered correctly across all completed quizzes.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
            <span className="text-4xl font-bold tabular-nums">
              {overallAccuracy}%
            </span>
            <span className="text-sm text-muted-foreground">
              {data.correct_answers} correct &middot; {data.incorrect_answers}{" "}
              incorrect of {data.questions_answered} questions
            </span>
          </div>
          <Progress value={overallAccuracy} className="flex-col" />
        </CardContent>
      </Card>

      {/* Headline stats */}
      <div className="mb-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
        <StatCard
          icon={<Trophy className="size-5" />}
          label="Quizzes Completed"
          value={String(data.quizzes_completed)}
        />
        <StatCard
          icon={<Target className="size-5" />}
          label="Average Score"
          value={`${data.average_score}%`}
          sub={
            data.best_score !== null
              ? `Best ${data.best_score}%`
              : undefined
          }
        />
        <StatCard
          icon={<ListChecks className="size-5" />}
          label="Questions Answered"
          value={String(data.questions_answered)}
          sub={`${data.correct_answers} correct · ${data.incorrect_answers} incorrect`}
        />
        <StatCard
          icon={<CreditCard className="size-5" />}
          label="Flashcards Reviewed"
          value={String(data.flashcards_reviewed)}
          sub={`${data.flashcards} cards saved`}
        />
        <StatCard
          icon={<Activity className="size-5" />}
          label="Study Sessions"
          value={String(data.study_sessions)}
          sub="quizzes + flashcard reviews"
        />
        <StatCard
          icon={<CalendarDays className="size-5" />}
          label="Days Active"
          value={String(data.days_studied)}
          sub="days with study activity"
        />
        <StatCard
          icon={<BookOpen className="size-5" />}
          label="Materials Studied"
          value={String(data.materials)}
          sub="uploaded material"
        />
        <StatCard
          icon={<Zap className="size-5" />}
          label="Best Score"
          value={data.best_score !== null ? `${data.best_score}%` : "--"}
          sub="highest quiz score"
        />
      </div>

      {data.topics.length > 0 && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Layers className="size-4 text-primary" />
              Performance by Topic
            </CardTitle>
            <CardDescription>
              Breakdown by study material. Lower-scoring topics are highlighted
              so you can practice them again.
            </CardDescription>
          </CardHeader>
          <CardContent className="divide-y">
            {data.topics.map((topic) => (
              <TopicRow key={topic.material_id} topic={topic} />
            ))}
          </CardContent>
        </Card>
      )}

      {data.score_trend.length > 1 && (
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="size-4 text-primary" />
              Score Trend
            </CardTitle>
            <CardDescription>
              Your most recent quiz scores. Hover a bar for details.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ScoreTrendChart
              points={data.score_trend.slice(-TREND_POINTS)}
            />
          </CardContent>
        </Card>
      )}

      {data.recent_activity.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="size-4 text-primary" />
              Recent Activity
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="divide-y">
              {data.recent_activity.map((item, idx) => (
                <ActivityRow key={idx} item={item} />
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  sub,
}: {
  icon: ReactNode;
  label: string;
  value: string;
  sub?: string;
}) {
  return (
    <Card size="sm">
      <CardContent className="flex flex-col gap-1">
        <div className="flex items-center gap-2 text-muted-foreground">
          {icon}
          <span className="text-sm font-medium">{label}</span>
        </div>
        <span className="text-2xl font-bold tabular-nums">{value}</span>
        {sub && <span className="text-xs text-muted-foreground">{sub}</span>}
      </CardContent>
    </Card>
  );
}

function TopicRow({ topic }: { topic: Analytics["topics"][number] }) {
  const weak = topic.needs_practice;
  return (
    <div className="py-4 first:pt-0 last:pb-0">
      <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
        <div className="flex min-w-0 flex-wrap items-center gap-2">
          <p className="truncate font-medium">{topic.title}</p>
          <Badge variant="secondary" className="shrink-0">
            {topic.quizzes_taken} quiz{topic.quizzes_taken === 1 ? "" : "zes"}
          </Badge>
          {weak && (
            <Badge variant="destructive" className="shrink-0">
              Needs practice
            </Badge>
          )}
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xl font-bold tabular-nums">
            {topic.average_score}%
          </span>
          <Button
            render={
              <Link href={`/quiz/setup?material_id=${topic.material_id}`} />
            }
            variant="outline"
            size="sm"
            className="gap-1"
            nativeButton={false}
          >
            <RotateCcw className="size-3.5" />
            Practice
          </Button>
        </div>
      </div>
      <div className="mb-2 flex h-2 w-full items-center overflow-hidden rounded-full bg-muted">
        <div
          className={`h-full rounded-full transition-all ${
            weak ? "bg-red-500" : "bg-primary"
          }`}
          style={{ width: `${topic.average_score}%` }}
        />
      </div>
      <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <CheckCircle2 className="size-3.5 text-green-500" />
          {topic.correct} correct
        </span>
        <span className="flex items-center gap-1">
          <XCircle className="size-3.5 text-red-500" />
          {topic.questions_answered - topic.correct} incorrect
        </span>
        <span>{topic.questions_answered} answered</span>
      </div>
    </div>
  );
}

function ScoreTrendChart({
  points,
}: {
  points: Analytics["score_trend"];
}) {
  return (
    <div>
      <div className="flex h-36 items-end gap-1.5">
        {points.map((pt, idx) => (
          <div key={idx} className="flex h-full flex-1 items-end">
            <div
              role="img"
              aria-label={`${pt.label}: ${pt.score}% on ${pt.material_title}`}
              title={`${pt.label} · ${pt.material_title} · ${pt.score}%`}
              className={`w-full rounded-t-md ${
                pt.score >= 80
                  ? "bg-primary"
                  : pt.score >= 60
                    ? "bg-primary/60"
                    : "bg-red-500/70"
              }`}
              style={{ height: `${pt.score}%` }}
            />
          </div>
        ))}
      </div>
      <div className="mt-2 flex gap-1.5">
        {points.map((pt, idx) => (
          <div key={idx} className="flex-1 text-center">
            <div className="truncate text-[10px] leading-tight text-muted-foreground">
              {pt.label}
            </div>
            <div className="text-[10px] font-medium leading-tight tabular-nums">
              {pt.score}%
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

const ACTIVITY_ICONS: Record<
  Analytics["recent_activity"][number]["kind"],
  ReactNode
> = {
  quiz: <ListChecks className="size-4" />,
  flashcards: <CreditCard className="size-4" />,
  material: <FileText className="size-4" />,
  notes: <NotebookPen className="size-4" />,
};

function ActivityRow({ item }: { item: Analytics["recent_activity"][number] }) {
  return (
    <li className="flex items-center gap-3 py-2.5 first:pt-0 last:pb-0">
      <span className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-muted text-muted-foreground">
        {ACTIVITY_ICONS[item.kind]}
      </span>
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium">
          {item.title}
          <span className="ml-1 hidden capitalize text-xs font-normal text-muted-foreground sm:inline">
            {item.kind}
          </span>
        </p>
        <p className="truncate text-xs text-muted-foreground">{item.detail}</p>
      </div>
      <span className="shrink-0 text-xs text-muted-foreground">
        {formatDate(item.created_at)}
      </span>
    </li>
  );
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  if (diffDays <= 0) {
    const hours = Math.floor(diffMs / (1000 * 60 * 60));
    if (hours >= 1) return `${hours}h ago`;
    return "today";
  }
  if (diffDays === 1) return "yesterday";
  if (diffDays < 30) return `${diffDays}d ago`;
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}