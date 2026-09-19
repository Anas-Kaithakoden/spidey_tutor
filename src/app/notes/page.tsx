"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  BookOpen,
  ListChecks,
  Loader2,
  RefreshCw,
  Sparkles,
} from "lucide-react";
import {
  generateStudyNotes,
  getStudyNotes,
  type StudyNotes,
} from "@/lib/api";
import { ModelSelect } from "@/components/model-select";
import {
  LanguageToggle,
  type StudyLanguage,
} from "@/components/language-toggle";

export default function Notes() {
  const router = useRouter();
  const { material, model } = useStudy();
  const [notes, setNotes] = useState<StudyNotes | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [language, setLanguage] = useState<StudyLanguage>("en");

  useEffect(() => {
    if (!material) {
      router.replace("/add");
      return;
    }
    let cancelled = false;
    getStudyNotes(material.id)
      .then((existing) => {
        if (!cancelled) setNotes(existing);
      })
      .catch((err) => {
        if (!cancelled) {
          toast.error(
            err instanceof Error ? err.message : "Failed to load study notes."
          );
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [material, router]);

  async function handleGenerate() {
    if (!material) return;
    setGenerating(true);
    try {
      const generated = await generateStudyNotes(
        material.id,
        model.provider,
        model.name,
        language
      );
      setNotes(generated);
      if (generated.generated_by === "mock") {
        toast.info(
          generated.warning ??
            `Showing sample notes — AI generation via ${model.provider} failed. Check the backend .env.`
        );
      } else if (generated.generated_by === "quick") {
        toast.info("Quick Mode: notes generated deterministically, no AI call.");
      } else {
        toast.success("Study notes generated!");
      }
    } catch (err) {
      toast.error(
        err instanceof Error ? err.message : "Failed to generate study notes."
      );
    } finally {
      setGenerating(false);
    }
  }

  if (!material) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Redirecting...</p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Study Notes</h1>
      <p className="mb-8 text-muted-foreground">
        Structured notes generated from your material, organized into clear
        topics with the key concepts highlighted.
      </p>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-24">
          <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
          <p className="text-muted-foreground">Loading study notes...</p>
        </div>
      ) : !notes ? (
        <div className="flex flex-col items-center gap-4 rounded-xl border border-dashed p-12 text-center">
          <BookOpen className="size-10 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            No study notes yet. Generate them from your study material — the AI
            structures the content into sections and highlights the important
            concepts and definitions.
          </p>
          <div className="flex w-full max-w-xs items-center gap-2">
            <ModelSelect className="flex-1" />
            <LanguageToggle value={language} onChange={setLanguage} />
          </div>
          <Button
            onClick={handleGenerate}
            disabled={generating}
            className="gap-2"
          >
            {generating ? (
              <>
                <Loader2 className="size-4 animate-spin" />
                Generating notes...
              </>
            ) : (
              <>
                <Sparkles className="size-4" />
                Generate Study Notes
              </>
            )}
          </Button>
        </div>
      ) : (
        <div className="space-y-6">
          {generating && (
            <Card>
              <CardContent className="flex items-center justify-center gap-2 py-6 text-muted-foreground">
                <Loader2 className="size-4 animate-spin" />
                Regenerating notes...
              </CardContent>
            </Card>
          )}

          <Card>
            <CardContent className="pt-2">
              <div className="flex items-center gap-2">
                <h2 className="text-lg font-semibold">{notes.title}</h2>
                {notes.generated_by === "quick" && (
                  <Badge variant="secondary" className="shrink-0">
                    Quick Mode
                  </Badge>
                )}
                {notes.language === "ml" && (
                  <Badge variant="secondary" className="shrink-0">
                    മലയാളം
                  </Badge>
                )}
              </div>
              {notes.summary && (
                <p className="mt-2 leading-relaxed text-muted-foreground">
                  {notes.summary}
                </p>
              )}
            </CardContent>
          </Card>

          {notes.sections.map((section, idx) => (
            <Card key={idx}>
              <CardContent className="pt-2">
                {section.heading && (
                  <h3 className="mb-2 text-base font-semibold">
                    {section.heading}
                  </h3>
                )}
                {section.content && (
                  <p className="whitespace-pre-wrap leading-relaxed text-muted-foreground">
                    {section.content}
                  </p>
                )}
                {section.bullet_points.length > 0 && (
                  <ul className="mt-3 space-y-1.5">
                    {section.bullet_points.map((point, i) => (
                      <li
                        key={i}
                        className="flex gap-2 leading-relaxed text-muted-foreground"
                      >
                        <span className="mt-2 size-1.5 shrink-0 rounded-full bg-primary" />
                        <span>{point}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </CardContent>
            </Card>
          ))}

          {notes.key_concepts.length > 0 && (
            <Card>
              <CardContent className="pt-2">
                <h3 className="mb-3 flex items-center gap-2 text-base font-semibold">
                  <ListChecks className="size-4 text-primary" />
                  Key Concepts
                </h3>
                <dl className="divide-y">
                  {notes.key_concepts.map((concept, idx) => (
                    <div key={idx} className="py-2">
                      <dt className="font-medium">{concept.term}</dt>
                      <dd className="mt-0.5 text-sm leading-relaxed text-muted-foreground">
                        {concept.definition}
                      </dd>
                    </div>
                  ))}
                </dl>
              </CardContent>
            </Card>
          )}

          {notes.generated_by === "mock" && (
            <p className="text-center text-xs text-muted-foreground">
              Sample notes shown — AI generation via {notes.provider} failed
              (check backend logs / .env).
            </p>
          )}

          <div className="flex items-center justify-center gap-2 pt-2">
            <LanguageToggle value={language} onChange={setLanguage} />
            <Button
              variant="outline"
              onClick={handleGenerate}
              disabled={generating}
              className="gap-2"
            >
              <RefreshCw className="size-4" />
              Regenerate Notes
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}