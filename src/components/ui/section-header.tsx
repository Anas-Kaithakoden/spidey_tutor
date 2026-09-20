import type { ReactNode } from "react"
import { cn } from "@/lib/utils"

function SectionHeader({ title, description, action, className }: { title: string; description?: string; action?: ReactNode; className?: string }) {
  return (
    <div className={cn("mb-4 flex items-start justify-between gap-4", className)}>
      <div><h2 className="text-lg font-semibold">{title}</h2>{description && <p className="mt-1 text-sm text-muted-foreground">{description}</p>}</div>
      {action}
    </div>
  )
}

export { SectionHeader }