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
  generated_by: "ai" | "mock" | "quick";
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
  generated_by: "ai" | "mock" | "quick";
  reviews: QuestionReview[];
}

export interface FlashcardOut {
  id: number;
  front: string;
  back: string;
  provider: string;
  model_name: string;
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

export interface StudyNoteSection {
  heading: string;
  content: string;
  bullet_points: string[];
}

export interface StudyNoteKeyConcept {
  term: string;
  definition: string;
}

export interface StudyNotes {
  id: number;
  material_id: number;
  title: string;
  summary: string;
  sections: StudyNoteSection[];
  key_concepts: StudyNoteKeyConcept[];
  generated_by: "ai" | "mock" | "quick";
  provider: string;
  model_name: string;
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

export function getStudyNotes(
  materialId: number
): Promise<StudyNotes | null> {
  return request<StudyNotes | null>(`/study-notes?material_id=${materialId}`);
}

export function generateStudyNotes(
  materialId: number,
  provider: string,
  model_name: string
): Promise<StudyNotes> {
  return request<StudyNotes>("/study-notes", {
    method: "POST",
    body: JSON.stringify({ material_id: materialId, provider, model_name }),
  });
}

export interface TopicPerformance {
  material_id: number;
  title: string;
  quizzes_taken: number;
  questions_answered: number;
  correct: number;
  average_score: number;
  needs_practice: boolean;
}

export interface RecentActivity {
  kind: "quiz" | "flashcards" | "material" | "notes";
  title: string;
  detail: string;
  material_id: number | null;
  created_at: string;
}

export interface ScoreTrendPoint {
  label: string;
  score: number;
  created_at: string;
  material_title: string;
}

export interface Analytics {
  has_activity: boolean;
  materials: number;
  quizzes_completed: number;
  questions_answered: number;
  correct_answers: number;
  incorrect_answers: number;
  average_score: number;
  best_score: number | null;
  flashcards: number;
  flashcards_reviewed: number;
  study_sessions: number;
  days_studied: number;
  topics: TopicPerformance[];
  score_trend: ScoreTrendPoint[];
  recent_activity: RecentActivity[];
}

export function getAnalytics(): Promise<Analytics> {
  return request<Analytics>("/analytics");
}

export function reviewFlashcard(
  cardId: number
): Promise<{ id: number; review_count: number }> {
  return request<{ id: number; review_count: number }>(
    `/flashcards/${cardId}/review`,
    { method: "POST" }
  );
}

export interface ChatMessage {
  id: number;
  material_id: number;
  role: "user" | "assistant";
  content: string;
  generated_by: string;
  created_at: string;
}

export interface ChatReply {
  user_message: ChatMessage;
  assistant_message: ChatMessage;
}

export function getChatMessages(materialId: number): Promise<ChatMessage[]> {
  return request<ChatMessage[]>(`/chat?material_id=${materialId}`);
}

export function sendChatMessage(
  materialId: number,
  content: string,
  provider: string,
  model_name: string
): Promise<ChatReply> {
  return request<ChatReply>("/chat", {
    method: "POST",
    body: JSON.stringify({
      material_id: materialId,
      content,
      provider,
      model_name,
    }),
  });
}

export function clearChat(materialId: number): Promise<void> {
  return request<void>(`/chat?material_id=${materialId}`, {
    method: "DELETE",
  });
}
}