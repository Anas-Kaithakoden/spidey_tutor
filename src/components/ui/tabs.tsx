"use client"

import { createContext, useContext, type ReactNode } from "react"
import { cn } from "cn"

const TabsContext = createContext<{ value: string; onValueChange: (value: string) => void } | null>(null)

function Tabs({ value, onValueChange, children, className }: { value: string; onValueChange: (value: string) => void; children: ReactNode; className?: string }) {
  return <TabsContext.Provider value={{ value, onValueChange }}><div className={className}>{children}</div></TabsContext.Provider>
}

function TabsList({ children, className }: { children: ReactNode; className?: string }) {
  return <div role="tablist" className={cn("flex flex-wrap gap-1 rounded-xl border bg-muted/60 p-1", className)}>{children}</div>
}

function TabsTrigger({ value, children, className }: { value: string; children: ReactNode; className?: string }) {
  const tabs = useContext(TabsContext)
  if (!tabs) throw new Error("TabsTrigger must be used inside Tabs")
  const active = tabs.value === value
  return <button type="button" role="tab" aria-selected={active} onClick={() => tabs.onValueChange(value)} className={cn("rounded-lg px-3 py-2 text-sm font-medium transition-colors", active ? "bg-background text-foreground shadow-sm" : "text-muted-foreground hover:text-foreground", className)}>{children}</button>
}

function TabsContent({ value, children, className }: { value: string; children: ReactNode; className?: string }) {
  const tabs = useContext(TabsContext)
  if (!tabs || tabs.value !== value) return null
  return <div role="tabpanel" className={className}>{children}</div>
}

export { Tabs, TabsList, TabsTrigger, TabsContent }