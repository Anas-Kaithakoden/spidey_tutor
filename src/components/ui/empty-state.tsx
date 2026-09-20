import type { ReactNode } from "react";
import { SpideyMascot, type SpideyMood } from "@/components/spidey-mascot";
import { cn } from "@/lib/utils";

interface EmptyStateProps {
  icon?: ReactNode;
  mascotMood?: SpideyMood;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

function EmptyState({
  icon,
  mascotMood = "idle",
  title,
  description,
  action,
  className,
}: EmptyStateProps) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center gap-4 rounded-2xl border border-dashed border-border/80 bg-card/60 p-8 sm:py-16 text-center shadow-xs backdrop-blur-xs",
        className
      )}
    >
      {icon ? (
        <div className="flex size-14 items-center justify-center rounded-2xl bg-secondary text-secondary-foreground shadow-xs">
          {icon}
        </div>
      ) : (
        <div className="flex items-center justify-center rounded-2xl bg-primary/10 border border-primary/20 p-2.5 shadow-xs">
          <SpideyMascot mood={mascotMood} size={54} />
        </div>
      )}
      <div className="max-w-md space-y-1.5">
        <h2 className="text-lg font-bold tracking-tight text-foreground">{title}</h2>
        {description && (
          <p className="text-sm leading-relaxed text-muted-foreground">{description}</p>
        )}
      </div>
      {action && <div className="pt-2">{action}</div>}
    </div>
  );
}

export { EmptyState };