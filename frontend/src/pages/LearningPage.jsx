import { useState, useEffect, useRef } from 'react'
import { useStore } from '../store/useStore'
import { T } from '../utils/translations'
import { learningAPI, profileAPI } from '../utils/api'
import { Spinner, AIOutput, TabBar, FileUploadBox, Badge, ProgressBar, ScoreCircle, EmptyState } from '../components/shared/UI'
import toast from 'react-hot-toast'

export default function LearningPage() {
  const { user, language, materials, setMaterials } = useStore()
  const t = T[language]
  const [tab, setTab] = useState('planner')

  useEffect(() => {
    learningAPI.getMaterials().then(r => setMaterials(r.data)).catch(() => {})
  }, [])

  const TABS = [
    { key: 'planner',    icon: '📋', label: 'Planner' },
    { key: 'notes',      icon: '📝', label: t.notesTitle },
    { key: 'flashcards', icon: '🃏', label: t.flashcardsTitle },
    { key: 'qa',         icon: '❓', label: t.qnaTitle },
    { key: 'mocktest',   icon: '📝', label: t.mockTest },
    { key: 'doubt',      icon: '💡', label: t.doubtSolver },
  ]

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="section-title">🎯 {t.nav[0]}</h1>
        <p className="section-sub">AI-powered personalised learning engine</p>
      </div>
      <TabBar tabs={TABS} active={tab} onChange={setTab} />
      {tab === 'planner'    && <PlannerTab t={t} lang={language} materials={materials} setMaterials={setMaterials} />}
      {tab === 'notes'      && <NotesTab t={t} lang={language} materials={materials} />}
      {tab === 'flashcards' && <FlashcardsTab t={t} materials={materials} />}
      {tab === 'qa'         && <QATab t={t} lang={language} materials={materials} />}
      {tab === 'mocktest'   && <MockTestTab t={t} lang={language} materials={materials} />}
      {tab === 'doubt'      && <DoubtTab t={t} lang={language} materials={materials} />}
    </div>
  )
}

// -- Planner --
function PlannerTab({ t, lang, materials, setMaterials }) {
  const [marksheetFile, setMarksheetFile] = useState(null)
  const [materialFile, setMaterialFile] = useState(null)
  const [subjects, setSubjects] = useState([])
  const [style, setStyle] = useState('')
  const [hours, setHours] = useState(3)
  const [matId, setMatId] = useState('')
  const [uploadingM, setUploadingM] = useState(false)
  const [uploadingMat, setUploadingMat] = useState(false)
  const [planLoading, setPlanLoading] = useState(false)
  const [plan, setPlan] = useState(null)
  const [activeWeekTab, setActiveWeekTab] = useState('week1')

  const uploadMarksheet = async () => {
    if (!marksheetFile) return toast.error('Select a marksheet file first')
    setUploadingM(true)
    try {
      const res = await learningAPI.uploadMarksheet(marksheetFile)
      setSubjects(res.data.subjects)
      toast.success('Marksheet analysed!')
    } catch { toast.error('Upload failed') }
    finally { setUploadingM(false) }
  }

  const uploadMaterial = async () => {
    if (!materialFile) return toast.error('Select a study material file first')
    setUploadingMat(true)
    try {
      const res = await learningAPI.uploadMaterial(materialFile)
      toast.success(`Material uploaded! ${res.data.topics?.length || 0} topics found.`)
      learningAPI.getMaterials().then(r => setMaterials(r.data))
    } catch { toast.error('Upload failed') }
    finally { setUploadingMat(false) }
  }

  const generatePlan = async () => {
    if (!subjects.length) return toast.error('Upload marksheet first')
    if (!style) return toast.error('Select a learning style')
    setPlanLoading(true)
    try {
      const res = await learningAPI.generatePlan({
        subjects: subjects.map(s => ({ name: s.name, score: s.score })),
        learning_style: style,
        daily_hours: hours,
        language: lang,
        material_id: matId ? +matId : null
      })
      setPlan(res.data)
      setActiveWeekTab('week1')
    } catch { toast.error('Plan generation failed') }
    finally { planLoading(false) }
  }

  const studyMats = (materials || []).filter(m => m.file_type === 'study_material')

  return (
    <div className="space-y-5">
      <div className="card">
        <div className="grid md:grid-cols-2 gap-5 mb-5">
          <div>
            <FileUploadBox label={t.uploadMarksheet} accept=".pdf,.jpg,.jpeg,.png"
              icon="📄" onFile={setMarksheetFile} fileName={marksheetFile?.name} />
            <button className="btn-primary mt-3" onClick={uploadMarksheet} disabled={uploadingM || !marksheetFile}>
              {uploadingM ? <Spinner /> : '🔍'} {t.analyseBtn}
            </button>
          </div>
          <div>
            <FileUploadBox label={t.uploadMaterial} accept=".pdf,.docx,.txt"
              icon="📚" onFile={setMaterialFile} fileName={materialFile?.name} />
            <button className="btn-secondary mt-3" onClick={uploadMaterial} disabled={uploadingMat || !materialFile}>
              {uploadingMat ? <Spinner /> : '⬆️'} Upload Material
            </button>
          </div>
        </div>

        {subjects.length > 0 && (
          <div className="mb-5">
            <label className="label">{t.weakSubjects}</label>
            {subjects.map(s => (
              <div key={s.name} className="flex items-center gap-3 py-2.5 border-b border-dark-600 last:border-0">
                <div className="w-36 text-sm font-semibold text-slate-800 shrink-0">{s.name}</div>
                <div className="flex-1"><ProgressBar value={s.score} /></div>
                <div className={`w-12 text-right text-sm font-bold ${s.score < 60 ? 'text-red-600' : s.score < 75 ? 'text-amber-600' : 'text-green-600'}`}>
                  {s.score}%
                </div>
                <Badge type={s.score < 60 ? 'red' : s.score < 75 ? 'yellow' : 'green'}>
                  {s.score < 60 ? '⚠ Focus' : s.score < 75 ? '📈 Improve' : '✅ Good'}
                </Badge>
              </div>
            ))}
          </div>
        )}

        <div className="grid md:grid-cols-2 gap-5 mb-5">
          <div>
            <label className="label">{t.learningStyle}</label>
            <div className="flex flex-wrap gap-2">
              {t.styles.map(s => (
                <button key={s}
                  className={`px-3 py-2 rounded-xl border text-sm font-medium transition-all
                    ${style === s ? 'border-indigo-500 bg-indigo-500/10 text-indigo-600'
                    : 'border-slate-200 bg-white text-slate-500 hover:border-indigo-500'}`}
                  onClick={() => setStyle(s)}>{s}</button>
              ))}
            </div>
          </div>
          <div>
            <label className="label">{t.timeLabel}: <strong className="text-indigo-600">{hours}h</strong></label>
            <input type="range" min={1} max={12} value={hours} onChange={e => setHours(+e.target.value)}
              className="w-full accent-indigo-500 mt-2" />
            <div className="flex justify-between text-xs text-slate-400 mt-1"><span>1h</span><span>12h</span></div>
          </div>
        </div>

        {studyMats.length > 0 && (
          <div className="mb-5">
            <label className="label">Reference Study Material (Optional)</label>
            <select className="input" value={matId} onChange={e => setMatId(e.target.value)}>
              <option value="">-- None (use general subject curriculum) --</option>
              {studyMats.map(m => <option key={m.id} value={m.id}>{m.original_name}</option>)}
            </select>
            <p className="text-xs text-slate-400 mt-1">If selected, the generated study plan will align study topics and daily targets with the chapters/concepts in the uploaded material.</p>
          </div>
        )}

        <button className="btn-primary" onClick={generatePlan} disabled={planLoading}>
          {planLoading ? <><Spinner /> Generating...</> : `🎯 ${t.analyseBtn}`}
        </button>
      </div>

      {plan && (
        <div className="card space-y-6">
          <h3 className="font-bold text-slate-800 text-xl border-b border-slate-200 pb-3">{t.yourPlan}</h3>
          
          {plan.tips && plan.tips.length > 0 && (
            <div>
              <label className="label">💡 Recommended Study Tips</label>
              <ul className="grid sm:grid-cols-2 gap-2 mt-2">
                {plan.tips?.map((tip, i) => (
                  <li key={i} className="text-slate-700 text-sm bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 flex items-start gap-2">
                    <span className="text-indigo-500 mt-0.5">⭐</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {plan.weekly_plan && (
            <div>
              <label className="label">📅 4-Week Study Schedule</label>
              <div className="flex flex-wrap gap-2 my-3 bg-slate-100 p-1.5 rounded-2xl w-fit border border-slate-200/60">
                {['week1', 'week2', 'week3', 'week4'].map((w, index) => (
                  <button
                    key={w}
                    className={`px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-wider transition-all
                      ${activeWeekTab === w 
                        ? 'bg-indigo-600 text-white shadow-sm' 
                        : 'text-slate-500 hover:text-slate-800'}`}
                    onClick={() => setActiveWeekTab(w)}
                  >
                    Week {index + 1}
                  </button>
                ))}
              </div>
              
              <div className="space-y-3 mt-3">
                {Object.entries(plan.weekly_plan[activeWeekTab] || {}).map(([day, slots]) => (
                  <div key={day} className="bg-slate-50/50 border border-slate-200/80 rounded-2xl p-4 flex flex-col md:flex-row md:items-center gap-3 hover:border-slate-300 transition-colors">
                    <div className="w-28 text-slate-700 font-bold text-sm shrink-0 border-b md:border-b-0 md:border-r border-slate-200 pb-2 md:pb-0 md:pr-4 py-0.5">
                      {day}
                    </div>
                    <div className="flex-1 space-y-2">
                      {slots && slots.length > 0 ? (
                        slots.map((slot, sIdx) => (
                          <div key={sIdx} className="flex flex-wrap items-center gap-2.5 text-xs">
                            <span className="bg-indigo-50 text-indigo-700 px-2 py-1 rounded-lg font-mono border border-indigo-100">
                              🕒 {slot.time} ({slot.duration})
                            </span>
                            <span className="bg-violet-50 text-violet-700 px-2.5 py-1 rounded-lg font-bold border border-violet-100 uppercase tracking-wider">
                              📚 {slot.subject}
                            </span>
                            <span className="text-slate-800 font-medium text-sm">
                              {slot.topic}
                            </span>
                          </div>
                        ))
                      ) : (
                        <span className="text-slate-400 text-xs italic">Rest / Self-study / Revisions</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {plan.daily_targets && Object.keys(plan.daily_targets).length > 0 && (
            <div>
              <label className="label">🎯 Daily Subject Targets</label>
              <div className="grid sm:grid-cols-2 gap-3 mt-2">
                {Object.entries(plan.daily_targets).map(([subj, target]) => (
                  <div key={subj} className="bg-slate-50/50 border border-slate-200/80 rounded-2xl px-4 py-3 text-sm flex flex-col gap-1">
                    <span className="text-indigo-600 font-bold text-sm">📚 {subj}</span>
                    <span className="text-slate-600">{target}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {plan.resources && Object.keys(plan.resources).length > 0 && (
            <div>
              <label className="label">📖 Recommended Books & Resources</label>
              <div className="grid sm:grid-cols-2 gap-4 mt-2">
                {Object.entries(plan.resources).map(([subj, resList]) => (
                  <div key={subj} className="bg-slate-50/30 border border-slate-200/60 rounded-2xl p-4">
                    <div className="text-slate-800 font-bold text-sm mb-2 pb-1 border-b border-slate-200/80">📚 {subj}</div>
                    <ul className="space-y-1.5 list-disc list-inside">
                      {resList.map((resItem, rIdx) => (
                        <li key={rIdx} className="text-slate-600 text-xs leading-relaxed">
                          {resItem}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// -- Notes --
function NotesTab({ t, lang, materials }) {
  const [topic, setTopic] = useState('')
  const [matId, setMatId] = useState('')
  const [notes, setNotes] = useState('')
  const [loading, setLoading] = useState(false)

  const generate = async () => {
    if (!topic) return toast.error('Enter a topic')
    setLoading(true)
    try {
      const res = await learningAPI.generateNotes({ topic, material_id: matId || null, language: lang })
      setNotes(res.data.notes)
    } catch { toast.error('Failed to generate notes') }
    finally { setLoading(false) }
  }

  const studyMats = materials.filter(m => m.file_type === 'study_material')

  return (
    <div className="card space-y-4">
      <div>
        <label className="label">{t.aiNotes}</label>
        <input className="input" placeholder={t.topicPlaceholder} value={topic}
               onChange={e => setTopic(e.target.value)} />
      </div>
      {studyMats.length > 0 && (
        <div>
          <label className="label">{t.selectMaterial} (optional)</label>
          <select className="input" value={matId} onChange={e => setMatId(e.target.value)}>
            <option value="">-- None (generate from topic only) --</option>
            {studyMats.map(m => <option key={m.id} value={m.id}>{m.original_name}</option>)}
          </select>
        </div>
      )}
      <button className="btn-primary" onClick={generate} disabled={loading || !topic}>
        {loading ? <><Spinner /> {t.generating}</> : `✨ ${t.generateNotes}`}
      </button>
      {notes && <AIOutput text={notes} />}
    </div>
  )
}

// -- Flashcards --
function FlashcardsTab({ t, materials }) {
  const [matId, setMatId] = useState('')
  const [cards, setCards] = useState([])
  const [flipped, setFlipped] = useState({})
  const [loading, setLoading] = useState(false)
  const [count, setCount] = useState(15)
  const [showHint, setShowHint] = useState({})

  const studyMats = materials.filter(m => m.file_type === 'study_material')

  const generate = async () => {
    if (!matId) return toast.error('Select a study material first')
    setLoading(true)
    try {
      const res = await learningAPI.generateFlashcards(+matId, count)
      setCards(res.data.flashcards)
      setFlipped({})
      toast.success(`${res.data.count} flashcards generated!`)
    } catch { toast.error('Failed') }
    finally { setLoading(false) }
  }

  const loadSaved = async () => {
    if (!matId) return
    try {
      const res = await learningAPI.getFlashcards(+matId)
      if (res.data.length) { setCards(res.data); toast.success('Loaded saved flashcards') }
      else toast.error('No saved cards for this material')
    } catch { toast.error('Failed to load') }
  }

  return (
    <div className="space-y-5">
      <div className="card">
        {studyMats.length === 0 ? (
          <EmptyState icon="📚" message={t.noMaterial} sub="Go to Planner tab → Upload Material" />
        ) : (
          <>
            <div className="grid sm:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="label">{t.selectMaterial}</label>
                <select className="input" value={matId} onChange={e => setMatId(e.target.value)}>
                  <option value="">Select material...</option>
                  {studyMats.map(m => <option key={m.id} value={m.id}>{m.original_name}</option>)}
                </select>
              </div>
              <div>
                <label className="label">Number of flashcards (10–15)</label>
                <select className="input" value={count} onChange={e => setCount(+e.target.value)}>
                  {[10, 12, 15].map(n => <option key={n} value={n}>{n} cards</option>)}
                </select>
              </div>
            </div>
            <div className="flex gap-3">
              <button className="btn-primary" onClick={generate} disabled={loading || !matId}>
                {loading ? <><Spinner /> Generating...</> : `🃏 ${t.generateFlashcards}`}
              </button>
              <button className="btn-secondary" onClick={loadSaved} disabled={!matId}>
                📂 Load Saved
              </button>
            </div>
          </>
        )}
      </div>

      {cards.length > 0 && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <label className="label">{cards.length} Flashcards</label>
            <div className="flex gap-2">
              {['easy', 'medium', 'hard'].map(d => (
                <Badge key={d} type={d}>{cards.filter(c => c.difficulty === d).length} {d}</Badge>
              ))}
            </div>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {cards.map((card, i) => (
              <div key={i} className="space-y-1">
                <div className="flashcard" onClick={() => setFlipped(f => ({...f, [i]: !f[i]}))}>
                  <div className={`flashcard-inner ${flipped[i] ? 'flipped' : ''}`}>
                    <div className="flashcard-face">
                      <div className="text-xs text-primary-400 font-semibold mb-2 uppercase tracking-wider">
                        ❓ {card.topic || 'Question'}
                      </div>
                      <div className="text-sm font-semibold text-slate-800">{card.question}</div>
                      <div className="text-xs text-slate-500 mt-3">{t.flipCard}</div>
                    </div>
                    <div className="flashcard-face flashcard-back">
                      <div className="text-xs text-green-400 font-semibold mb-2 uppercase tracking-wider">
                        ✅ Answer
                      </div>
                      <div className="text-sm text-slate-800">{card.answer}</div>
                    </div>
                  </div>
                </div>
                {card.hint && (
                  <button className="text-xs text-slate-500 hover:text-primary-400 transition-colors w-full text-left px-1"
                          onClick={() => setShowHint(h => ({...h, [i]: !h[i]}))}>
                    💡 {t.hint}: {showHint[i] ? card.hint : '...'}
                  </button>
                )}
                <Badge type={card.difficulty || 'medium'}>{card.difficulty || 'medium'}</Badge>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// -- Q&A --
function QATab({ t, lang, materials }) {
  const [matId, setMatId] = useState('')
  const [count, setCount] = useState(10)
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(false)

  const studyMats = materials.filter(m => m.file_type === 'study_material')

  const generate = async () => {
    if (!matId) return toast.error('Select a material')
    setLoading(true)
    setAnswers({})
    try {
      const res = await learningAPI.generateQA(+matId, count, lang)
      setQuestions(res.data.questions)
    } catch { toast.error('Failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="space-y-5">
      <div className="card">
        {studyMats.length === 0 ? (
          <EmptyState icon="📚" message={t.noMaterial} />
        ) : (
          <div className="flex flex-wrap gap-4 items-end">
            <div className="flex-1 min-w-48">
              <label className="label">{t.selectMaterial}</label>
              <select className="input" value={matId} onChange={e => setMatId(e.target.value)}>
                <option value="">Select material...</option>
                {studyMats.map(m => <option key={m.id} value={m.id}>{m.original_name}</option>)}
              </select>
            </div>
            <div>
              <label className="label">{t.numQuestions}</label>
              <select className="input w-28" value={count} onChange={e => setCount(+e.target.value)}>
                {[5, 8, 10, 15].map(n => <option key={n} value={n}>{n} Qs</option>)}
              </select>
            </div>
            <button className="btn-primary" onClick={generate} disabled={loading || !matId}>
              {loading ? <><Spinner /> Generating...</> : `❓ ${t.generateQA}`}
            </button>
          </div>
        )}
      </div>

      {questions.map((q, i) => (
        <div key={i} className="card-sm bg-slate-50 border border-slate-200">
          <div className="flex gap-2 mb-3">
            <span className="text-xs font-bold text-slate-500">Q{i+1}.</span>
            <div className="text-sm font-semibold text-slate-800 flex-1">{q.question}</div>
            <Badge type={q.difficulty || 'medium'}>{q.difficulty || 'medium'}</Badge>
          </div>
          <div className="grid sm:grid-cols-2 gap-2 mb-3">
            {q.options?.map((opt, j) => {
              const sel = answers[i]
              let cls = 'bg-white border-slate-300 text-slate-700'
              if (sel !== undefined) {
                if (j === q.correct_index) cls = 'bg-green-50 border-green-300 text-green-700'
                else if (j === sel && j !== q.correct_index) cls = 'bg-red-50 border-red-300 text-red-700'
              }
              return (
                <button key={j} disabled={sel !== undefined}
                  onClick={() => sel === undefined && setAnswers(a => ({...a, [i]: j}))}
                  className={`border rounded-xl px-4 py-2.5 text-sm text-left transition-all ${cls}
                              ${sel === undefined ? 'hover:border-indigo-500 cursor-pointer' : 'cursor-default'}`}>
                  {opt}
                </button>
              )
            })}
          </div>
          {answers[i] !== undefined && (
            <div className="bg-slate-100 rounded-xl p-3 text-xs text-slate-600">
              <span className={answers[i] === q.correct_index ? 'text-green-600 font-bold' : 'text-red-600 font-bold'}>
                {answers[i] === q.correct_index ? `✅ ${t.correct}` : `❌ ${t.wrong}`}
              </span>
              {' — '}{q.explanation}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

// -- Mock Test --
function MockTestTab({ t, lang, materials }) {
  const [matId, setMatId] = useState('')
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(false)
  const [idx, setIdx] = useState(0)
  const [selected, setSelected] = useState(null)
  const [score, setScore] = useState(0)
  const [done, setDone] = useState(false)

  const studyMats = materials.filter(m => m.file_type === 'study_material')

  const start = async () => {
    if (!matId) return toast.error('Select a material')
    setLoading(true)
    setIdx(0); setScore(0); setDone(false); setSelected(null)
    try {
      const res = await learningAPI.generateMockTest(+matId)
      setQuestions(res.data.questions)
    } catch { toast.error('Failed') }
    finally { setLoading(false) }
  }

  const handleAnswer = (j) => {
    if (selected !== null) return
    setSelected(j)
    if (j === questions[idx].correct_index) setScore(s => s + 1)
  }

  const next = () => {
    if (idx + 1 >= questions.length) {
      setDone(true)
      profileAPI.saveTestResult({ topic: 'Mock Test', total_questions: questions.length,
        correct: score + (selected === questions[idx].correct_index ? 1 : 0),
        score_pct: Math.round(((score + (selected === questions[idx].correct_index ? 1 : 0)) / questions.length) * 100)
      }).catch(() => {})
    } else {
      setIdx(i => i + 1)
      setSelected(null)
    }
  }

  if (done) {
    const finalScore = score
    return (
      <div className="card text-center py-10">
        <ScoreCircle score={finalScore} total={questions.length} />
        <div className="mt-6 text-lg font-bold text-slate-800">Test Complete!</div>
        <div className="text-slate-500 text-sm mt-2">
          {finalScore >= questions.length * 0.7 ? '🏆 Excellent work!' :
           finalScore >= questions.length * 0.5 ? '👍 Good effort!' : '📚 Keep practising!'}
        </div>
        <button className="btn-primary mt-6 mx-auto" onClick={start}>Retake Test</button>
      </div>
    )
  }

  return (
    <div className="space-y-5">
      {questions.length === 0 ? (
        <div className="card text-center py-10">
          <div className="text-5xl mb-4">📝</div>
          {studyMats.length === 0 ? (
            <EmptyState icon="📚" message={t.noMaterial} />
          ) : (
            <>
              <label className="label text-center">Select Material for Mock Test</label>
              <select className="input max-w-xs mx-auto mb-5" value={matId} onChange={e => setMatId(e.target.value)}>
                <option value="">Select material...</option>
                {studyMats.map(m => <option key={m.id} value={m.id}>{m.original_name}</option>)}
              </select>
              <br />
              <button className="btn-primary mx-auto" onClick={start} disabled={loading || !matId}>
                {loading ? <><Spinner /> Generating...</> : `🎯 ${t.startTest}`}
              </button>
            </>
          )}
        </div>
      ) : (
        <div className="card">
          <div className="flex justify-between mb-3 text-sm">
            <span className="text-slate-500">Question {idx + 1} / {questions.length}</span>
            <span className="text-indigo-600 font-semibold">{t.score}: {score}</span>
          </div>
          <div className="progress-bar mb-5">
            <div className="progress-fill" style={{ width: `${(idx / questions.length) * 100}%` }} />
          </div>
          <div className="text-base font-semibold text-slate-800 mb-5">{questions[idx]?.question}</div>
          <div className="grid sm:grid-cols-2 gap-3">
            {questions[idx]?.options?.map((opt, j) => {
              let cls = 'bg-white border-slate-300 text-slate-700'
              if (selected !== null) {
                if (j === questions[idx].correct_index) cls = 'bg-green-50 border-green-300 text-green-700'
                else if (j === selected) cls = 'bg-red-50 border-red-300 text-red-700'
              }
              return (
                <button key={j} onClick={() => handleAnswer(j)} disabled={selected !== null}
                  className={`border rounded-xl px-4 py-3 text-sm text-left transition-all ${cls}
                              ${selected === null ? 'hover:border-indigo-500 cursor-pointer' : 'cursor-default'}`}>
                  {String.fromCharCode(65+j)}) {opt}
                </button>
              )
            })}
          </div>
          {selected !== null && (
            <div className="mt-4">
              <div className="bg-slate-100 rounded-xl p-3 text-xs text-slate-600 mb-3">
                <strong className={selected === questions[idx].correct_index ? 'text-green-600' : 'text-red-600'}>
                  {selected === questions[idx].correct_index ? `✅ ${t.correct}` : `❌ ${t.wrong}`}
                </strong>
                {' — '}{questions[idx].explanation}
              </div>
              <button className="btn-primary" onClick={next}>
                {idx + 1 < questions.length ? t.nextQ : 'See Results →'}
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// -- Doubt Solver --
function DoubtTab({ t, lang, materials }) {
  const [question, setQuestion] = useState('')
  const [matId, setMatId] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)

  const studyMats = materials.filter(m => m.file_type === 'study_material')

  const solve = async () => {
    if (!question.trim()) return toast.error('Enter a question')
    setLoading(true)
    try {
      const res = await learningAPI.solveDoubt(question, matId || null, lang)
      setAnswer(res.data.answer)
    } catch { toast.error('Failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="card space-y-4">
      {studyMats.length > 0 && (
        <div>
          <label className="label">{t.selectMaterial} (optional — for context)</label>
          <select className="input" value={matId} onChange={e => setMatId(e.target.value)}>
            <option value="">-- None --</option>
            {studyMats.map(m => <option key={m.id} value={m.id}>{m.original_name}</option>)}
          </select>
        </div>
      )}
      <div>
        <label className="label">{t.doubtSolver}</label>
        <textarea className="textarea" rows={4} placeholder={t.askPlaceholder}
          value={question} onChange={e => setQuestion(e.target.value)} />
      </div>
      <button className="btn-primary" onClick={solve} disabled={loading || !question.trim()}>
        {loading ? <><Spinner /> Solving...</> : `💡 ${t.askBtn}`}
      </button>
      {answer && <AIOutput text={answer} />}
    </div>
  )
}
