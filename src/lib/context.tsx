"use client";

import { createContext, useContext, useState, type ReactNode } from "react";
import type { Exam, ExamResult, Material, Quiz, QuizResult } from "./api";

interface ModelOption {
  provider: string;
  name: string;
  label: string;
}

function loadModel(): ModelOption {
  if (typeof window === "undefined")
    return { provider: "gemini", name: "gemini-3-flash-preview", label: "Gemini" };
  try {
    const raw = localStorage.getItem("spidey-model");
    if (raw) {
      const m = JSON.parse(raw);
      // auto-migrate old deprecated model
      if (m.name === "gemini-2.5-flash" || m.name === "gemini-2.0-flash" || m.name === "gemini-2.5-flash-lite") {
        m.name = "gemini-3-flash-preview";
        m.label = "Gemini";
        localStorage.setItem("spidey-model", JSON.stringify(m));
      }
      return m;
    }
  } catch {
    // fall through
  }
  return { provider: "gemini", name: "gemini-3-flash-preview", label: "Gemini" };
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

export interface ExamConfig {
  difficulty: "easy" | "medium" | "hard";
  questionCount: number;
  durationMinutes: number;
  title: string;
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
  examConfig: ExamConfig;
  setExamConfig: (c: ExamConfig) => void;
  activeExam: Exam | null;
  setActiveExam: (e: Exam | null) => void;
  examResult: ExamResult | null;
  setExamResult: (r: ExamResult | null) => void;
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
  const [examConfig, setExamConfig] = useState<ExamConfig>({
    difficulty: "medium",
    questionCount: 8,
    durationMinutes: 20,
    title: "",
  });
  const [activeExam, setActiveExam] = useState<Exam | null>(null);
  const [examResult, setExamResult] = useState<ExamResult | null>(null);
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
        examConfig,
        setExamConfig,
        activeExam,
        setActiveExam,
        examResult,
        setExamResult,
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