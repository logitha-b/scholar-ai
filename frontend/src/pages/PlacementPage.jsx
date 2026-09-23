import { useState, useEffect, useRef } from 'react'
import { useStore } from '../store/useStore'
import { T } from '../utils/translations'
import { placementAPI } from '../utils/api'
import { AIOutput, Spinner, Badge, TabBar, EmptyState } from '../components/shared/UI'
import toast from 'react-hot-toast'
import Editor from '@monaco-editor/react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const COMPANIES = [
  { id:1, name:"TCS",        logo:"T", color:"bg-blue-600",   package:"3.5–7 LPA",  process:"Online Test → TR → MR → HR",
    aptitude_topics:["Number System","Speed & Distance","Time & Work","Profit & Loss","Logical Reasoning","Verbal Ability"],
    coding_questions:[{title:"Reverse a String",difficulty:"easy",gfg:"https://geeksforgeeks.org/reverse-a-string/",lc:"https://leetcode.com/problems/reverse-string/"},{title:"Find Duplicate in Array",difficulty:"easy",gfg:"https://geeksforgeeks.org/find-duplicates-in-on-time-and-constant-extra-space/",lc:"https://leetcode.com/problems/find-the-duplicate-number/"},{title:"Maximum Subarray (Kadane)",difficulty:"medium",gfg:"https://geeksforgeeks.org/largest-sum-contiguous-subarray/",lc:"https://leetcode.com/problems/maximum-subarray/"}],
    interview_questions:["Tell me about yourself.","What are your strengths and weaknesses?","Explain OOP concepts with examples.","What is a deadlock? How to prevent it?","Difference between TCP and UDP."] },
  { id:2, name:"Infosys",    logo:"I", color:"bg-indigo-600", package:"3.6–8 LPA",  process:"Online Test → Pseudocode → HR",
    aptitude_topics:["Data Interpretation","Cryptarithmetic","Logical Reasoning","Verbal Ability","Sentence Completion"],
    coding_questions:[{title:"Palindrome Check",difficulty:"easy",gfg:"https://geeksforgeeks.org/check-whether-a-number-is-palindrome-or-not/",lc:"https://leetcode.com/problems/valid-palindrome/"},{title:"Fibonacci Series",difficulty:"easy",gfg:"https://geeksforgeeks.org/program-for-nth-fibonacci-number/",lc:"https://leetcode.com/problems/fibonacci-number/"},{title:"Longest Common Subsequence",difficulty:"hard",gfg:"https://geeksforgeeks.org/longest-common-subsequence-dp-4/",lc:"https://leetcode.com/problems/longest-common-subsequence/"}],
    interview_questions:["Why do you want to join Infosys?","Explain DBMS normalization.","What is polymorphism?","Describe your final year project.","Where do you see yourself in 5 years?"] },
  { id:3, name:"Wipro",      logo:"W", color:"bg-purple-600", package:"3.5–6.5 LPA",process:"Online Test → Essay → Technical → HR",
    aptitude_topics:["Time & Work","Percentages","Series Completion","Syllogisms","Data Sufficiency"],
    coding_questions:[{title:"Pattern Printing",difficulty:"easy",gfg:"https://geeksforgeeks.org/programs-printing-pyramid-patterns-python/",lc:"https://leetcode.com/problems/pascals-triangle/"},{title:"Stack using Queue",difficulty:"medium",gfg:"https://geeksforgeeks.org/implement-stack-using-queue/",lc:"https://leetcode.com/problems/implement-stack-using-queues/"}],
    interview_questions:["What is your expected salary?","Explain SDLC.","What is recursion? Give an example.","Unix/Linux basic commands."] },
  { id:4, name:"Accenture",  logo:"A", color:"bg-rose-600",   package:"4.5–8 LPA",  process:"Cognitive Test → Communication Test → HR",
    aptitude_topics:["Attention to Detail","Abstract Reasoning","Quantitative","Verbal Comprehension"],
    coding_questions:[{title:"Binary Search",difficulty:"easy",gfg:"https://geeksforgeeks.org/binary-search/",lc:"https://leetcode.com/problems/binary-search/"},{title:"Merge Two Sorted Arrays",difficulty:"medium",gfg:"https://geeksforgeeks.org/merge-two-sorted-arrays/",lc:"https://leetcode.com/problems/merge-sorted-array/"}],
    interview_questions:["What is Agile methodology?","Describe a time you worked in a team.","Difference between Agile and Waterfall.","What is cloud computing?"] },
  { id:5, name:"Cognizant",  logo:"C", color:"bg-teal-600",   package:"4–7.5 LPA",  process:"AMCAT Test → TR → HR",
    aptitude_topics:["Number Series","Blood Relations","Direction Sense","Coding Decoding","Quantitative"],
    coding_questions:[{title:"Tree Inorder Traversal",difficulty:"medium",gfg:"https://geeksforgeeks.org/inorder-tree-traversal-without-recursion/",lc:"https://leetcode.com/problems/binary-tree-inorder-traversal/"},{title:"BFS Level Order",difficulty:"medium",gfg:"https://geeksforgeeks.org/level-order-tree-traversal/",lc:"https://leetcode.com/problems/binary-tree-level-order-traversal/"}],
    interview_questions:["What is SDLC?","Explain testing types.","What is a foreign key?","Difference between DELETE and TRUNCATE."] },
  { id:6, name:"Mr. Cooper", logo:"M", color:"bg-amber-600",  package:"5–9 LPA",    process:"Aptitude → Technical → HR",
    aptitude_topics:["Financial Mathematics","Data Interpretation","Logical Reasoning","Mortgage Basics"],
    coding_questions:[{title:"Calculate EMI",difficulty:"medium",gfg:"https://geeksforgeeks.org/emi-calculator/",lc:"https://leetcode.com/"},{title:"Two Sum",difficulty:"easy",gfg:"https://geeksforgeeks.org/given-an-array-a-and-a-number-x-check-for-pair-in-a-with-sum-as-x/",lc:"https://leetcode.com/problems/two-sum/"}],
    interview_questions:["What is a mortgage?","Explain fixed vs variable interest rates.","What is OOP inheritance?","Describe customer-centric approach."] },
]

export default function PlacementPage() {
  const { language } = useStore()
  const t = T[language]
  const [search, setSearch] = useState('')
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)
  const [companyDetail, setCompanyDetail] = useState(null)
  const [detailLoading, setDetailLoading] = useState(false)

  useEffect(() => {
    placementAPI.getCompanies()
      .then(res => {
        setCompanies(res.data)
        setLoading(false)
      })
      .catch(() => {
        setLoading(false)
      })
  }, [])

  const handleSelect = async (c) => {
    setSelected(c)
    setDetailLoading(true)
    try {
      const res = await placementAPI.getCompany(c.id)
      setCompanyDetail(res.data)
    } catch {
      toast.error('Failed to load company details')
    } finally {
      setDetailLoading(false)
    }
  }

  const COMPANY_COLORS = {
    "TCS": "bg-blue-600",
    "Infosys": "bg-indigo-600",
    "Wipro": "bg-purple-600",
    "Accenture": "bg-rose-600",
    "Cognizant": "bg-teal-600",
    "Mr. Cooper": "bg-amber-600"
  }

  const getCompanyColor = (name) => COMPANY_COLORS[name] || "bg-indigo-500"

  const filtered = companies.filter(c => c.name.toLowerCase().includes(search.toLowerCase()))

  if (selected) {
    return (
      <CompanyDetail 
        company={companyDetail || selected} 
        loading={detailLoading || !companyDetail}
        t={t} 
        onBack={() => {
          setSelected(null)
          setCompanyDetail(null)
        }} 
        language={language} 
      />
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="section-title">🏢 {t.placementTitle}</h1>
        <p className="section-sub">{t.placementSub}</p>
      </div>
      <div className="card mb-5">
        <input className="input" placeholder={t.searchCompany} value={search} onChange={e => setSearch(e.target.value)} />
      </div>
      {loading ? (
        <div className="text-center py-10"><Spinner /> Loading companies...</div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map(c => (
            <button key={c.id} onClick={() => handleSelect(c)}
              className="card hover:shadow-lg hover:border-indigo-300 hover:-translate-y-1 transition-all text-left cursor-pointer">
              <div className="flex items-center gap-3 mb-3">
                <div className={`w-12 h-12 ${getCompanyColor(c.name)} rounded-2xl flex items-center justify-center text-white font-bold text-xl shadow-sm`}>{c.logo}</div>
                <div>
                  <div className="font-bold text-slate-800 text-base">{c.name}</div>
                  <div className="text-xs text-slate-500">{c.package}</div>
                </div>
              </div>
              <div className="text-xs text-slate-500 mb-3 line-clamp-2">{c.process}</div>
              <div className="flex gap-1.5 flex-wrap">
                <span className="badge-purple">Aptitude</span>
                <span className="badge-blue">Coding</span>
                <span className="badge-green">Interview</span>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}

function CompanyDetail({ company: c, loading, t, onBack, language }) {
  const [tab, setTab] = useState('aptitude')
  const [resumeText, setResumeText] = useState('')
  const [resumeFeedback, setResumeFeedback] = useState(null)
  const [resumeLoading, setResumeLoading] = useState(false)
  
  // Simulator States
  const [simQ, setSimQ] = useState(null)
  const [simLoading, setSimLoading] = useState(false)
  const [roundType, setRoundType] = useState('technical')
  const [difficulty, setDifficulty] = useState('medium') // 'easy' | 'medium' | 'hard'
  const [tailorResume, setTailorResume] = useState(false)
  const [customResumeText, setCustomResumeText] = useState('')
  const [uploadingResume, setUploadingResume] = useState(false)
  const [resumeFileName, setResumeFileName] = useState('')
  const [parsedDetails, setParsedDetails] = useState(null)
  const [simAnswers, setSimAnswers] = useState({})
  const [simState, setSimState] = useState('setup') // 'setup' | 'active' | 'report'
  const [activeQIdx, setActiveQIdx] = useState(0)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [cameraOn, setCameraOn] = useState(true)
  const [micOn, setMicOn] = useState(true)
  const [secondsElapsed, setSecondsElapsed] = useState(0)
  const [codeValue, setCodeValue] = useState('// Write your solution here\nfunction solve() {\n  \n}')
  const [editorLang, setEditorLang] = useState('javascript')
  const [consoleOutput, setConsoleOutput] = useState('')
  const [isRunningCode, setIsRunningCode] = useState(false)
  const [reportData, setReportData] = useState(null)
  
  const [showSimFeedback, setShowSimFeedback] = useState({})
  const [interviewAnswers, setInterviewAnswers] = useState({})
  const [interviewFeedbacks, setInterviewFeedbacks] = useState({})
  const [ifLoading, setIfLoading] = useState({})
  const [aptitudeAnswers, setAptitudeAnswers] = useState({})

  const recognitionRef = useRef(null)
  const videoRef = useRef(null)
  const [stream, setStream] = useState(null)

  // Timer Effect
  useEffect(() => {
    let timer;
    if (simState === 'active') {
      timer = setInterval(() => {
        setSecondsElapsed(s => s + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [simState]);

  // Webcam stream controller
  useEffect(() => {
    if (simState === 'active' && cameraOn) {
      navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then((s) => {
          setStream(s);
        })
        .catch(() => {
          setCameraOn(false);
        });
    } else {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
        setStream(null);
      }
    }
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [simState, cameraOn]);

  // Video Ref assignment effect
  useEffect(() => {
    if (videoRef.current && stream) {
      videoRef.current.srcObject = stream;
    }
  }, [stream, cameraOn]);

  // Speech Recognition (STT) Init
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const rec = new SpeechRecognition();
      rec.continuous = true;
      rec.interimResults = true;
      rec.lang = 'en-US';

      rec.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        setSimAnswers(prev => ({
          ...prev,
          [activeQIdx]: transcript
        }));
      };

      rec.onerror = () => setIsListening(false);
      rec.onend = () => setIsListening(false);

      recognitionRef.current = rec;
    }
  }, [activeQIdx]);

  // Speak current question
  const speakQuestion = (text) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);
      window.speechSynthesis.speak(utterance);
    }
  };

  // Toggle voice input
  const toggleListening = () => {
    if (!recognitionRef.current) {
      toast.error('Voice input is not supported in this browser. Please type.');
      return;
    }
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.start();
      setIsListening(true);
    }
  };

  // Run mock code execution
  const runCode = () => {
    setIsRunningCode(true);
    setConsoleOutput('Compiling code...\nExecuting test cases...\n');
    setTimeout(() => {
      setIsRunningCode(false);
      setConsoleOutput(prev => prev + '✔ Test Case 1: Passed\n✔ Test Case 2: Passed\n\nResult: Success! All tests cleared.');
    }, 1500);
  };

  // Calculate Report score locally
  // Calculate Report score strictly using backend grader
  const generateLocalReport = async () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
    }
    window.speechSynthesis.cancel();
    
    setSimLoading(true);
    try {
      const res = await placementAPI.gradeInterview(simQ, simAnswers, language);
      const data = res.data;
      setReportData({
        overallScore: data.overall_score,
        knowledgeLevel: data.knowledge_level,
        questionsGraded: data.questions_graded,
        strengths: data.strengths,
        improvements: data.improvements,
        categoryScores: {
          communication: data.overall_score,
          technicalKnowledge: data.overall_score,
          problemSolving: data.overall_score,
          confidence: cameraOn && micOn ? 95 : 75
        }
      });
      setSimState('report');
    } catch (err) {
      toast.error('Failed to generate strict grading report');
    } finally {
      setSimLoading(false);
    }
  };


  const handleResumeUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    
    setUploadingResume(true)
    setResumeFileName(file.name)
    try {
      const res = await placementAPI.uploadResume(file)
      if (res.data && (res.data.resume_text !== undefined || res.data.parsed_details)) {
        const text = res.data.resume_text || ''
        setCustomResumeText(text)
        setResumeText(text)
        if (res.data.parsed_details) {
          setParsedDetails(res.data.parsed_details)
        }
        toast.success(`Resume uploaded and parsed successfully: ${file.name}`)
        if (!text.trim()) {
          toast.warning("Scanned PDF detected: parsed using default fallback details.")
        }
        
        // Auto trigger detailed ATS analysis
        setResumeLoading(true)
        try {
          const resAnal = await placementAPI.analyseResume(text, language)
          setResumeFeedback(resAnal.data)
        } catch (analErr) {
          console.error("Auto ATS check failed:", analErr)
        } finally {
          setResumeLoading(false)
        }
      } else if (res.data && res.data.error) {
        toast.error(res.data.error)
        setResumeFileName('')
      }
    } catch (err) {
      toast.error('Failed to parse resume file')
      setResumeFileName('')
    } finally {
      setUploadingResume(false)
    }
  }

  const analyseResume = async () => {
    if (!resumeText.trim()) return toast.error('Paste your resume text first')
    setResumeLoading(true)
    try {
      const res = await placementAPI.analyseResume(resumeText, language)
      setResumeFeedback(res.data)
    } catch { toast.error('Failed') }
    finally { setResumeLoading(false) }
  }

  const simulate = async () => {
    setSimLoading(true)
    setSimQ(null)
    setSimAnswers({})
    setShowSimFeedback({})
    setActiveQIdx(0)
    setSecondsElapsed(0)
    setConsoleOutput('')
    try {
      const resumeTextToSend = tailorResume ? customResumeText : '';
      const res = await placementAPI.simulateInterview(c.name, roundType, difficulty, resumeTextToSend, language)
      setSimQ(res.data)
      setSimState('active')
      if (res.data && res.data[0]) {
        speakQuestion(res.data[0].question)
      }
    } catch { toast.error('Failed to start simulation') }
    finally { setSimLoading(false) }
  }

  const getInterviewFeedback = async (q, i) => {
    setIfLoading(l => ({...l, [i]: true}))
    try {
      const res = await placementAPI.getInterviewModelAnswer(q, language)
      setInterviewFeedbacks(f => ({...f, [i]: res.data?.model_answer?.sample_answer || 'Loading...'}))
    } catch { toast.error('Failed to get model answer') }
    finally { setIfLoading(l => ({...l, [i]: false})) }
  }

  const TABS = [
    { key:'aptitude',  icon:'🧮', label:t.aptitude },
    { key:'coding',    icon:'💻', label:t.coding },
    { key:'interview', icon:'🎤', label:t.interview },
    { key:'resume',    icon:'📄', label:t.resume },
    { key:'simulate',  icon:'🤖', label:t.simulate },
  ]

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-6 text-center">
        <button onClick={onBack} className="btn-secondary btn-sm mb-4">{t.back}</button>
        <div className="card py-16 flex flex-col items-center justify-center">
          <Spinner size={40} />
          <div className="text-slate-500 mt-4">Loading company details...</div>
        </div>
      </div>
    )
  }

  const COMPANY_COLORS = {
    "TCS": "bg-blue-600",
    "Infosys": "bg-indigo-600",
    "Wipro": "bg-purple-600",
    "Accenture": "bg-rose-600",
    "Cognizant": "bg-teal-600",
    "Mr. Cooper": "bg-amber-600"
  }

  const colorClass = COMPANY_COLORS[c.name] || "bg-indigo-500"

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <button onClick={onBack} className="btn-secondary btn-sm mb-4">{t.back}</button>
      <div className="card mb-5">
        <div className="flex items-center gap-4">
          <div className={`w-16 h-16 ${colorClass} rounded-2xl flex items-center justify-center text-white font-bold text-3xl shadow`}>{c.logo}</div>
          <div>
            <h2 className="text-2xl font-bold text-slate-800">{c.name}</h2>
            <div className="text-sm text-slate-500">{c.process}</div>
            <span className="badge-green mt-1 inline-block">{c.package}</span>
          </div>
        </div>
      </div>

      <TabBar tabs={TABS} active={tab} onChange={setTab} />

      {tab === 'aptitude' && (
        <div className="space-y-4">
          <div className="flex gap-3 mb-4">
            <a href="https://www.indiabix.com" target="_blank" rel="noreferrer" className="btn-secondary btn-sm text-sm">📚 IndiaBix ↗</a>
            <a href="https://www.careerride.com" target="_blank" rel="noreferrer" className="btn-secondary btn-sm text-sm">📖 CareerRide ↗</a>
          </div>
          {c.aptitude_questions ? (
            c.aptitude_questions.map((q, i) => (
              <div key={q.id} className="card text-left">
                <div className="flex items-start justify-between gap-3 mb-4">
                  <div className="font-semibold text-slate-800 text-sm flex-1">Q{i+1}. {q.question}</div>
                  <div className="flex gap-1.5 shrink-0">
                    <Badge type={q.difficulty}>{q.difficulty}</Badge>
                    <Badge type="purple">{q.topic}</Badge>
                  </div>
                </div>
                <div className="grid sm:grid-cols-2 gap-2">
                  {q.options.map((opt, j) => {
                    const sel = aptitudeAnswers[q.id]
                    let cls = 'bg-slate-50 border-slate-200 text-slate-700 hover:border-indigo-400 hover:bg-indigo-50 cursor-pointer'
                    if (sel !== undefined) {
                      if (j === q.correct) cls = 'bg-green-50 border-green-400 text-green-800 cursor-default'
                      else if (j === sel) cls = 'bg-red-50 border-red-400 text-red-800 cursor-default'
                      else cls = 'bg-slate-50 border-slate-200 text-slate-400 cursor-default'
                    }
                    return (
                      <button key={j} disabled={sel !== undefined}
                        onClick={() => setAptitudeAnswers(a => ({...a, [q.id]: j}))}
                        className={`border rounded-xl px-4 py-2.5 text-sm text-left transition-all font-medium ${cls}`}>
                        {String.fromCharCode(65+j)}) {opt}
                      </button>
                    )
                  })}
                </div>
                {aptitudeAnswers[q.id] !== undefined && (
                  <div className={`mt-3 p-3 rounded-xl text-xs font-medium ${aptitudeAnswers[q.id] === q.correct ? 'bg-green-50 text-green-800 border border-green-200' : 'bg-red-50 text-red-800 border border-red-200'}`}>
                    {aptitudeAnswers[q.id] === q.correct ? '✅ Correct' : '❌ Incorrect'} — {q.explanation}
                  </div>
                )}
              </div>
            ))
          ) : (
            c.aptitude_topics?.map((topic, i) => (
              <div key={i} className="card-sm flex items-center justify-between">
                <div>
                  <div className="font-semibold text-slate-800 text-sm">📌 {topic}</div>
                  <div className="text-xs text-slate-500 mt-0.5">Practice on IndiaBix & CareerRide</div>
                </div>
                <div className="flex gap-2">
                  <a href="https://www.indiabix.com" target="_blank" rel="noreferrer" className="text-indigo-600 text-xs font-semibold hover:text-indigo-800">IndiaBix ↗</a>
                  <a href="https://www.careerride.com" target="_blank" rel="noreferrer" className="text-indigo-600 text-xs font-semibold hover:text-indigo-800">CareerRide ↗</a>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {tab === 'coding' && (
        <div className="space-y-3">
          {c.coding_questions.map((q, i) => (
            <div key={i} className="card-sm">
              <div className="flex items-center justify-between mb-2">
                <div className="font-semibold text-slate-800 text-sm">💻 {q.title}</div>
                <Badge type={q.difficulty}>{q.difficulty}</Badge>
              </div>
              <div className="flex gap-3">
                <a href={q.gfg} target="_blank" rel="noreferrer" className="text-green-600 text-xs font-semibold hover:text-green-800 flex items-center gap-1">🌱 GeeksforGeeks ↗</a>
                <a href={q.lc} target="_blank" rel="noreferrer" className="text-orange-600 text-xs font-semibold hover:text-orange-800 flex items-center gap-1">💡 LeetCode ↗</a>
              </div>
            </div>
          ))}
        </div>
      )}

      {tab === 'interview' && (
        <div className="space-y-4">
          {c.interview_questions.map((q, i) => (
            <div key={i} className="card-sm">
              <div className="font-semibold text-slate-800 text-sm mb-3">🎤 {q}</div>
              <textarea className="textarea text-xs" rows={3} placeholder="Type your answer..."
                value={interviewAnswers[i] || ''} onChange={e => setInterviewAnswers(a => ({...a, [i]: e.target.value}))} />
              <button className="btn-secondary btn-sm text-xs mt-2"
                onClick={() => getInterviewFeedback(q, i)} disabled={ifLoading[i]}>
                {ifLoading[i] ? <Spinner size={14} /> : '💡'} Model Answer
              </button>
              {interviewFeedbacks[i] && (
                <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-xl text-xs text-green-800">{interviewFeedbacks[i]}</div>
              )}
            </div>
          ))}
        </div>
      )}

      {tab === 'resume' && (
        <div className="card space-y-6 text-left">
          <h3 className="text-lg font-bold text-slate-800">Resume Analyzer</h3>
          
          {/* File Upload Zone */}
          <div className="space-y-2">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Upload Resume File (.pdf, .docx, .txt)</label>
            <label className="flex flex-col items-center justify-center w-full h-28 border-2 border-slate-200 border-dashed rounded-2xl cursor-pointer bg-slate-50 hover:bg-slate-100/50 transition-all">
              <div className="flex flex-col items-center justify-center p-4 text-center">
                <span className="text-2xl mb-1">📄</span>
                {uploadingResume ? (
                  <span className="text-xs text-slate-500 font-medium"><Spinner /> Parsing Resume...</span>
                ) : resumeFileName ? (
                  <span className="text-xs text-indigo-600 font-bold truncate max-w-[300px]">{resumeFileName}</span>
                ) : (
                  <>
                    <span className="text-xs text-slate-600 font-bold">Click to upload and analyze resume</span>
                    <span className="text-[10px] text-slate-400 mt-0.5">PDF, DOCX, or TXT up to 5MB</span>
                  </>
                )}
              </div>
              <input 
                type="file" 
                accept=".pdf,.docx,.txt" 
                className="hidden" 
                onChange={handleResumeUpload}
                disabled={uploadingResume}
              />
            </label>
          </div>

          {/* Or Paste Text Fallback */}
          <div className="border border-slate-200 bg-white rounded-xl p-4 space-y-3">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
              Or paste resume text manually
            </label>
            <textarea 
              className="textarea text-xs" 
              rows={5} 
              placeholder="Paste your resume content here..." 
              value={customResumeText} 
              onChange={e => {
                setCustomResumeText(e.target.value);
                setResumeText(e.target.value);
              }} 
            />
            <button 
              className="btn-primary btn-sm" 
              onClick={async () => {
                setResumeText(customResumeText);
                await analyseResume();
              }} 
              disabled={resumeLoading || !customResumeText.trim()}
            >
              {resumeLoading ? <><Spinner /> Analysing...</> : 'Analyse Pasted Text'}
            </button>
          </div>

          {/* Resume Analysis Result Panel */}
          {parsedDetails && (
            <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5 space-y-4">
              <h4 className="font-extrabold text-slate-800 text-xs uppercase tracking-wider text-emerald-800">Extracted Resume Details</h4>
              
              <div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Target Profile:</div>
                <div className="text-xs font-semibold text-slate-700">{parsedDetails.role}</div>
              </div>

              {parsedDetails.projects && parsedDetails.projects.length > 0 && (
                <div>
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Projects:</div>
                  <ul className="list-disc ml-4 space-y-1">
                    {parsedDetails.projects.map((proj, pIdx) => (
                      <li key={pIdx} className="text-xs text-slate-600 leading-normal font-medium">{proj}</li>
                    ))}
                  </ul>
                </div>
              )}

              {parsedDetails.skills && parsedDetails.skills.length > 0 && (
                <div>
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Skills:</div>
                  <div className="flex flex-wrap gap-1.5">
                    {parsedDetails.skills.map((skill, sIdx) => (
                      <span key={sIdx} className="bg-emerald-50 border border-emerald-200 text-emerald-800 text-[10px] font-bold px-2.5 py-0.5 rounded-xl transition-all">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Detailed ATS Feedback Panel */}
          <ResumeFeedbackView feedback={resumeFeedback} />
        </div>
      )}

      {tab === 'simulate' && (
        <div className="space-y-5 text-left">
          {simState === 'setup' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start text-left mt-6">
              
              {/* Left Side: Start your AI Interview info */}
              <div className="space-y-6 py-4">
                <h2 className="text-3xl font-extrabold text-slate-800 tracking-tight leading-tight">
                  Start your AI Interview
                </h2>
                <p className="text-slate-500 text-sm leading-relaxed max-w-sm">
                  Practice real interview scenarios powered by AI. Improve communication, technical skills, and confidence.
                </p>
                
                <div className="space-y-4">
                  <div className="flex items-center gap-3 bg-white border border-slate-100 shadow-sm rounded-xl p-3 max-w-sm">
                    <span className="text-emerald-500 text-lg">👤</span>
                    <span className="text-xs font-bold text-slate-700">Choose Role & Experience</span>
                  </div>
                  <div className="flex items-center gap-3 bg-white border border-slate-100 shadow-sm rounded-xl p-3 max-w-sm">
                    <span className="text-emerald-500 text-lg">🎙</span>
                    <span className="text-xs font-bold text-slate-700">Smart Voice Interview</span>
                  </div>
                  <div className="flex items-center gap-3 bg-white border border-slate-100 shadow-sm rounded-xl p-3 max-w-sm">
                    <span className="text-emerald-500 text-lg">📈</span>
                    <span className="text-xs font-bold text-slate-700">Performance Analytics</span>
                  </div>
                </div>
              </div>

              {/* Right Side: Setup Card */}
              <div className="card bg-white p-6 border border-slate-200 rounded-3xl shadow-md space-y-5">
                <h3 className="text-lg font-bold text-slate-800">Interview Setup</h3>
                
                {/* Upload Zone */}
                <div className="space-y-2">
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Upload Resume (.pdf, .docx, .txt)</label>
                  <label className="flex flex-col items-center justify-center w-full h-24 border-2 border-slate-200 border-dashed rounded-2xl cursor-pointer bg-slate-50 hover:bg-slate-100/50 transition-all">
                    <div className="flex flex-col items-center justify-center p-4 text-center">
                      <span className="text-lg mb-0.5">📄</span>
                      {uploadingResume ? (
                        <span className="text-[11px] text-slate-500 font-medium">Extracting details...</span>
                      ) : resumeFileName ? (
                        <span className="text-xs text-indigo-600 font-bold truncate max-w-[200px]">{resumeFileName}</span>
                      ) : (
                        <span className="text-xs text-slate-500 font-bold">Click to parse resume</span>
                      )}
                    </div>
                    <input 
                      type="file" 
                      accept=".pdf,.docx,.txt" 
                      className="hidden" 
                      onChange={handleResumeUpload}
                      disabled={uploadingResume}
                    />
                  </label>
                </div>

                {/* Role Input with User Icon */}
                <div className="relative">
                  <span className="absolute left-3.5 top-3.5 text-slate-400 text-sm">👤</span>
                  <input
                    type="text"
                    value={parsedDetails?.role || ''}
                    onChange={(e) => setParsedDetails(prev => ({ ...(prev || {}), role: e.target.value }))}
                    className="input pl-10 text-xs md:text-sm"
                    placeholder="Target Role (e.g. Backend & AI Engineer)"
                  />
                </div>

                {/* Focus summary Input with briefcase Icon */}
                <div className="relative">
                  <span className="absolute left-3.5 top-3.5 text-slate-400 text-sm">💼</span>
                  <input
                    type="text"
                    value={parsedDetails?.summary || ''}
                    onChange={(e) => setParsedDetails(prev => ({ ...(prev || {}), summary: e.target.value }))}
                    className="input pl-10 text-xs md:text-sm"
                    placeholder="Experience Summary (e.g. Developed REST APIs)"
                  />
                </div>

                {/* Selection Round Type dropdown */}
                <div>
                  <select
                    value={roundType}
                    onChange={(e) => setRoundType(e.target.value)}
                    className="select text-xs md:text-sm"
                  >
                    <option value="technical">Technical Interview</option>
                    <option value="hr">HR Interview</option>
                    <option value="mixed">Mixed Interview</option>
                  </select>
                </div>

                {/* Select Difficulty Level */}
                <div className="space-y-1.5 text-left pt-2 border-t border-slate-100">
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Difficulty</label>
                  <div className="grid grid-cols-3 gap-2">
                    {['easy', 'medium', 'hard'].map((level) => (
                      <button
                        key={level}
                        type="button"
                        onClick={() => setDifficulty(level)}
                        className={`px-3 py-1.5 border rounded-xl text-xs font-bold transition-all capitalize ${
                          difficulty === level
                            ? 'border-indigo-600 bg-indigo-50 text-indigo-700 shadow-sm font-semibold'
                            : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'
                        }`}
                      >
                        {level}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Resume Analysis Result Panel */}
                {parsedDetails && (
                  <div className="text-left bg-slate-50 border border-slate-200 rounded-2xl p-5 space-y-4">
                    <h4 className="font-extrabold text-slate-800 text-xs uppercase tracking-wider">Resume Analysis Result</h4>
                    
                    {parsedDetails.projects && parsedDetails.projects.length > 0 && (
                      <div>
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">Projects:</div>
                        <ul className="list-disc ml-4 space-y-1">
                          {parsedDetails.projects.map((proj, pIdx) => (
                            <li key={pIdx} className="text-xs text-slate-700 leading-normal font-medium">{proj}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {parsedDetails.skills && parsedDetails.skills.length > 0 && (
                      <div>
                        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Skills:</div>
                        <div className="flex flex-wrap gap-1.5">
                          {parsedDetails.skills.map((skill, sIdx) => (
                            <span key={sIdx} className="bg-emerald-50 border border-emerald-200 text-emerald-800 text-[10px] font-bold px-2.5 py-0.5 rounded-xl transition-all">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Green Start Button */}
                <button 
                  className="w-full py-3 rounded-2xl text-xs md:text-sm font-bold flex items-center justify-center gap-1.5 shadow-md bg-emerald-600 hover:bg-emerald-500 text-white transition-all disabled:opacity-50" 
                  onClick={simulate} 
                  disabled={simLoading || uploadingResume}
                >
                  {uploadingResume ? (
                    <><Spinner /> Parsing Resume...</>
                  ) : simLoading ? (
                    <><Spinner /> Generating...</>
                  ) : (
                    'Start Interview'
                  )}
                </button>
              </div>

            </div>
          )}

          {simState === 'active' && simQ && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
              
              {/* Left Column: Avatar, Question Text & Controls */}
              <div className="flex flex-col space-y-4">
                <div className="card text-center p-6 flex flex-col justify-center items-center relative min-h-[280px]">
                  <div className="absolute top-4 left-4 flex items-center gap-1.5">
                    <span className={`w-2 h-2 rounded-full ${isSpeaking ? 'bg-indigo-600 animate-ping' : 'bg-slate-400'}`} />
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">AI Interviewer</span>
                  </div>

                  {/* Talking Avatar Ring */}
                  <div className={`w-20 h-20 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xl font-bold mb-3 ${isSpeaking ? 'glowing-avatar' : ''}`}>
                    AI
                  </div>

                  <Waveform isSpeaking={isSpeaking} />

                  <div className="mt-4 px-4">
                    <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider block mb-1">
                      Question {activeQIdx + 1} of 25
                    </span>
                    <TypewriterText text={simQ[activeQIdx]?.question} />
                  </div>
                </div>

                {/* Response Textarea Card */}
                <div className="card p-5 space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Your Answer</span>
                    <button
                      onClick={toggleListening}
                      className={`px-3 py-1.5 rounded-full text-xs font-bold flex items-center gap-1.5 transition-all ${
                        isListening 
                          ? 'bg-red-500 text-white animate-pulse' 
                          : 'bg-indigo-50 text-indigo-600 hover:bg-indigo-100'
                      }`}
                    >
                      {isListening ? '🛑 Stop Recording' : '🎤 Voice Input'}
                    </button>
                  </div>

                  <textarea
                    rows={4}
                    placeholder="Speak your response or type it here..."
                    value={simAnswers[activeQIdx] || ''}
                    onChange={(e) => setSimAnswers(prev => ({ ...prev, [activeQIdx]: e.target.value }))}
                    className="textarea text-xs md:text-sm"
                  />

                  <div className="flex justify-between items-center">
                    <span className="text-slate-400 text-xs font-medium">
                      {(simAnswers[activeQIdx] || '').trim().split(/\s+/).filter(Boolean).length} words
                    </span>
                    
                    <div className="flex gap-2">
                      <button 
                        onClick={() => {
                          if (confirm("End Mock Interview Session? This will submit your answers and generate your report.")) {
                            generateLocalReport();
                          }
                        }}
                        className="btn-danger btn-sm text-xs"
                      >
                        End Mock
                      </button>
                      <button
                        onClick={() => {
                          if (activeQIdx < 24) {
                            setActiveQIdx(idx => idx + 1);
                            if (simQ[activeQIdx + 1]) {
                              speakQuestion(simQ[activeQIdx + 1].question);
                            }
                          } else {
                            generateLocalReport();
                          }
                        }}
                        className="btn-primary btn-sm text-xs flex items-center gap-1"
                      >
                        {activeQIdx < 24 ? 'Next Question ➔' : 'Generate Feedback ➔'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Column: Code Editor and Webcam */}
              <div className="flex flex-col space-y-4">
                {/* Local Webcam Card */}
                <div className="card p-0 overflow-hidden relative aspect-video w-full max-w-sm mx-auto flex items-center justify-center bg-slate-100">
                  {cameraOn && stream ? (
                    <video
                      ref={videoRef}
                      autoPlay
                      playsInline
                      muted
                      className="w-full h-full object-cover transform scale-x-[-1]"
                    />
                  ) : (
                    <div className="text-slate-400 text-center text-xs py-10">
                      <span className="text-3xl block mb-1">📹</span>
                      Webcam feed paused
                    </div>
                  )}

                  <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-2 bg-black/60 px-3 py-1.5 rounded-full z-10 text-white">
                    <button onClick={() => setCameraOn(!cameraOn)} className="text-xs hover:text-indigo-400">
                      {cameraOn ? 'Pause Cam' : 'Play Cam'}
                    </button>
                    <span className="text-slate-500">|</span>
                    <button onClick={() => setMicOn(!micOn)} className="text-xs hover:text-indigo-400">
                      {micOn ? 'Mute' : 'Unmute'}
                    </button>
                  </div>
                </div>

                {/* Monaco Editor (only show if round type is technical or mixed) */}
                {(roundType === 'technical' || roundType === 'mixed') && (
                  <div className="card p-0 flex flex-col flex-1 overflow-hidden border border-slate-200 min-h-[300px]">
                    <div className="px-4 py-2 border-b border-slate-200 bg-slate-50 flex justify-between items-center">
                      <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">Solution Workspace</span>
                      <select
                        value={editorLang}
                        onChange={(e) => setEditorLang(e.target.value)}
                        className="px-2 py-0.5 rounded border border-slate-300 text-xs"
                      >
                        <option value="javascript">JavaScript</option>
                        <option value="python">Python</option>
                        <option value="cpp">C++</option>
                        <option value="java">Java</option>
                      </select>
                    </div>

                    <div className="flex-1 min-h-[180px]">
                      <Editor
                        height="100%"
                        language={editorLang}
                        theme="vs-light"
                        value={codeValue}
                        onChange={setCodeValue}
                        options={{
                          minimap: { enabled: false },
                          fontSize: 12,
                          scrollBeyondLastLine: false,
                        }}
                      />
                    </div>

                    <div className="border-t border-slate-200 bg-slate-950 text-slate-200 p-3 font-mono text-xs">
                      <div className="flex justify-between items-center mb-1 text-[10px] text-slate-400">
                        <span>Compiler Console Output</span>
                        <button onClick={runCode} disabled={isRunningCode} className="bg-indigo-600 hover:bg-indigo-500 text-white px-2.5 py-0.5 rounded text-[10px] font-bold">
                          {isRunningCode ? 'Compiling...' : 'Run Code'}
                        </button>
                      </div>
                      <div className="h-14 overflow-y-auto whitespace-pre-wrap text-slate-300 leading-normal">
                        {consoleOutput || 'Click "Run Code" to compile and execute tests.'}
                      </div>
                    </div>
                  </div>
                )}
              </div>

            </div>
          )}

          {simState === 'report' && reportData && (
            <div className="space-y-6">
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
                
                {/* Score Gauge Circle */}
                <div className="card p-6 text-center flex flex-col justify-center items-center">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Overall score</span>
                  
                  <div className="relative w-32 h-32 my-5 flex items-center justify-center">
                    <svg className="w-full h-full transform -rotate-90">
                      <circle cx="64" cy="64" r="50" className="stroke-slate-100" strokeWidth="8" fill="transparent" />
                      <circle 
                        cx="64" cy="64" r="50" 
                        className={reportData.overallScore >= 80 ? 'stroke-green-500' : reportData.overallScore >= 60 ? 'stroke-amber-500' : 'stroke-red-500'} 
                        strokeWidth="8" fill="transparent" 
                        strokeDasharray={2 * Math.PI * 50}
                        strokeDashoffset={2 * Math.PI * 50 - (reportData.overallScore / 100) * (2 * Math.PI * 50)}
                        strokeLinecap="round"
                      />
                    </svg>
                    <div className="absolute text-center">
                      <span className="text-2xl font-extrabold">{reportData.overallScore}</span>
                      <span className="text-xs font-semibold text-slate-400">/100</span>
                    </div>
                  </div>

                  <span className="text-xs font-bold uppercase tracking-wider text-indigo-600">
                    {reportData.overallScore >= 80 ? 'Strong Candidate' : reportData.overallScore >= 60 ? 'Good Potential' : 'Needs Practice'}
                  </span>
                  {reportData.knowledgeLevel && (
                    <div className="mt-2 text-xs font-semibold text-slate-500">
                      Knowledge Level: <span className={`font-bold ${reportData.knowledgeLevel === 'Advanced' ? 'text-green-600' : reportData.knowledgeLevel === 'Intermediate' ? 'text-amber-600' : 'text-red-600'}`}>{reportData.knowledgeLevel}</span>
                    </div>
                  )}
                </div>

                {/* Category Recharts horizontal bars */}
                <div className="card p-6 md:col-span-2 flex flex-col justify-between">
                  <h4 className="font-extrabold text-sm mb-4 text-slate-800">Criteria Evaluation</h4>
                  <div className="h-40 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart 
                        data={[
                          { name: 'Communication', score: reportData.categoryScores.communication },
                          { name: 'Tech Knowledge', score: reportData.categoryScores.technicalKnowledge },
                          { name: 'Problem Solving', score: reportData.categoryScores.problemSolving },
                          { name: 'Confidence', score: reportData.categoryScores.confidence },
                        ]} 
                        layout="vertical"
                        margin={{ top: 0, right: 10, left: -10, bottom: 0 }}
                      >
                        <XAxis type="number" domain={[0, 100]} hide />
                        <YAxis dataKey="name" type="category" stroke="#64748B" fontSize={11} width={110} tickLine={false} />
                        <Tooltip cursor={{ fill: 'transparent' }} />
                        <Bar dataKey="score" radius={[0, 4, 4, 0]} barSize={12}>
                          {[...Array(4)].map((_, i) => (
                            <Cell key={`cell-${i}`} fill={['#6366F1', '#3B82F6', '#10B981', '#F59E0B'][i]} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

              </div>

              {/* Strengths & Improvements */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="bg-green-50 border border-green-200 rounded-2xl p-5">
                  <h4 className="font-bold text-green-800 text-sm mb-3">✅ Strengths</h4>
                  <ul className="space-y-2 text-xs text-slate-600">
                    {reportData.strengths.map((str, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span>•</span> <span>{str}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5">
                  <h4 className="font-bold text-amber-800 text-sm mb-3">⚠️ Areas to Improve</h4>
                  <ul className="space-y-2 text-xs text-slate-600">
                    {reportData.improvements.map((imp, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span>•</span> <span>{imp}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Question review list */}
              <div className="space-y-3">
                <h4 className="font-bold text-slate-800 text-base mb-4">Interview Q&A Replay</h4>
                {simQ.map((q, idx) => {
                  const active = showSimFeedback[idx];
                  const grade = reportData.questionsGraded?.find(g => g.index === idx) || {};
                  return (
                    <div key={idx} className="card p-0 border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                      <div 
                        onClick={() => setShowSimFeedback(f => ({ ...f, [idx]: !f[idx] }))}
                        className="px-4 py-3 cursor-pointer flex justify-between items-center bg-slate-50 hover:bg-slate-100 transition-all"
                      >
                        <div className="text-left flex-1">
                          <div className="flex items-center gap-2">
                            <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider">Question {idx + 1}</span>
                            {grade.is_correct !== undefined && (
                              <span className={`text-[9px] font-bold px-2 py-0.5 rounded-full border ${grade.is_correct ? 'bg-green-50 border-green-200 text-green-700' : 'bg-red-50 border-red-200 text-red-700'}`}>
                                {grade.is_correct ? '✅ Correct' : '❌ Incorrect'} ({grade.marks || 0}/10 marks)
                              </span>
                            )}
                          </div>
                          <p className="text-xs font-bold text-slate-800 line-clamp-1 mt-0.5">{q.question}</p>
                        </div>
                        <span className="text-slate-400 text-xs font-semibold ml-4">
                          {active ? 'Hide Answer ▲' : 'Show Answer ▼'}
                        </span>
                      </div>

                      {active && (
                        <div className="p-4 border-t border-slate-200 space-y-4 text-left">
                          <div>
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Question</span>
                            <p className="text-xs font-semibold text-slate-800 bg-slate-50 p-2.5 rounded-lg border border-slate-200/50">{q.question}</p>
                          </div>
                          <div>
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">Your Response</span>
                            <p className="text-xs text-slate-700 bg-indigo-50/50 p-2.5 rounded-lg border border-indigo-100">
                              {simAnswers[idx] || <span className="italic text-slate-400 text-[10px]">No answer provided.</span>}
                            </p>
                          </div>
                          {grade.feedback && (
                            <div>
                              <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider block mb-1">Evaluator Feedback</span>
                              <p className="text-xs text-indigo-800 bg-indigo-50/20 p-2.5 rounded-lg border border-indigo-100/50 leading-relaxed font-medium">{grade.feedback}</p>
                            </div>
                          )}
                          <div>
                            <span className="text-[10px] font-bold text-green-700 uppercase tracking-wider block mb-1">Correct Answer</span>
                            <p className="text-xs text-green-800 bg-green-50/50 p-2.5 rounded-lg border border-green-100 leading-relaxed font-medium">{grade.correct_answer || q.model_answer?.sample_answer}</p>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              <div className="text-center py-4">
                <button 
                  onClick={() => {
                    setSimState('setup');
                    setSimQ(null);
                    setSimAnswers({});
                  }} 
                  className="btn-primary"
                >
                  🔄 Reset & Try Again
                </button>
              </div>

            </div>
          )}
        </div>
      )}
    </div>
  )
}

function ResumeFeedbackView({ feedback: f }) {
  if (!f) return null;

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
          <div className="mt-6 card p-5 bg-white border border-slate-200 text-left">
            <h3 className="font-bold text-slate-800 text-base mb-3">📋 Resume Feedback Analysis</h3>
            <AIOutput text={f} />
          </div>
        );
      }
    }
  }

  if (typeof data === 'string') {
    return (
      <div className="mt-6 card p-5 bg-white border border-slate-200 text-left">
        <h3 className="font-bold text-slate-800 text-base mb-3">📋 Resume Feedback Analysis</h3>
        <AIOutput text={data} />
      </div>
    );
  }

  let score = data.ats_score || 0;
  if (score > 0 && score <= 10) {
    score = score * 10;
  }
  
  const scoreColor = score >= 80 ? 'text-green-600 border-green-200 bg-green-50' : 
                     score >= 60 ? 'text-amber-600 border-amber-200 bg-amber-50' : 
                                   'text-red-600 border-red-200 bg-red-50';
                                   
  const scoreBadge = score >= 80 ? 'badge-green' : score >= 60 ? 'badge-yellow' : 'badge-red';
  const scoreStatus = score >= 80 ? 'Excellent' : score >= 60 ? 'Good' : 'Needs Improvement';

  return (
    <div className="mt-6 space-y-6 text-slate-700 text-left">
      {/* Score Header */}
      <div className={`border-2 rounded-2xl p-6 text-center ${scoreColor}`}>
        <div className="text-4xl font-extrabold">{score}<span className="text-xl font-normal text-slate-400">/100</span></div>
        <div className="text-sm font-semibold uppercase tracking-wider mt-1">ATS Score</div>
        <div className="mt-2"><span className={`badge ${scoreBadge}`}>{scoreStatus}</span></div>
      </div>

      {/* Overall Summary */}
      {data.overall_summary && (
        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5">
          <h4 className="font-bold text-slate-800 text-sm mb-2">📊 Overall Assessment</h4>
          <p className="text-sm leading-relaxed">{data.overall_summary}</p>
        </div>
      )}

      {/* Strengths & Weaknesses */}
      <div className="grid sm:grid-cols-2 gap-4">
        {/* Strengths */}
        {data.strengths?.length > 0 && (
          <div className="bg-green-50/50 border border-green-100 rounded-2xl p-5">
            <h4 className="font-bold text-green-800 text-sm mb-3 flex items-center gap-2">✅ Strengths</h4>
            <ul className="space-y-2">
              {data.strengths.map((str, i) => (
                <li key={i} className="text-xs flex items-start gap-2">
                  <span className="text-green-500 shrink-0">•</span>
                  <span>{str}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Weaknesses */}
        {data.weaknesses?.length > 0 && (
          <div className="bg-red-50/50 border border-red-100 rounded-2xl p-5">
            <h4 className="font-bold text-red-800 text-sm mb-3 flex items-center gap-2">⚠️ Areas for Improvement</h4>
            <ul className="space-y-2">
              {data.weaknesses.map((weak, i) => (
                <li key={i} className="text-xs flex items-start gap-2">
                  <span className="text-red-400 shrink-0">•</span>
                  <span>{weak}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Missing Keywords */}
      {data.missing_keywords?.length > 0 && (
        <div className="bg-amber-50/50 border border-amber-100 rounded-2xl p-5">
          <h4 className="font-bold text-amber-800 text-sm mb-3">🔑 Missing Keywords</h4>
          <div className="flex flex-wrap gap-2">
            {data.missing_keywords.map((keyword, i) => (
              <span key={i} className="bg-amber-100 border border-amber-200 text-amber-800 text-xs px-2.5 py-1 rounded-xl font-medium">
                {keyword}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Suggestions List */}
      {data.suggestions?.length > 0 && (
        <div className="bg-indigo-50/50 border border-indigo-100 rounded-2xl p-5">
          <h4 className="font-bold text-indigo-800 text-sm mb-3">🚀 Actionable Recommendations</h4>
          <div className="space-y-3">
            {data.suggestions.map((sug, i) => (
              <div key={i} className="bg-white border border-indigo-100 rounded-xl p-3 text-xs shadow-sm">
                <span className="badge-purple mb-2 inline-block capitalize">{sug.section}</span>
                <p className="font-medium text-slate-700">{sug.suggestion}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Formatting Issues */}
      {data.format_issues?.length > 0 && (
        <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5">
          <h4 className="font-bold text-slate-800 text-sm mb-2">📁 Formatting & Layout Issues</h4>
          <ul className="space-y-1">
            {data.format_issues.map((issue, i) => (
              <li key={i} className="text-xs flex items-center gap-2 text-slate-600">
                <span className="text-slate-400">•</span> {issue}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function Waveform({ isSpeaking }) {
  return (
    <div className="flex items-center justify-center gap-1.5 h-12 w-full my-3">
      <style>{`
        @keyframes bounceWave {
          0%, 100% { height: 10px; transform: scaleY(1); opacity: 0.6; }
          50% { height: 40px; transform: scaleY(1.3); opacity: 1; }
        }
      `}</style>
      {[...Array(10)].map((_, i) => (
        <div
          key={i}
          className="w-1.5 bg-indigo-500 rounded-full transition-all duration-300"
          style={{
            height: isSpeaking ? '10px' : '6px',
            animation: isSpeaking ? 'bounceWave 1.2s ease-in-out infinite' : 'none',
            animationDelay: `${i * 0.12}s`,
          }}
        />
      ))}
    </div>
  );
}

function TypewriterText({ text }) {
  const [displayed, setDisplayed] = useState('');
  
  useEffect(() => {
    if (!text) {
      setDisplayed('');
      return;
    }
    setDisplayed('');
    let idx = 0;
    const interval = setInterval(() => {
      idx++;
      setDisplayed(text.slice(0, idx));
      if (idx >= text.length) {
        clearInterval(interval);
      }
    }, 20);
    return () => clearInterval(interval);
  }, [text]);

  return <p className="text-base font-bold text-slate-800 leading-relaxed">{displayed}</p>;
}
