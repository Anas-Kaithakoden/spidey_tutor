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
  const [options, setOptions] = useState<ModelOption[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getModels()
      .then((data) => {
        if (data.providers.length) {
          setOptions(data.providers);
        } else {
          setOptions([
            { provider: "gemini", name: "gemini-2.5-flash", label: "Gemini" },
          ]);
        }
      })
      .catch(() => {
        setOptions([
          { provider: "gemini", name: "gemini-2.5-flash", label: "Gemini" },
        ]);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className={className}>
      <label className="mb-1.5 block text-sm font-medium text-muted-foreground">
        AI Model
      </label>
      <select
        disabled={loading}
        value={`${model.provider}:${model.name}`}
        onChange={(e) => {
          const opt = options.find(
            (o) => `${o.provider}:${o.name}` === e.target.value
          );
          if (opt) setModel(opt);
        }}
        className="flex h-9 w-full rounded-md border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring"
      >
        {loading && <option>Loading models...</option>}
        {!loading &&
          options.map((opt) => (
            <option key={`${opt.provider}:${opt.name}`} value={`${opt.provider}:${opt.name}`}>
              {providerBadge(opt.provider)} — {opt.label}
            </option>
          ))}
      </select>
    </div>
  );
}