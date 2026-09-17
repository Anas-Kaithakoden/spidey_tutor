"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { Upload, FileText, ArrowRight, Loader2 } from "lucide-react";
import { useStudy } from "@/lib/context";
import { createMaterial, uploadPdf } from "@/lib/api";

export default function AddMaterial() {
  const router = useRouter();
  const { setMaterial } = useStudy();
  const [tab, setTab] = useState<"pdf" | "text">("text");
  const [text, setText] = useState("");
  const [title, setTitle] = useState("");
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  async function handleContinue() {
    setSubmitting(true);
    try {
      if (tab === "text") {
        const material = await createMaterial(text.trim(), title.trim());
        setMaterial(material);
      } else if (tab === "pdf" && pdfFile) {
        const material = await uploadPdf(pdfFile);
        setMaterial(material);
      }
      router.push("/preview");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  const canContinue = submitting
    ? false
    : (tab === "text" && text.trim().length > 0) ||
      (tab === "pdf" && pdfFile !== null);

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Add Study Material</h1>
      <p className="mb-8 text-muted-foreground">
        Upload a PDF or paste text from your notes.
      </p>

      <div className="mb-6 grid grid-cols-2 gap-2 rounded-lg border p-1">
        <button
          onClick={() => setTab("text")}
          disabled={submitting}
          className={`flex items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-medium transition-colors cursor-pointer disabled:opacity-50 ${
            tab === "text"
              ? "bg-primary text-primary-foreground"
              : "text-muted-foreground hover:bg-muted"
          }`}
        >
          <FileText className="size-4" />
          Paste Text
        </button>
        <button
          onClick={() => setTab("pdf")}
          disabled={submitting}
          className={`flex items-center justify-center gap-2 rounded-md px-4 py-2.5 text-sm font-medium transition-colors cursor-pointer disabled:opacity-50 ${
            tab === "pdf"
              ? "bg-primary text-primary-foreground"
              : "text-muted-foreground hover:bg-muted"
          }`}
        >
          <Upload className="size-4" />
          Upload PDF
        </button>
      </div>

      <Card>
        <CardContent className="pt-6">
          {tab === "text" ? (
            <div className="space-y-3">
              <Label htmlFor="material-title">
                Title <span className="text-muted-foreground">(optional)</span>
              </Label>
              <Input
                id="material-title"
                placeholder="e.g. Operating Systems - Chapter 1"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
              <Label htmlFor="study-text">Paste your study material</Label>
              <Textarea
                id="study-text"
                placeholder="Paste your lecture notes, textbook content, or any study material here..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="min-h-[250px] resize-y"
              />
              {text.length > 0 && (
                <p className="text-xs text-muted-foreground">
                  {text.split(/\s+/).filter(Boolean).length} words &middot;{" "}
                  {text.length} characters
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <div
                onClick={() => fileInputRef.current?.click()}
                className="flex cursor-pointer flex-col items-center gap-3 rounded-lg border-2 border-dashed p-12 text-center transition-colors hover:border-primary/50 hover:bg-muted/50"
              >
                {pdfFile ? (
                  <>
                    <FileText className="size-10 text-primary" />
                    <div>
                      <p className="font-medium">{pdfFile.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {(pdfFile.size / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  </>
                ) : (
                  <>
                    <Upload className="size-10 text-muted-foreground" />
                    <div>
                      <p className="font-medium">Click to upload a PDF</p>
                      <p className="text-sm text-muted-foreground">
                        PDF files only
                      </p>
                    </div>
                  </>
                )}
              </div>
              <Input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                className="hidden"
                onChange={(e) => setPdfFile(e.target.files?.[0] ?? null)}
              />
            </div>
          )}
        </CardContent>
      </Card>

      <div className="mt-6 flex justify-end">
        <Button
          onClick={handleContinue}
          disabled={!canContinue}
          className="gap-2"
        >
          {submitting ? (
            <>
              <Loader2 className="size-4 animate-spin" />
              Processing...
            </>
          ) : (
            <>
              Continue
              <ArrowRight className="size-4" />
            </>
          )}
        </Button>
      </div>
    </div>
  );
}