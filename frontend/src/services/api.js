import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.detail || 'Something went wrong'
    return Promise.reject(new Error(message))
  }
)

// ─────────────────────────────────────────────
// CIVIC TWIN APIs
// ─────────────────────────────────────────────

export const civicTwinAPI = {
  create: (userInput, language = 'en') =>
    api.post('/twin/create', { user_input: userInput, language }),

  get: (sessionId) =>
    api.get(`/twin/${sessionId}`),

  update: (sessionId, newInput) =>
    api.put('/twin/update', { session_id: sessionId, new_input: newInput }),

  query: (query, sessionId = null, language = 'en') =>
    api.post('/twin/query', { query, session_id: sessionId, language }),

  checkEligibility: (sessionId) =>
    api.get(`/twin/${sessionId}/eligibility`),

  delete: (sessionId) =>
    api.delete(`/twin/${sessionId}`),
}

// ─────────────────────────────────────────────
// JOURNEY APIs
// ─────────────────────────────────────────────

export const journeyAPI = {
  create: (sessionId) =>
    api.post('/journey/create', { session_id: sessionId }),

  get: (sessionId) =>
    api.get(`/journey/${sessionId}`),

  getSummary: (sessionId) =>
    api.get(`/journey/${sessionId}/summary`),

  getNextSteps: (sessionId) =>
    api.get(`/journey/${sessionId}/next-steps`),

  updateStep: (sessionId, phaseId, stepId, isCompleted) =>
    api.put('/journey/step/update', {
      session_id: sessionId,
      phase_id: phaseId,
      step_id: stepId,
      is_completed: isCompleted,
    }),

  getDocuments: (sessionId) =>
    api.get(`/journey/${sessionId}/documents`),

  findPollingStation: (sessionId, userAddress = null) =>
    api.post('/journey/polling-station', {
      session_id: sessionId,
      user_address: userAddress,
    }),
}

// ─────────────────────────────────────────────
// MISSION APIs
// ─────────────────────────────────────────────

export const missionAPI = {
  start: (sessionId, missionNumber) =>
    api.post('/mission/start', {
      session_id: sessionId,
      mission_number: missionNumber,
    }),

  submitAnswer: (sessionId, missionId, questionId, userAnswer, correctAnswer, explanation) =>
    api.post('/mission/answer', {
      session_id: sessionId,
      mission_id: missionId,
      question_id: questionId,
      user_answer: userAnswer,
      correct_answer: correctAnswer,
      explanation,
    }),

  runScenario: (sessionId, scenario) =>
    api.post('/mission/scenario', {
      session_id: sessionId,
      scenario,
    }),

  simulatePollDay: (sessionId) =>
    api.post('/mission/poll-day-simulation', {
      session_id: sessionId,
    }),

  getProgress: (sessionId) =>
    api.get(`/mission/${sessionId}/progress`),

  completeMission: (sessionId, missionId) =>
    api.post(`/mission/${sessionId}/complete/${missionId}`),
}

// ─────────────────────────────────────────────
// ASSESSMENT APIs
// ─────────────────────────────────────────────

export const assessmentAPI = {
  calculateReadiness: (sessionId) =>
    api.post('/assessment/readiness', { session_id: sessionId }),

  getScore: (sessionId) =>
    api.get(`/assessment/${sessionId}/score`),

  calculateMissionScore: (sessionId, missionResults) =>
    api.post('/assessment/mission-score', {
      session_id: sessionId,
      mission_results: missionResults,
    }),

  generateProof: (sessionId) =>
    api.post('/assessment/proof-of-readiness', { session_id: sessionId }),

  getPredictions: (sessionId) =>
    api.get(`/assessment/${sessionId}/predictions`),

  getLogs: (sessionId) =>
    api.get(`/assessment/${sessionId}/logs`),
}

// ─────────────────────────────────────────────
// TRANSLATION API
// ─────────────────────────────────────────────

export const translationAPI = {
  translate: (text, targetLanguage, sourceLanguage = 'en') =>
    api.post('/translate', {
      text,
      target_language: targetLanguage,
      source_language: sourceLanguage,
    }),

  translateBatch: (texts, targetLanguage, sourceLanguage = 'en') =>
    api.post('/translate/batch', {
      texts,
      target_language: targetLanguage,
      source_language: sourceLanguage,
    }),
}

// ─────────────────────────────────────────────
// AUTH APIs
// ─────────────────────────────────────────────

export const authAPI = {
  verifyToken: (idToken) =>
    api.post('/auth/verify', { id_token: idToken }),

  linkSession: (sessionId, idToken) =>
    api.post('/auth/link-session', {
      session_id: sessionId,
      id_token: idToken,
    }),

  getUserProfile: (userId) =>
    api.get(`/auth/profile/${userId}`),

  getUserSessions: (userId) =>
    api.get(`/auth/sessions/${userId}`),

  logout: (userId) =>
    api.delete(`/auth/logout/${userId}`),
}

export default api