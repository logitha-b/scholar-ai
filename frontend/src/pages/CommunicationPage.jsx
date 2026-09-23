import { useState, useRef } from 'react'
import { useStore } from '../store/useStore'
import { T } from '../utils/translations'
import { commAPI } from '../utils/api'
import { AIOutput, Spinner, TabBar } from '../components/shared/UI'
import toast from 'react-hot-toast'

const SPEAK_TOPICS = [
  "Artificial Intelligence in Education",
  "Importance of time management for students",
  "Climate change and its effects on India",
  "Digital India – opportunities and challenges",
  "Role of technology in healthcare",
  "Entrepreneurship opportunities in India",
  "Social media: benefits and drawbacks",
  "Women empowerment in modern India",
]

export default function CommunicationPage() {
  const { language } = useStore()
  const t = T[language]
  const [tab, setTab] = useState('speaking')
  const TABS = [
    { key:'speaking', icon:'🎤', label:t.speakTopic },
    { key:'writing',  icon:'✍️', label:t.writeTopic },
  ]
  return (
    <div className="max-w-4xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="section-title">🎤 {t.commTitle}</h1>
        <p className="section-sub">AI-powered speaking and writing trainer</p>
      </div>
      <TabBar tabs={TABS} active={tab} onChange={setTab} />
      {tab === 'speaking' && <SpeakingTab t={t} language={language} />}
      {tab === 'writing'  && <WritingTab  t={t} language={language} />}
    </div>
  )
}

function SpeakingTab({ t, language }) {
  const [topic, setTopic] = useState(SPEAK_TOPICS[0])
  const [customTopic, setCustomTopic] = useState('')
  const [customTopics, setCustomTopics] = useState([])
  const [recording, setRecording] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(false)
  const recRef = useRef(null)

  const startRec = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SR) return toast.error('Speech recognition needs Chrome browser')
    const r = new SR()
    r.lang = 'en-IN'; r.continuous = true; r.interimResults = true
    r.onresult = e => {
      let text = ''
      for (let i = 0; i < e.results.length; i++) text += e.results[i][0].transcript
      setTranscript(text)
    }
    r.start(); recRef.current = r; setRecording(true)
  }

  const stopRec = async () => {
    recRef.current?.stop(); setRecording(false)
    if (!transcript.trim()) return toast.error('No speech detected')
    setLoading(true)
    try {
      const res = await commAPI.speakingFeedback(transcript, topic, language)
      setFeedback(res.data)
    } catch { toast.error('Analysis failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="space-y-5">
      <div className="card">
        <label className="label">Choose Speaking Topic</label>
        <div className="flex flex-wrap gap-2 mb-4">
          {SPEAK_TOPICS.concat(customTopics).map(tp => (
            <button key={tp} onClick={() => setTopic(tp)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold border transition-all
                ${topic === tp ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-slate-600 border-slate-300 hover:border-indigo-400'}`}>
              {tp}
            </button>
          ))}
        </div>

        {/* Custom topic input */}
        <div className="flex gap-2 mb-6 max-w-md">
          <input className="input" placeholder="Or enter your own custom topic..."
            value={customTopic} onChange={e => setCustomTopic(e.target.value)}
            style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }} />
          <button className="btn-secondary btn-sm rounded-xl shrink-0" onClick={() => {
            if (customTopic.trim()) {
              const tp = customTopic.trim();
              if (!SPEAK_TOPICS.concat(customTopics).includes(tp)) {
                setCustomTopics([...customTopics, tp]);
              }
              setTopic(tp);
              setCustomTopic('');
              toast.success('Custom topic added!');
            }
          }}>Add Topic</button>
        </div>

        <div className="bg-indigo-50 border border-indigo-200 rounded-2xl p-6 text-center">
          <div className="text-sm font-semibold text-indigo-600 mb-1">Speaking on:</div>
          <div className="text-lg font-bold text-slate-800 mb-6">"{topic}"</div>

          <button
            onClick={recording ? stopRec : startRec}
            className={`w-24 h-24 rounded-full border-4 flex items-center justify-center text-4xl mx-auto transition-all
              ${recording
                ? 'border-red-400 bg-red-50 recording-pulse'
                : 'border-indigo-300 bg-white hover:border-indigo-500 hover:bg-indigo-50 shadow-md'}`}>
            {recording ? '⏹' : '🎤'}
          </button>
          <div className={`mt-3 text-sm font-medium ${recording ? 'text-red-600' : 'text-slate-500'}`}>
            {recording ? t.recordingMsg : 'Tap to start speaking'}
          </div>
          {!recording && transcript && (
            <button className="btn-primary mx-auto mt-4" onClick={stopRec}>
              Analyse Speech
            </button>
          )}
        </div>

        {transcript && (
          <div className="mt-4">
            <label className="label">Your Transcript</label>
            <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm text-slate-700 min-h-16">{transcript}</div>
          </div>
        )}

        {loading && (
          <div className="flex items-center gap-2 text-indigo-600 text-sm mt-4"><Spinner /> {t.processingAudio}</div>
        )}
      </div>

      {feedback && <FeedbackPanel feedback={feedback} type="speaking" t={t} />}
    </div>
  )
}

function WritingTab({ t, language }) {
  const [mode, setMode] = useState('essay')
  const [text, setText] = useState('')
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(false)

  const analyse = async () => {
    const wordCount = text.trim().split(/\s+/).filter(Boolean).length
    if (!text.trim() || wordCount < 10) return toast.error('Write at least 10 words')
    setLoading(true)
    try {
      const res = await commAPI.writingFeedback(text, mode, language)
      setFeedback(res.data)
    } catch { toast.error('Analysis failed') }
    finally { setLoading(false) }
  }

  return (
    <div className="space-y-5">
      <div className="card">
        <div className="flex gap-2 mb-4">
          {['essay','email','report','paragraph','letter'].map(m => (
            <button key={m} onClick={() => setMode(m)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all capitalize
                ${mode === m ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-slate-600 border-slate-300 hover:border-indigo-400'}`}>
              {m}
            </button>
          ))}
        </div>
        <label className="label">{t.writeHere}</label>
        <textarea className="textarea" rows={8} placeholder={t.writeHere} value={text} onChange={e => setText(e.target.value)} />
        <div className="flex items-center justify-between mt-2">
          <span className="text-xs text-slate-400">{text.trim().split(/\s+/).filter(Boolean).length} words</span>
          <button className="btn-primary" onClick={analyse} disabled={loading || text.trim().split(/\s+/).filter(Boolean).length < 10}>
            {loading ? <><Spinner /> Analysing...</> : `📊 ${t.analyseWriting}`}
          </button>
        </div>
      </div>
      {feedback && <FeedbackPanel feedback={feedback} type="writing" t={t} />}
    </div>
  )
}

function FeedbackPanel({ feedback: f, type, t }) {
  if (!f) return null

  // Support both string feedback and parsed objects
  let data = f;
  if (typeof f === 'string') {
    try {
      data = JSON.parse(f);
    } catch (e) {
      try {
        const clean = f.replace(/```json|```/g, '').trim();
        data = JSON.parse(clean);
      } catch (err) {
        return (
          <div className="card mt-4 p-5 bg-white border border-slate-200 text-left">
            <h3 className="font-bold text-slate-800 text-base mb-3">📋 Feedback Analysis</h3>
            <AIOutput text={f} />
          </div>
        );
      }
    }
  }

  if (typeof data === 'string') {
    return (
      <div className="card mt-4 p-5 bg-white border border-slate-200 text-left">
        <h3 className="font-bold text-slate-800 text-base mb-3">📋 Feedback Analysis</h3>
        <AIOutput text={data} />
      </div>
    );
  }

  // Normalize keys to support variations in API responses
  const score = data.overall_score || data.score || 0
  const scoreColor = score >= 7 ? 'text-green-600' : score >= 5 ? 'text-amber-600' : 'text-red-600'
  const scoreBg = score >= 7 ? 'bg-green-50 border-green-200' : score >= 5 ? 'bg-amber-50 border-amber-200' : 'bg-red-50 border-red-200'

  const vocabList = data.vocabulary_suggestions || data.vocabulary_improvements || data.vocabulary || []
  const improvements = data.top_improvements || data.improvements || data.suggestions || data.tips || []
  const grammarErrors = data.grammar_errors || data.grammar_corrections || data.grammar || []
  const spellingMistakes = data.spelling_mistakes || data.spelling_errors || data.spelling || []
  const strengths = data.strengths || []
  const correctedVersion = data.corrected_version || data.corrected_text || data.corrected || ''
  const structureFeedback = data.structure_feedback || data.structure || ''
  const readabilityScore = data.readability_score || data.readability || 0
  const tone = data.tone || ''

  return (
    <div className="space-y-4 text-left">
      {/* Score Header */}
      <div className={`card border-2 ${scoreBg} text-center`}>
        <div className={`text-5xl font-bold ${scoreColor}`}>{score}<span className="text-2xl text-slate-400">/10</span></div>
        <div className="text-slate-600 font-semibold mt-1">
          {type === 'speaking' ? t.speakingFeedback : t.writingFeedback}
        </div>
        {data.positive_feedback && <p className="text-sm text-slate-600 mt-2 italic">"{data.positive_feedback}"</p>}
      </div>

      {/* Writing Metrics (Readability, Tone, Structure) */}
      {type === 'writing' && (readabilityScore || tone || structureFeedback) && (
        <div className="grid sm:grid-cols-3 gap-4">
          {readabilityScore !== undefined && readabilityScore !== 0 && (
            <div className="card p-4 text-center bg-slate-50 border-slate-200">
              <div className="text-xl font-bold text-slate-800">{readabilityScore}/10</div>
              <div className="text-xs text-slate-500 mt-1 font-semibold">Readability Score</div>
            </div>
          )}
          {tone && (
            <div className="card p-4 text-center bg-slate-50 border-slate-200">
              <div className="text-xl font-bold text-indigo-600 capitalize">{tone}</div>
              <div className="text-xs text-slate-500 mt-1 font-semibold">Writing Tone</div>
            </div>
          )}
          {structureFeedback && (
            <div className="card p-4 sm:col-span-3 text-left bg-slate-50 border-slate-200">
              <div className="text-xs font-semibold text-slate-800 mb-1">🏗️ Structure Feedback</div>
              <p className="text-xs text-slate-600 leading-relaxed">{structureFeedback}</p>
            </div>
          )}
        </div>
      )}

      <div className="grid sm:grid-cols-2 gap-4">
        {/* Grammar Errors */}
        {Array.isArray(grammarErrors) && grammarErrors.length > 0 && (
          <div className="card">
            <div className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
              📝 Grammar Issues <span className="badge-red">{grammarErrors.length}</span>
            </div>
            <div className="space-y-2">
              {grammarErrors.slice(0, 5).map((e, i) => {
                if (!e) return null;
                const isObj = typeof e === 'object';
                const errorVal = isObj ? (e.error || e.wrong || '') : e;
                const correctionVal = isObj ? (e.correction || e.correct || '') : '';
                const lineVal = isObj ? (e.line || e.sentence || '') : '';
                return (
                  <div key={i} className="text-xs p-2.5 bg-red-50/50 rounded-xl border border-red-100">
                    {lineVal && <div className="text-slate-400 mb-1 italic">"{lineVal}"</div>}
                    {errorVal && <span className="line-through text-red-500">{errorVal}</span>}
                    {correctionVal && (
                      <>
                        <span className="text-slate-400"> → </span>
                        <span className="text-green-600 font-bold">{correctionVal}</span>
                      </>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Spelling Mistakes (Writing only) */}
        {type === 'writing' && Array.isArray(spellingMistakes) && spellingMistakes.length > 0 && (
          <div className="card">
            <div className="font-semibold text-slate-800 mb-3 flex items-center gap-2">
              ✏️ Spelling Mistakes <span className="badge-red">{spellingMistakes.length}</span>
            </div>
            <div className="space-y-2">
              {spellingMistakes.slice(0, 5).map((e, i) => {
                if (!e) return null;
                const isObj = typeof e === 'object';
                const wrongVal = isObj ? (e.wrong || e.error || '') : e;
                const correctVal = isObj ? (e.correct || e.correction || '') : '';
                return (
                  <div key={i} className="text-xs p-2 bg-red-50/50 rounded-xl border border-red-100">
                    {wrongVal && <span className="line-through text-red-500">{wrongVal}</span>}
                    {correctVal && (
                      <>
                        <span className="text-slate-400"> → </span>
                        <span className="text-green-600 font-bold">{correctVal}</span>
                      </>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Vocabulary Improvements */}
        {Array.isArray(vocabList) && vocabList.length > 0 && (
          <div className="card">
            <div className="font-semibold text-slate-800 mb-3">💬 Better Word Choices</div>
            <div className="space-y-2.5">
              {vocabList.slice(0, 5).map((v, i) => {
                if (!v) return null;
                const isObj = typeof v === 'object';
                const originalVal = isObj ? (v.word_used || v.original || '') : v;
                const suggestionVal = isObj ? (v.better_word || v.suggestion || '') : '';
                const reasonVal = isObj ? v.reason : '';
                const contextVal = isObj ? v.context : '';
                return (
                  <div key={i} className="text-xs p-2.5 bg-blue-50/50 rounded-xl border border-blue-100">
                    <div className="flex items-center gap-2 mb-1">
                      {originalVal && <span className="text-slate-500 font-semibold">{originalVal}</span>}
                      {suggestionVal && (
                        <>
                          <span className="text-slate-400">→</span>
                          <span className="text-blue-700 font-bold">{suggestionVal}</span>
                        </>
                      )}
                    </div>
                    {contextVal && <p className="text-[10px] text-slate-400 italic">Context: "{contextVal}"</p>}
                    {reasonVal && <p className="text-[10px] text-slate-400 italic">Reason: {reasonVal}</p>}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Filler words - speaking only */}
        {type === 'speaking' && data.filler_words && Object.keys(data.filler_words).length > 0 && (
          <div className="card">
            <div className="font-semibold text-slate-800 mb-3">⚠️ Filler Words</div>
            <div className="flex flex-wrap gap-2">
              {Object.entries(data.filler_words).map(([word, count]) => (
                <span key={word} className="bg-amber-50 border border-amber-200 text-amber-700 text-xs px-2.5 py-1 rounded-xl font-semibold">
                  "{word}" × {count}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Strengths (Writing only) */}
        {type === 'writing' && Array.isArray(strengths) && strengths.length > 0 && (
          <div className="card">
            <div className="font-semibold text-green-800 mb-3 flex items-center gap-2">✅ Key Strengths</div>
            <ul className="space-y-1.5">
              {strengths.map((str, i) => (
                <li key={i} className="text-xs text-slate-600 flex gap-2">
                  <span className="text-green-500 shrink-0">•</span>{str}
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Top Improvements / Recommendations */}
        {Array.isArray(improvements) && improvements.length > 0 && (
          <div className="card">
            <div className="font-semibold text-slate-800 mb-3">🚀 Top Improvements</div>
            <ul className="space-y-1.5">
              {improvements.map((tip, i) => (
                <li key={i} className="text-xs text-slate-600 flex gap-2">
                  <span className="text-indigo-500 shrink-0">{i+1}.</span>{tip}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Corrected version - writing only */}
      {type === 'writing' && correctedVersion && (
        <div className="card border-green-200 bg-green-50">
          <div className="font-semibold text-green-800 mb-2">✅ Corrected Version</div>
          <div className="text-sm text-slate-700 leading-relaxed">{correctedVersion}</div>
        </div>
      )}
    </div>
  )
}
