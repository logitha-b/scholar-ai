import axios from 'axios'
import toast from 'react-hot-toast'

const api = axios.create({ baseURL: '/api' })

// Attach token to every request
api.interceptors.request.use(config => {
  const token = localStorage.getItem('scholr_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Handle 401 globally
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('scholr_token')
      localStorage.removeItem('scholr_user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (email, password) => {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    return api.post('/auth/login', form, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
  },
  getMe: () => api.get('/auth/me'),
}

// ── Profile ───────────────────────────────────────────────────────────────────
export const profileAPI = {
  update: (data) => api.put('/profile/update', data),
  dashboard: () => api.get('/profile/dashboard'),
  saveTestResult: (data) => api.post('/profile/test-result', data),
  logSession: (module, minutes) => api.post(`/profile/session?module=${module}&duration_minutes=${minutes}`),
}

// ── Learning ──────────────────────────────────────────────────────────────────
export const learningAPI = {
  uploadMarksheet: (file) => {
    const fd = new FormData(); fd.append('file', file)
    return api.post('/learning/upload/marksheet', fd)
  },
  uploadMaterial: (file) => {
    const fd = new FormData(); fd.append('file', file)
    return api.post('/learning/upload/material', fd)
  },
  getMaterials: () => api.get('/learning/materials'),
  generatePlan: (data) => api.post('/learning/study-plan', data),
  generateNotes: (data) => api.post('/learning/notes', data),
  generateFlashcards: (material_id, count = 15) => api.post('/learning/flashcards', { material_id, count }),
  getFlashcards: (material_id) => api.get(`/learning/flashcards/${material_id}`),
  generateQA: (material_id, count = 10, language = 'en') => api.post('/learning/qa', { material_id, count, language }),
  solveDoubt: (question, material_id, language) => api.post('/learning/doubt', { question, material_id, language }),
  generateMockTest: (material_id) => api.post(`/learning/mock-test?material_id=${material_id}`),
  saveTestResult: (data) => api.post('/learning/test-result', data),
}

// ── Communication ─────────────────────────────────────────────────────────────
export const commAPI = {
  speakingFeedback: (transcript, topic, language) =>
    api.post('/communication/speaking-feedback', { transcript, topic, language }),
  writingFeedback: (text, mode, language) =>
    api.post('/communication/writing-feedback', { text, mode, language }),
}

// ── Placement ─────────────────────────────────────────────────────────────────
export const placementAPI = {
  getCompanies: () => api.get('/placement/companies'),
  getCompany: (id) => api.get(`/placement/companies/${id}`),
  analyseResume: (resume_text, language = 'en') =>
    api.post(`/placement/resume-analyse?language=${language}`, { resume_text }),
  uploadResume: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/placement/upload-resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  simulateInterview: (company_name, round_type = 'technical', difficulty = 'medium', resume_text = '', language = 'en') =>
    api.post(`/placement/interview-simulate?language=${language}`, { company_name, round_type, difficulty, resume_text }),
  getInterviewModelAnswer: (question, language = 'en') =>
    api.post(`/placement/interview-model-answer?question=${encodeURIComponent(question)}&language=${language}`),
  gradeInterview: (questions, answers, language = 'en') =>
    api.post(`/placement/interview-grade?language=${language}`, { questions, answers }),
}

// ── Resources ─────────────────────────────────────────────────────────────────
export const resourcesAPI = {
  getBooks: (class_level) => api.get(`/resources/books?class_level=${class_level}`),
  getAllBooks: () => api.get('/resources/books/all-classes'),
  getPYQ: (subject, chapter, language) =>
    api.post('/resources/pyq', null, { params: { subject, chapter, language } }),
}

// ── Aptitude ──────────────────────────────────────────────────────────────────
export const aptitudeAPI = {
  getQuestions: (topic, difficulty) =>
    api.get('/aptitude/questions', { params: { topic, difficulty } }),
  getCoding: (difficulty, topic) =>
    api.get('/aptitude/coding', { params: { difficulty, topic } }),
}

// ── Admin ─────────────────────────────────────────────────────────────────────
export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  getStudents: () => api.get('/admin/students'),
  toggleStudent: (id) => api.put(`/admin/students/${id}/toggle`),
  deleteStudent: (id) => api.delete(`/admin/students/${id}`),
  getAnnouncements: () => api.get('/admin/announcements'),
  createAnnouncement: (data) => api.post('/admin/announcements', data),
  deleteAnnouncement: (id) => api.delete(`/admin/announcements/${id}`),
}

export default api
