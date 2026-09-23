import { useState } from 'react'
import { useStore } from '../store/useStore'
import { T } from '../utils/translations'
import { resourcesAPI } from '../utils/api'
import { AIOutput, Spinner, EmptyState } from '../components/shared/UI'
import toast from 'react-hot-toast'

const BOOKS = {
  "12": { Mathematics:["NCERT Maths Part 1 & 2","RD Sharma Class 12","NCERT Exemplar","Arihant Skills in Maths"], Physics:["NCERT Physics Part 1 & 2","HC Verma Concepts Vol 1 & 2","DC Pandey","Arihant Physics"], Chemistry:["NCERT Chemistry Part 1 & 2","OP Tandon Physical Chemistry","MS Chauhan Organic","VK Jaiswal Inorganic"], Biology:["NCERT Biology","Trueman's Biology Vol 1 & 2","Pradeep Biology","MTG NCERT Fingertips"], "Computer Science":["NCERT CS","Sumita Arora Python","Preeti Arora"], English:["NCERT Flamingo & Vistas","Wren & Martin Grammar"], Accountancy:["NCERT Accountancy Part 1 & 2","TS Grewal","DK Goel"], "Business Studies":["NCERT Business Studies","Poonam Gandhi"], Economics:["NCERT Economics","TR Jain & VK Ohri"] },
  "11": { Mathematics:["NCERT Maths","RD Sharma Class 11","SL Loney Trigonometry","Hall & Knight Algebra"], Physics:["NCERT Physics Part 1 & 2","HC Verma Vol 1","DC Pandey","IE Irodov (advanced)"], Chemistry:["NCERT Chemistry Part 1 & 2","OP Tandon","NCERT Exemplar Chemistry"], Biology:["NCERT Biology","Trueman's Biology","Pradeep Biology"], "Computer Science":["NCERT CS","Sumita Arora C++/Python"] },
  "10": { Mathematics:["NCERT Maths","RS Aggarwal","RD Sharma Class 10","Exam Idea Maths"], Science:["NCERT Science","Lakhmir Singh Physics/Chemistry/Biology","Exam Idea Science"], "Social Science":["NCERT SST (4 books)","Together with Social Science"], English:["NCERT First Flight & Footprints","Wren & Martin"], Hindi:["NCERT Kshitij & Kritika"] },
  "9":  { Mathematics:["NCERT Maths","RD Sharma Class 9","RS Aggarwal"], Science:["NCERT Science","Lakhmir Singh"], "Social Science":["NCERT SST (4 books)"], English:["NCERT Beehive & Moments"] },
  "8":  { Mathematics:["NCERT Maths","RS Aggarwal Class 8"], Science:["NCERT Science"], "Social Science":["NCERT SST"] },
  "6-7":{ Mathematics:["NCERT Maths"], Science:["NCERT Science"], "Social Science":["NCERT SST"] },
}

const BOOK_LINKS = {
  // Class 12
  "NCERT Maths Part 1 & 2": "https://www.tiwariacademy.com/ncert-solutions/class-12/maths/",
  "RD Sharma Class 12": "https://www.vedantu.com/rd-sharma-solutions/class-12-maths",
  "NCERT Exemplar": "https://www.selfstudys.com/books/ncert-exemplar/class-12th",
  "NCERT Exemplar Maths": "https://www.selfstudys.com/books/ncert-exemplar/class-12th",
  "Arihant Skills in Maths": "https://archive.org/details/skillsinmathematicsplaywithgraphs",
  "Arihant Skills in Mathematics": "https://archive.org/details/skillsinmathematicsplaywithgraphs",
  "NCERT Physics Part 1 & 2": "https://www.tiwariacademy.com/ncert-solutions/class-12/physics/",
  "HC Verma Concepts Vol 1 & 2": "https://www.selfstudys.com/books/hc-verma-solution",
  "HC Verma Concepts of Physics Vol 1 & 2": "https://www.selfstudys.com/books/hc-verma-solution",
  "DC Pandey": "https://www.selfstudys.com/books/dc-pandey-solution/class-12-physics",
  "Arihant Physics": "https://archive.org/search?query=arihant+physics+class+12",
  "NCERT Chemistry Part 1 & 2": "https://www.tiwariacademy.com/ncert-solutions/class-12/chemistry/",
  "OP Tandon Physical Chemistry": "https://archive.org/search?query=op+tandon+chemistry",
  "MS Chauhan Organic": "https://archive.org/search?query=ms+chauhan+organic+chemistry",
  "MS Chauhan Organic Chemistry": "https://archive.org/search?query=ms+chauhan+organic+chemistry",
  "VK Jaiswal Inorganic": "https://archive.org/search?query=vk+jaiswal+inorganic+chemistry",
  "NCERT Biology": "https://www.tiwariacademy.com/ncert-solutions/class-12/biology/",
  "Trueman's Biology Vol 1 & 2": "https://archive.org/search?query=trueman+biology",
  "Trueman's Biology": "https://archive.org/search?query=trueman+biology",
  "Pradeep Biology": "https://archive.org/search?query=pradeep+biology",
  "MTG NCERT Fingertips": "https://archive.org/search?query=mtg+ncert+at+your+fingertips",
  "MTG NCERT at your Fingertips": "https://archive.org/search?query=mtg+ncert+at+your+fingertips",
  "NCERT CS": "https://www.selfstudys.com/books/ncert/class-12th",
  "NCERT Computer Science": "https://www.selfstudys.com/books/ncert/class-12th",
  "Sumita Arora Python": "https://archive.org/search?query=sumita+arora+python+class+12",
  "Preeti Arora": "https://archive.org/search?query=preeti+arora+computer+science",
  "NCERT Flamingo & Vistas": "https://www.selfstudys.com/books/ncert/class-12th",
  "Wren & Martin Grammar": "https://archive.org/details/wren-martin-high-school-english-grammar-composition-by-wren-and-martin",
  "NCERT Accountancy Part 1 & 2": "https://www.tiwariacademy.com/ncert-solutions/class-12/accountancy/",
  "TS Grewal": "https://www.selfstudys.com/books/ts-grewal-solutions/class-12",
  "DK Goel": "https://www.selfstudys.com/books/dk-goel-solution/class-12",
  "NCERT Business Studies": "https://www.tiwariacademy.com/ncert-solutions/class-12/business-studies/",
  "Poonam Gandhi": "https://www.selfstudys.com/books/poonam-gandhi-solutions/class-12-business-studies",
  "NCERT Economics": "https://www.tiwariacademy.com/ncert-solutions/class-12/economics/",
  "TR Jain & VK Ohri": "https://www.selfstudys.com/books/tr-jain-vk-ohri-solutions/class-12-economics",

  // Class 11
  "NCERT Maths": "https://www.tiwariacademy.com/ncert-solutions/class-11/maths/",
  "RD Sharma Class 11": "https://www.vedantu.com/rd-sharma-solutions/class-11-maths",
  "SL Loney Trigonometry": "https://archive.org/details/plane-trigonometry-s-l-loney",
  "Hall & Knight Algebra": "https://archive.org/details/higheralgebrase00kniggoog",
  "Hall & Knight Higher Algebra": "https://archive.org/details/higheralgebrase00kniggoog",
  "HC Verma Vol 1": "https://www.selfstudys.com/books/hc-verma-solution",
  "IE Irodov (advanced)": "https://archive.org/details/I.E.IrodovProblemsInGeneralPhysics",
  "NCERT Exemplar Chemistry": "https://www.selfstudys.com/books/ncert-exemplar/class-11th",
  "Sumita Arora C++/Python": "https://archive.org/search?query=sumita+arora+class+11",

  // Class 10
  "RS Aggarwal": "https://www.vedantu.com/rs-aggarwal-solutions/class-10-maths",
  "RD Sharma Class 10": "https://www.vedantu.com/rd-sharma-solutions/class-10-maths",
  "Exam Idea Maths": "https://archive.org/search?query=xam+idea+class+10+maths",
  "NCERT Science": "https://www.tiwariacademy.com/ncert-solutions/class-10/science/",
  "Lakhmir Singh Physics/Chemistry/Biology": "https://www.selfstudys.com/books/lakhmir-singh-solution/class-10",
  "Exam Idea Science": "https://archive.org/search?query=xam+idea+class+10+science",
  "NCERT SST (all 4 books)": "https://www.tiwariacademy.com/ncert-solutions/class-10/social-science/",
  "NCERT SST (4 books)": "https://www.tiwariacademy.com/ncert-solutions/class-10/social-science/",
  "Together with Social Science": "https://archive.org/search?query=together+with+social+science+class+10",
  "NCERT First Flight & Footprints": "https://www.selfstudys.com/books/ncert/class-10th",
  "NCERT Kshitij & Kritika": "https://www.tiwariacademy.com/ncert-solutions/class-10/hindi/",

  // Class 9
  "RD Sharma Class 9": "https://www.vedantu.com/rd-sharma-solutions/class-9-maths",
  "RS Aggarwal Class 9": "https://www.vedantu.com/rs-aggarwal-solutions/class-9-maths",
  "Lakhmir Singh": "https://www.selfstudys.com/books/lakhmir-singh-solution/class-9",
  "NCERT SST": "https://www.tiwariacademy.com/ncert-solutions/class-9/social-science/",
  "NCERT Beehive & Moments": "https://www.selfstudys.com/books/ncert/class-9th",

  // Class 8
  "RS Aggarwal Class 8": "https://www.vedantu.com/rs-aggarwal-solutions/class-8-maths",
}

const getBookUrl = (bk, subj, cls) => {
  const bkLower = bk.toLowerCase();
  
  // 1. Class-specific overrides for reference books (using highly stable Vedantu / SelfStudys solutions)
  if (bkLower.includes("rs aggarwal")) {
    if (cls === "8") return "https://www.vedantu.com/rs-aggarwal-solutions/class-8-maths";
    if (cls === "9") return "https://www.vedantu.com/rs-aggarwal-solutions/class-9-maths";
    return "https://www.vedantu.com/rs-aggarwal-solutions/class-10-maths";
  }
  
  if (bkLower.includes("rd sharma")) {
    if (cls === "12") return "https://www.vedantu.com/rd-sharma-solutions/class-12-maths";
    if (cls === "11") return "https://www.vedantu.com/rd-sharma-solutions/class-11-maths";
    if (cls === "10") return "https://www.vedantu.com/rd-sharma-solutions/class-10-maths";
    if (cls === "9") return "https://www.vedantu.com/rd-sharma-solutions/class-9-maths";
  }
  
  if (bkLower.includes("hc verma")) {
    return "https://www.selfstudys.com/books/hc-verma-solution";
  }

  // 2. Handle NCERT books dynamically
  if (bkLower.startsWith("ncert")) {
    // Check if there is an exact mapping in BOOK_LINKS first
    const mapped = BOOK_LINKS[bk];
    if (mapped) return mapped;

    let s = subj.toLowerCase().trim();
    if (s === "mathematics") s = "maths";
    else if (s === "computer science" || s === "cs") s = "computer-science";
    else if (s === "social science" || s === "sst") s = "social-science";
    else if (s === "business studies") s = "business-studies";
    
    let c = cls;
    if (cls === "6-7") c = "7"; // default to class 7
    
    let suffix = "th";
    if (c === "6-7") suffix = "7th";
    else suffix = c + "th";

    if (bkLower.includes("exemplar")) {
      return `https://www.selfstudys.com/books/ncert-exemplar/class-${suffix}`;
    }
    
    // For Computer Science or subjects not supported on Tiwari Academy, use SelfStudys class-specific folder
    if (s === "computer-science" || s === "cs") {
      return `https://www.selfstudys.com/books/ncert/class-${suffix}`;
    }
    
    return `https://www.tiwariacademy.com/ncert-solutions/class-${c}/${s}/`;
  }
  
  // 3. Fallback to general lookup table or Google search
  const mapped = BOOK_LINKS[bk];
  if (mapped) return mapped;
  
  return `https://www.google.com/search?q=${encodeURIComponent(bk + ' Class ' + cls + ' PDF free download')}`;
}

const SUBJECT_ICONS = { Mathematics:'➕', Physics:'⚡', Chemistry:'🧪', Biology:'🌿', "Computer Science":'💻', English:'📖', Accountancy:'💰', "Business Studies":'📊', Economics:'📈', Science:'🔬', "Social Science":'🌍', Hindi:'🇮🇳' }

export default function ResourcesPage() {
  const { language } = useStore()
  const t = T[language]
  const [cls, setCls] = useState('12')
  const [subject, setSubject] = useState('')
  const [chapter, setChapter] = useState('')
  const [pyq, setPyq] = useState('')
  const [pyqLoading, setPyqLoading] = useState(false)

  const fetchPYQ = async () => {
    if (!subject) return toast.error('Enter a subject first')
    setPyqLoading(true)
    try {
      const res = await resourcesAPI.getPYQ(subject, chapter, language)
      setPyq(res.data.questions)
    } catch { toast.error('Failed to fetch PYQs') }
    finally { setPyqLoading(false) }
  }

  const books = BOOKS[cls] || {}

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="section-title">📚 {t.resourcesTitle}</h1>
        <p className="section-sub">{t.resourcesSub}</p>
      </div>

      {/* Class selector */}
      <div className="card mb-5">
        <label className="label">Select Class</label>
        <div className="flex flex-wrap gap-2">
          {Object.keys(BOOKS).map(c => (
            <button key={c} onClick={() => setCls(c)}
              className={`px-4 py-2 rounded-xl text-sm font-semibold border transition-all
                ${cls === c ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' : 'bg-white text-slate-600 border-slate-300 hover:border-indigo-400 hover:text-indigo-700'}`}>
              Class {c}
            </button>
          ))}
        </div>
      </div>

      {/* Books grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
        {Object.entries(books).map(([subj, bks]) => (
          <div key={subj} className="card hover:shadow-md transition-all hover:border-indigo-200">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-2xl">{SUBJECT_ICONS[subj] || '📗'}</span>
              <div className="font-bold text-slate-800 text-sm">{subj}</div>
            </div>
            <div className="space-y-2">
              {bks.map((bk, i) => {
                const url = getBookUrl(bk, subj, cls);
                return (
                  <a key={i} href={url} target="_blank" rel="noopener noreferrer"
                    className="flex items-start gap-2 text-xs text-slate-600 hover:text-indigo-600 transition-colors group">
                    <span className="text-indigo-400 mt-0.5 shrink-0 group-hover:scale-110 transition-transform">📖</span>
                    <span className="underline decoration-slate-200 group-hover:decoration-indigo-500 transition-colors">{bk}</span>
                    <span className="text-[10px] text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity">↗</span>
                  </a>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {/* PYQ Section */}
      <div className="card">
        <h2 className="font-bold text-slate-800 text-lg mb-4">📋 {t.prevYearQ}</h2>
        <div className="grid sm:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="label">Subject *</label>
            <input className="input" placeholder="e.g. Physics, Mathematics" value={subject} onChange={e => setSubject(e.target.value)} />
          </div>
          <div>
            <label className="label">Chapter / Topic (optional)</label>
            <input className="input" placeholder="e.g. Electrostatics, Calculus" value={chapter} onChange={e => setChapter(e.target.value)} />
          </div>
        </div>
        <button className="btn-primary" onClick={fetchPYQ} disabled={pyqLoading || !subject}>
          {pyqLoading ? <><Spinner /> Fetching...</> : `📋 ${t.fetchPYQ}`}
        </button>
        {pyq && <AIOutput text={pyq} />}
      </div>
    </div>
  )
}
