"use client"

import { useEffect, type ReactNode } from "react"
import { X } from "lucide-react"
import { cn } from "cn"

function Dialog({ open, onOpenChange, title, children, className }: { open: boolean; onOpenChange: (open: boolean) => void; title: string; children: ReactNode; className?: string }) {
  useEffect(() => {
    if (!open) return
    const onKeyDown = (event: KeyboardEvent) => { if (event.key === "Escape") onOpenChange(false) }
    document.addEventListener("keydown", onKeyDown)
    return () => document.removeEventListener("keydown", onKeyDown)
  }, [open, onOpenChange])

  if (!open) return null
  return <div role="presentation" className="fixed inset-0 z-50 flex items-center justify-center bg-foreground/40 p-4" onMouseDown={() => onOpenChange(false)}>
    <section role="dialog" aria-modal="true" aria-labelledby="dialog-title" onMouseDown={(event) => event.stopPropagation()} className={cn("w-full max-w-lg rounded-2xl border bg-card p-6 shadow-2xl", className)}>
      <div className="mb-4 flex items-start justify-between gap-4"><h2 id="dialog-title" className="text-lg font-semibold">{title}</h2><button type="button" onClick={() => onOpenChange(false)} aria-label="Close dialog" className="rounded-lg p-1 text-muted-foreground hover:bg-muted hover:text-foreground"><X className="size-4" /></button></div>
      {children}
    </section>
  </div>
}

export { Dialog }