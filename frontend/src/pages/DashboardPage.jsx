import { useEffect, useState } from 'react'
import { useStore } from '../store/useStore'
import { T } from '../utils/translations'
import { profileAPI } from '../utils/api'
import { StatCard, ProgressBar, EmptyState, Spinner } from '../components/shared/UI'

export default function DashboardPage() {
  const { user, language } = useStore()
  const t = T[language]
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    profileAPI.dashboard()
      .then(r => setData(r.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false))
  }, [])

  const profile = data?.profile || {}
  const subjects = profile.subjects || []
  const recentTests = data?.recent_tests || []
  const weeklySessions = data?.weekly_study || []

  // demo weekly bar data if no sessions
  const weekDays = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
  const weekData = weekDays.map((d, i) => {
    const s = weeklySessions[i]
    return { day: d, minutes: s ? s.minutes : [40,55,30,70,65,80,45][i] }
  })
  const maxMin = Math.max(...weekData.map(w => w.minutes), 1)

  const todayTasks = data?.today_tasks || []

  if (loading) return (
    <div className="flex items-center justify-center h-64 gap-3">
      <Spinner size={24} /> <span className="text-slate-500">Loading dashboard...</span>
    </div>
  )

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="section-title">📊 {t.dashTitle}</h1>
        <p className="section-sub">Welcome back, <span className="font-semibold text-indigo-600">{user?.name}</span> 👋</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard icon="🔥" value={profile.streak || 0} label={t.streak} color="orange" />
        <StatCard icon="✅" value={profile.total_questions_solved || 0} label={t.solved} color="green" />
        <StatCard icon="🎯" value={`${profile.avg_score || 0}%`} label={t.avgScore} color="indigo" />
        <StatCard icon="📈" value={`+${recentTests.length ? Math.round((recentTests[0]?.score_pct||0) - (recentTests[recentTests.length-1]?.score_pct||0)) : 0}%`} label={t.improvement} color="purple" />
      </div>

      <div className="grid lg:grid-cols-2 gap-5 mb-5">
        {/* Subject Progress */}
        <div className="card">
          <h3 className="font-bold text-slate-800 mb-4">📚 Subject Progress</h3>
          {subjects.length === 0 ? (
            <EmptyState icon="📋" message="Upload your marksheet to see subject progress" />
          ) : (
            <div className="space-y-3">
              {subjects.map(s => (
                <div key={s.name}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium text-slate-700">{s.name}</span>
                    <span className={`font-bold text-xs ${s.score<60?'text-red-600':s.score<75?'text-amber-600':'text-green-600'}`}>{s.score}%</span>
                  </div>
                  <ProgressBar value={s.score} />
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Weekly Activity */}
        <div className="card">
          <h3 className="font-bold text-slate-800 mb-4">📅 Weekly Activity (mins studied)</h3>
          <div className="flex items-end gap-2 h-36">
            {weekData.map((w, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-1">
                <div className="text-xs text-slate-500">{w.minutes}</div>
                <div className="w-full rounded-t-lg transition-all duration-700"
                  style={{ height: `${(w.minutes/maxMin)*100}%`, minHeight:4,
                    background: i === new Date().getDay()-1 ? '#4f46e5' : '#e0e7ff' }} />
                <div className="text-xs text-slate-500">{w.day}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-2 gap-5">
        {/* Today's Plan */}
        <div className="card">
          <h3 className="font-bold text-slate-800 mb-4">🗓 Today's Study Schedule</h3>
          <div className="space-y-1">
            {todayTasks.map((task, i) => (
              <div key={i} className={`flex items-center gap-3 p-3 rounded-xl transition-all
                ${task.done ? 'opacity-60' : 'hover:bg-slate-50'}`}>
                <div className="text-xl">{task.done ? '✅' : '⬜'}</div>
                <div className="w-20 text-xs text-slate-400 shrink-0">{task.time}</div>
                <div className="flex-1">
                  <div className={`text-sm font-medium ${task.done ? 'line-through text-slate-400' : 'text-slate-800'}`}>
                    {task.subject}
                  </div>
                  <div className="text-xs text-slate-500">{task.topic} · {task.duration}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Tests */}
        <div className="card">
          <h3 className="font-bold text-slate-800 mb-4">📝 Recent Test Results</h3>
          {recentTests.length === 0 ? (
            <EmptyState icon="📝" message="No tests taken yet" sub="Complete mock tests to see results here" />
          ) : (
            <div className="space-y-3">
              {recentTests.map((test, i) => (
                <div key={i} className="flex items-center gap-3 p-3 bg-slate-50 rounded-xl">
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold
                    ${test.score_pct>=70?'bg-green-100 text-green-700':test.score_pct>=50?'bg-amber-100 text-amber-700':'bg-red-100 text-red-700'}`}>
                    {Math.round(test.score_pct)}%
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-semibold text-slate-800">{test.topic}</div>
                    <div className="text-xs text-slate-500">{test.correct}/{test.total} correct · {new Date(test.date).toLocaleDateString()}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
