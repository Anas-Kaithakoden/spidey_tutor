"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, FileText, Loader2, NotebookPen, Type } from "lucide-react";

export default function Preview() {
  const router = useRouter();
  const { material } = useStudy();

  useEffect(() => {
    if (!material) router.replace("/add");
  }, [material, router]);

  if (!material) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Redirecting...</p>
      </div>
    );
  }

  const type = material.source_type;

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Material Preview</h1>
      <p className="mb-8 text-muted-foreground">
        Review your material before generating study content.
      </p>

      <Card>
        <CardContent className="pt-6">
          <div className="mb-4 flex items-center gap-3">
            <div className="flex size-10 items-center justify-center rounded-lg bg-muted">
              {type === "pdf" ? (
                <FileText className="size-5 text-muted-foreground" />
              ) : (
                <Type className="size-5 text-muted-foreground" />
              )}
            </div>
            <div>
              <h2 className="font-semibold">{material.title}</h2>
              <div className="flex flex-wrap gap-2">
                <Badge variant="secondary" className="text-xs">
                  {type.toUpperCase()}
                </Badge>
                <Badge variant="secondary" className="text-xs">
                  {material.word_count.toLocaleString()} words
                </Badge>
                <Badge variant="secondary" className="text-xs">
                  {material.char_count.toLocaleString()} chars
                </Badge>
              </div>
            </div>
          </div>

          <div className="mt-4 max-h-80 overflow-y-auto rounded-lg border bg-muted/30 p-4">
            <p className="whitespace-pre-wrap text-sm leading-relaxed text-muted-foreground">
              {material.content}
            </p>
          </div>
        </CardContent>
      </Card>

      <div className="mt-6 flex justify-between gap-3">
        <Button
          variant="outline"
          onClick={() => router.push("/notes")}
          className="gap-2"
        >
          <NotebookPen className="size-4" />
          Study Notes
        </Button>
        <Button onClick={() => router.push("/quiz/setup")} className="gap-2">
          Continue
          <ArrowRight className="size-4" />
        </Button>
      </div>
    </div>
  );
}