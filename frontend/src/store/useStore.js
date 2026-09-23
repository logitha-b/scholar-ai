import { create } from 'zustand'

export const useStore = create((set, get) => ({
  // Auth
  user: JSON.parse(localStorage.getItem('scholr_user') || 'null'),
  token: localStorage.getItem('scholr_token') || null,
  language: localStorage.getItem('scholr_lang') || 'en',

  setAuth: (user, token) => {
    localStorage.setItem('scholr_user', JSON.stringify(user))
    localStorage.setItem('scholr_token', token)
    set({ user, token })
  },
  logout: () => {
    localStorage.removeItem('scholr_user')
    localStorage.removeItem('scholr_token')
    set({ user: null, token: null })
  },
  setLanguage: (lang) => {
    localStorage.setItem('scholr_lang', lang)
    set({ language: lang })
  },

  // Materials
  materials: [],
  setMaterials: (materials) => set({ materials }),

  // Dashboard data
  dashboardData: null,
  setDashboardData: (data) => set({ dashboardData: data }),
}))
