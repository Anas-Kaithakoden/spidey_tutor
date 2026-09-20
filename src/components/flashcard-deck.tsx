"use client";

import { useState, useEffect, useCallback } from "react";
import { type FlashcardOut, reviewFlashcard } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { SpideyMascot } from "@/components/spidey-mascot";
import {
  ChevronLeft,
  ChevronRight,
  RotateCw,
  Sparkles,
  CheckCircle2,
  HelpCircle,
  Trophy,
  RotateCcw,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface FlashcardDeckProps {
  cards: FlashcardOut[];
  onTakeQuiz?: () => void;
}

export function FlashcardDeck({ cards, onTakeQuiz }: FlashcardDeckProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [masteredIds, setMasteredIds] = useState<Set<number>>(new Set());
  const [reviewIds, setReviewIds] = useState<Set<number>>(new Set());
  const [isFinished, setIsFinished] = useState(false);

  const currentCard = cards[currentIndex];
  const totalCards = cards.length;

  const handleFlip = useCallback(() => {
    setIsFlipped((prev) => !prev);
    if (!isFlipped && currentCard) {
      // Best-effort review tracking on first flip
      reviewFlashcard(currentCard.id).catch(() => {});
    }
  }, [isFlipped, currentCard]);

  const goNext = useCallback(() => {
    setIsFlipped(false);
    if (currentIndex < totalCards - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      setIsFinished(true);
    }
  }, [currentIndex, totalCards]);

  const goPrev = useCallback(() => {
    setIsFlipped(false);
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  }, [currentIndex]);

  const markMastered = useCallback(() => {
    if (!currentCard) return;
    setMasteredIds((prev) => new Set(prev).add(currentCard.id));
    setReviewIds((prev) => {
      const next = new Set(prev);
      next.delete(currentCard.id);
      return next;
    });
    goNext();
  }, [currentCard, goNext]);

  const markStillLearning = useCallback(() => {
    if (!currentCard) return;
    setReviewIds((prev) => new Set(prev).add(currentCard.id));
    setMasteredIds((prev) => {
      const next = new Set(prev);
      next.delete(currentCard.id);
      return next;
    });
    goNext();
  }, [currentCard, goNext]);

  // Keyboard navigation
  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      // Ignore if user is typing in an input
      if (["INPUT", "TEXTAREA"].includes((e.target as HTMLElement).tagName)) return;

      if (e.code === "Space" || e.code === "Enter") {
        e.preventDefault();
        handleFlip();
      } else if (e.code === "ArrowRight") {
        e.preventDefault();
        goNext();
      } else if (e.code === "ArrowLeft") {
        e.preventDefault();
        goPrev();
      } else if (isFlipped && (e.key === "1" || e.code === "Digit1")) {
        e.preventDefault();
        markStillLearning();
      } else if (isFlipped && (e.key === "2" || e.code === "Digit2")) {
        e.preventDefault();
        markMastered();
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleFlip, goNext, goPrev, markMastered, markStillLearning, isFlipped]);

  function restartDeck() {
    setCurrentIndex(0);
    setIsFlipped(false);
    setIsFinished(false);
    setMasteredIds(new Set());
    setReviewIds(new Set());
  }

  // Completion Screen
  if (isFinished) {
    const masteredCount = masteredIds.size;
    const reviewCount = reviewIds.size;

    return (
      <div className="flex flex-col items-center justify-center p-8 sm:p-12 text-center rounded-3xl border border-primary/30 bg-card/80 shadow-2xl backdrop-blur-md max-w-xl mx-auto animate-in zoom-in-95">
        <div className="mb-4">
          <SpideyMascot mood="cheering" size={80} interactive={false} />
        </div>

        <div className="inline-flex items-center gap-1.5 rounded-full border border-brand-gold/30 bg-brand-gold/15 px-3 py-1 text-xs font-bold text-brand-gold mb-3">
          <Trophy className="size-4" />
          <span>Deck Completed!</span>
        </div>

        <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-foreground mb-2">
          Awesome review session!
        </h2>
        <p className="text-sm text-muted-foreground mb-8 max-w-md">
          You have reviewed all {totalCards} cards in this deck. Repetition strengthens neural pathways.
        </p>

        {/* Score Pills */}
        <div className="flex items-center justify-center gap-4 w-full mb-8">
          <div className="flex-1 rounded-2xl border border-success/30 bg-success/10 p-4">
            <span className="block text-2xl font-extrabold text-success">{masteredCount}</span>
            <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Mastered</span>
          </div>
          <div className="flex-1 rounded-2xl border border-warning/30 bg-warning/10 p-4">
            <span className="block text-2xl font-extrabold text-warning">{reviewCount}</span>
            <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">Still Learning</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-3 w-full">
          <Button
            onClick={restartDeck}
            variant="outline"
            className="flex-1 h-12 rounded-xl font-semibold border-border/80 hover:bg-muted"
          >
            <RotateCcw className="size-4 mr-2" />
            Restart Deck
          </Button>
          {onTakeQuiz && (
            <Button
              onClick={onTakeQuiz}
              className="flex-1 h-12 rounded-xl font-semibold bg-primary text-primary-foreground shadow-md shadow-primary/20 hover:shadow-primary/30"
            >
              <Sparkles className="size-4 mr-2" />
              Take Quiz
            </Button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center w-full max-w-xl mx-auto">
      {/* Top Meta Bar */}
      <div className="flex items-center justify-between w-full mb-4 px-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
            Card {currentIndex + 1} of {totalCards}
          </span>
          {masteredIds.has(currentCard.id) && (
            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-success bg-success/10 px-2 py-0.5 rounded-full border border-success/20">
              <CheckCircle2 className="size-3" /> Mastered
            </span>
          )}
          {reviewIds.has(currentCard.id) && (
            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-warning bg-warning/10 px-2 py-0.5 rounded-full border border-warning/20">
              <HelpCircle className="size-3" /> Review
            </span>
          )}
        </div>

        {/* Mini progress bar */}
        <div className="w-24 h-2 bg-muted rounded-full overflow-hidden border border-border/60">
          <div
            className="h-full bg-primary transition-all duration-300 rounded-full"
            style={{ width: `${((currentIndex + 1) / totalCards) * 100}%` }}
          />
        </div>
      </div>

      {/* 3D Flip Card Container */}
      <div
        className="w-full h-80 sm:h-96 perspective-1200 cursor-pointer select-none group"
        onClick={handleFlip}
        role="button"
        tabIndex={0}
        aria-label={`Flashcard: ${isFlipped ? "Answer" : "Question"}. Click to flip.`}
      >
        <div
          className={cn(
            "relative w-full h-full preserve-3d transition-transform duration-500 ease-out",
            isFlipped && "rotate-y-180"
          )}
        >
          {/* FRONT FACE */}
          <div className="absolute inset-0 backface-hidden rounded-3xl border border-primary/25 bg-card/90 p-6 sm:p-8 flex flex-col justify-between shadow-xl backdrop-blur-md transition-all group-hover:border-primary/50 group-hover:shadow-primary/10">
            {/* Front Header */}
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-brand-teal bg-brand-teal/10 px-2.5 py-1 rounded-lg border border-brand-teal/20">
                Question
              </span>
              <span className="text-xs text-muted-foreground flex items-center gap-1">
                <RotateCw className="size-3" /> Flip
              </span>
            </div>

            {/* Front Content */}
            <div className="my-auto text-center px-4">
              <p className="text-lg sm:text-2xl font-bold tracking-tight text-foreground leading-relaxed">
                {currentCard.front}
              </p>
            </div>

            {/* Front Footer Hint */}
            <div className="text-center pt-2 border-t border-border/50">
              <span className="text-xs text-muted-foreground">
                Click to flip or press <kbd className="px-1.5 py-0.5 rounded bg-muted text-[10px] font-mono border">Space</kbd>
              </span>
            </div>
          </div>

          {/* BACK FACE */}
          <div className="absolute inset-0 backface-hidden rotate-y-180 rounded-3xl border border-accent/40 bg-card/95 p-6 sm:p-8 flex flex-col justify-between shadow-xl backdrop-blur-md">
            {/* Back Header */}
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-accent-foreground bg-accent/20 px-2.5 py-1 rounded-lg border border-accent/30">
                Answer
              </span>
              <span className="text-xs text-muted-foreground flex items-center gap-1">
                <RotateCw className="size-3" /> Flip back
              </span>
            </div>

            {/* Back Content */}
            <div className="my-auto text-center px-4 overflow-y-auto max-h-48">
              <p className="text-base sm:text-xl font-medium text-foreground leading-relaxed">
                {currentCard.back}
              </p>
            </div>

            {/* Back Self-Scoring Triggers */}
            <div
              className="flex items-center gap-3 pt-4 border-t border-border/50"
              onClick={(e) => e.stopPropagation()} // Prevent card flipping when clicking buttons
            >
              <Button
                type="button"
                onClick={markStillLearning}
                variant="outline"
                size="sm"
                className="flex-1 rounded-xl h-10 border-warning/40 text-warning hover:bg-warning/10 font-semibold"
              >
                <HelpCircle className="size-4 mr-1.5" />
                <span>Still Learning</span>
                <kbd className="ml-2 px-1 py-0.2 rounded bg-muted text-[9px] font-mono opacity-70">1</kbd>
              </Button>
              <Button
                type="button"
                onClick={markMastered}
                size="sm"
                className="flex-1 rounded-xl h-10 bg-success text-white hover:bg-success/90 font-semibold shadow-xs"
              >
                <CheckCircle2 className="size-4 mr-1.5" />
                <span>Got It!</span>
                <kbd className="ml-2 px-1 py-0.2 rounded bg-black/20 text-[9px] font-mono opacity-80">2</kbd>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="flex items-center justify-between w-full mt-6 px-2">
        <Button
          variant="outline"
          onClick={goPrev}
          disabled={currentIndex === 0}
          className="rounded-xl px-4 border-border/80 hover:bg-muted"
        >
          <ChevronLeft className="size-4 mr-1" />
          Previous
        </Button>

        <div className="flex gap-1.5">
          {cards.map((_, idx) => (
            <button
              key={idx}
              onClick={() => {
                setIsFlipped(false);
                setCurrentIndex(idx);
              }}
              className={cn(
                "size-2 rounded-full transition-all cursor-pointer",
                idx === currentIndex
                  ? "w-6 bg-primary"
                  : masteredIds.has(cards[idx].id)
                  ? "bg-success/70"
                  : reviewIds.has(cards[idx].id)
                  ? "bg-warning/70"
                  : "bg-muted-foreground/30 hover:bg-muted-foreground/60"
              )}
              aria-label={`Jump to card ${idx + 1}`}
            />
          ))}
        </div>

        <Button
          variant="outline"
          onClick={goNext}
          className="rounded-xl px-4 border-border/80 hover:bg-muted"
        >
          <span>{currentIndex === totalCards - 1 ? "Finish" : "Next"}</span>
          <ChevronRight className="size-4 ml-1" />
        </Button>
      </div>
    </div>
  );
}
