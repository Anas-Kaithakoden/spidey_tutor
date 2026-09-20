import type { Metadata } from "next";
import { Geist, Geist_Mono, Space_Grotesk, Caveat } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider";
import { StudyProvider } from "@/lib/context";
import { AppSidebar } from "@/components/app-sidebar";
import { AppHeader } from "@/components/app-header";
import { Toaster } from "@/components/ui/sonner";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const spaceGrotesk = Space_Grotesk({
  variable: "--font-space-grotesk",
  subsets: ["latin"],
});

const caveat = Caveat({
  variable: "--font-caveat",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Spidey Tutor - Study Less. Remember Everything.",
  description: "Cosmic AI study workspace for quizzes, 3D flashcards, and grounded midnight tutoring.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} ${spaceGrotesk.variable} ${caveat.variable} h-full antialiased dark`}
      suppressHydrationWarning
    >
      <head>
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200"
        />
      </head>
      <body className="min-h-full bg-background text-foreground font-sans selection:bg-primary selection:text-primary-foreground">
        <ThemeProvider>
          <StudyProvider>
            <div className="min-h-screen flex bg-background text-foreground">
              {/* Fixed Left Sidebar */}
              <AppSidebar />

              {/* Main Content Pane with fixed Top Header */}
              <div className="flex-1 flex flex-col lg:pl-72 min-w-0 transition-all duration-300">
                <AppHeader />
                <main className="flex-1 pt-16 min-h-[calc(100vh-4rem)]">
                  {children}
                </main>
              </div>
            </div>
            <Toaster />
          </StudyProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
