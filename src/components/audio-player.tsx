"use client";

import { useEffect, useRef, useState } from "react";
import { Volume2, Play, Pause, Mic, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import type { AudioSummaryOut } from "@/lib/api";

interface Props {
  data: AudioSummaryOut | null;
}

export function AudioPlayer({ data, speed = 1 }: Props & { speed?: number }) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  const hasGeminiAudio = !!data?.audio_base64;
  const src = hasGeminiAudio
    ? `data:${data.mime_type};base64,${data.audio_base64}`
    : null;

  useEffect(() => {
    if (audioRef.current) audioRef.current.playbackRate = speed;
  }, [speed, hasGeminiAudio]);

  function toggleGemini() {
    if (!audioRef.current || !src) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.playbackRate = speed;
      audioRef.current.play().then(() => setIsPlaying(true)).catch(console.error);
    }
  }

  function toggleBrowser() {
    if (!data?.summary_text) return;
    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
      return;
    }
    const utter = new SpeechSynthesisUtterance(data.summary_text);
    utter.rate = speed;
    // detect Malayalam vs English for voice
    const isML = /[\u0D00-\u0D7F]/.test(data.summary_text);
    utter.lang = isML ? "ml-IN" : "en-US";
    utter.onend = () => setIsPlaying(false);
    utter.onerror = () => setIsPlaying(false);
    window.speechSynthesis.speak(utter);
    setIsPlaying(true);
  }

  function toggle() {
    if (hasGeminiAudio) toggleGemini();
    else toggleBrowser();
  }

  if (!data) return null;

  return (
    <Card className="mt-6">
      <CardContent className="pt-6">
        <div className="mb-3 flex items-center gap-2">
          <Volume2 className="size-5" />
          <h3 className="font-semibold">1-Min Audio Summary</h3>
          {data.generated_by === "mock" && (
            <span className="ml-auto flex items-center gap-1 text-xs text-muted-foreground">
              <AlertCircle className="size-3" /> mock fallback
            </span>
          )}
          {!hasGeminiAudio && (
            <span className="ml-auto text-xs text-muted-foreground">browser TTS</span>
          )}
        </div>

        <p className="mb-4 whitespace-pre-wrap text-sm leading-relaxed text-muted-foreground">
          {data.summary_text}
        </p>

        <div className="flex items-center gap-3">
          <Button onClick={toggle} variant="outline" className="gap-2">
            {isPlaying ? <Pause className="size-4" /> : <Play className="size-4" />}
            {isPlaying ? "Pause" : hasGeminiAudio ? "Play Gemini Audio" : "Play (Browser)"}
          </Button>
          {hasGeminiAudio && (
            <span className="text-xs text-muted-foreground flex items-center gap-1">
              <Mic className="size-3" /> Gemini TTS • {data.mime_type}
            </span>
          )}
        </div>

        {src && (
          <audio
            ref={audioRef}
            src={src}
            onEnded={() => setIsPlaying(false)}
            onPause={() => setIsPlaying(false)}
            controls
            className="mt-4 w-full"
          />
        )}
      </CardContent>
    </Card>
  );
}
