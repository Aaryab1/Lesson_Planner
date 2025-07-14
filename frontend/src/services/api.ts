import axios from 'axios';
import { LessonPlanRequest, LessonPlanResponse } from '../types/lessonPlan';

const API_BASE_URL = 'https://lesson-planner-backend.onrender.com/';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const lessonPlanApi = {
  createLessonPlan: async (request: LessonPlanRequest): Promise<LessonPlanResponse> => {
    try {
      const response = await api.post<LessonPlanResponse>('/create-lesson-plan', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.message || 'Failed to create lesson plan');
      }
      throw error;
    }
  },

  checkHealth: async (): Promise<{ status: string; message: string }> => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Backend server is not responding');
    }
  },
}; 