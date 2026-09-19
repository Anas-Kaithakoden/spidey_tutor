"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { AudioLines, Loader2 } from "lucide-react";
import {
  createPodcast,
  getMaterial,
  listMaterials,
  PODCAST_DURATIONS,
  type Material,
  type PodcastMode,
} from "@/lib/api";
import { ModelSelect } from "@/components/model-select";

const modes: { value: PodcastMode; label: string; desc: string }[] = [
  {
    value: "learn",
    label: "Learn",
    desc: "Deep explanations & connections",
  },
  {
    value: "revise",
    label: "Revise",
    desc: "Fast, dense review of the essentials",
  },
  {
    value: "exam_prep",
    label: "Exam Prep",
    desc: "High-value concepts + quick self-checks",
  },
  {
    value: "weak_topics",
    label: "Weak Topics",
    desc: "Built around your low-scoring areas",
  },
];

export default function PodcastSetup() {
  const router = useRouter();
  const { model } = useStudy();
  const [materials, setMaterials] = useState<Material[]>([]);
  const [materialId, setMaterialId] = useState<number | null>(() => {
    if (typeof window === "undefined") return null;
    const id = Number(
      new URLSearchParams(window.location.search).get("material_id")
    );
    return Number.isFinite(id) && id > 0 ? id : null;
  });
  const [mode, setMode] = useState<PodcastMode>("learn");
  const [durationMinutes, setDurationMinutes] = useState(5);
  const [focusTopic, setFocusTopic] = useState("");
  const [title, setTitle] = useState("");
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    if (materialId !== null) return;
    listMaterials()
      .then((mats) => {
        setMaterials(mats);
        setMaterialId(mats[0]?.id ?? null);
      })
      .catch(() => toast.error("Failed to load study materials."));
  }, [materialId]);

  async function handleGenerate() {
    if (!materialId) {
      toast.error("Add study material first.");
      router.push("/add");
      return;
    }
    setGenerating(true);
    try {
      let currentMaterial: Material | null = null;
      try {
        currentMaterial = await getMaterial(materialId);
      } catch {
        // fall through — the create call reports a clearer error
      }
      if (!currentMaterial) {
        toast.error("Could not load the selected material.");
        return;
      }

      const episode = await createPodcast({
        material_id: currentMaterial.id,
        title: title || undefined,
        mode,
        duration_minutes: durationMinutes,
        focus_topic: focusTopic || undefined,
        provider: model.provider,
        model_name: model.name,
      });

      if (episode.generated_by === "mock") {
        toast.info(
          episode.warning ??
            `AI generation via ${model.provider} failed — showing a grounded fallback script. Check the backend .env.`
        );
      } else if (episode.generated_by === "quick") {
        toast.info("Quick Mode: script generated deterministically, no AI call.");
      } else if (episode.audio_status === "unavailable" && episode.warning) {
        toast.info(episode.warning);
      } else if (episode.audio_status === "error") {
        toast.info(episode.warning ?? "Script saved, but audio synthesis failed.");
      }

      router.push(`/podcast?id=${episode.id}`);
    } catch (err) {
      toast.error(
        err instanceof Error ? err.message : "Failed to create podcast."
      );
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Podcast Setup</h1>
      <p className="mb-8 text-muted-foreground">
        A two-host conversational audio episode generated from your study
        material.
      </p>

      <div className="space-y-8">
        {/* Model */}
        <ModelSelect />

        {/* Material */}
        {materials.length > 0 && (
          <section>
            <Label className="mb-3 block text-base font-medium">
              Study Material
            </Label>
            <select
              value={materialId ?? ""}
              disabled={generating}
              onChange={(e) => setMaterialId(Number(e.target.value))}
              className="flex h-9 w-full rounded-md border bg-background px-3 text-sm outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
            >
              {materials.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.title}
                </option>
              ))}
            </select>
          </section>
        )}

        {/* Mode */}
        <section>
          <Label className="mb-3 block text-base font-medium">Episode Style</Label>
          <div className="grid grid-cols-2 gap-3">
            {modes.map((m) => (
              <button
                key={m.value}
                onClick={() => setMode(m.value)}
                disabled={generating}
                className={`flex flex-col items-start gap-1 rounded-xl border-2 p-4 text-left transition-colors cursor-pointer disabled:opacity-50 ${
                  mode === m.value
                    ? "border-primary bg-primary/5"
                    : "border-transparent bg-muted/50 hover:bg-muted"
                }`}
              >
                <span className="font-medium">{m.label}</span>
                <span className="text-xs text-muted-foreground">{m.desc}</span>
              </button>
            ))}
          </div>
        </section>

        {/* Duration */}
        <section>
          <Label className="mb-3 block text-base font-medium">
            Duration{" "}
            <span className="text-xs font-normal text-muted-foreground">
              (max 10 min)
            </span>
          </Label>
          <div className="grid grid-cols-4 gap-3">
            {PODCAST_DURATIONS.map((mins) => (
              <button
                key={mins}
                onClick={() => setDurationMinutes(mins)}
                disabled={generating}
                className={`rounded-xl border-2 px-4 py-3 text-center font-medium transition-colors cursor-pointer disabled:opacity-50 ${
                  durationMinutes === mins
                    ? "border-primary bg-primary/5"
                    : "border-transparent bg-muted/50 hover:bg-muted"
                }`}
              >
                {mins} min
              </button>
            ))}
          </div>
        </section>

        {/* Focus topic */}
        <section>
          <Label className="mb-3 block text-base font-medium">
            Focus Topic/Unit{" "}
            <span className="text-xs font-normal text-muted-foreground">
              (optional)
            </span>
          </Label>
          <Input
            value={focusTopic}
            onChange={(e) => setFocusTopic(e.target.value)}
            placeholder="e.g. Chapter 3 — Chemical Bonding"
            disabled={generating}
          />
          <p className="mt-1 text-xs text-muted-foreground">
            The hosts will prioritize this topic when the material covers it.
            In Weak Topics mode, your low-scoring areas are prioritized
            automatically.
          </p>
        </section>

        {/* Title */}
        <section>
          <Label className="mb-3 block text-base font-medium">
            Episode Title{" "}
            <span className="text-xs font-normal text-muted-foreground">
              (optional)
            </span>
          </Label>
          <Input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g. Photosynthesis — Evening Listen"
            disabled={generating}
          />
        </section>
      </div>

      <div className="mt-10 flex justify-end">
        <Button
          onClick={handleGenerate}
          disabled={generating || materials.length === 0}
          className="gap-2 px-8"
        >
          {generating ? (
            <>
              <Loader2 className="size-4 animate-spin" />
              Generating episode...
            </>
          ) : (
            <>
              <AudioLines className="size-4" />
              Generate Podcast
            </>
          )}
        </Button>
      </div>
    </div>
  );
}