import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { authAPI } from '../../utils/api'
import { useStore } from '../../store/useStore'
import { T } from '../../utils/translations'
import { Spinner } from '../shared/UI'
import toast from 'react-hot-toast'

function AuthLayout({ children, title, sub }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-indigo-600 rounded-2xl flex items-center justify-center text-3xl text-white mx-auto mb-4 shadow-lg">✦</div>
          <h1 className="text-3xl font-extrabold text-indigo-600">Scholr AI</h1>
          <p className="text-slate-500 text-sm mt-1">Your AI-powered study companion</p>
        </div>
        <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">
          <h2 className="text-xl font-bold text-slate-800 mb-1">{title}</h2>
          {sub && <p className="text-sm text-slate-500 mb-6">{sub}</p>}
          {children}
        </div>
      </div>
    </div>
  )
}

export function LoginPage() {
  const [form, setForm] = useState({ email:'', password:'' })
  const [loading, setLoading] = useState(false)
  const { setAuth, language } = useStore()
  const t = T[language]
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault(); setLoading(true)
    try {
      const res = await authAPI.login(form.email, form.password)
      setAuth(res.data.user, res.data.access_token)
      toast.success(`Welcome back, ${res.data.user.name}!`)
      navigate(res.data.user.role === 'admin' ? '/admin' : '/')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Login failed. Check your credentials.')
    } finally { setLoading(false) }
  }

  return (
    <AuthLayout title={t.loginTitle} sub="Sign in to continue learning">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="label">{t.email}</label>
          <input className="input" type="email" required placeholder="you@example.com"
            value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
        </div>
        <div>
          <label className="label">{t.password}</label>
          <input className="input" type="password" required placeholder="••••••••"
            value={form.password} onChange={e => setForm({...form, password: e.target.value})} />
        </div>
        <button type="submit" className="btn-primary w-full justify-center py-3" disabled={loading}>
          {loading ? <Spinner /> : null} {t.login}
        </button>
      </form>
      <p className="text-center text-slate-500 text-sm mt-5">
        {t.dontHave}{' '}
        <Link to="/register" className="text-indigo-600 hover:text-indigo-700 font-semibold">{t.register}</Link>
      </p>
    </AuthLayout>
  )
}

export function RegisterPage() {
  const [form, setForm] = useState({ name:'', email:'', password:'', role:'student', college:'', class_level:'' })
  const [loading, setLoading] = useState(false)
  const { setAuth, language } = useStore()
  const t = T[language]
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault(); setLoading(true)
    try {
      const res = await authAPI.register(form)
      setAuth(res.data.user, res.data.access_token)
      toast.success('Account created successfully!')
      navigate(res.data.user.role === 'admin' ? '/admin' : '/')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed')
    } finally { setLoading(false) }
  }

  return (
    <AuthLayout title={t.registerTitle} sub="Join thousands of students learning smarter">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="label">{t.name}</label>
          <input className="input" required placeholder="Your full name"
            value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
        </div>
        <div>
          <label className="label">{t.email}</label>
          <input className="input" type="email" required placeholder="you@example.com"
            value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
        </div>
        <div>
          <label className="label">{t.password}</label>
          <input className="input" type="password" required placeholder="Min 8 characters"
            value={form.password} onChange={e => setForm({...form, password: e.target.value})} />
        </div>
        <div>
          <label className="label">{t.role}</label>
          <div className="grid grid-cols-2 gap-2">
            {[{val:'student',icon:'🎓',label:t.student},{val:'admin',icon:'🛡',label:t.admin}].map(r => (
              <button key={r.val} type="button" onClick={() => setForm({...form, role: r.val})}
                className={`p-3 border-2 rounded-xl text-sm font-semibold transition-all flex items-center justify-center gap-2
                  ${form.role === r.val ? 'border-indigo-500 bg-indigo-50 text-indigo-700' : 'border-slate-200 bg-white text-slate-600 hover:border-indigo-300'}`}>
                {r.icon} {r.label}
              </button>
            ))}
          </div>
        </div>
        {form.role === 'student' && (
          <>
            <div>
              <label className="label">{t.college}</label>
              <input className="input" placeholder="e.g. RMK Engineering College"
                value={form.college} onChange={e => setForm({...form, college: e.target.value})} />
            </div>
            <div>
              <label className="label">{t.classLevel}</label>
              <select className="input" value={form.class_level} onChange={e => setForm({...form, class_level: e.target.value})}>
                <option value="">Select your class / year</option>
                <optgroup label="School">
                  {['10','11','12'].map(c => <option key={c} value={`school_${c}`}>Class {c}</option>)}
                </optgroup>
                <optgroup label="College">
                  {['1','2','3','4'].map(y => <option key={y} value={`college_${y}`}>Year {y}</option>)}
                </optgroup>
              </select>
            </div>
          </>
        )}
        <button type="submit" className="btn-primary w-full justify-center py-3" disabled={loading}>
          {loading ? <Spinner /> : null} {t.register}
        </button>
      </form>
      <p className="text-center text-slate-500 text-sm mt-5">
        {t.alreadyHave}{' '}
        <Link to="/login" className="text-indigo-600 hover:text-indigo-700 font-semibold">{t.login}</Link>
      </p>
    </AuthLayout>
  )
}
