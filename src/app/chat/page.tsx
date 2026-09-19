"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { useStudy } from "@/lib/context";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Textarea } from "@/components/ui/textarea";
import { ModelSelect } from "@/components/model-select";
import {
  LanguageToggle,
  type StudyLanguage,
} from "@/components/language-toggle";
import {
  clearChat,
  getChatMessages,
  sendChatMessage,
  type ChatMessage,
} from "@/lib/api";
import {
  FileText,
  Loader2,
  MessageCircle,
  PlaySquare,
  Send,
  Trash2,
  Type,
  User,
} from "lucide-react";

const SUGGESTIONS = [
  "Summarize the main points of this material.",
  "What are the most important concepts?",
  "List the key definitions and terms.",
];

const SUGGESTIONS_ML = [
  "ഈ മെറ്റീരിയലിലെ പ്രധാന പോയിന്റുകൾ സംഗ്രഹിക്കുക.",
  "ഏതൊക്കെയാണ് ഏറ്റവും പ്രധാനപ്പെട്ട ആശയങ്ങൾ?",
  "പ്രധാന നിർവചനങ്ങളും പദങ്ങളും പട്ടികപ്പെടുത്തുക.",
];

export default function Chat() {
  const router = useRouter();
  const { material, model } = useStudy();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [input, setInput] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [language, setLanguage] = useState<StudyLanguage>("en");
  const endRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (!material) {
      router.replace("/add");
      return;
    }
    let cancelled = false;
    getChatMessages(material.id)
      .then((existing) => {
        if (!cancelled) setMessages(existing);
      })
      .catch((err) => {
        if (!cancelled) {
          toast.error(
            err instanceof Error ? err.message : "Failed to load the chat."
          );
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [material, router]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, sending]);

  const canSend = !sending && input.trim().length > 0;

  async function handleSend() {
    if (!material || !canSend) return;
    const content = input.trim();
    setInput("");
    setError(null);
    setSending(true);

    const optimistic: ChatMessage = {
      id: -Date.now(),
      material_id: material.id,
      role: "user",
      content,
      generated_by: "",
      language,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimistic]);

    try {
      const reply = await sendChatMessage(
        material.id,
        content,
        model.provider,
        model.name,
        language
      );
      if (reply.assistant_message.generated_by === "mock") {
        toast.info(
          reply.warning ??
            `Showing sample answers — AI chat via ${model.provider} failed. Check the backend .env.`
        );
      } else if (reply.assistant_message.generated_by === "quick") {
        toast.info("Quick Mode: answers drawn deterministically, no AI call.");
      }
      setMessages((prev) => [
        ...prev.filter((m) => m.id !== optimistic.id),
        reply.user_message,
        reply.assistant_message,
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
      setMessages((prev) => prev.filter((m) => m.id !== optimistic.id));
      setInput((prev) => prev || content);
    } finally {
      setSending(false);
      textareaRef.current?.focus();
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) {
      e.preventDefault();
      void handleSend();
    }
  }

  async function handleClear() {
    if (!material || messages.length === 0) return;
    try {
      await clearChat(material.id);
      setMessages([]);
      setError(null);
      toast.success("Chat cleared.");
    } catch (err) {
      toast.error(
        err instanceof Error ? err.message : "Failed to clear the chat."
      );
    }
  }

  function suggest(prompt: string) {
    setInput(prompt);
    textareaRef.current?.focus();
  }

  if (!material) {
    return (
      <div className="flex flex-col items-center justify-center py-24">
        <Loader2 className="mb-4 size-6 animate-spin text-muted-foreground" />
        <p className="text-muted-foreground">Redirecting...</p>
      </div>
    );
  }

  return (
    <div className="mx-auto flex h-[calc(100dvh-3.5rem)] max-w-3xl flex-col px-4 py-6">
      <div className="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold">Ask Your Material</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Chat about your upload — the assistant stays grounded in it.
          </p>
        </div>
        <div className="flex flex-wrap items-end gap-2">
          <ModelSelect className="w-56" />
          <LanguageToggle value={language} onChange={setLanguage} />
          {messages.length > 0 && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleClear}
              className="h-9 gap-1.5"
            >
              <Trash2 className="size-3.5" />
              Clear
            </Button>
          )}
        </div>
      </div>

      <Card size="sm" className="mb-4 shrink-0">
        <CardContent className="flex items-center gap-3 pt-3">
          <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-muted">
            {material.source_type === "youtube" ? (
              <PlaySquare className="size-4 text-muted-foreground" />
            ) : material.source_type === "pdf" ? (
              <FileText className="size-4 text-muted-foreground" />
            ) : (
              <Type className="size-4 text-muted-foreground" />
            )}
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium">{material.title}</p>
            <p className="text-xs text-muted-foreground">
              {material.word_count.toLocaleString()} words &middot;{" "}
              {material.char_count.toLocaleString()} chars
            </p>
          </div>
          <Badge variant="secondary" className="shrink-0 text-xs">
            {material.source_type.toUpperCase()}
          </Badge>
        </CardContent>
      </Card>

      <div className="flex min-h-0 flex-1 flex-col overflow-hidden rounded-xl border bg-card ring-1 ring-foreground/10">
        <div
          role="log"
          aria-live="polite"
          aria-busy={sending}
          className="flex-1 space-y-4 overflow-y-auto p-4"
        >
          {loading ? (
            <div className="flex h-full flex-col items-center justify-center gap-2 py-16">
              <Loader2 className="size-6 animate-spin text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                Loading conversation...
              </p>
            </div>
          ) : error ? (
            <div className="rounded-lg border border-destructive/30 bg-destructive/5 px-3 py-2.5 text-sm text-destructive">
              {error}
            </div>
          ) : messages.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center gap-4 py-16 text-center">
              <div className="flex size-12 items-center justify-center rounded-full bg-muted">
                <MessageCircle className="size-6 text-muted-foreground" />
              </div>
              <div className="max-w-sm">
                <p className="font-medium">Ask anything about this material</p>
                <p className="mt-1 text-sm text-muted-foreground">
                  The assistant answers using only the uploaded material — when
                  the answer isn&apos;t there, it says so.
                </p>
              </div>
              <div className="flex flex-wrap justify-center gap-2 pt-1">
                {(language === "ml" ? SUGGESTIONS_ML : SUGGESTIONS).map((s) => (
                  <Button
                    key={s}
                    variant="outline"
                    size="sm"
                    onClick={() => suggest(s)}
                  >
                    {s}
                  </Button>
                ))}
              </div>
            </div>
          ) : (
            messages.map((m) => (
              <div
                key={m.id}
                className={`flex w-full ${
                  m.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div className="flex max-w-[85%] flex-col">
                  <div
                    className={`flex gap-2 whitespace-pre-wrap rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${
                      m.role === "user"
                        ? "rounded-br-md bg-primary text-primary-foreground"
                        : "rounded-bl-md bg-muted"
                    }`}
                  >
                    {m.role === "assistant" && (
                      <MessageCircle className="mt-0.5 size-4 shrink-0 text-muted-foreground" />
                    )}
                    <span>{m.content}</span>
                  </div>
                  {m.role === "user" && (
                    <p className="mt-1 flex items-center justify-end gap-1 pr-1 text-[10px] text-muted-foreground">
                      <User className="size-3" />
                      You
                    </p>
                  )}
                  {m.role === "assistant" &&
                    (m.language === "ml" ||
                      m.generated_by === "quick" ||
                      m.generated_by === "mock") && (
                      <p className="mt-1 pl-1 text-[10px] text-muted-foreground">
                        {m.generated_by === "quick"
                          ? "Quick Mode — deterministic reply, no AI call"
                          : m.generated_by === "mock"
                            ? "Sample reply — AI generation failed for the selected model"
                            : "മലയാളം"}
                      </p>
                    )}
                </div>
              </div>
            ))
          )}

          {sending && (
            <div className="flex w-full justify-start">
              <div className="flex items-center gap-2 rounded-2xl rounded-bl-md bg-muted px-3.5 py-2.5 text-sm text-muted-foreground">
                <Loader2 className="size-4 animate-spin" />
                Thinking...
              </div>
            </div>
          )}

          <div ref={endRef} className="h-px" />
        </div>

        <div className="border-t p-3">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void handleSend();
            }}
            className="flex items-end gap-2"
          >
            <Textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Ask about "${material.title}"...`}
              aria-label="Write a question about your material"
              rows={1}
              disabled={sending}
              className="max-h-40 flex-1"
            />
            <Button
              type="submit"
              size="icon"
              disabled={!canSend}
              aria-label="Send message"
            >
              {sending ? (
                <Loader2 className="size-4 animate-spin" />
              ) : (
                <Send className="size-4" />
              )}
            </Button>
          </form>
          <p className="mt-2 text-center text-[10px] text-muted-foreground">
            Enter to send &middot; Shift+Enter for a new line
          </p>
        </div>
      </div>
    </div>
  );
}