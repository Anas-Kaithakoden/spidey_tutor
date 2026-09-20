"use client";

import { useState, useEffect } from "react";
import { getModels, type ModelOption } from "@/lib/api";
import { useStudy } from "@/lib/context";

const PROVIDER_BADGE: Record<string, string> = {
  gemini: "Cloud",
  ollama: "Local",
  groq: "Groq",
  openrouter: "OpenRouter",
  quick: "Quick",
};

function providerBadge(provider: string): string {
  return PROVIDER_BADGE[provider] ?? provider;
}

export function ModelSelect({ className }: { className?: string }) {
  const { model, setModel } = useStudy();
  const [options, setOptions] = useState<ModelOption[]>([model]);

  useEffect(() => {
    let cancelled = false;
    getModels()
      .then((data) => {
        if (cancelled) return;
        if (data.providers.length) {
          setOptions(data.providers);
        }
      })
      .catch(() => {
        // keep current model as option
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className={className}>
      <label className="mb-1.5 block text-sm font-medium text-muted-foreground">
        AI Model
      </label>
      <select
        value={`${model.provider}:${model.name}`}
        onChange={(e) => {
          const opt = options.find(
            (o) => `${o.provider}:${o.name}` === e.target.value
          );
          if (opt) setModel(opt);
        }}
        className="flex h-9 w-full rounded-md border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring"
      >
        {options.map((opt) => (
          <option key={`${opt.provider}:${opt.name}`} value={`${opt.provider}:${opt.name}`}>
            {providerBadge(opt.provider)} — {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}