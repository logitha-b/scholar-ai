import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useStore } from '../../store/useStore'
import { LANGS, T } from '../../utils/translations'
import toast from 'react-hot-toast'

const NAV = [
  { path: '/learning',      icon: '🎯' },
  { path: '/resources',     icon: '📚' },
  { path: '/placement',     icon: '🏢' },
  { path: '/aptitude',      icon: '🧮' },
  { path: '/communication', icon: '🎤' },
  { path: '/dashboard',     icon: '📊' },
]

export default function Header() {
  const { user, logout, language, setLanguage } = useStore()
  const t = T[language]
  const navigate = useNavigate()
  const location = useLocation()
  const [dropOpen, setDropOpen] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-3">

        {/* Logo */}
        <button onClick={() => navigate(user?.role === 'admin' ? '/admin' : '/')}
          className="flex items-center gap-2 shrink-0">
          <div className="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-sm">✦</div>
          <span className="text-lg font-extrabold text-indigo-600 hidden sm:block">Scholr AI</span>
        </button>

        {/* Desktop nav - student only */}
        {user?.role === 'student' && (
          <nav className="hidden lg:flex items-center gap-0.5 flex-1 justify-center">
            {NAV.map((r, i) => (
              <button key={r.path} onClick={() => navigate(r.path)}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition-all
                  ${location.pathname === r.path
                    ? 'bg-indigo-50 text-indigo-700 font-semibold'
                    : 'text-slate-600 hover:text-indigo-600 hover:bg-slate-50'}`}>
                {r.icon} {t.nav[i]}
              </button>
            ))}
          </nav>
        )}
        {user?.role === 'admin' && (
          <div className="flex-1 flex justify-center">
            <span className="text-sm font-semibold text-amber-700 bg-amber-50 border border-amber-200 px-3 py-1 rounded-full">🛡 Admin Panel</span>
          </div>
        )}

        {/* Right controls */}
        <div className="flex items-center gap-2 shrink-0">
          <select value={language} onChange={e => setLanguage(e.target.value)}
            className="hidden sm:block bg-slate-50 border border-slate-200 text-slate-700 text-xs px-2 py-1.5 rounded-lg cursor-pointer focus:outline-none focus:border-indigo-400">
            {Object.entries(LANGS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>

          {user && (
            <div className="relative">
              <button onClick={() => setDropOpen(!dropOpen)}
                className="flex items-center gap-2 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-xl text-sm hover:bg-indigo-50 hover:border-indigo-300 transition-all">
                <div className="w-7 h-7 bg-indigo-600 rounded-full flex items-center justify-center text-xs font-bold text-white">
                  {user.name?.[0]?.toUpperCase()}
                </div>
                <span className="hidden md:block text-slate-700 font-medium max-w-24 truncate">{user.name?.split(' ')[0]}</span>
                <span className="text-slate-400 text-xs">▾</span>
              </button>
              {dropOpen && (
                <div className="absolute right-0 top-full mt-2 w-52 bg-white border border-slate-200 rounded-2xl shadow-xl z-50 overflow-hidden">
                  <div className="px-4 py-3 bg-slate-50 border-b border-slate-100">
                    <div className="text-sm font-semibold text-slate-800">{user.name}</div>
                    <div className="text-xs text-slate-500">{user.email}</div>
                    <span className={`mt-1 inline-block text-xs font-semibold px-2 py-0.5 rounded-full ${user.role === 'admin' ? 'bg-amber-100 text-amber-700' : 'bg-indigo-100 text-indigo-700'}`}>{user.role}</span>
                  </div>
                  <button onClick={() => { navigate(user.role === 'admin' ? '/admin' : '/dashboard'); setDropOpen(false) }}
                    className="w-full text-left px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 transition-all">📊 {t.dashTitle}</button>
                  <button onClick={() => { logout(); toast.success('Logged out'); navigate('/login') }}
                    className="w-full text-left px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-all border-t border-slate-100">🚪 {t.logout}</button>
                </div>
              )}
            </div>
          )}
          <button className="lg:hidden text-slate-600 p-1.5 rounded-lg hover:bg-slate-100" onClick={() => setMobileOpen(!mobileOpen)}>☰</button>
        </div>
      </div>

      {/* Mobile nav */}
      {mobileOpen && user?.role === 'student' && (
        <div className="lg:hidden border-t border-slate-100 bg-white px-4 py-3 grid grid-cols-3 gap-2">
          {NAV.map((r, i) => (
            <button key={r.path} onClick={() => { navigate(r.path); setMobileOpen(false) }}
              className={`flex flex-col items-center gap-1 p-2 rounded-xl text-xs font-medium transition-all
                ${location.pathname === r.path ? 'bg-indigo-50 text-indigo-700' : 'text-slate-500 hover:bg-slate-50'}`}>
              <span className="text-xl">{r.icon}</span>{t.nav[i]}
            </button>
          ))}
        </div>
      )}
    </header>
  )
}
