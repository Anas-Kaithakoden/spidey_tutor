"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { PodcastPlayer } from "@/components/podcast-player";
import {
  AudioLines,
  Clock,
  Loader2,
  Plus,
  RefreshCw,
  Trash2,
} from "lucide-react";
import { cn } from "cn";
import {
  deletePodcast,
  getPodcast,
  listPodcasts,
  type PodcastEpisode,
  type PodcastMode,
} from "@/lib/api";

const MODE_SHORT: Record<PodcastMode, string> = {
  learn: "Learn",
  revise: "Revise",
  exam_prep: "Exam Prep",
  weak_topics: "Weak Topics",
};

function readEpisodeId(): number | null {
  if (typeof window === "undefined") return null;
  const id = Number(
    new URLSearchParams(window.location.search).get("id")
  );
  return Number.isFinite(id) && id > 0 ? id : null;
}

export default function PodcastPage() {
  const [episodes, setEpisodes] = useState<PodcastEpisode[]>([]);
  const [active, setActive] = useState<PodcastEpisode | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const requestedId = readEpisodeId();

  useEffect(() => {
    let cancelled = false;
    listPodcasts()
      .then((list) => {
        if (cancelled) return;
        setEpisodes(list);
        if (list.length === 0) {
          setActive(null);
          setLoading(false);
          return;
        }
        if (requestedId !== null) {
          const match = list.find((e) => e.id === requestedId);
          if (match) {
            setActive(match);
            setLoading(false);
            return;
          }
          getPodcast(requestedId)
            .then((ep) => {
              if (!cancelled) {
                setEpisodes((prev) =>
                  prev.some((e) => e.id === ep.id) ? prev : [ep, ...prev]
                );
                setActive(ep);
              }
            })
            .catch(() => {
              if (!cancelled) {
                toast.error("Could not load the requested episode.");
                setActive(list[0] ?? null);
              }
            })
            .finally(() => {
              if (!cancelled) setLoading(false);
            });
          return;
        }
        setActive(list[0] ?? null);
        setLoading(false);
      })
      .catch(() => {
        if (!cancelled) {
          toast.error("Failed to load podcast episodes.");
          setLoading(false);
        }
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleUpdated(updated: PodcastEpisode) {
    setEpisodes((prev) =>
      prev.map((e) => (e.id === updated.id ? updated : e))
    );
    setActive(updated);
  }

  async function handleDelete() {
    if (!active) return;
    if (!window.confirm(`Delete "${active.title}"?`)) return;
    setDeleting(true);
    try {
      await deletePodcast(active.id);
      toast.success("Podcast deleted.");
      const next = episodes.filter((e) => e.id !== active.id);
      setEpisodes(next);
      setActive(next[0] ?? null);
    } catch (err) {
      toast.error(
        err instanceof Error ? err.message : "Failed to delete podcast."
      );
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-12">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">Study Podcasts</h1>
          <p className="mt-1 text-muted-foreground">
            Two-host conversational episodes generated from your study material.
          </p>
        </div>
        <Button render={<Link href="/podcast/setup" />} className="gap-2">
          <Plus className="size-4" />
          New Podcast
        </Button>
      </div>

      {loading ? (
        <div className="flex items-center gap-2 text-muted-foreground">
          <Loader2 className="size-4 animate-spin" />
          Loading episodes...
        </div>
      ) : episodes.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-3 py-14 text-center">
            <AudioLines className="size-8 text-muted-foreground" />
            <p className="font-medium">No podcasts yet</p>
            <p className="max-w-sm text-sm text-muted-foreground">
              Generate a two-host audio episode from any of your study
              materials, in Learn, Revise, Exam Prep, or Weak Topics mode.
            </p>
            <Button render={<Link href="/podcast/setup" />} className="gap-2 mt-1">
              <Plus className="size-4" />
              Generate your first podcast
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-[260px_1fr]">
          <aside className="space-y-2">
            {episodes.map((ep) => (
              <button
                key={ep.id}
                onClick={() => setActive(ep)}
                className={cn(
                  "w-full rounded-xl border-2 p-3 text-left transition-colors cursor-pointer",
                  active?.id === ep.id
                    ? "border-primary bg-primary/5"
                    : "border-transparent bg-muted/50 hover:bg-muted"
                )}
              >
                <span className="block truncate text-sm font-medium">
                  {ep.title}
                </span>
                <span className="mt-1 flex flex-wrap items-center gap-1.5 text-xs text-muted-foreground">
                  <Badge variant="secondary">{MODE_SHORT[ep.mode]}</Badge>
                  <Badge variant="outline" className="gap-1">
                    <Clock className="size-3" /> {ep.duration_minutes} min
                  </Badge>
                  {ep.audio_status !== "ready" && (
                    <Badge variant="destructive">no audio</Badge>
                  )}
                </span>
              </button>
            ))}
          </aside>

          <div className="min-w-0 space-y-4">
            {active && (
              <>
                <PodcastPlayer key={active.id} episode={active} onUpdated={handleUpdated} />
                <div className="flex justify-end gap-2">
                  <Button
                    onClick={handleDelete}
                    disabled={deleting}
                    variant="ghost"
                    size="sm"
                    className="gap-2 text-destructive hover:text-destructive"
                  >
                    {deleting ? (
                      <RefreshCw className="size-4 animate-spin" />
                    ) : (
                      <Trash2 className="size-4" />
                    )}
                    Delete episode
                  </Button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}