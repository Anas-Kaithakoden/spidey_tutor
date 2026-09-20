"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { EmptyState } from "@/components/ui/empty-state";
import { FlashcardDeck } from "@/components/flashcard-deck";
import { StagedGeneration } from "@/components/staged-generation";
import { MaterialPicker } from "@/components/material-picker";
import { ModelSelect } from "@/components/model-select";
import {
  generateFlashcards,
  getFlashcards,
  type FlashcardOut,
} from "@/lib/api";
import { Sparkles, Layers, RotateCcw } from "lucide-react";

export default function Flashcards() {
  const router = useRouter();
  const { material, model } = useStudy();
  const [cards, setCards] = useState<FlashcardOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (!material) {
      setTimeout(() => setLoading(false), 0);
      return;
    }
    let cancelled = false;
    setTimeout(() => setLoading(true), 0);
    getFlashcards(material.id)
      .then((existing) => {
        if (!cancelled) setCards(existing);
      })
      .catch((err) => {
        if (!cancelled) {
          toast.error(err instanceof Error ? err.message : "Failed to load flashcards.");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [material]);

  async function handleGenerate() {
    if (!material) return;
    setGenerating(true);
    try {
      const generated = await generateFlashcards(material.id, model.provider, model.name);
      setCards(generated);
      if (generated.length && generated[0].provider === "quick") {
        toast.info("Quick Mode: flashcards generated deterministically, no AI call.");
      } else {
        toast.success("Flashcards generated successfully!");
      }
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to generate flashcards.");
    } finally {
      setGenerating(false);
    }
  }

  // If no material is selected, show the in-page MaterialPicker instead of redirecting!
  if (!material) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-12">
        <MaterialPicker
          title="Choose a Study Set for Flashcards"
          description="Select which of your uploaded materials you want to review or generate 3D flashcards for."
        />
      </div>
    );
  }

  if (generating) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-20">
        <StagedGeneration
          title="Spidey is weaving your flashcard deck..."
          stages={[
            "Reading lecture concepts",
            "Pairing terms & explanations",
            "Refining active-recall cards",
            "Ready for study!",
          ]}
        />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-10 sm:py-14">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <div className="inline-flex items-center gap-1.5 rounded-full border border-accent/30 bg-accent/15 px-3 py-0.5 text-xs font-semibold text-accent-foreground mb-2 shadow-xs">
            <Layers className="size-3.5 text-brand-gold" />
            <span>Active Recall Deck</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-foreground">
            Study Flashcards
          </h1>
          <p className="text-sm text-muted-foreground mt-1">
            Studying: <strong className="text-foreground">{material.title || "Untitled Material"}</strong>
          </p>
        </div>

        {cards.length > 0 && (
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleGenerate}
              disabled={generating}
              className="rounded-xl border-border/80 hover:bg-muted"
            >
              <RotateCcw className="size-3.5 mr-1.5" />
              Regenerate
            </Button>
          </div>
        )}
      </div>

      {cards.length > 0 && cards[0].provider === "quick" && (
        <Badge variant="secondary" className="mb-6 font-mono text-xs">
          Quick Mode — Deterministic synthesis
        </Badge>
      )}

      {/* Main Content Area */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-24 text-center">
          <div className="size-8 rounded-full border-2 border-primary border-t-transparent animate-spin mb-4" />
          <p className="text-sm text-muted-foreground">Loading your flashcards...</p>
        </div>
      ) : cards.length === 0 ? (
        <EmptyState
          mascotMood="idle"
          title="No flashcards generated yet"
          description="Give Spidey your study material and I will extract the most critical definitions, equations, and active recall concepts."
          action={
            <div className="flex flex-col items-center gap-4 w-full max-w-sm mt-4">
              <ModelSelect className="w-full" />
              <Button
                onClick={handleGenerate}
                disabled={generating}
                size="lg"
                className="w-full rounded-xl font-semibold shadow-md shadow-primary/20 hover:shadow-primary/30"
              >
                <Sparkles className="size-4 mr-2" />
                Generate Flashcard Deck
              </Button>
            </div>
          }
        />
      ) : (
        <FlashcardDeck
          cards={cards}
          onTakeQuiz={() => router.push("/quiz/setup")}
        />
      )}
    </div>
  );
}