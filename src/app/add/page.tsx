"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import {
  Upload,
  FileText,
  ArrowRight,
  Loader2,
  Image as ImageIcon,
  FileSpreadsheet,
  Video,
} from "lucide-react";
import { useStudy } from "@/lib/context";
import {
  createMaterial,
  createYoutubeMaterial,
  uploadPdf,
  uploadImage,
  uploadOffice,
} from "@/lib/api";

function isYoutubeUrl(value: string): boolean {
  return /^(https?:\/\/)?(www\.|m\.|music\.)?(youtube\.com|youtu\.be)\//i.test(
    value.trim()
  );
}

export default function AddMaterial() {
  const router = useRouter();
  const { setMaterial } = useStudy();
  const [tab, setTab] = useState<
    "text" | "pdf" | "image" | "office" | "youtube"
  >("text");
  const [text, setText] = useState("");
  const [title, setTitle] = useState("");
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [officeFile, setOfficeFile] = useState<File | null>(null);
  const [ytUrl, setYtUrl] = useState("");
  const [ytTitle, setYtTitle] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const officeInputRef = useRef<HTMLInputElement>(null);

  async function handleContinue() {
    setSubmitting(true);
    try {
      if (tab === "text") {
        const material = await createMaterial(text.trim(), title.trim());
        setMaterial(material);
      } else if (tab === "pdf" && pdfFile) {
        const material = await uploadPdf(pdfFile);
        setMaterial(material);
      } else if (tab === "image" && imageFile) {
        const material = await uploadImage(imageFile);
        setMaterial(material);
      } else if (tab === "office" && officeFile) {
        const material = await uploadOffice(officeFile);
        setMaterial(material);
      } else if (tab === "youtube") {
        const material = await createYoutubeMaterial(
          ytUrl.trim(),
          ytTitle.trim() || undefined
        );
        setMaterial(material);
      }
      router.push("/preview");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setSubmitting(false);
    }
  }

  const ytUrlEmpty = ytUrl.trim().length === 0;
  const ytUrlInvalid = !ytUrlEmpty && !isYoutubeUrl(ytUrl);
  const canContinue = submitting
    ? false
    : (tab === "text" && text.trim().length > 0) ||
      (tab === "pdf" && pdfFile !== null) ||
      (tab === "image" && imageFile !== null) ||
      (tab === "office" && officeFile !== null) ||
      (tab === "youtube" && !ytUrlEmpty && !ytUrlInvalid);

  return (
    <div className="mx-auto max-w-2xl px-4 py-12">
      <h1 className="mb-2 text-2xl font-bold">Add Study Material</h1>
      <p className="mb-8 text-muted-foreground">
        Paste text, upload a PDF, image, or office doc, or add a YouTube video.
      </p>

      <div className="mb-6 grid grid-cols-2 gap-2 rounded-lg border p-1 sm:grid-cols-3 lg:grid-cols-5">
        <button
          onClick={() => setTab("text")}
          disabled={submitting}
          className={`flex items-center justify-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium transition-colors cursor-pointer disabled:opacity-50 ${
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
          className={`flex items-center justify-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium transition-colors cursor-pointer disabled:opacity-50 ${
            tab === "pdf"
              ? "bg-primary text-primary-foreground"
              : "text-muted-foreground hover:bg-muted"
          }`}
        >
          <Upload className="size-4" />
          PDF
        </button>
        <button
          onClick={() => setTab("image")}
          disabled={submitting}
          className={`flex items-center justify-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium transition-colors cursor-pointer disabled:opacity-50 ${
            tab === "image"
              ? "bg-primary text-primary-foreground"
              : "text-muted-foreground hover:bg-muted"
          }`}
        >
          <ImageIcon className="size-4" />
          Image
        </button>
        <button
          onClick={() => setTab("office")}
          disabled={submitting}
          className={`flex items-center justify-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium transition-colors cursor-pointer disabled:opacity-50 ${
            tab === "office"
              ? "bg-primary text-primary-foreground"
              : "text-muted-foreground hover:bg-muted"
          }`}
        >
          <FileSpreadsheet className="size-4" />
          Office
        </button>
        <button
          onClick={() => setTab("youtube")}
          disabled={submitting}
          className={`flex items-center justify-center gap-2 rounded-md px-3 py-2.5 text-sm font-medium transition-colors cursor-pointer disabled:opacity-50 ${
            tab === "youtube"
              ? "bg-primary text-primary-foreground"
              : "text-muted-foreground hover:bg-muted"
          }`}
        >
          <Video className="size-4" />
          YouTube
        </button>
      </div>

      <Card>
        <CardContent className="pt-6">
          {tab === "text" ? (
            <div key="text" className="space-y-3">
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
          ) : tab === "pdf" ? (
            <div key="pdf" className="space-y-4">
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
                      <p className="text-sm text-muted-foreground">PDF files only</p>
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
          ) : tab === "image" ? (
            <div key="image" className="space-y-4">
              <div
                onClick={() => imageInputRef.current?.click()}
                className="flex cursor-pointer flex-col items-center gap-3 rounded-lg border-2 border-dashed p-12 text-center transition-colors hover:border-primary/50 hover:bg-muted/50"
              >
                {imageFile ? (
                  <>
                    <ImageIcon className="size-10 text-primary" />
                    <div>
                      <p className="font-medium">{imageFile.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {(imageFile.size / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  </>
                ) : (
                  <>
                    <ImageIcon className="size-10 text-muted-foreground" />
                    <div>
                      <p className="font-medium">Click to upload an image</p>
                      <p className="text-sm text-muted-foreground">png, jpg, jpeg, webp, bmp — OCR via Gemini</p>
                    </div>
                  </>
                )}
              </div>
              <Input
                ref={imageInputRef}
                type="file"
                accept=".png,.jpg,.jpeg,.webp,.bmp"
                className="hidden"
                onChange={(e) => setImageFile(e.target.files?.[0] ?? null)}
              />
            </div>
          ) : tab === "office" ? (
            <div key="office" className="space-y-4">
              <div
                onClick={() => officeInputRef.current?.click()}
                className="flex cursor-pointer flex-col items-center gap-3 rounded-lg border-2 border-dashed p-12 text-center transition-colors hover:border-primary/50 hover:bg-muted/50"
              >
                {officeFile ? (
                  <>
                    <FileSpreadsheet className="size-10 text-primary" />
                    <div>
                      <p className="font-medium">{officeFile.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {(officeFile.size / 1024).toFixed(1)} KB
                      </p>
                    </div>
                  </>
                ) : (
                  <>
                    <FileSpreadsheet className="size-10 text-muted-foreground" />
                    <div>
                      <p className="font-medium">Click to upload office document</p>
                      <p className="text-sm text-muted-foreground">docx, pptx, xlsx, txt, csv — text extracted</p>
                    </div>
                  </>
                )}
              </div>
              <Input
                ref={officeInputRef}
                type="file"
                accept=".docx,.pptx,.xlsx,.xls,.txt,.md,.csv"
                className="hidden"
                onChange={(e) => setOfficeFile(e.target.files?.[0] ?? null)}
              />
            </div>
          ) : (
            <div key="youtube" className="space-y-3">
              <Label htmlFor="yt-url">YouTube video URL</Label>
              <Input
                id="yt-url"
                type="url"
                placeholder="https://www.youtube.com/watch?v=..."
                value={ytUrl}
                onChange={(e) => setYtUrl(e.target.value)}
              />
              {ytUrlInvalid && (
                <p className="text-xs text-destructive">
                  That doesn&apos;t look like a YouTube video URL. Use a
                  youtube.com or youtu.be link.
                </p>
              )}
              {!ytUrlInvalid && ytUrl.trim().length > 0 && (
                <p className="text-xs text-muted-foreground">
                  We&apos;ll fetch the video&apos;s captions and turn them into
                  study material.
                </p>
              )}
              <Label htmlFor="yt-title">
                Title{" "}
                <span className="text-muted-foreground">
                  (optional — defaults to the video title)
                </span>
              </Label>
              <Input
                id="yt-title"
                placeholder="e.g. Operating Systems - Lecture 3"
                value={ytTitle}
                onChange={(e) => setYtTitle(e.target.value)}
              />
              <p className="text-xs text-muted-foreground">
                Only videos with captions or an auto-generated transcript can be
                processed. If a video has no transcript, we&apos;ll let you know
                instead of making one up.
              </p>
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