const API_BASE = "/api";

export interface Material {
  id: number;
  title: string;
  content: string;
  source_type: "text" | "pdf";
  char_count: number;
  word_count: number;
}

export interface QuizQuestionBrief {
  id: number;
  question: string;
  options: string[];
}

export interface Quiz {
  id: number;
  material_id: number;
  difficulty: string;
  question_count: number;
  timer_enabled: boolean;
  timer_minutes: number;
  generated_by: "ai" | "mock";
  questions: QuizQuestionBrief[];
}

export interface QuestionReview {
  question: string;
  options: string[];
  correct_answer: number;
  user_answer: number | null;
  is_correct: boolean;
  explanation: string;
}

export interface QuizResult {
  result_id: number;
  quiz_id: number;
  score: number;
  total: number;
  percentage: number;
  answers: (number | null)[];
  generated_by: "ai" | "mock";
  reviews: QuestionReview[];
}

export interface FlashcardOut {
  id: number;
  front: string;
  back: string;
}

export interface CreateQuizPayload {
  material_id: number;
  difficulty: "easy" | "medium" | "hard";
  question_count: number;
  timer_enabled: boolean;
  timer_minutes: number;
  provider: string;
  model_name: string;
}

export interface ModelOption {
  provider: string;
  name: string;
  label: string;
}

export function getModels(): Promise<{ providers: ModelOption[] }> {
  return request<{ providers: ModelOption[] }>("/models");
}

async function request<T>(
  path: string,
  init?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers:
      init?.body instanceof FormData
        ? { ...init?.headers }
        : { "Content-Type": "application/json", ...init?.headers },
  });

  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const data = await res.json();
      if (data?.detail) {
        detail = typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail);
      }
    } catch {
      // fall back to the generic message
    }
    throw new Error(detail);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export function createMaterial(
  text: string,
  title?: string
): Promise<Material> {
  return request<Material>("/materials", {
    method: "POST",
    body: JSON.stringify({ title, text }),
  });
}

export function uploadPdf(file: File): Promise<Material> {
  const form = new FormData();
  form.append("file", file);
  return request<Material>("/materials/pdf", {
    method: "POST",
    body: form,
  });
}

export function getMaterial(id: number): Promise<Material> {
  return request<Material>(`/materials/${id}`);
}

export function createQuiz(payload: CreateQuizPayload): Promise<Quiz> {
  return request<Quiz>("/quizzes", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function submitQuiz(
  quizId: number,
  answers: (number | null)[],
  timeTakenSeconds: number
): Promise<QuizResult> {
  return request<QuizResult>(`/quizzes/${quizId}/submit`, {
    method: "POST",
    body: JSON.stringify({ answers, time_taken_seconds: timeTakenSeconds }),
  });
}

export function getFlashcards(materialId: number): Promise<FlashcardOut[]> {
  return request<FlashcardOut[]>(`/flashcards?material_id=${materialId}`);
}

export function generateFlashcards(
  materialId: number,
  provider: string,
  model_name: string
): Promise<FlashcardOut[]> {
  return request<FlashcardOut[]>("/flashcards", {
    method: "POST",
    body: JSON.stringify({ material_id: materialId, provider, model_name }),
  });
}

export interface AudioSummaryOut {
  material_id: number;
  summary_text: string;
  audio_base64: string;
  mime_type: string;
  generated_by: "ai" | "mock";
  provider: string;
  model_name: string;
}

export function generateAudioSummary(
  materialId: number,
  provider: string,
  model_name: string,
  voice_name: string = "Kore",
  language: string = "en"
): Promise<AudioSummaryOut> {
  return request<AudioSummaryOut>("/audio/summary", {
    method: "POST",
    body: JSON.stringify({
      material_id: materialId,
      provider,
      model_name,
      voice_name,
      language,
    }),
  });
}