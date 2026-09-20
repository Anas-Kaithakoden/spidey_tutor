"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useRef, useEffect, type ComponentType } from "react";
import {
  BarChart3,
  BookOpen,
  CalendarDays,
  ChevronDown,
  FileText,
  FlaskConical,
  Headphones,
  Menu,
  MessageCircle,
  NotebookPen,
  X,
} from "lucide-react";
import { ThemeToggle } from "./theme-toggle";
import { Button } from "@/components/ui/button";
import { SpideyMascot } from "@/components/spidey-mascot";
import { useStudy } from "@/lib/context";
import { cn } from "@/lib/utils";

type NavItem = { href: string; label: string; icon: ComponentType<{ className?: string }> };

const primaryLinks: NavItem[] = [
  { href: "/add", label: "Study", icon: BookOpen },
  { href: "/notes", label: "Notes", icon: NotebookPen },
  { href: "/flashcards", label: "Flashcards", icon: FileText },
  { href: "/chat", label: "Tutor chat", icon: MessageCircle },
  { href: "/progress", label: "Progress", icon: BarChart3 },
];

const toolLinks: NavItem[] = [
  { href: "/exam/setup", label: "Practice exam", icon: BookOpen },
  { href: "/podcast", label: "Study podcast", icon: Headphones },
  { href: "/study-plan", label: "Study plan", icon: CalendarDays },
  { href: "/formula-sheet", label: "Formula sheet", icon: FlaskConical },
];

function isActive(pathname: string, href: string) {
  return pathname === href || (href !== "/" && pathname.startsWith(`${href}/`));
}

function NavLink({ item, onClick }: { item: NavItem; onClick?: () => void }) {
  const pathname = usePathname();
  const active = isActive(pathname, item.href);
  const Icon = item.icon;

  return (
    <Link
      href={item.href}
      onClick={onClick}
      aria-current={active ? "page" : undefined}
      className={cn(
        "flex items-center gap-2 rounded-lg px-3 py-2 text-sm font-medium transition-all",
        active
          ? "bg-primary/12 text-primary font-semibold shadow-xs border border-primary/20"
          : "text-muted-foreground hover:bg-muted/70 hover:text-foreground"
      )}
    >
      <Icon className="size-4" aria-hidden="true" />
      {item.label}
    </Link>
  );
}

export function Navbar() {
  const pathname = usePathname();
  const { material } = useStudy();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [moreOpen, setMoreOpen] = useState(false);
  const moreRef = useRef<HTMLDivElement>(null);
  const toolsActive = toolLinks.some((link) => isActive(pathname, link.href));

  // Close "More" dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (moreRef.current && !moreRef.current.contains(event.target as Node)) {
        setMoreOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="sticky top-0 z-50 border-b border-border/70 bg-background/85 backdrop-blur-xl transition-colors">
      <div className="mx-auto flex min-h-16 max-w-7xl items-center gap-4 px-4 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="group flex shrink-0 items-center gap-2.5 transition-transform active:scale-95"
          aria-label="Spidey Tutor home"
        >
          <div className="flex size-10 items-center justify-center rounded-xl bg-primary/15 border border-primary/30 text-primary shadow-xs transition-colors group-hover:border-primary/60">
            <SpideyMascot mood="idle" size={26} interactive={false} />
          </div>
          <span className="hidden font-bold tracking-tight text-base sm:inline">
            Spidey<span className="text-primary font-extrabold ml-1">Tutor</span>
          </span>
        </Link>

        <nav className="hidden min-w-0 flex-1 items-center gap-1.5 lg:flex" aria-label="Primary navigation">
          {primaryLinks.map((item) => (
            <NavLink key={item.href} item={item} />
          ))}

          {/* Controlled "More" dropdown */}
          <div className="relative ml-1" ref={moreRef}>
            <button
              type="button"
              onClick={() => setMoreOpen((prev) => !prev)}
              aria-expanded={moreOpen}
              className={cn(
                "flex cursor-pointer items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium transition-all",
                toolsActive
                  ? "bg-primary/12 text-primary font-semibold border border-primary/20"
                  : "text-muted-foreground hover:bg-muted/70 hover:text-foreground"
              )}
            >
              More <ChevronDown className={cn("size-3.5 transition-transform duration-200", moreOpen && "rotate-180")} aria-hidden="true" />
            </button>
            {moreOpen && (
              <div className="absolute left-0 top-full mt-2 w-52 rounded-xl border border-border/80 bg-popover/95 p-1.5 shadow-xl backdrop-blur-md ring-1 ring-foreground/10 animate-in fade-in-50 zoom-in-95">
                {toolLinks.map((item) => (
                  <NavLink
                    key={item.href}
                    item={item}
                    onClick={() => setMoreOpen(false)}
                  />
                ))}
              </div>
            )}
          </div>
        </nav>

        <div className="ml-auto hidden min-w-0 items-center gap-3 lg:flex">
          {material && (
            <Link
              href="/preview"
              className="group flex max-w-56 items-center gap-2 rounded-xl border border-primary/20 bg-secondary/50 px-3 py-1.5 text-left transition-all hover:border-primary/50 hover:bg-secondary/80"
              title={material.title}
            >
              <div className="size-2 rounded-full bg-primary animate-pulse" />
              <div className="min-w-0">
                <span className="block text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">Studying</span>
                <span className="block truncate text-xs font-semibold text-foreground group-hover:text-primary">{material.title || "Current Material"}</span>
              </div>
            </Link>
          )}
          <ThemeToggle />
        </div>

        <div className="ml-auto flex items-center gap-1.5 lg:hidden">
          <ThemeToggle />
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setMobileOpen((open) => !open)}
            aria-label={mobileOpen ? "Close navigation" : "Open navigation"}
            aria-expanded={mobileOpen}
          >
            {mobileOpen ? <X className="size-5" /> : <Menu className="size-5" />}
          </Button>
        </div>
      </div>

      {/* Mobile drawer */}
      {mobileOpen && (
        <nav className="border-t border-border/80 bg-background/95 backdrop-blur-md px-4 py-3 lg:hidden animate-in slide-in-from-top-2" aria-label="Mobile navigation">
          <div className="mx-auto grid max-w-7xl gap-1.5 sm:grid-cols-2">
            {[...primaryLinks, ...toolLinks].map((item) => (
              <NavLink key={item.href} item={item} onClick={() => setMobileOpen(false)} />
            ))}
          </div>
          {material && (
            <Link
              href="/preview"
              onClick={() => setMobileOpen(false)}
              className="mx-auto mt-3 flex max-w-7xl items-center gap-2.5 rounded-xl border border-primary/20 bg-secondary/50 px-3 py-2"
            >
              <div className="size-2 rounded-full bg-primary animate-pulse" />
              <div className="min-w-0">
                <span className="block text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">Studying</span>
                <span className="block truncate text-sm font-semibold">{material.title || "Current Material"}</span>
              </div>
            </Link>
          )}
        </nav>
      )}
    </header>
  );
}
