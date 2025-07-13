export interface LessonTopic {
  title: string;
  duration_minutes: number;
  description: string;
}

export interface LessonPlan {
  topic: string;
  grade_level: string;
  duration_minutes: number;
  learning_objectives: string[];
  materials_needed: string[];
  lesson_overview: LessonTopic[];
  exercises: string[];
  assessment: string[];
  urls: string[];
}

export interface LessonPlanRequest {
  topic: string;
  grade_level?: string;
}

export interface LessonPlanResponse {
  success: boolean;
  lesson_plan?: LessonPlan;
  error?: string;
  message: string;
} 