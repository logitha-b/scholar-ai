import { useEffect, useState } from 'react'
import { useStore } from '../store/useStore'
import { T } from '../utils/translations'
import { adminAPI } from '../utils/api'
import { StatCard, Spinner, EmptyState, Modal } from '../components/shared/UI'
import toast from 'react-hot-toast'

export default function AdminPage() {
  const { language } = useStore()
  const t = T[language]
  const [tab, setTab] = useState('stats')
  const [stats, setStats] = useState(null)
  const [students, setStudents] = useState([])
  const [announcements, setAnnouncements] = useState([])
  const [loading, setLoading] = useState(true)
  const [annModal, setAnnModal] = useState(false)
  const [annForm, setAnnForm] = useState({ title:'', content:'' })
  const [search, setSearch] = useState('')

  useEffect(() => {
    Promise.all([
      adminAPI.getStats(),
      adminAPI.getStudents(),
      adminAPI.getAnnouncements(),
    ]).then(([s, st, an]) => {
      setStats(s.data); setStudents(st.data); setAnnouncements(an.data)
    }).catch(() => toast.error('Failed to load admin data'))
    .finally(() => setLoading(false))
  }, [])

  const toggleStudent = async (id) => {
    try {
      const res = await adminAPI.toggleStudent(id)
      setStudents(prev => prev.map(s => s.id === id ? {...s, is_active: res.data.is_active} : s))
      toast.success('Updated')
    } catch { toast.error('Failed') }
  }

  const deleteStudent = async (id) => {
    if (!window.confirm('Delete this student permanently?')) return
    try {
      await adminAPI.deleteStudent(id)
      setStudents(prev => prev.filter(s => s.id !== id))
      toast.success('Student deleted')
    } catch { toast.error('Failed') }
  }

  const postAnnouncement = async () => {
    if (!annForm.title || !annForm.content) return toast.error('Fill all fields')
    try {
      await adminAPI.createAnnouncement(annForm)
      toast.success('Announcement posted!')
      setAnnModal(false)
      setAnnForm({ title:'', content:'' })
      const res = await adminAPI.getAnnouncements()
      setAnnouncements(res.data)
    } catch { toast.error('Failed') }
  }

  const deleteAnn = async (id) => {
    try {
      await adminAPI.deleteAnnouncement(id)
      setAnnouncements(prev => prev.filter(a => a.id !== id))
      toast.success('Deleted')
    } catch { toast.error('Failed') }
  }

  const filteredStudents = students.filter(s =>
    s.name?.toLowerCase().includes(search.toLowerCase()) ||
    s.email?.toLowerCase().includes(search.toLowerCase())
  )

  if (loading) return (
    <div className="flex items-center justify-center h-64 gap-3">
      <Spinner size={24} /><span className="text-slate-500">Loading admin panel...</span>
    </div>
  )

  const TABS = ['stats','students','announcements']
  const TAB_LABELS = { stats:'📊 Stats', students:'👥 Students', announcements:'📢 Announcements' }

  return (
    <div className="max-w-6xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="section-title">🛡 {t.adminDash}</h1>
        <p className="section-sub">Manage students, view platform stats, post announcements</p>
      </div>

      {/* Tab Bar */}
      <div className="flex border-b border-slate-200 mb-6">
        {TABS.map(tb => (
          <button key={tb} onClick={() => setTab(tb)}
            className={`px-5 py-3 text-sm font-semibold border-b-2 transition-all
              ${tab===tb ? 'text-indigo-600 border-indigo-600' : 'text-slate-500 border-transparent hover:text-slate-700'}`}>
            {TAB_LABELS[tb]}
          </button>
        ))}
      </div>

      {/* Stats */}
      {tab === 'stats' && stats && (
        <div>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <StatCard icon="🎓" value={stats.total_students} label={t.totalStudents} color="indigo" />
            <StatCard icon="📁" value={stats.total_materials_uploaded} label="Materials Uploaded" color="blue" />
            <StatCard icon="📝" value={stats.total_tests_taken} label="Tests Taken" color="green" />
            <StatCard icon="🎯" value={`${stats.platform_avg_score}%`} label="Platform Avg Score" color="purple" />
          </div>
          <div className="card">
            <h3 className="font-bold text-slate-800 mb-3">Platform Overview</h3>
            <div className="grid sm:grid-cols-3 gap-4 text-center">
              <div className="p-4 bg-indigo-50 rounded-xl border border-indigo-100">
                <div className="text-2xl font-bold text-indigo-600">{stats.total_students}</div>
                <div className="text-xs text-slate-500 mt-1">Registered Students</div>
              </div>
              <div className="p-4 bg-green-50 rounded-xl border border-green-100">
                <div className="text-2xl font-bold text-green-600">{stats.total_admins}</div>
                <div className="text-xs text-slate-500 mt-1">Admin Users</div>
              </div>
              <div className="p-4 bg-amber-50 rounded-xl border border-amber-100">
                <div className="text-2xl font-bold text-amber-600">{stats.platform_avg_score}%</div>
                <div className="text-xs text-slate-500 mt-1">Average Score</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Students */}
      {tab === 'students' && (
        <div>
          <div className="card mb-4">
            <input className="input" placeholder="Search by name or email..." value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          <div className="card p-0 overflow-hidden">
            <div className="p-4 border-b border-slate-100 flex items-center justify-between">
              <h3 className="font-bold text-slate-800">{t.manageStudents} ({filteredStudents.length})</h3>
            </div>
            {filteredStudents.length === 0 ? (
              <EmptyState icon="👥" message="No students found" />
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-slate-50 text-left">
                      <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase">Student</th>
                      <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase">College</th>
                      <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase">Stats</th>
                      <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase">Status</th>
                      <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredStudents.map(s => (
                      <tr key={s.id} className="border-t border-slate-100 hover:bg-slate-50 transition-all">
                        <td className="px-4 py-3">
                          <div className="font-semibold text-slate-800">{s.name}</div>
                          <div className="text-xs text-slate-500">{s.email}</div>
                        </td>
                        <td className="px-4 py-3 text-xs text-slate-600">{s.college || '—'}</td>
                        <td className="px-4 py-3">
                          <div className="text-xs text-slate-600">🔥 {s.streak} days</div>
                          <div className="text-xs text-slate-600">✅ {s.questions_solved} solved</div>
                          <div className="text-xs text-slate-600">🎯 {s.avg_score}% avg</div>
                        </td>
                        <td className="px-4 py-3">
                          <span className={`text-xs font-semibold px-2 py-1 rounded-full ${s.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                            {s.is_active ? 'Active' : 'Inactive'}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex gap-2">
                            <button onClick={() => toggleStudent(s.id)}
                              className={`text-xs font-semibold px-2.5 py-1 rounded-lg border transition-all
                                ${s.is_active ? 'border-amber-300 text-amber-700 bg-amber-50 hover:bg-amber-100' : 'border-green-300 text-green-700 bg-green-50 hover:bg-green-100'}`}>
                              {s.is_active ? t.deactivate : t.activate}
                            </button>
                            <button onClick={() => deleteStudent(s.id)} className="btn-danger text-xs px-2.5 py-1">
                              {t.deleteUser}
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Announcements */}
      {tab === 'announcements' && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-bold text-slate-800 text-lg">{t.announcements}</h3>
            <button className="btn-primary" onClick={() => setAnnModal(true)}>
              ➕ {t.newAnnouncement}
            </button>
          </div>
          {announcements.length === 0 ? (
            <EmptyState icon="📢" message="No announcements yet" sub="Post one to notify all students" />
          ) : (
            <div className="space-y-3">
              {announcements.map(a => (
                <div key={a.id} className="card flex items-start gap-4">
                  <div className="flex-1">
                    <div className="font-bold text-slate-800">{a.title}</div>
                    <div className="text-sm text-slate-600 mt-1">{a.content}</div>
                    <div className="text-xs text-slate-400 mt-2">{new Date(a.created_at).toLocaleDateString()}</div>
                  </div>
                  <button onClick={() => deleteAnn(a.id)} className="btn-danger btn-sm text-xs shrink-0">Delete</button>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Announcement Modal */}
      <Modal open={annModal} onClose={() => setAnnModal(false)} title={t.newAnnouncement}>
        <div className="space-y-4">
          <div>
            <label className="label">{t.annTitle}</label>
            <input className="input" placeholder="Announcement title..." value={annForm.title} onChange={e => setAnnForm({...annForm, title: e.target.value})} />
          </div>
          <div>
            <label className="label">{t.annContent}</label>
            <textarea className="textarea" rows={5} placeholder="Announcement content..." value={annForm.content} onChange={e => setAnnForm({...annForm, content: e.target.value})} />
          </div>
          <button className="btn-primary w-full justify-center" onClick={postAnnouncement}>
            📢 {t.postAnn}
          </button>
        </div>
      </Modal>
    </div>
  )
}
