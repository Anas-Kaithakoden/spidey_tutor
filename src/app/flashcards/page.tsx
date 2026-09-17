"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  ChevronLeft,
  ChevronRight,
  CreditCard,
  Loader2,
  RotateCcw,
} from "lucide-react";
import {
  generateFlashcards,
  getFlashcards,
  type FlashcardOut,
} from "@/lib/api";
import { ModelSelect } from "@/components/model-select";

export default function Flashcards() {
  const router = useRouter();
  const { material, model } = useStudy();
  const [cards, setCards] = useState<FlashcardOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [current, setCurrent] = useState(0);
  const [flipped, setFlipped] = useState(false);

  useEffect(() => {
    if (!material) {
      router.replace("/add");
      return;
    }
    let cancelled = false;
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
  }, [material, router]);

  async function handleGenerate() {
    if (!material) return;
    setGenerating(true);
    try {
      const generated = await generateFlashcards(material.id, model.provider, model.name);
      setCards(generated);
      setCurrent(0);
      setFlipped(false);
      toast.success("Flashcards generated!");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to generate flashcards.");
    } finally {
      setGenerating(false);
    }
  }

  function goNext() {
    setFlipped(false);
    setCurrent((prev) => (prev < cards.length - 1 ? prev + 1 : 0));
  }

  function goPrev() {
    setFlipped(false);
    setCurrent((prev) => (prev > 0 ? prev - 1 : cards.length - 1));
  }

  if (!material) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Redirecting...</p>
      </div>
    );
  }

  const card = cards[current];

  return (
    <div className="mx-auto max-w-lg px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Flashcards</h1>
      <p className="mb-8 text-muted-foreground">
        {cards.length > 0
          ? "Click the card to flip it. Use arrows to navigate."
          : "Your flashcards are saved alongside your study material."}
      </p>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-24">
          <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
          <p className="text-muted-foreground">Loading flashcards...</p>
        </div>
      ) : cards.length === 0 ? (
        <div className="flex flex-col items-center gap-4 rounded-xl border border-dashed p-12 text-center">
          <CreditCard className="size-10 text-muted-foreground" />
          <p className="text-sm text-muted-foreground">
            No flashcards yet. Generate them from your study material — the AI
            pulls out the most important concepts and definitions.
          </p>
          <ModelSelect className="w-full max-w-xs" />
          <Button
            onClick={handleGenerate}
            disabled={generating}
            className="gap-2"
          >
            {generating ? (
              <>
                <Loader2 className="size-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <CreditCard className="size-4" />
                Generate Flashcards
              </>
            )}
          </Button>
        </div>
      ) : (
        <>
          {/* Card */}
          <div
            onClick={() => setFlipped(!flipped)}
            className="mb-8 cursor-pointer"
            style={{ perspective: "1000px" }}
          >
            <Card className="min-h-[250px]">
              <CardContent className="flex flex-col items-center justify-center pt-6 text-center">
                <p className="mb-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">
                  {flipped ? "Back" : "Front"}
                </p>
                <p className="text-lg font-medium leading-relaxed">
                  {flipped ? card.back : card.front}
                </p>
                <p className="mt-4 text-xs text-muted-foreground">
                  Click to {flipped ? "see front" : "reveal answer"}
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Navigation */}
          <div className="flex items-center justify-between">
            <Button variant="outline" onClick={goPrev} className="gap-1">
              <ChevronLeft className="size-4" />
              Previous
            </Button>

            <span className="text-sm text-muted-foreground">
              {current + 1} / {cards.length}
            </span>

            <Button variant="outline" onClick={goNext} className="gap-1">
              Next
              <ChevronRight className="size-4" />
            </Button>
          </div>

          {/* Dots */}
          <div className="mt-6 flex flex-wrap justify-center gap-2">
            {cards.map((_, idx) => (
              <button
                key={idx}
                onClick={() => {
                  setFlipped(false);
                  setCurrent(idx);
                }}
                className={`size-2.5 rounded-full transition-colors cursor-pointer ${
                  idx === current ? "bg-primary" : "bg-muted"
                }`}
              />
            ))}
          </div>

          {/* Actions */}
          <div className="mt-8 flex justify-center">
            <Button
              variant="outline"
              onClick={() => router.push("/quiz/setup")}
              className="gap-2"
            >
              <RotateCcw className="size-4" />
              Take a Quiz
            </Button>
          </div>
        </>
      )}
    </div>
  );
}