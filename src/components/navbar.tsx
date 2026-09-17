"use client";

import Link from "next/link";
import { Bug } from "lucide-react";
import { ThemeToggle } from "./theme-toggle";
import { Button } from "@/components/ui/button";

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur-sm">
      <div className="mx-auto flex h-14 max-w-4xl items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <Bug className="size-5" />
          <span>Spidey Tutor</span>
        </Link>
        <nav className="flex items-center gap-1">
          <Button render={<Link href="/add" />} variant="ghost" size="sm">
            Study
          </Button>
          <Button render={<Link href="/flashcards" />} variant="ghost" size="sm">
            Flashcards
          </Button>
          <ThemeToggle />
        </nav>
      </div>
    </header>
  );
}
