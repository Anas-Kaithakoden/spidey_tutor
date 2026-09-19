"use client";

import { useRef, useState } from "react";
import { toast } from "sonner";
import {
  AlertCircle,
  AudioLines,
  Clock,
  List,
  Mic,
  Pause,
  Play,
  RefreshCw,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "cn";
import {
  regeneratePodcastAudio,
  type PodcastAudioStatus,
  type PodcastEpisode,
  type PodcastMode,
} from "@/lib/api";

const MODE_LABELS: Record<PodcastMode, string> = {
  learn: "Learn",
  revise: "Revise",
  exam_prep: "Exam Prep",
  weak_topics: "Weak Topics",
};

const SPEEDS = [0.75, 1, 1.25, 1.5];

function formatTime(seconds: number): string {
  if (!Number.isFinite(seconds) || seconds < 0) return "0:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

interface Props {
  episode: PodcastEpisode;
  onUpdated: (episode: PodcastEpisode) => void;
}

export function PodcastPlayer({ episode, onUpdated }: Props) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [speed, setSpeed] = useState(1);
  const [showTranscript, setShowTranscript] = useState(false);
  const [regenerating, setRegenerating] = useState(false);

  const canPlay = episode.has_audio && !!episode.audio_url;

  function toggle() {
    const audio = audioRef.current;
    if (!audio) return;
    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      audio.playbackRate = speed;
      audio.play().catch(() => toast.error("Playback failed to start."));
    }
  }

  function seek(value: number) {
    const audio = audioRef.current;
    if (!audio || !Number.isFinite(value)) return;
    audio.currentTime = value;
    setCurrentTime(value);
  }

  function changeSpeed(next: number) {
    setSpeed(next);
    if (audioRef.current) audioRef.current.playbackRate = next;
  }

  async function retryAudio() {
    setRegenerating(true);
    try {
      const updated = await regeneratePodcastAudio(episode.id);
      onUpdated(updated);
      toast.success(updated.warning ?? "Audio is ready to play.");
    } catch (err) {
      toast.error(
        err instanceof Error ? err.message : "Audio regeneration failed."
      );
    } finally {
      setRegenerating(false);
    }
  }

  const statusText: Record<PodcastAudioStatus, string> = {
    unavailable:
      "Audio unavailable — add a GEMINI_API_KEY to generate it.",
    error: "Audio generation failed. You can retry below.",
    ready: "",
  };

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="mb-4 flex flex-wrap items-center gap-2">
          <AudioLines className="size-5 shrink-0" />
          <h2 className="font-semibold">{episode.title}</h2>
          <Badge variant="secondary">{MODE_LABELS[episode.mode]}</Badge>
          <Badge variant="outline" className="gap-1">
            <Clock className="size-3" /> {episode.duration_minutes} min
          </Badge>
          {episode.generated_by !== "ai" && (
            <Badge
              variant={episode.generated_by === "mock" ? "destructive" : "outline"}
              className="gap-1"
            >
              <Sparkles className="size-3" />
              {episode.generated_by === "mock" ? "mock fallback" : "quick mode"}
            </Badge>
          )}
          {episode.focus_topic && (
            <Badge variant="outline">Focus: {episode.focus_topic}</Badge>
          )}
        </div>

        {canPlay ? (
          <>
            <audio
              ref={audioRef}
              src={episode.audio_url ?? undefined}
              preload="metadata"
              onPlay={() => setIsPlaying(true)}
              onPause={() => setIsPlaying(false)}
              onEnded={() => setIsPlaying(false)}
              onLoadedMetadata={(e) => setDuration(e.currentTarget.duration)}
              onTimeUpdate={(e) => setCurrentTime(e.currentTarget.currentTime)}
            />

            <div className="flex items-center gap-3">
              <Button
                onClick={toggle}
                variant="outline"
                className="size-10 shrink-0 rounded-full p-0"
                aria-label={isPlaying ? "Pause" : "Play"}
              >
                {isPlaying ? (
                  <Pause className="size-4" />
                ) : (
                  <Play className="size-4 translate-x-px" />
                )}
              </Button>
              <span className="w-10 text-right text-xs tabular-nums text-muted-foreground">
                {formatTime(currentTime)}
              </span>
              <input
                type="range"
                min={0}
                max={duration || 0}
                step={0.25}
                value={Math.min(currentTime, duration || 0)}
                onChange={(e) => seek(Number(e.target.value))}
                className="h-1.5 flex-1 cursor-pointer appearance-none rounded-full bg-muted accent-primary"
                aria-label="Seek"
              />
              <span className="w-10 text-xs tabular-nums text-muted-foreground">
                {formatTime(duration || episode.duration_minutes * 60)}
              </span>
              <div className="flex items-center gap-1">
                {SPEEDS.map((s) => (
                  <button
                    key={s}
                    onClick={() => changeSpeed(s)}
                    className={cn(
                      "rounded-md px-1.5 py-1 text-xs font-medium transition-colors cursor-pointer",
                      speed === s
                        ? "bg-primary text-primary-foreground"
                        : "text-muted-foreground hover:bg-muted"
                    )}
                  >
                    {s}x
                  </button>
                ))}
              </div>
            </div>
          </>
        ) : (
          <div className="flex flex-wrap items-center gap-3 rounded-lg border border-dashed p-4">
            <AlertCircle className="size-5 shrink-0 text-muted-foreground" />
            <div className="min-w-0 flex-1">
              <p className="text-sm font-medium">Script ready, audio pending</p>
              <p className="text-xs text-muted-foreground">{statusText[episode.audio_status]}</p>
            </div>
            {episode.lines.length > 0 && (
              <Button
                onClick={retryAudio}
                disabled={regenerating}
                variant="outline"
                size="sm"
                className="gap-2"
              >
                <RefreshCw
                  className={cn("size-4", regenerating && "animate-spin")}
                />
                {regenerating ? "Synthesizing..." : "Retry audio"}
              </Button>
            )}
          </div>
        )}

        <div className="mt-4 flex items-center gap-2 border-t pt-4">
          <Button
            onClick={() => setShowTranscript((v) => !v)}
            variant="ghost"
            size="sm"
            className="gap-2"
          >
            <List className="size-4" />
            {showTranscript ? "Hide transcript" : "Show transcript"}
          </Button>
          <span className="ml-auto flex items-center gap-1 text-xs text-muted-foreground">
            <Mic className="size-3" /> Gemini TTS
            {episode.provider !== "gemini" && ` • script via ${episode.provider}`}
          </span>
        </div>

        {showTranscript && (
          <div className="mt-3 space-y-2 border-t pt-4">
            {episode.lines.map((line, i) => {
              const isOne = line.speaker === "host_one";
              return (
                <div
                  key={i}
                  className={cn(
                    "flex gap-3 rounded-lg p-3",
                    isOne ? "bg-muted/50" : "bg-primary/5"
                  )}
                >
                  <span
                    className={cn(
                      "mt-0.5 h-6 w-6 shrink-0 rounded-full text-center text-xs leading-6 font-medium",
                      isOne
                        ? "bg-primary/10 text-primary"
                        : "bg-secondary text-secondary-foreground"
                    )}
                  >
                    {isOne ? "1" : "2"}
                  </span>
                  <p className="text-sm leading-relaxed">{line.text}</p>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}