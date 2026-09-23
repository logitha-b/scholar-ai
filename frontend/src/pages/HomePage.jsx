import { useNavigate } from 'react-router-dom'
import { useStore } from '../store/useStore'
import { T } from '../utils/translations'

const MODULES = [
  { path:'/learning',      icon:'🎯', color:'bg-indigo-500', light:'bg-indigo-50 border-indigo-200 hover:border-indigo-400', desc:'AI notes, flashcards, mock tests & doubt solver' },
  { path:'/resources',     icon:'📚', color:'bg-teal-500',   light:'bg-teal-50 border-teal-200 hover:border-teal-400',     desc:'NCERT, RD Sharma, board previous year questions' },
  { path:'/placement',     icon:'🏢', color:'bg-rose-500',   light:'bg-rose-50 border-rose-200 hover:border-rose-400',     desc:'Company-wise aptitude, coding & interview prep' },
  { path:'/aptitude',      icon:'🧮', color:'bg-amber-500',  light:'bg-amber-50 border-amber-200 hover:border-amber-400',  desc:'Top aptitude & coding questions with links' },
  { path:'/communication', icon:'🎤', color:'bg-green-500',  light:'bg-green-50 border-green-200 hover:border-green-400',  desc:'AI speaking & writing trainer with feedback' },
  { path:'/dashboard',     icon:'📊', color:'bg-blue-500',   light:'bg-blue-50 border-blue-200 hover:border-blue-400',     desc:'Progress tracking, streaks & study schedule' },
]

export default function HomePage() {
  const { user, language } = useStore()
  const t = T[language]
  const navigate = useNavigate()

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      {/* Hero */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 bg-indigo-50 border border-indigo-200 text-indigo-700 text-sm font-semibold px-4 py-1.5 rounded-full mb-4">
          ✦ India's AI Study Companion
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-slate-800 mb-3 leading-tight">
          Study Smarter with <span className="text-indigo-600">Scholr AI</span>
        </h1>
        <p className="text-slate-500 text-lg max-w-xl mx-auto">{t.tagline}</p>
        {user && (
          <div className="mt-4 text-slate-500 text-sm">
            Welcome back, <span className="font-semibold text-indigo-600">{user.name}</span> 👋
          </div>
        )}
      </div>

      {/* Module Cards */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {MODULES.map((m, i) => (
          <button key={m.path} onClick={() => navigate(m.path)}
            className={`${m.light} border-2 rounded-2xl p-6 text-left transition-all hover:-translate-y-1 hover:shadow-md duration-200 cursor-pointer`}>
            <div className={`w-14 h-14 ${m.color} rounded-2xl flex items-center justify-center text-3xl mb-4 shadow-sm`}>
              {m.icon}
            </div>
            <div className="font-bold text-slate-800 text-lg mb-1">{t.nav[i]}</div>
            <div className="text-slate-500 text-sm">{m.desc}</div>
          </button>
        ))}
      </div>

      {/* Feature strip */}
      <div className="mt-12 grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
        {[
          { icon:'🌐', label:'6 Languages' },
          { icon:'🤖', label:'AI-Powered' },
          { icon:'🏢', label:'6+ Companies' },
          { icon:'📱', label:'Mobile Ready' },
        ].map(f => (
          <div key={f.label} className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div className="text-2xl mb-1">{f.icon}</div>
            <div className="text-xs font-semibold text-slate-600">{f.label}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
