"use client";

import { useId } from "react";
import { cn } from "@/lib/utils";

export type SpideyMood = "idle" | "weaving" | "cheering" | "tangled" | "pondering";

interface SpideyMascotProps {
  mood?: SpideyMood;
  size?: number;
  className?: string;
  showThread?: boolean;
  interactive?: boolean;
}

/**
 * SpideyMascot: The Cosmic Playground study companion.
 * Cream body (#F2ECF8), dark plum eyes (#0E0B16), lavender legs (#8B7CFF),
 * and warm butter-yellow highlight star (#F7D774).
 */
export function SpideyMascot({
  mood = "idle",
  size = 40,
  className,
  showThread = false,
  interactive = true,
}: SpideyMascotProps) {
  const filterId = useId();

  return (
    <div
      className={cn(
        "relative inline-flex items-center justify-center transition-transform select-none",
        interactive && "hover:scale-105 active:scale-95 cursor-pointer",
        className
      )}
      style={{ width: size, height: showThread ? size * 1.35 : size }}
      role="img"
      aria-label={`Spidey mascot (${mood})`}
    >
      <svg
        viewBox="0 0 100 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full drop-shadow-md select-none"
      >
        <defs>
          {/* Lavender glow */}
          <filter id={`glow-${filterId}`} x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>

          {/* Body Cream to Soft Lavender Gradient */}
          <linearGradient id={`bodyGrad-${filterId}`} x1="30" y1="25" x2="70" y2="85" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="60%" stopColor="#F2ECF8" />
            <stop offset="100%" stopColor="#E4D9F5" />
          </linearGradient>

          {/* Legs Lavender Gradient */}
          <linearGradient id={`legGrad-${filterId}`} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#9E90FF" />
            <stop offset="100%" stopColor="#8B7CFF" />
          </linearGradient>

          {/* Butter Yellow Star Gradient */}
          <linearGradient id={`starGrad-${filterId}`} x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#FFF2A8" />
            <stop offset="100%" stopColor="#F7D774" />
          </linearGradient>
        </defs>

        {/* Optional Dangling Lavender Thread */}
        {showThread && (
          <line
            x1="50"
            y1="0"
            x2="50"
            y2="34"
            stroke="#8B7CFF"
            strokeWidth="1.75"
            strokeDasharray="2 2"
            opacity="0.75"
          />
        )}

        {/* --- LEGS (8 lavender rounded legs with joint dots) --- */}
        {mood === "cheering" ? (
          <g stroke="#8B7CFF" strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M28 48 Q14 32 18 16" />
            <path d="M25 56 Q8 46 12 30" />
            <path d="M26 64 Q10 62 14 48" />
            <path d="M30 70 Q18 80 24 90" />
            <path d="M72 48 Q86 32 82 16" />
            <path d="M75 56 Q92 46 88 30" />
            <path d="M74 64 Q90 62 86 48" />
            <path d="M70 70 Q82 80 76 90" />
          </g>
        ) : mood === "weaving" ? (
          <g stroke="#8B7CFF" strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M28 48 Q10 36 16 25" />
            <path d="M24 56 Q6 54 22 60" />
            <path d="M26 65 Q8 74 30 78" />
            <path d="M30 72 Q22 90 40 86" />
            <path d="M72 48 Q90 36 84 25" />
            <path d="M76 56 Q94 54 78 60" />
            <path d="M74 65 Q92 74 70 78" />
            <path d="M70 72 Q78 90 60 86" />
          </g>
        ) : mood === "tangled" ? (
          <g stroke="#8B7CFF" strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round" opacity="0.8">
            <path d="M28 52 Q10 40 20 30" />
            <path d="M26 60 Q8 70 28 75" />
            <path d="M26 66 Q18 85 38 82" />
            <path d="M32 70 Q28 90 43 88" />
            <path d="M72 52 Q90 40 80 30" />
            <path d="M74 60 Q92 70 72 75" />
            <path d="M74 66 Q82 85 62 82" />
            <path d="M68 70 Q72 90 57 88" />
          </g>
        ) : mood === "pondering" ? (
          // Pondering legs: left leg raised to tap chin/temple in deep thought
          <g stroke="#8B7CFF" strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M28 48 Q16 42 34 52" />
            <path d="M24 57 Q6 55 16 70" />
            <path d="M26 66 Q10 74 20 86" />
            <path d="M30 72 Q22 88 34 92" />
            <path d="M72 48 Q90 36 86 24" />
            <path d="M76 57 Q94 55 84 70" />
            <path d="M74 66 Q90 74 80 86" />
            <path d="M70 72 Q78 88 66 92" />
          </g>
        ) : (
          // Idle legs
          <g stroke="#8B7CFF" strokeWidth="4.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M28 48 Q10 36 14 24" />
            <path d="M24 57 Q6 55 16 70" />
            <path d="M26 66 Q10 74 20 86" />
            <path d="M30 72 Q22 88 34 92" />
            <path d="M72 48 Q90 36 86 24" />
            <path d="M76 57 Q94 55 84 70" />
            <path d="M74 66 Q90 74 80 86" />
            <path d="M70 72 Q78 88 66 92" />
          </g>
        )}

        {/* --- MAIN CREAM BODY (#F2ECF8) --- */}
        <ellipse
          cx="50"
          cy="58"
          rx="27"
          ry="25"
          fill={`url(#bodyGrad-${filterId})`}
          stroke="#8B7CFF"
          strokeWidth="2.5"
        />

        {/* --- BUTTER YELLOW STAR ON FOREHEAD (#F7D774) --- */}
        <g transform="translate(50, 42) scale(0.95)" fill={`url(#starGrad-${filterId})`}>
          <path d="M0 -7 L1.8 -2 L7 0 L1.8 2 L0 7 L-1.8 2 L-7 0 L-1.8 -2 Z" />
        </g>

        {/* --- WEAVING GLOWING STRAND (when weaving) --- */}
        {mood === "weaving" && (
          <g stroke="#F7D774" strokeWidth="2.5" strokeLinecap="round" strokeDasharray="3 3">
            <path d="M30 74 Q50 66 70 74" />
            <circle cx="50" cy="70" r="3.5" fill="#F7D774" />
          </g>
        )}

        {/* --- PONDERING THOUGHT BUBBLES (when pondering) --- */}
        {mood === "pondering" && (
          <g className="animate-pulse" style={{ animationDuration: "2s" }}>
            <circle cx="68" cy="30" r="2.5" fill="#F7D774" opacity="0.8" />
            <circle cx="75" cy="22" r="3.5" fill="#8E7FFF" opacity="0.8" />
            <circle cx="83" cy="13" r="5" fill="#F7D774" opacity="0.9" />
          </g>
        )}

        {/* --- TANGLED LOOPS (when tangled) --- */}
        {mood === "tangled" && (
          <path
            d="M28 52 Q55 35 68 62 Q72 82 46 76 Q24 72 52 56"
            stroke="#FF8387"
            strokeWidth="2"
            fill="none"
          />
        )}

        {/* --- EYES (Dark Plum #0E0B16 with big cute catchlights) --- */}
        {mood === "cheering" ? (
          <g stroke="#0E0B16" strokeWidth="4" strokeLinecap="round">
            <path d="M37 54 Q42 47 47 54" />
            <path d="M53 54 Q58 47 63 54" />
          </g>
        ) : mood === "tangled" ? (
          <g stroke="#0E0B16" strokeWidth="3" strokeLinecap="round">
            <line x1="37" y1="49" x2="45" y2="57" />
            <line x1="45" y1="49" x2="37" y2="57" />
            <line x1="55" y1="49" x2="63" y2="57" />
            <line x1="63" y1="49" x2="55" y2="57" />
          </g>
        ) : mood === "pondering" ? (
          <g>
            {/* Left Eye looking up-right */}
            <ellipse cx="43" cy="51" rx="6" ry="7" fill="#0E0B16" />
            <circle cx="45.5" cy="48" r="2.2" fill="#FFFFFF" />
            <circle cx="41.5" cy="53" r="1.1" fill="#FFFFFF" />

            {/* Right Eye looking up-right */}
            <ellipse cx="60" cy="51" rx="6" ry="7" fill="#0E0B16" />
            <circle cx="62.5" cy="48" r="2.2" fill="#FFFFFF" />
            <circle cx="58.5" cy="53" r="1.1" fill="#FFFFFF" />
          </g>
        ) : (
          <g>
            {/* Left Eye */}
            <ellipse cx="41.5" cy="53" rx="6" ry="7.5" fill="#0E0B16" />
            <circle cx="43.5" cy="50.5" r="2.2" fill="#FFFFFF" />
            <circle cx="39.5" cy="55.5" r="1.1" fill="#FFFFFF" />

            {/* Right Eye */}
            <ellipse cx="58.5" cy="53" rx="6" ry="7.5" fill="#0E0B16" />
            <circle cx="60.5" cy="50.5" r="2.2" fill="#FFFFFF" />
            <circle cx="56.5" cy="55.5" r="1.1" fill="#FFFFFF" />
          </g>
        )}

        {/* Tiny sweet smile */}
        {mood !== "tangled" && (
          <path
            d={mood === "pondering" ? "M48 66 Q50 63 53 65" : "M47 65 Q50 68 53 65"}
            stroke="#0E0B16"
            strokeWidth="2.2"
            strokeLinecap="round"
            fill="none"
          />
        )}

        {/* Soft rosy cheeks */}
        <circle cx="33" cy="61" r="3.5" fill="#FF8387" opacity="0.35" />
        <circle cx="67" cy="61" r="3.5" fill="#FF8387" opacity="0.35" />
      </svg>
    </div>
  );
}
