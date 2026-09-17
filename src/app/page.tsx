"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Bug, BookOpen, Zap, Brain } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center px-4 py-24 text-center">
      <div className="mb-6 flex size-16 items-center justify-center rounded-2xl bg-primary/10">
        <Bug className="size-8 text-primary" />
      </div>

      <h1 className="mb-3 text-4xl font-bold tracking-tight">Spidey Tutor</h1>

      <p className="mb-10 max-w-md text-muted-foreground">
        Upload your lecture material and let AI generate quizzes and flashcards
        to help you study smarter.
      </p>

      <Button render={<Link href="/add" />} size="lg" className="mb-16 px-8">
        Start Studying
      </Button>

      <div className="grid max-w-2xl gap-6 sm:grid-cols-3">
        <FeatureCard
          icon={<BookOpen className="size-5" />}
          title="Upload Material"
          description="Drop in a PDF or paste text from your notes"
        />
        <FeatureCard
          icon={<Zap className="size-5" />}
          title="Take a Quiz"
          description="Test your knowledge with AI-generated questions"
        />
        <FeatureCard
          icon={<Brain className="size-5" />}
          title="Study Flashcards"
          description="Review key concepts one card at a time"
        />
      </div>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: ReactNode;
  title: string;
  description: string;
}) {
  return (
    <div className="flex flex-col items-center gap-2 rounded-xl border p-6 text-center">
      <div className="mb-1 flex size-10 items-center justify-center rounded-lg bg-muted">
        {icon}
      </div>
      <h3 className="font-medium">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}
