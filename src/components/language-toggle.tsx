"use client";

import { Button } from "@/components/ui/button";

export type StudyLanguage = "en" | "ml";

interface LanguageToggleProps {
  value: StudyLanguage;
  onChange: (language: StudyLanguage) => void;
}

export function LanguageToggle({ value, onChange }: LanguageToggleProps) {
  return (
    <div className="flex items-center gap-1 rounded-lg border bg-card px-1 py-1">
      <Button
        size="sm"
        variant={value === "en" ? "secondary" : "ghost"}
        onClick={() => onChange("en")}
        className="h-6 px-2 text-xs"
      >
        English
      </Button>
      <Button
        size="sm"
        variant={value === "ml" ? "secondary" : "ghost"}
        onClick={() => onChange("ml")}
        className="h-6 px-2 text-xs"
      >
        മലയാളം
      </Button>
    </div>
  );
}