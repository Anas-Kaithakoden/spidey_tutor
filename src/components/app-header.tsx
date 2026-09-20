"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { SpideyMascot } from "@/components/spidey-mascot";
import { ThemeToggle } from "@/components/theme-toggle";
import { useStudy } from "@/lib/context";
import { Menu, X } from "lucide-react";

export function AppHeader() {
  const { material } = useStudy();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState("02:44 AM");

  useEffect(() => {
    function updateClock() {
      const now = new Date();
      setCurrentTime(
        now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      );
    }
    updateClock();
    const interval = setInterval(updateClock, 30000);
    return () => clearInterval(interval);
  }, []);


  return (
    <header className="fixed top-0 left-0 lg:left-72 right-0 h-16 bg-[#1d1a25]/90 backdrop-blur-xl border-b border-white/5 z-40 flex items-center justify-between px-4 sm:px-6 shadow-sm">
      {/* Mobile Menu Toggle & Brand Logo */}
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="lg:hidden p-1.5 rounded-lg bg-[#2c2834] text-white"
          aria-label="Toggle Navigation"
        >
          {mobileMenuOpen ? <X className="size-5" /> : <Menu className="size-5" />}
        </button>

        <div className="flex items-center gap-2.5">
          <div className="flex size-8 shrink-0 items-center justify-center rounded-lg bg-[#8e7fff]/15 border border-[#8e7fff]/30">
            <SpideyMascot mood="idle" size={24} interactive={false} />
          </div>

          <div className="flex items-center gap-2 min-w-0">
            <span className="material-symbols-outlined text-[#8e7fff] text-[18px]">bookmark</span>
            {material ? (
              <>
                <span className="text-[11px] font-bold uppercase tracking-wider text-[#c8c4d6] hidden xl:inline">
                  CURRENTLY STUDYING:
                </span>
                <Link
                  href="/preview"
                  className="text-xs sm:text-sm font-semibold text-white truncate max-w-[200px] sm:max-w-[320px] hover:text-[#8e7fff] transition-colors"
                >
                  {material.title}
                </Link>
                <span className="hidden sm:inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#8e7fff] text-white text-[10px] font-bold shadow-xs">
                  Active
                </span>
              </>
            ) : (
              <Link
                href="/add"
                className="text-xs text-[#c8c4d6] hover:text-[#8e7fff] transition-colors flex items-center gap-1.5"
              >
                <span>No active study set</span>
                <span className="text-[10px] font-bold text-[#8e7fff] bg-[#8e7fff]/15 px-2 py-0.5 rounded-md border border-[#8e7fff]/30">
                  + Add Material
                </span>
              </Link>
            )}
          </div>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-3">
        {/* Quick Nav Tabs */}
        <nav className="hidden md:flex items-center gap-1 bg-[#211e2a] p-1 rounded-xl border border-white/5">
          <Link
            href="/notes"
            className="px-3 py-1 rounded-lg text-xs font-semibold text-[#c8c4d6] hover:text-white hover:bg-[#2c2834] transition-all"
          >
            Canvas
          </Link>
          <Link
            href="/flashcards"
            className="px-3 py-1 rounded-lg text-xs font-semibold text-[#c8c4d6] hover:text-white hover:bg-[#2c2834] transition-all"
          >
            Flashcards
          </Link>
          <Link
            href="/chat"
            className="px-3 py-1 rounded-lg text-xs font-semibold text-[#c8c4d6] hover:text-white hover:bg-[#2c2834] transition-all"
          >
            Co-pilot
          </Link>
        </nav>

        {/* Live Clock Pill */}
        <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-xl bg-[#211e2a] border border-white/5 text-xs font-medium text-[#c8c4d6]">
          <span className="material-symbols-outlined text-[16px] text-[#e3c464]">schedule</span>
          <span>{currentTime}</span>
        </div>

        {/* Theme Toggle */}
        <ThemeToggle />

        {/* User Profile Avatar */}
        <div className="size-8 rounded-full bg-[#8e7fff] text-white flex items-center justify-center font-bold text-xs shadow-sm ring-2 ring-[#8e7fff]/40">
          AR
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden fixed inset-x-0 top-16 bg-[#1d1a25] border-b border-white/10 p-4 shadow-2xl animate-in slide-in-from-top-2">
          <div className="grid grid-cols-2 gap-2">
            <Link
              href="/"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2.5 rounded-xl bg-[#8e7fff] text-white font-bold text-xs"
            >
              <span className="material-symbols-outlined text-[18px]">grid_view</span>
              <span>Study Desk</span>
            </Link>
            <Link
              href="/add"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2.5 rounded-xl bg-[#211e2a] text-white font-semibold text-xs"
            >
              <span className="material-symbols-outlined text-[18px]">auto_stories</span>
              <span>Add Material</span>
            </Link>
            <Link
              href="/quiz/setup"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2.5 rounded-xl bg-[#211e2a] text-white font-semibold text-xs"
            >
              <span className="material-symbols-outlined text-[18px]">quiz</span>
              <span>Active Quiz</span>
            </Link>
            <Link
              href="/flashcards"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2.5 rounded-xl bg-[#211e2a] text-white font-semibold text-xs"
            >
              <span className="material-symbols-outlined text-[18px]">style</span>
              <span>3D Flashcards</span>
            </Link>
            <Link
              href="/notes"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2.5 rounded-xl bg-[#211e2a] text-white font-semibold text-xs"
            >
              <span className="material-symbols-outlined text-[18px]">draw</span>
              <span>Notes Canvas</span>
            </Link>
            <Link
              href="/chat"
              onClick={() => setMobileMenuOpen(false)}
              className="flex items-center gap-2 p-2.5 rounded-xl bg-[#211e2a] text-white font-semibold text-xs"
            >
              <span className="material-symbols-outlined text-[18px]">smart_toy</span>
              <span>Tutor Chat</span>
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
