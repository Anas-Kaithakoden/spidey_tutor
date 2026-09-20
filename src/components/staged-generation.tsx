"use client";

import { useEffect, useState } from "react";
import { SpideyMascot } from "@/components/spidey-mascot";
import { Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface StagedGenerationProps {
  title?: string;
  stages?: string[];
  currentStageIndex?: number;
  className?: string;
}

const defaultStages = [
  "Reading your material",
  "Extracting core concepts",
  "Weaving questions & answers",
  "Finalizing study deck",
];

export function StagedGeneration({
  title = "Spidey is weaving your study session...",
  stages = defaultStages,
  currentStageIndex: controlledIndex,
  className,
}: StagedGenerationProps) {
  // If no controlled index is provided, simulate progression through stages for high perceived responsiveness
  const [internalIndex, setInternalIndex] = useState(0);
  const activeIndex = controlledIndex !== undefined ? controlledIndex : internalIndex;

  useEffect(() => {
    if (controlledIndex !== undefined) return;
    const interval = setInterval(() => {
      setInternalIndex((prev) => {
        if (prev < stages.length - 1) return prev + 1;
        return prev;
      });
    }, 2400);
    return () => clearInterval(interval);
  }, [controlledIndex, stages.length]);

  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center p-8 sm:p-12 text-center max-w-xl mx-auto rounded-3xl border border-primary/25 bg-card/80 shadow-xl backdrop-blur-md",
        className
      )}
      role="status"
      aria-live="polite"
    >
      {/* Animated Weaving Mascot */}
      <div className="mb-4 relative">
        <div className="absolute inset-0 rounded-full bg-primary/20 blur-xl animate-pulse" />
        <SpideyMascot mood="weaving" size={72} interactive={false} />
      </div>

      <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-foreground mb-2">
        {title}
      </h2>

      <p className="text-xs sm:text-sm text-muted-foreground mb-8">
        Analyzing your content to generate high-retention practice material.
      </p>

      {/* 4-Stage Stepper with Connecting Web Strand */}
      <div className="w-full relative px-2">
        {/* Background Connecting Strand */}
        <div className="absolute top-4 left-6 right-6 h-0.5 bg-border/80 -z-0" />

        {/* Active Animated Strand */}
        <div
          className="absolute top-4 left-6 h-0.5 bg-primary -z-0 transition-all duration-700 ease-out"
          style={{
            width: `${(activeIndex / (stages.length - 1)) * 100}%`,
          }}
        />

        {/* Stage Nodes */}
        <div className="relative flex justify-between items-start z-10">
          {stages.map((stage, idx) => {
            const isCompleted = idx < activeIndex;
            const isCurrent = idx === activeIndex;
            return (
              <div key={stage} className="flex flex-col items-center max-w-[80px] sm:max-w-[100px]">
                <div
                  className={cn(
                    "flex size-8 items-center justify-center rounded-full text-xs font-bold transition-all duration-300",
                    isCompleted && "bg-primary text-primary-foreground shadow-xs shadow-primary/40",
                    isCurrent && "bg-primary/20 border-2 border-primary text-primary ring-4 ring-primary/15 animate-pulse",
                    !isCompleted && !isCurrent && "bg-muted text-muted-foreground border border-border"
                  )}
                >
                  {isCompleted ? <Check className="size-4 stroke-[3]" /> : idx + 1}
                </div>
                <span
                  className={cn(
                    "text-[10px] sm:text-xs mt-2.5 font-medium leading-tight text-center transition-colors",
                    isCurrent ? "text-primary font-bold" : isCompleted ? "text-foreground" : "text-muted-foreground/70"
                  )}
                >
                  {stage}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
