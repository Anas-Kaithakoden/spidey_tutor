"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, FileText, Loader2, Type, Volume2 } from "lucide-react";
import { generateAudioSummary, type AudioSummaryOut } from "@/lib/api";
import { AudioPlayer } from "@/components/audio-player";
import { toast } from "sonner";

export default function Preview() {
  const router = useRouter();
  const { material, model } = useStudy();
  const [audio, setAudio] = useState<AudioSummaryOut | null>(null);
  const [audioLoading, setAudioLoading] = useState(false);
  const [language, setLanguage] = useState<"en" | "ml">("en");
  const [speed, setSpeed] = useState(1);

  useEffect(() => {
    if (!material) router.replace("/add");
  }, [material, router]);

  if (!material) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Redirecting...</p>
      </div>
    );
  }

  const type = material.source_type;

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Material Preview</h1>
      <p className="mb-8 text-muted-foreground">
        Review your material before generating study content.
      </p>

      <Card>
        <CardContent className="pt-6">
          <div className="mb-4 flex items-center gap-3">
            <div className="flex size-10 items-center justify-center rounded-lg bg-muted">
              {type === "pdf" ? (
                <FileText className="size-5 text-muted-foreground" />
              ) : (
                <Type className="size-5 text-muted-foreground" />
              )}
            </div>
            <div>
              <h2 className="font-semibold">{material.title}</h2>
              <div className="flex flex-wrap gap-2">
                <Badge variant="secondary" className="text-xs">
                  {type.toUpperCase()}
                </Badge>
                <Badge variant="secondary" className="text-xs">
                  {material.word_count.toLocaleString()} words
                </Badge>
                <Badge variant="secondary" className="text-xs">
                  {material.char_count.toLocaleString()} chars
                </Badge>
              </div>
            </div>
          </div>

          <div className="mt-4 max-h-80 overflow-y-auto rounded-lg border bg-muted/30 p-4">
            <p className="whitespace-pre-wrap text-sm leading-relaxed text-muted-foreground">
              {material.content}
            </p>
          </div>
        </CardContent>
      </Card>

      <div className="mt-6 flex flex-wrap items-center justify-end gap-3">
        <div className="flex items-center gap-2 rounded-lg border bg-card px-2 py-1">
          <Button
            size="sm"
            variant={language === "en" ? "secondary" : "ghost"}
            onClick={() => setLanguage("en")}
            className="h-7 px-2 text-xs"
          >
            English
          </Button>
          <Button
            size="sm"
            variant={language === "ml" ? "secondary" : "ghost"}
            onClick={() => setLanguage("ml")}
            className="h-7 px-2 text-xs"
          >
            മലയാളം
          </Button>
        </div>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span>Speed</span>
          <input
            type="range"
            min={0.5}
            max={2}
            step={0.25}
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
            className="h-1 w-20 accent-primary"
          />
          <span className="w-8">{speed}x</span>
        </div>
        <Button
          variant="outline"
          onClick={async () => {
            if (!material) return;
            setAudioLoading(true);
            try {
              const res = await generateAudioSummary(
                material.id,
                model.provider,
                model.name,
                "Kore",
                language
              );
              setAudio(res);
              if (res.generated_by === "mock") toast("Summary from mock data");
              else if (!res.audio_base64) toast("Audio text ready — playing via browser TTS");
            } catch (e) {
              toast.error(e instanceof Error ? e.message : "Audio generation failed");
            } finally {
              setAudioLoading(false);
            }
          }}
          disabled={audioLoading}
          className="gap-2"
        >
          {audioLoading ? (
            <Loader2 className="size-4 animate-spin" />
          ) : (
            <Volume2 className="size-4" />
          )}
          {audioLoading ? "Generating..." : language === "ml" ? "മലയാളം സംഗ്രഹം" : "1-Min Audio Summary"}
        </Button>
        <Button onClick={() => router.push("/quiz/setup")} className="gap-2">
          Continue
          <ArrowRight className="size-4" />
        </Button>
      </div>

      <AudioPlayer data={audio} speed={speed} />
    </div>
  );
}