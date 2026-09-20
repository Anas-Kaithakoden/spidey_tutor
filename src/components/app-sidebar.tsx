"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { SpideyMascot } from "@/components/spidey-mascot";
import { cn } from "@/lib/utils";

interface NavLinkItem {
  href: string;
  label: string;
  icon: string;
}

const mainNav: NavLinkItem[] = [
  { href: "/", label: "Study Desk", icon: "grid_view" },
  { href: "/add", label: "Materials & Syllabus", icon: "auto_stories" },
];

const studySuiteNav: NavLinkItem[] = [
  { href: "/quiz/setup", label: "Active Recall Quiz", icon: "quiz" },
  { href: "/flashcards", label: "3D Flashcards", icon: "style" },
  { href: "/notes", label: "Notes Canvas", icon: "draw" },
  { href: "/chat", label: "AI Tutor Companion", icon: "smart_toy" },
  { href: "/exam/setup", label: "Exam Simulator", icon: "hourglass_empty" },
];

const toolsNav: NavLinkItem[] = [
  { href: "/podcast", label: "Audio Podcast", icon: "podcasts" },
  { href: "/study-plan", label: "Study Plan Planner", icon: "event_note" },
  { href: "/formula-sheet", label: "Formula Sheet", icon: "functions" },
];

const progressNav: NavLinkItem[] = [
  { href: "/progress", label: "Mastery Web & Analytics", icon: "hub" },
];

export function AppSidebar() {
  const pathname = usePathname();

  function isActive(href: string) {
    if (href === "/") return pathname === "/";
    return pathname === href || pathname.startsWith(`${href}/`);
  }

  function renderNavGroup(title: string, items: NavLinkItem[]) {
    return (
      <div className="flex flex-col gap-1 mb-4">
        <div className="px-3 py-1 text-[11px] font-bold uppercase tracking-wider text-outline">
          {title}
        </div>
        {items.map((item) => {
          const active = isActive(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-xl text-sm font-medium transition-all",
                active
                  ? "bg-[#8e7fff] text-white font-bold shadow-md shadow-[#8e7fff]/25"
                  : "text-[#c8c4d6] hover:bg-[#2c2834] hover:text-white"
              )}
            >
              <span className="material-symbols-outlined text-[20px]">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </div>
    );
  }

  return (
    <aside className="hidden lg:flex fixed left-0 top-0 h-full w-72 bg-[#1d1a25] z-50 flex-col justify-between overflow-y-auto border-r border-white/5 shadow-2xl">
      <div className="flex flex-col">
        {/* Brand Header */}
        <Link
          href="/"
          className="h-16 px-4 flex items-center gap-3 bg-[#1d1a25]/60 border-b border-white/5 group hover:bg-[#2c2834]/40 transition-colors"
        >
          <div className="flex items-center justify-center size-9 rounded-xl bg-[#8e7fff]/15 border border-[#8e7fff]/30 shadow-xs">
            <SpideyMascot mood="idle" size={28} interactive={false} />
          </div>
          <div className="flex flex-col">
            <span className="font-space text-lg font-bold text-white tracking-tight leading-none">
              Spidey Tutor
            </span>
            <span className="text-[11px] text-[#c8c4d6] leading-tight font-medium mt-0.5">
              v3.0 · cosmic night
            </span>
          </div>
        </Link>

        {/* Navigation Sections */}
        <nav className="flex flex-col px-3 py-4">
          {renderNavGroup("Main", mainNav)}
          {renderNavGroup("Study Suite", studySuiteNav)}
          {renderNavGroup("Tools", toolsNav)}
          {renderNavGroup("Progress", progressNav)}
        </nav>
      </div>

      {/* User Session Footer Card */}
      <div className="p-3 m-3 rounded-2xl bg-[#211e2a] border border-white/5 flex flex-col gap-2 shadow-inner">
        <div className="flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-xs font-bold text-white">Study Session</span>
            <span className="text-[11px] text-[#c8c4d6]">Personal Workspace</span>
          </div>
          <div className="size-8 rounded-full bg-[#8e7fff]/20 border border-[#8e7fff]/40 text-[#8e7fff] flex items-center justify-center font-bold text-xs shadow-xs">
            <span className="material-symbols-outlined text-[16px]">school</span>
          </div>
        </div>
        <div className="flex items-center justify-between pt-1 border-t border-white/5">
          <span className="inline-flex items-center gap-1.5 text-xs text-[#e3c464] font-semibold">
            <span className="material-symbols-outlined text-[14px]">auto_awesome</span>
            <span>Focus Mode</span>
          </span>
          <span className="px-2 py-0.5 rounded-full bg-[#2c2834] text-[10px] font-bold text-[#8e7fff] border border-[#8e7fff]/30">
            Active
          </span>
        </div>
      </div>
    </aside>
  );
}
