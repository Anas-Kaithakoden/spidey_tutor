"use client";

import { useState, useRef, DragEvent, ChangeEvent } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { SpideyMascot } from "@/components/spidey-mascot";
import { StagedGeneration } from "@/components/staged-generation";
import {
  Upload,
  FileText,
  ArrowRight,
  Sparkles,
  Video,
  File,
  X,
  Image as ImageIcon,
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

  // Mode: "drop" | "text" | "youtube"
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [fileCategory, setFileCategory] = useState<"pdf" | "image" | "office" | "text" | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  // Paste form state
  const [textNotes, setTextNotes] = useState("");
  const [sessionTitle, setSessionTitle] = useState("");

  // YouTube state
  const [showYoutube, setShowYoutube] = useState(false);
  const [ytUrl, setYtUrl] = useState("");

  const [submitting, setSubmitting] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Classify file by extension/MIME
  function handleFileSelected(file: File) {
    const ext = file.name.split(".").pop()?.toLowerCase() || "";
    const type = file.type.toLowerCase();

    if (ext === "pdf" || type === "application/pdf") {
      setFileCategory("pdf");
    } else if (["png", "jpg", "jpeg", "webp"].includes(ext) || type.startsWith("image/")) {
      setFileCategory("image");
    } else if (["docx", "pptx", "xlsx", "doc", "ppt"].includes(ext)) {
      setFileCategory("office");
    } else {
      // Default to text or generic office
      setFileCategory("text");
    }

    setSelectedFile(file);
    // If title is empty, prefill with file name (without extension)
    if (!sessionTitle.trim()) {
      const baseName = file.name.replace(/\.[^/.]+$/, "");
      setSessionTitle(baseName);
    }
  }

  function handleFileInputChange(e: ChangeEvent<HTMLInputElement>) {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFileSelected(files[0]);
    }
  }

  function handleDragOver(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(true);
  }

  function handleDragLeave(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
  }

  function handleDrop(e: DragEvent<HTMLDivElement>) {
    e.preventDefault();
    setIsDragging(false);
    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFileSelected(files[0]);
    }
  }

  function clearSelectedFile() {
    setSelectedFile(null);
    setFileCategory(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  }

  async function handleContinue() {
    setSubmitting(true);
    try {
      let material;

      if (selectedFile) {
        if (fileCategory === "pdf") {
          material = await uploadPdf(selectedFile);
        } else if (fileCategory === "image") {
          material = await uploadImage(selectedFile);
        } else if (fileCategory === "office") {
          material = await uploadOffice(selectedFile);
        } else {
          // Read text file
          const textContent = await selectedFile.text();
          material = await createMaterial(textContent, sessionTitle.trim() || selectedFile.name);
        }
      } else if (showYoutube && ytUrl.trim()) {
        material = await createYoutubeMaterial(ytUrl.trim(), sessionTitle.trim() || undefined);
      } else if (textNotes.trim()) {
        material = await createMaterial(textNotes.trim(), sessionTitle.trim());
      } else {
        toast.error("Please drop a file or paste your notes to continue.");
        setSubmitting(false);
        return;
      }

      setMaterial(material);
      toast.success("Study material processed successfully!");
      router.push("/preview");
    } catch (err) {
      toast.error(err instanceof Error ? err.message : "Failed to process material.");
    } finally {
      setSubmitting(false);
    }
  }

  const ytValid = ytUrl.trim().length > 0 && isYoutubeUrl(ytUrl);
  const canSubmit = !submitting && (
    selectedFile !== null ||
    textNotes.trim().length > 0 ||
    (showYoutube && ytValid)
  );

  if (submitting) {
    return (
      <div className="mx-auto max-w-3xl px-4 py-24">
        <StagedGeneration
          title="Spidey is weaving your material..."
          stages={[
            "Reading uploaded content",
            "Parsing key concepts & terms",
            "Synthesizing knowledge structure",
            "Preparing your study hub",
          ]}
        />
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:py-16">
      {/* Header */}
      <div className="text-center mb-10">
        <div className="inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/10 px-3 py-0.5 text-xs font-semibold text-primary mb-3 shadow-xs">
          <Sparkles className="size-3.5" />
          <span>New Study Session</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-foreground mb-3">
          Add your study material
        </h1>
        <p className="text-base text-muted-foreground max-w-lg mx-auto leading-relaxed">
          Drop lecture slides, notes, or readings. Spidey turns them into interactive quizzes and 3D flashcards.
        </p>
      </div>

      <div className="space-y-8">
        {/* Hidden Global File Input */}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.pptx,.xlsx,.txt,.png,.jpg,.jpeg"
          onChange={handleFileInputChange}
          className="hidden"
          aria-label="Upload study material file"
        />

        {/* 1. Magnetic Drop Arena */}
        {!selectedFile ? (
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`relative group cursor-pointer flex flex-col items-center justify-center p-8 sm:p-14 rounded-3xl border-2 border-dashed transition-all duration-200 text-center ${
              isDragging
                ? "border-primary bg-primary/10 scale-[1.01] shadow-xl shadow-primary/15 ring-4 ring-primary/20"
                : "border-border/80 bg-card/60 hover:border-primary/50 hover:bg-card/90 shadow-xs"
            }`}
          >
            {/* Mascot in Drop Zone */}
            <div className="mb-4 transition-transform group-hover:scale-110 duration-200">
              <SpideyMascot mood={isDragging ? "cheering" : "idle"} size={64} interactive={false} />
            </div>

            <h2 className="text-xl font-bold tracking-tight text-foreground mb-1.5">
              {isDragging ? "Release to drop your material!" : "Drop your study material here"}
            </h2>
            <p className="text-sm text-muted-foreground mb-6 max-w-sm">
              Supports <strong className="text-foreground">PDF</strong>, <strong className="text-foreground">DOCX</strong>, <strong className="text-foreground">PPTX</strong>, <strong className="text-foreground">TXT</strong>, and lecture images
            </p>

            <Button
              type="button"
              variant="outline"
              size="sm"
              className="rounded-xl border-primary/30 text-primary hover:bg-primary/10 pointer-events-none"
            >
              <Upload className="size-4 mr-2" />
              <span>Browse files on device</span>
            </Button>
          </div>
        ) : (
          /* File Selected Card */
          <div className="flex items-center justify-between p-4 sm:p-5 rounded-2xl border border-primary/40 bg-primary/10 shadow-xs backdrop-blur-xs">
            <div className="flex items-center gap-3.5 min-w-0">
              <div className="flex size-11 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground shadow-xs">
                {fileCategory === "pdf" ? (
                  <FileText className="size-5" />
                ) : fileCategory === "image" ? (
                  <ImageIcon className="size-5" />
                ) : (
                  <File className="size-5" />
                )}
              </div>
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-foreground truncate">{selectedFile.name}</span>
                  <span className="shrink-0 text-[10px] font-bold uppercase tracking-wider bg-primary/20 text-primary px-2 py-0.5 rounded-md">
                    {fileCategory}
                  </span>
                </div>
                <span className="text-xs text-muted-foreground">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB · Ready to weave
                </span>
              </div>
            </div>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              onClick={clearSelectedFile}
              className="size-8 rounded-lg hover:bg-destructive/15 hover:text-destructive"
              aria-label="Remove file"
            >
              <X className="size-4" />
            </Button>
          </div>
        )}

        {/* Divider */}
        <div className="relative flex items-center justify-center">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-border/80" />
          </div>
          <span className="relative bg-background px-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            or paste your notes directly
          </span>
        </div>

        {/* 2. Direct Note Pasting Surface */}
        <div className="rounded-2xl border border-border/80 bg-card/60 p-5 sm:p-6 shadow-xs backdrop-blur-xs space-y-4">
          <div className="space-y-1.5">
            <Label htmlFor="session-title" className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
              Session Title (Optional)
            </Label>
            <Input
              id="session-title"
              placeholder="e.g., Chapter 4: Photosynthesis & Cellular Respiration"
              value={sessionTitle}
              onChange={(e) => setSessionTitle(e.target.value)}
              className="rounded-xl bg-background/80"
            />
          </div>

          <div className="space-y-1.5">
            <Label htmlFor="session-notes" className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
              Lecture Notes / Summary Text
            </Label>
            <Textarea
              id="session-notes"
              placeholder="Paste raw lecture text, key definitions, or textbook notes here..."
              value={textNotes}
              onChange={(e) => {
                setTextNotes(e.target.value);
                if (selectedFile) clearSelectedFile();
              }}
              rows={5}
              className="rounded-xl bg-background/80 font-normal leading-relaxed resize-y"
            />
          </div>

          {/* 3. YouTube Expander Pill */}
          <div className="pt-2 border-t border-border/50">
            {!showYoutube ? (
              <button
                type="button"
                onClick={() => setShowYoutube(true)}
                className="inline-flex items-center gap-2 text-xs font-medium text-muted-foreground hover:text-foreground transition-colors cursor-pointer"
              >
                <Video className="size-4 text-red-500" />
                <span>Studying from a YouTube lecture? Click here to add video link</span>
              </button>
            ) : (
              <div className="space-y-3 pt-1">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground flex items-center gap-1.5">
                    <Video className="size-4 text-red-500" />
                    YouTube Lecture Video
                  </span>
                  <button
                    type="button"
                    onClick={() => {
                      setShowYoutube(false);
                      setYtUrl("");
                    }}
                    className="text-xs text-muted-foreground hover:text-foreground"
                  >
                    Cancel
                  </button>
                </div>
                <Input
                  placeholder="https://www.youtube.com/watch?v=..."
                  value={ytUrl}
                  onChange={(e) => setYtUrl(e.target.value)}
                  className="rounded-xl bg-background/80"
                />
              </div>
            )}
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-2">
          <Button
            type="button"
            onClick={handleContinue}
            disabled={!canSubmit}
            size="lg"
            className="w-full h-13 rounded-2xl text-base font-semibold shadow-md shadow-primary/20 hover:shadow-primary/30 transition-all hover:scale-[1.01] active:scale-[0.99] disabled:opacity-50"
          >
            <span>Turn into Study Hub</span>
            <ArrowRight className="size-4.5 ml-2" />
          </Button>
        </div>
      </div>
    </div>
  );
}