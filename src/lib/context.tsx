"use client";

import { createContext, useContext, useState, type ReactNode } from "react";
import type { Material, Quiz, QuizResult } from "./api";

interface ModelOption {
  provider: string;
  name: string;
  label: string;
}

function loadModel(): ModelOption {
  if (typeof window === "undefined")
    return { provider: "gemini", name: "gemini-2.5-flash", label: "Gemini" };
  try {
    const raw = localStorage.getItem("spidey-model");
    if (raw) return JSON.parse(raw);
  } catch {
    // fall through
  }
  return { provider: "gemini", name: "gemini-2.5-flash", label: "Gemini" };
}

function saveModel(m: ModelOption) {
  try {
    localStorage.setItem("spidey-model", JSON.stringify(m));
  } catch {
    // ignore
  }
}

interface QuizConfig {
  difficulty: "easy" | "medium" | "hard";
  questionCount: number;
  timerEnabled: boolean;
  timerMinutes: number;
}

interface StudyContextType {
  material: Material | null;
  setMaterial: (m: Material) => void;
  quizConfig: QuizConfig;
  setQuizConfig: (c: QuizConfig) => void;
  activeQuiz: Quiz | null;
  setActiveQuiz: (q: Quiz | null) => void;
  quizResult: QuizResult | null;
  setQuizResult: (r: QuizResult | null) => void;
  model: ModelOption;
  setModel: (m: ModelOption) => void;
}

const StudyContext = createContext<StudyContextType | null>(null);

export function StudyProvider({ children }: { children: ReactNode }) {
  const [material, setMaterial] = useState<Material | null>(null);
  const [quizConfig, setQuizConfig] = useState<QuizConfig>({
    difficulty: "medium",
    questionCount: 5,
    timerEnabled: false,
    timerMinutes: 10,
  });
  const [activeQuiz, setActiveQuiz] = useState<Quiz | null>(null);
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null);
  const [model, setModelState] = useState<ModelOption>(loadModel);

  function setModel(m: ModelOption) {
    setModelState(m);
    saveModel(m);
  }

  return (
    <StudyContext.Provider
      value={{
        material,
        setMaterial,
        quizConfig,
        setQuizConfig,
        activeQuiz,
        setActiveQuiz,
        quizResult,
        setQuizResult,
        model,
        setModel,
      }}
    >
      {children}
    </StudyContext.Provider>
  );
}

export function useStudy() {
  const ctx = useContext(StudyContext);
  if (!ctx) throw new Error("useStudy must be used within StudyProvider");
  return ctx;
}