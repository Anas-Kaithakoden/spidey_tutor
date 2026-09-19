"use client";

import Link from "next/link";
import { Bug } from "lucide-react";
import { ThemeToggle } from "./theme-toggle";
import { Button } from "@/components/ui/button";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur-sm">
      <div className="mx-auto flex min-h-14 max-w-4xl flex-wrap items-center justify-between gap-y-1 px-4 py-2">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <Bug className="size-5 shrink-0" />
          <span className="hidden sm:inline">Spidey Tutor</span>
        </Link>
        <nav className="flex flex-wrap items-center justify-end gap-1">
          <Button render={<Link href="/add" />} variant="ghost" size="sm" nativeButton={false}>
            Study
          </Button>
          <Button render={<Link href="/notes" />} variant="ghost" size="sm" nativeButton={false}>
            Notes
          </Button>
          <Button render={<Link href="/flashcards" />} variant="ghost" size="sm" nativeButton={false}>
            Flashcards
          </Button>
          <Button render={<Link href="/exam/setup" />} variant="ghost" size="sm" nativeButton={false}>
            Exam
          </Button>
          <Button render={<Link href="/podcast" />} variant="ghost" size="sm" nativeButton={false}>
            Podcast
          </Button>
          <Button render={<Link href="/chat" />} variant="ghost" size="sm" nativeButton={false}>
            Chat
          </Button>
          <Button render={<Link href="/progress" />} variant="ghost" size="sm" nativeButton={false}>
            Progress
          </Button>
          <ThemeToggle />
        </nav>
      </div>
    </header>
  );
}
