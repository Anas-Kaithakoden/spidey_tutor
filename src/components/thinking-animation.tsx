"use client";

import { useEffect, useState } from "react";
import { SpideyMascot } from "@/components/spidey-mascot";
import { cn } from "@/lib/utils";

interface ThinkingAnimationProps {
  variant?: "chat" | "card" | "inline";
  text?: string;
  subtext?: string;
  className?: string;
}

const DEFAULT_THOUGHTS = [
  "Spidey is referencing your lecture material...",
  "Synthesizing key formulas and concepts...",
  "Verifying citations against your notes...",
  "Formulating a grounded response...",
];

export function ThinkingAnimation({
  variant = "chat",
  text,
  subtext,
  className,
}: ThinkingAnimationProps) {
  const [thoughtIndex, setThoughtIndex] = useState(0);

  useEffect(() => {
    if (text) return; // if custom static text is provided, don't cycle
    const interval = setInterval(() => {
      setThoughtIndex((prev) => (prev + 1) % DEFAULT_THOUGHTS.length);
    }, 2800);
    return () => clearInterval(interval);
  }, [text]);

  const currentText = text || DEFAULT_THOUGHTS[thoughtIndex];

  if (variant === "inline") {
    return (
      <div className={cn("inline-flex items-center gap-2 text-xs text-[#c8c4d6]", className)}>
        <SpideyMascot mood="pondering" size={24} interactive={false} />
        <span className="font-medium text-white">{currentText}</span>
        <span className="flex items-center gap-1 ml-1">
          <span className="size-1.5 rounded-full bg-[#8e7fff] animate-bounce" style={{ animationDelay: "0ms" }} />
          <span className="size-1.5 rounded-full bg-[#e3c464] animate-bounce" style={{ animationDelay: "150ms" }} />
          <span className="size-1.5 rounded-full bg-[#ff8387] animate-bounce" style={{ animationDelay: "300ms" }} />
        </span>
      </div>
    );
  }

  if (variant === "card") {
    return (
      <div
        className={cn(
          "relative overflow-hidden p-6 sm:p-8 rounded-2xl bg-[#1d1a25]/90 border border-[#8e7fff]/30 shadow-xl backdrop-blur-md flex flex-col items-center justify-center text-center",
          className
        )}
      >
        {/* Subtle Ambient Radial Glow */}
        <div className="absolute inset-0 bg-radial from-[#8e7fff]/15 via-transparent to-transparent pointer-events-none" />

        {/* Mascot in deep thought */}
        <div className="relative mb-3 animate-pulse" style={{ animationDuration: "3s" }}>
          <div className="absolute -inset-2 rounded-full bg-[#8e7fff]/20 blur-lg" />
          <SpideyMascot mood="pondering" size={64} interactive={false} />
        </div>

        {/* Thinking wave text */}
        <div className="flex items-center gap-2 mb-1 z-10">
          <span className="font-space font-bold text-sm sm:text-base text-white">
            {currentText}
          </span>
          <span className="flex items-center gap-1">
            <span className="size-1.5 rounded-full bg-[#8e7fff] animate-bounce" style={{ animationDelay: "0ms" }} />
            <span className="size-1.5 rounded-full bg-[#e3c464] animate-bounce" style={{ animationDelay: "150ms" }} />
            <span className="size-1.5 rounded-full bg-[#ff8387] animate-bounce" style={{ animationDelay: "300ms" }} />
          </span>
        </div>

        <p className="text-xs text-[#c8c4d6] z-10">
          {subtext || "Strictly grounded in your material with zero hallucinations."}
        </p>

        {/* Glowing Strand Shimmer Bar */}
        <div className="w-48 h-1 bg-[#2c2834] rounded-full mt-4 overflow-hidden relative">
          <div className="absolute top-0 bottom-0 w-1/3 bg-gradient-to-r from-transparent via-[#8e7fff] to-transparent rounded-full animate-pulse" />
        </div>
      </div>
    );
  }

  // Default: Chat Bubble Variant
  return (
    <div className={cn("flex w-full justify-start items-start gap-2.5 my-2", className)}>
      {/* Mini Spidey Avatar */}
      <div className="size-8 rounded-full bg-[#211e2a] border border-[#8e7fff]/40 flex items-center justify-center shrink-0 shadow-sm mt-0.5">
        <SpideyMascot mood="pondering" size={26} interactive={false} />
      </div>

      {/* Thinking Chat Bubble */}
      <div className="flex flex-col gap-1 max-w-[85%]">
        <div className="flex items-center gap-2.5 rounded-2xl rounded-tl-sm bg-[#211e2a] border border-[#8e7fff]/20 px-4 py-3 shadow-md">
          <span className="text-xs sm:text-sm font-medium text-[#e7dff0]">
            {currentText}
          </span>

          {/* Glowing Wave Dots */}
          <span className="inline-flex items-center gap-1 ml-1">
            <span
              className="size-1.5 rounded-full bg-[#8e7fff] animate-bounce"
              style={{ animationDelay: "0ms", animationDuration: "1s" }}
            />
            <span
              className="size-1.5 rounded-full bg-[#e3c464] animate-bounce"
              style={{ animationDelay: "200ms", animationDuration: "1s" }}
            />
            <span
              className="size-1.5 rounded-full bg-[#ff8387] animate-bounce"
              style={{ animationDelay: "400ms", animationDuration: "1s" }}
            />
          </span>
        </div>

        <span className="text-[10px] text-[#c8c4d6]/80 pl-2 font-mono">
          {subtext || "Grounded analysis · zero hallucination check"}
        </span>
      </div>
    </div>
  );
}
