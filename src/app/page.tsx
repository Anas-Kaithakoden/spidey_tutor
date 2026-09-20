"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { SpideyMascot } from "@/components/spidey-mascot";
import { useStudy } from "@/lib/context";
import { listMaterials, type Material } from "@/lib/api";

export default function StudyDesk() {
  const { material, setMaterial } = useStudy();
  const [materials, setMaterials] = useState<Material[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    listMaterials()
      .then((data) => {
        if (!cancelled) setMaterials(data);
      })
      .catch(() => {
        if (!cancelled) setMaterials([]);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const activeMaterial = material || (materials.length > 0 ? materials[0] : null);

  return (
    <div className="w-full min-h-screen bg-[#15121d] text-[#e7dff0] px-4 sm:px-8 lg:px-12 py-8 overflow-x-hidden">
      <div className="max-w-7xl mx-auto flex flex-col gap-14">

        {/* 1. HERO EDITORIAL DESK ZONE */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative pt-2">
          {/* Ambient Purple Glow */}
          <div className="absolute -right-16 top-1/2 -translate-y-1/2 size-96 rounded-full bg-[#8e7fff]/10 blur-3xl pointer-events-none -z-0" />

          {/* Left Column: Editorial & Intent */}
          <div className="lg:col-span-7 flex flex-col items-start z-10">
            {/* Hand-noted annotation tag */}
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#2c2834]/80 border border-white/5 mb-4 shadow-sm backdrop-blur-md">
              <span className="size-2 rounded-full bg-[#e3c464] animate-pulse" />
              <span className="font-caveat text-[20px] leading-none text-[#e3c464] tracking-wide">
                {material ? `${material.title} · active study desk ~` : "personal study desk · ready ~"}
              </span>
            </div>

            {/* Headline */}
            <h1 className="font-space text-4xl sm:text-5xl lg:text-[56px] lg:leading-[1.1] tracking-tight font-bold text-white mb-4">
              Let’s make this chapter{" "}
              <span className="text-[#8e7fff] underline decoration-[#8e7fff]/40 underline-offset-8">
                stick
              </span>
              .
            </h1>

            {/* Subtitle */}
            <p className="text-base sm:text-lg text-[#c8c4d6] max-w-xl mb-8 leading-relaxed font-normal">
              Drop your lecture slides, notes, or readings. Spidey weaves them into tactile recall quizzes, 3D flashcards, and grounded midnight revision sessions.
            </p>

            {/* CTA Button Group */}
            <div className="flex flex-wrap items-center gap-3 mb-8">
              <Link
                href="/add"
                className="group inline-flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-[#8e7fff] text-white font-space text-sm font-bold shadow-lg shadow-[#8e7fff]/25 hover:bg-[#8e7fff]/90 hover:-translate-y-0.5 active:scale-[0.98] transition-all duration-200"
              >
                <span className="material-symbols-outlined text-[20px] transition-transform group-hover:rotate-12">
                  upload_file
                </span>
                <span>Add Study Material</span>
                <span className="text-white/70 ml-1">→</span>
              </Link>

              {activeMaterial ? (
                <Link
                  href="/flashcards"
                  onClick={() => {
                    if (!material) setMaterial(activeMaterial);
                  }}
                  className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-[#211e2a] hover:bg-[#2c2834] text-white font-space text-sm font-medium transition-all shadow-sm border border-white/5"
                >
                  <span className="material-symbols-outlined text-[18px] text-[#8e7fff]">
                    menu_book
                  </span>
                  <span className="truncate max-w-[240px]">
                    Study: {activeMaterial.title}
                  </span>
                </Link>
              ) : (
                <Link
                  href="/quiz/setup"
                  className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-[#211e2a] hover:bg-[#2c2834] text-[#c8c4d6] hover:text-white font-space text-sm font-medium transition-all shadow-sm border border-white/5"
                >
                  <span className="material-symbols-outlined text-[18px] text-[#8e7fff]">
                    help
                  </span>
                  <span>Explore Practice Modes</span>
                </Link>
              )}
            </div>

            {/* Trust Badges */}
            <div className="flex flex-wrap items-center gap-y-2 gap-x-4 pt-1 text-[#c8c4d6] text-xs">
              <div className="flex items-center gap-1.5">
                <span className="size-2 rounded-full bg-emerald-400" />
                <span>Zero hallucinations</span>
              </div>
              <span className="text-white/20">•</span>
              <div className="flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[15px] text-[#8e7fff]">verified</span>
                <span>Strict textbook citations</span>
              </div>
              <span className="text-white/20">•</span>
              <div className="flex items-center gap-1.5">
                <span className="material-symbols-outlined text-[15px] text-[#e3c464]">lock</span>
                <span>Local encryption</span>
              </div>
            </div>
          </div>

          {/* Right Column: Interactive Constellation & Mascot */}
          <div className="lg:col-span-5 relative w-full h-[380px] flex items-center justify-center select-none">
            {/* SVG Web / Constellation backdrop */}
            <svg
              className="absolute inset-0 w-full h-full pointer-events-none"
              fill="none"
              viewBox="0 0 460 380"
            >
              <circle cx="230" cy="190" r="70" stroke="#8e7fff" strokeDasharray="3 3" strokeOpacity="0.2" />
              <circle cx="230" cy="190" r="140" stroke="#8e7fff" strokeDasharray="4 4" strokeOpacity="0.12" />
              <line stroke="#8e7fff" strokeDasharray="4 2" strokeOpacity="0.5" strokeWidth="1.5" x1="230" y1="190" x2="80" y2="70" />
              <line stroke="#8e7fff" strokeOpacity="0.6" strokeWidth="1.5" x1="230" y1="190" x2="380" y2="100" />
              <line stroke="#e3c464" strokeOpacity="0.7" strokeWidth="1.5" x1="230" y1="190" x2="260" y2="330" />
              <line stroke="#8e7fff" strokeDasharray="3 3" strokeWidth="1.5" x1="230" y1="0" x2="230" y2="140" />
            </svg>

            {/* Node 1 (Top Left): Material Status */}
            <div className="absolute left-2 top-8 z-20 flex items-center gap-2.5 p-2.5 rounded-xl bg-[#2c2834]/95 backdrop-blur-md shadow-xl border border-white/10 hover:scale-105 transition-transform duration-200">
              <div className="size-8 rounded-lg bg-[#90162d]/60 flex items-center justify-center text-[#ffb3b6]">
                <span className="material-symbols-outlined text-[18px]">
                  {activeMaterial?.source_type === "pdf" ? "picture_as_pdf" : "description"}
                </span>
              </div>
              <div className="flex flex-col max-w-[140px]">
                <span className="font-space text-xs font-bold text-white truncate">
                  {activeMaterial ? activeMaterial.title : "Add Lecture Notes"}
                </span>
                <span className="text-[11px] text-[#c8c4d6]">
                  {activeMaterial
                    ? `${activeMaterial.word_count || Math.round(activeMaterial.char_count / 5)} words indexed`
                    : "Ready for upload"}
                </span>
              </div>
            </div>

            {/* Node 2 (Top Right): Practice Recall */}
            <div className="absolute right-2 top-14 z-20 flex items-center gap-2 px-3 py-2 rounded-xl bg-[#2c2834]/95 backdrop-blur-md shadow-xl border border-white/10 hover:scale-105 transition-transform duration-200">
              <span className="size-2 rounded-full bg-[#8e7fff] animate-ping" />
              <div className="flex flex-col">
                <span className="font-space text-xs font-bold text-white">Active Recall</span>
                <span className="text-[10px] text-[#8e7fff] font-semibold">Adaptive Questions</span>
              </div>
            </div>

            {/* Node 3 (Bottom Right): Spaced Repetition */}
            <div className="absolute right-6 bottom-4 z-20 flex items-center gap-2 px-3 py-2 rounded-xl bg-[#211e2a]/95 backdrop-blur-md shadow-xl border border-white/10 hover:scale-105 transition-transform duration-200">
              <span className="material-symbols-outlined text-[16px] text-[#e3c464]">star</span>
              <div className="flex flex-col">
                <span className="font-space text-xs font-bold text-white">Spaced Memory</span>
                <span className="text-[10px] text-[#e3c464] font-semibold">3D Flashcards</span>
              </div>
            </div>

            {/* Spidey Mascot Hub */}
            <div className="relative z-10 flex flex-col items-center">
              {/* Mascot Speech Bubble */}
              <div
                className="mb-2 px-3.5 py-1.5 rounded-2xl bg-[#37333f] shadow-lg text-white text-xs flex items-center gap-1.5 border border-white/10 animate-bounce"
                style={{ animationDuration: "3s" }}
              >
                <span>
                  {activeMaterial
                    ? `Ready to study ${activeMaterial.title}?`
                    : "Feed me notes to weave your deck!"}
                </span>
                <span className="font-caveat text-[#e3c464] text-base font-bold">~ spidey</span>
              </div>

              {/* Spidey Avatar Container with cozy purple glow */}
              <div className="relative size-28 rounded-full bg-[#211e2a] border border-[#8e7fff]/30 flex items-center justify-center shadow-2xl group cursor-pointer">
                <div className="absolute inset-0 rounded-full bg-[#8e7fff]/15 blur-xl group-hover:bg-[#8e7fff]/30 transition-colors" />
                <SpideyMascot mood="idle" size={72} interactive={true} />
              </div>
            </div>
          </div>
        </section>

        {/* 2. STUDY MODES FOR ACTIVE MATERIAL */}
        <section className="flex flex-col gap-6">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-2">
            <div>
              <div className="font-caveat text-[#e3c464] text-2xl leading-none mb-1">
                spidey woven modalities
              </div>
              <h2 className="font-space text-2xl sm:text-3xl font-bold text-white tracking-tight">
                Study Modes
              </h2>
              <p className="text-sm text-[#c8c4d6] mt-1">
                Select any modality below to trigger a structured revision ritual grounded in your material.
              </p>
            </div>

            {activeMaterial && (
              <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-[#211e2a] border border-white/5 text-xs text-[#c8c4d6]">
                <span className="size-2 rounded-full bg-[#8e7fff] animate-pulse" />
                <span>Ready for:</span>
                <span className="font-bold text-white truncate max-w-[180px]">{activeMaterial.title}</span>
              </div>
            )}
          </div>

          {/* 6 Capabilities Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {/* Card 1: Active Recall Quiz */}
            <Link
              href="/quiz/setup"
              className="group p-6 rounded-2xl bg-[#1d1a25] border border-white/5 hover:border-[#8e7fff]/60 hover:bg-[#211e2a] transition-all duration-300 flex flex-col justify-between shadow-sm hover:-translate-y-1"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-1 rounded-full bg-[#8e7fff]/15 text-[#8e7fff] text-xs font-bold border border-[#8e7fff]/25">
                    Adaptive Recall
                  </span>
                  <div className="size-9 rounded-xl bg-[#2c2834] flex items-center justify-center text-[#8e7fff] group-hover:bg-[#8e7fff] group-hover:text-white transition-colors">
                    <span className="material-symbols-outlined text-[20px]">quiz</span>
                  </div>
                </div>
                <h3 className="font-space text-lg font-bold text-white mb-2 group-hover:text-[#8e7fff] transition-colors">
                  Active Recall Quiz
                </h3>
                <p className="text-sm text-[#c8c4d6] leading-relaxed">
                  Adaptive multiple-choice and step-by-step recall exercises grounded strictly in your study material.
                </p>
              </div>
              <div className="pt-5 border-t border-white/5 mt-4 flex items-center justify-between text-xs text-[#8e7fff] font-bold">
                <span className="group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Drill Quiz →
                </span>
                <span className="font-caveat text-[#c8c4d6] text-base">instant scoring</span>
              </div>
            </Link>

            {/* Card 2: 3D Flashcard Deck */}
            <Link
              href="/flashcards"
              className="group p-6 rounded-2xl bg-[#1d1a25] border border-white/5 hover:border-[#e3c464]/60 hover:bg-[#211e2a] transition-all duration-300 flex flex-col justify-between shadow-sm hover:-translate-y-1"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-1 rounded-full bg-[#e3c464]/15 text-[#e3c464] text-xs font-bold border border-[#e3c464]/25">
                    Spatial Memory
                  </span>
                  <div className="size-9 rounded-xl bg-[#2c2834] flex items-center justify-center text-[#e3c464] group-hover:bg-[#e3c464] group-hover:text-black transition-colors">
                    <span className="material-symbols-outlined text-[20px]">style</span>
                  </div>
                </div>
                <h3 className="font-space text-lg font-bold text-white mb-2 group-hover:text-[#e3c464] transition-colors">
                  3D Flashcard Deck
                </h3>
                <p className="text-sm text-[#c8c4d6] leading-relaxed">
                  Tactile double-sided spatial cards with Leitner spaced repetition interval and instant hint toggles.
                </p>
              </div>
              <div className="pt-5 border-t border-white/5 mt-4 flex items-center justify-between text-xs text-[#e3c464] font-bold">
                <span className="group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Flip Cards →
                </span>
                <span className="font-caveat text-[#c8c4d6] text-base">spaced reviews</span>
              </div>
            </Link>

            {/* Card 3: Notes Canvas */}
            <Link
              href="/notes"
              className="group p-6 rounded-2xl bg-[#1d1a25] border border-white/5 hover:border-[#8e7fff]/60 hover:bg-[#211e2a] transition-all duration-300 flex flex-col justify-between shadow-sm hover:-translate-y-1"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-1 rounded-full bg-[#2c2834] text-[#c8c4d6] text-xs font-bold">
                    Cornell Synthesis
                  </span>
                  <div className="size-9 rounded-xl bg-[#2c2834] flex items-center justify-center text-[#c8c4d6] group-hover:bg-[#8e7fff] group-hover:text-white transition-colors">
                    <span className="material-symbols-outlined text-[20px]">draw</span>
                  </div>
                </div>
                <h3 className="font-space text-lg font-bold text-white mb-2 group-hover:text-[#8e7fff] transition-colors">
                  Structured Notes Canvas
                </h3>
                <p className="text-sm text-[#c8c4d6] leading-relaxed">
                  Dual-column Cornell synthesis with marginal diagrams, highlighted formula anchors, and margin glossaries.
                </p>
              </div>
              <div className="pt-5 border-t border-white/5 mt-4 flex items-center justify-between text-xs text-[#8e7fff] font-bold">
                <span className="group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Read Notes →
                </span>
                <span className="font-caveat text-[#c8c4d6] text-base">annotated</span>
              </div>
            </Link>

            {/* Card 4: AI Desk Copilot */}
            <Link
              href="/chat"
              className="group p-6 rounded-2xl bg-[#1d1a25] border border-white/5 hover:border-[#8e7fff]/60 hover:bg-[#211e2a] transition-all duration-300 flex flex-col justify-between shadow-sm hover:-translate-y-1"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-1 rounded-full bg-[#8e7fff]/15 text-[#8e7fff] text-xs font-bold border border-[#8e7fff]/25">
                    Strictly Grounded
                  </span>
                  <div className="size-9 rounded-xl bg-[#2c2834] flex items-center justify-center text-[#8e7fff] group-hover:bg-[#8e7fff] group-hover:text-white transition-colors">
                    <span className="material-symbols-outlined text-[20px]">smart_toy</span>
                  </div>
                </div>
                <h3 className="font-space text-lg font-bold text-white mb-2 group-hover:text-[#8e7fff] transition-colors">
                  AI Desk Copilot
                </h3>
                <p className="text-sm text-[#c8c4d6] leading-relaxed">
                  Direct inquiries with verbatim slide citations. Spidey reasons step-by-step through algorithmic edge cases.
                </p>
              </div>
              <div className="pt-5 border-t border-white/5 mt-4 flex items-center justify-between text-xs text-[#8e7fff] font-bold">
                <span className="group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Ask Spidey →
                </span>
                <span className="font-caveat text-[#c8c4d6] text-base">instant reply</span>
              </div>
            </Link>

            {/* Card 5: Midterm Simulator */}
            <Link
              href="/exam/setup"
              className="group p-6 rounded-2xl bg-[#1d1a25] border border-white/5 hover:border-[#ffb4ab]/60 hover:bg-[#211e2a] transition-all duration-300 flex flex-col justify-between shadow-sm hover:-translate-y-1"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-1 rounded-full bg-[#2c2834] text-[#ffb4ab] text-xs font-bold">
                    Exam Grade
                  </span>
                  <div className="size-9 rounded-xl bg-[#2c2834] flex items-center justify-center text-[#c8c4d6] group-hover:bg-[#90162d] group-hover:text-[#ffb4ab] transition-colors">
                    <span className="material-symbols-outlined text-[20px]">hourglass_empty</span>
                  </div>
                </div>
                <h3 className="font-space text-lg font-bold text-white mb-2 group-hover:text-[#ffb4ab] transition-colors">
                  Midterm Simulator
                </h3>
                <p className="text-sm text-[#c8c4d6] leading-relaxed">
                  Exam-grade free-response format with autograded rubric criteria, negative marking warnings, and analysis.
                </p>
              </div>
              <div className="pt-5 border-t border-white/5 mt-4 flex items-center justify-between text-xs text-[#ffb4ab] font-bold">
                <span className="group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Simulate →
                </span>
                <span className="font-caveat text-[#c8c4d6] text-base">exam mode</span>
              </div>
            </Link>

            {/* Card 6: Synthesized Audio Podcast */}
            <Link
              href="/podcast/setup"
              className="group p-6 rounded-2xl bg-[#1d1a25] border border-white/5 hover:border-[#8e7fff]/60 hover:bg-[#211e2a] transition-all duration-300 flex flex-col justify-between shadow-sm hover:-translate-y-1"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="px-2.5 py-1 rounded-full bg-[#8e7fff]/15 text-[#8e7fff] text-xs font-bold border border-[#8e7fff]/25">
                    Audio Digest
                  </span>
                  <div className="size-9 rounded-xl bg-[#2c2834] flex items-center justify-center text-[#8e7fff] group-hover:bg-[#8e7fff] group-hover:text-white transition-colors">
                    <span className="material-symbols-outlined text-[20px]">podcasts</span>
                  </div>
                </div>
                <h3 className="font-space text-lg font-bold text-white mb-2 group-hover:text-[#8e7fff] transition-colors">
                  Synthesized Audio Recap
                </h3>
                <p className="text-sm text-[#c8c4d6] leading-relaxed">
                  Conversational podcast synthesis between Spidey and a guest host, tailored for late walk commutes.
                </p>
              </div>
              <div className="pt-5 border-t border-white/5 mt-4 flex items-center justify-between text-xs text-[#8e7fff] font-bold">
                <span className="group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Play Audio →
                </span>
                <span className="font-caveat text-[#c8c4d6] text-base">cozy tone</span>
              </div>
            </Link>
          </div>
        </section>

        {/* 3. RECENT COURSE ARCHIVES SHELF */}
        <section className="flex flex-col gap-5 pb-12">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#8e7fff] text-[22px]">shelves</span>
              <h2 className="font-space text-xl sm:text-2xl font-bold text-white">
                Course Archives & Study Sets
              </h2>
            </div>

            <Link
              href="/add"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#211e2a] hover:bg-[#2c2834] text-[#8e7fff] text-xs font-bold transition-colors shadow-sm border border-white/5"
            >
              <span className="material-symbols-outlined text-[16px]">add</span>
              <span>Add New Material</span>
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
              {[1, 2, 3].map((n) => (
                <div key={n} className="h-44 rounded-2xl bg-[#1d1a25] animate-pulse border border-white/5" />
              ))}
            </div>
          ) : materials.length === 0 ? (
            <div className="p-8 rounded-3xl bg-[#1d1a25] border border-white/5 flex flex-col items-center justify-center text-center gap-3">
              <div className="size-12 rounded-2xl bg-[#8e7fff]/15 flex items-center justify-center text-[#8e7fff]">
                <span className="material-symbols-outlined text-[28px]">library_books</span>
              </div>
              <h3 className="font-space text-base font-bold text-white">No Study Sets Uploaded Yet</h3>
              <p className="text-xs text-[#c8c4d6] max-w-sm">
                Upload lecture slides, PDF readings, or paste raw notes to automatically generate quizzes, flashcards, and Cornell notes.
              </p>
              <Link
                href="/add"
                className="mt-2 inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-[#8e7fff] hover:bg-[#8e7fff]/90 text-white font-bold text-xs shadow-md shadow-[#8e7fff]/25 transition-all"
              >
                <span className="material-symbols-outlined text-[16px]">upload_file</span>
                <span>Upload First Material</span>
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {materials.map((m) => {
                const isActive = material?.id === m.id;
                return (
                  <div
                    key={m.id}
                    className={`p-5 rounded-2xl bg-[#1d1a25] border transition-all flex flex-col justify-between shadow-sm relative overflow-hidden group hover:bg-[#211e2a] ${
                      isActive ? "border-[#8e7fff]/60 ring-1 ring-[#8e7fff]/40" : "border-white/5"
                    }`}
                  >
                    <div className={`absolute top-0 left-0 right-0 h-1 ${isActive ? "bg-[#8e7fff]" : "bg-white/10"}`} />
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span
                          className={`text-[10px] uppercase tracking-wider font-bold ${
                            isActive ? "text-[#8e7fff]" : "text-[#c8c4d6]"
                          }`}
                        >
                          {isActive ? "Active Focus" : m.source_type}
                        </span>
                        <span className="text-xs text-[#c8c4d6]">
                          {m.word_count || Math.round(m.char_count / 5)} words
                        </span>
                      </div>
                      <h4 className="font-space text-base text-white font-bold mb-1 group-hover:text-[#8e7fff] transition-colors truncate">
                        {m.title}
                      </h4>
                      <p className="text-xs text-[#c8c4d6] line-clamp-2 mb-4">
                        {m.content.slice(0, 100)}...
                      </p>
                    </div>

                    <div className="pt-3 border-t border-white/5 flex items-center justify-between">
                      <button
                        type="button"
                        onClick={() => setMaterial(m)}
                        className={`text-xs font-bold transition-colors inline-flex items-center gap-1 ${
                          isActive ? "text-[#8e7fff]" : "text-[#c8c4d6] hover:text-white"
                        }`}
                      >
                        {isActive ? "Currently Selected ✓" : "Set as Active Focus →"}
                      </button>

                      <Link
                        href={`/quiz/setup?material_id=${m.id}`}
                        onClick={() => setMaterial(m)}
                        className="px-2.5 py-1 rounded-lg bg-[#2c2834] hover:bg-[#8e7fff] hover:text-white text-[11px] font-semibold text-[#8e7fff] transition-colors"
                      >
                        Quiz
                      </Link>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </section>

      </div>
    </div>
  );
}
