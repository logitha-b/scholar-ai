import ReactMarkdown from 'react-markdown'

export function Spinner({ size = 18 }) {
  return <span className="spinner" style={{ width: size, height: size }} />
}

export function Badge({ type = 'purple', children }) {
  const m = { easy:'badge-easy', medium:'badge-medium', hard:'badge-hard',
    purple:'badge-purple', blue:'badge-blue', green:'badge-green', red:'badge-red', yellow:'badge-yellow' }
  return <span className={m[type] || m.purple}>{children}</span>
}

export function ProgressBar({ value, max = 100 }) {
  const pct = Math.min(100, (value / max) * 100)
  const color = pct < 60 ? 'bg-red-400' : pct < 75 ? 'bg-amber-400' : 'bg-green-500'
  return <div className="progress-bar"><div className={`progress-fill ${color}`} style={{ width: `${pct}%` }} /></div>
}

export function AIOutput({ text }) {
  if (!text) return null
  return (
    <div className="ai-output">
      <ReactMarkdown components={{
        h2: ({children}) => <h2 className="font-bold text-slate-800 text-base mt-4 mb-1">{children}</h2>,
        h3: ({children}) => <h3 className="font-semibold text-slate-800 text-sm mt-3 mb-1">{children}</h3>,
        ul: ({children}) => <ul className="list-disc ml-4 space-y-1">{children}</ul>,
        li: ({children}) => <li className="text-slate-700">{children}</li>,
        strong: ({children}) => <strong className="font-semibold text-slate-800">{children}</strong>,
        p: ({children}) => <p className="mb-2 text-slate-700">{children}</p>,
      }}>{text}</ReactMarkdown>
    </div>
  )
}

export function TabBar({ tabs, active, onChange }) {
  return (
    <div className="flex border-b border-slate-200 mb-5 overflow-x-auto">
      {tabs.map(tab => (
        <button key={tab.key} className={`tab-btn ${active === tab.key ? 'active' : ''}`} onClick={() => onChange(tab.key)}>
          {tab.icon} {tab.label}
        </button>
      ))}
    </div>
  )
}

export function Modal({ open, onClose, title, children }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50 p-4 backdrop-blur-sm"
         onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-2xl w-full max-h-[88vh] overflow-y-auto shadow-2xl">
        <div className="flex justify-between items-center mb-5">
          <h3 className="text-lg font-bold text-slate-800">{title}</h3>
          <button onClick={onClose} className="w-8 h-8 flex items-center justify-center rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-700 transition-all">✕</button>
        </div>
        {children}
      </div>
    </div>
  )
}

export function StatCard({ icon, value, label, color = 'indigo' }) {
  const colors = {
    indigo: 'bg-indigo-50 text-indigo-600 border-indigo-100',
    green:  'bg-green-50  text-green-600  border-green-100',
    blue:   'bg-blue-50   text-blue-600   border-blue-100',
    orange: 'bg-orange-50 text-orange-600 border-orange-100',
    purple: 'bg-purple-50 text-purple-600 border-purple-100',
    red:    'bg-red-50    text-red-600    border-red-100',
  }
  const cls = colors[color] || colors.indigo
  return (
    <div className={`rounded-2xl p-5 text-center border ${cls}`}>
      <div className="text-3xl mb-2">{icon}</div>
      <div className={`text-3xl font-bold ${cls.split(' ')[1]}`}>{value}</div>
      <div className="text-xs text-slate-500 mt-1 font-medium">{label}</div>
    </div>
  )
}

export function EmptyState({ icon, message, sub }) {
  return (
    <div className="text-center py-14">
      <div className="text-5xl mb-3">{icon}</div>
      <div className="font-semibold text-slate-700 text-base">{message}</div>
      {sub && <div className="text-slate-400 text-sm mt-1">{sub}</div>}
    </div>
  )
}

export function FileUploadBox({ label, accept, onFile, fileName, icon = '📄' }) {
  return (
    <div>
      {label && <label className="label">{label}</label>}
      <label className="flex items-center gap-3 bg-slate-50 border-2 border-dashed border-slate-300 rounded-xl p-4 cursor-pointer hover:border-indigo-400 hover:bg-indigo-50 transition-all group">
        <span className="text-3xl">{icon}</span>
        <div>
          <div className="text-sm font-semibold text-indigo-600 group-hover:text-indigo-700">{fileName || 'Click to upload'}</div>
          <div className="text-xs text-slate-400 mt-0.5">{accept}</div>
        </div>
        <input type="file" accept={accept} className="hidden" onChange={e => e.target.files[0] && onFile(e.target.files[0])} />
      </label>
    </div>
  )
}

export function ScoreCircle({ score, total }) {
  const pct = total > 0 ? Math.round((score / total) * 100) : 0
  const color = pct >= 70 ? '#16a34a' : pct >= 50 ? '#d97706' : '#dc2626'
  const r = 44, circ = 2 * Math.PI * r
  return (
    <div className="flex flex-col items-center">
      <svg width="110" height="110" viewBox="0 0 110 110">
        <circle cx="55" cy="55" r={r} fill="none" stroke="#e2e8f0" strokeWidth="9" />
        <circle cx="55" cy="55" r={r} fill="none" stroke={color} strokeWidth="9"
          strokeDasharray={circ} strokeDashoffset={circ * (1 - pct / 100)}
          strokeLinecap="round" transform="rotate(-90 55 55)"
          style={{ transition: 'stroke-dashoffset 1s ease' }} />
        <text x="55" y="55" textAnchor="middle" dominantBaseline="middle" fill={color} fontSize="20" fontWeight="bold">{pct}%</text>
      </svg>
      <div className="text-slate-500 text-sm">{score}/{total} correct</div>
    </div>
  )
}
