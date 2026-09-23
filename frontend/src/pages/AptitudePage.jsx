import { useState } from 'react'
import { useStore } from '../store/useStore'
import { T } from '../utils/translations'
import { Badge, TabBar } from '../components/shared/UI'

const APTITUDE_QS = [
  { id:1, question:"A train 150m long passes a pole in 15 seconds. Speed of train?", options:["8 m/s","10 m/s","12 m/s","15 m/s"], correct:1, topic:"Speed & Distance", difficulty:"easy", explanation:"Speed = Distance/Time = 150/15 = 10 m/s" },
  { id:2, question:"15 workers finish a job in 48 days. Workers needed to finish in 30 days?", options:["20","22","24","26"], correct:2, topic:"Time & Work", difficulty:"medium", explanation:"15×48 = x×30 → x = 720/30 = 24 workers" },
  { id:3, question:"What is 30% of 25% of 400?", options:["25","30","35","40"], correct:1, topic:"Percentages", difficulty:"easy", explanation:"25% of 400 = 100. 30% of 100 = 30" },
  { id:4, question:"Man buys for ₹800, sells for ₹1000. Profit percentage?", options:["20%","25%","30%","15%"], correct:1, topic:"Profit & Loss", difficulty:"easy", explanation:"Profit = 200. Profit% = (200/800)×100 = 25%" },
  { id:5, question:"Next number: 2, 6, 12, 20, 30, ?", options:["40","42","44","45"], correct:1, topic:"Number Series", difficulty:"medium", explanation:"Differences: 4,6,8,10,12. Next = 30+12 = 42" },
  { id:6, question:"Simple interest on ₹5000 at 8% per annum for 3 years?", options:["₹1000","₹1200","₹1500","₹1800"], correct:1, topic:"Simple Interest", difficulty:"easy", explanation:"SI = P×R×T/100 = 5000×8×3/100 = ₹1200" },
  { id:7, question:"A:B = 3:4, B:C = 5:6. Find A:B:C.", options:["15:20:24","12:16:20","9:12:16","3:4:6"], correct:0, topic:"Ratios", difficulty:"medium", explanation:"A:B = 15:20, B:C = 20:24 → A:B:C = 15:20:24" },
  { id:8, question:"A can do work in 20 days, B in 30 days. Together?", options:["10 days","12 days","14 days","15 days"], correct:1, topic:"Time & Work", difficulty:"easy", explanation:"1/20+1/30 = 5/60 = 1/12 → 12 days" },
  { id:9, question:"Two pipes fill tank in 10h and 15h. Together in?", options:["5h","6h","7h","8h"], correct:1, topic:"Pipes & Cisterns", difficulty:"medium", explanation:"1/10+1/15 = 5/30 = 1/6 → 6 hours" },
  { id:10, question:"If 40% of a number is 120, what is the number?", options:["280","300","320","350"], correct:1, topic:"Percentages", difficulty:"easy", explanation:"40% of x = 120 → x = 120×100/40 = 300" },
  { id:11, question:"A sum of money doubles itself in 8 years at simple interest. What is the rate of interest per annum?", options:["10%","12.5%","15%","16.67%"], correct:1, topic:"Simple Interest", difficulty:"easy", explanation:"Interest = Principal. P = P*R*8/100 => R = 12.5% per annum." },
  { id:12, question:"What is the probability of rolling a sum of 8 with two six-sided dice?", options:["5/36","1/6","7/36","1/12"], correct:0, topic:"Probability", difficulty:"medium", explanation:"Favorable outcomes: (2,6), (3,5), (4,4), (5,3), (6,2) - total 5. Total outcomes = 36. Prob = 5/36." },
  { id:13, question:"The ratio of ages of Ram and Shyam is 4:5. After 6 years, their ratio becomes 5:6. Ram's present age?", options:["18 years","20 years","24 years","30 years"], correct:2, topic:"Age Problems", difficulty:"medium", explanation:"(4x+6)/(5x+6) = 5/6 => 24x+36 = 25x+30 => x=6. Ram's age = 4x = 24." },
  { id:14, question:"In a family party, every person shakes hands with every other person. If there are 10 people, how many handshakes take place?", options:["45","55","90","100"], correct:0, topic:"Permutations & Combinations", difficulty:"medium", explanation:"Handshakes = 10C2 = (10*9)/2 = 45." },
  { id:15, question:"By selling a watch for ₹1440, a man suffers a loss of 10%. Selling price to gain 10%?", options:["₹1600","₹1720","₹1760","₹1800"], correct:2, topic:"Profit & Loss", difficulty:"medium", explanation:"CP = 1440 / 0.9 = ₹1600. SP for 10% gain = 1600 * 1.1 = ₹1760." },
  { id:16, question:"A batsman scores 98 runs in his 17th inning and increases his average by 3. What is his average after 17 innings?", options:["45","47","50","52"], correct:2, topic:"Averages", difficulty:"hard", explanation:"Let old average be x. 16x + 98 = 17(x+3) => x = 47. New average = 47 + 3 = 50." },
  { id:17, question:"How many times do the hands of a clock overlap in a single day (24 hours)?", options:["20","21","22","24"], correct:2, topic:"Clocks", difficulty:"medium", explanation:"Hands overlap 11 times every 12 hours. In 24 hours, they overlap 22 times." },
  { id:18, question:"If 3rd January of a year is Sunday, what day will be 3rd February of that year (non-leap year)?", options:["Tuesday","Wednesday","Thursday","Friday"], correct:1, topic:"Calendars", difficulty:"medium", explanation:"Days from Jan 3 to Feb 3 = 31 days. 31 % 7 = 3 odd days. Sunday + 3 days = Wednesday." },
  { id:19, question:"A shopkeeper cheats by using a weight of 800g instead of 1kg. What is his actual profit percentage?", options:["20%","25%","30%","33.3%"], correct:1, topic:"Profit & Loss", difficulty:"hard", explanation:"Profit% = (Error / True Value - Error) * 100 = (200 / 800) * 100 = 25%." },
  { id:20, question:"A sum of money placed at compound interest doubles itself in 5 years. In how many years will it become 8 times itself?", options:["10 years","12 years","15 years","20 years"], correct:2, topic:"Compound Interest", difficulty:"medium", explanation:"P doubles in 5 years. Becomes 4 times in 10 years, and 8 times in 15 years." },
  { id:21, question:"A container holds 80 litres of milk. 8 litres is replaced with water. This process is repeated once more. Milk left?", options:["64.8 litres","65.6 litres","66.2 litres","68.4 litres"], correct:0, topic:"Mixtures & Alligations", difficulty:"hard", explanation:"Milk left = 80 * (1 - 8/80)^2 = 80 * 0.81 = 64.8 litres." },
  { id:22, question:"What is the unit digit of 7^95 - 3^58?", options:["0","4","6","7"], correct:1, topic:"Number System", difficulty:"hard", explanation:"7^95 unit digit is 3 (cycle of 4). 3^58 unit digit is 9. 13 - 9 = 4." },
  { id:23, question:"If log 2 = 0.3010 and log 3 = 0.4771, find the value of log 6.", options:["0.7012","0.7781","0.8112","0.8451"], correct:1, topic:"Logarithms", difficulty:"easy", explanation:"log 6 = log 2 + log 3 = 0.3010 + 0.4771 = 0.7781." },
  { id:24, question:"In a group of 80 people, 40 speak English and 50 speak Hindi. If every person speaks at least one language, how many speak both?", options:["5","10","15","20"], correct:1, topic:"Venn Diagrams", difficulty:"easy", explanation:"Both = N(E) + N(H) - Total = 40 + 50 - 80 = 10." },
  { id:25, question:"A cuboid of 4x3x3 cm is painted red on all faces and cut into 1cm cubes. How many cubes have no paint?", options:["2","4","6","8"], correct:0, topic:"Cube Cuts", difficulty:"hard", explanation:"Inner cubes = (l-2)*(w-2)*(h-2) = (4-2)*(3-2)*(3-2) = 2 * 1 * 1 = 2." }
]

const CODING_QS = [
  { id:1, title:"Two Sum", difficulty:"easy", company:"TCS, Infosys, Amazon", topic:"Arrays", gfg:"https://www.geeksforgeeks.org/given-an-array-a-and-a-number-x-check-for-pair-in-a-with-sum-as-x/", lc:"https://leetcode.com/problems/two-sum/" },
  { id:2, title:"Reverse a Linked List", difficulty:"easy", company:"Wipro, Cognizant, Microsoft", topic:"Linked List", gfg:"https://www.geeksforgeeks.org/reverse-a-linked-list/", lc:"https://leetcode.com/problems/reverse-linked-list/" },
  { id:3, title:"Valid Parentheses", difficulty:"easy", company:"All Companies", topic:"Stack", gfg:"https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/", lc:"https://leetcode.com/problems/valid-parentheses/" },
  { id:4, title:"Binary Search", difficulty:"easy", company:"TCS, Accenture, Google", topic:"Searching", gfg:"https://www.geeksforgeeks.org/binary-search/", lc:"https://leetcode.com/problems/binary-search/" },
  { id:5, title:"Maximum Subarray – Kadane's", difficulty:"medium", company:"TCS, Cognizant, Amazon", topic:"Dynamic Programming", gfg:"https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/", lc:"https://leetcode.com/problems/maximum-subarray/" },
  { id:6, title:"Longest Common Subsequence", difficulty:"medium", company:"Infosys, Wipro, Google", topic:"Dynamic Programming", gfg:"https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/", lc:"https://leetcode.com/problems/longest-common-subsequence/" },
  { id:7, title:"Number of Islands (BFS/DFS)", difficulty:"medium", company:"Amazon, Accenture, Microsoft", topic:"Graphs", gfg:"https://www.geeksforgeeks.org/find-number-of-islands/", lc:"https://leetcode.com/problems/number-of-islands/" },
  { id:8, title:"Trapping Rain Water", difficulty:"hard", company:"Google, Amazon", topic:"Arrays", gfg:"https://www.geeksforgeeks.org/trapping-rain-water/", lc:"https://leetcode.com/problems/trapping-rain-water/" },
  { id:9, title:"LRU Cache", difficulty:"hard", company:"Amazon, Microsoft, Flipkart", topic:"Design", gfg:"https://www.geeksforgeeks.org/lru-cache-implementation/", lc:"https://leetcode.com/problems/lru-cache/" },
  { id:10, title:"Merge K Sorted Lists", difficulty:"hard", company:"Google, Amazon, Microsoft", topic:"Linked List", gfg:"https://www.geeksforgeeks.org/merge-k-sorted-linked-lists/", lc:"https://leetcode.com/problems/merge-k-sorted-lists/" },
  { id:11, title:"Container With Most Water", difficulty:"medium", company:"TCS, Wipro, Facebook", topic:"Two Pointers", gfg:"https://www.geeksforgeeks.org/container-with-most-water/", lc:"https://leetcode.com/problems/container-with-most-water/" },
  { id:12, title:"Best Time to Buy and Sell Stock", difficulty:"easy", company:"TCS, Cognizant, Amazon", topic:"Arrays", gfg:"https://www.geeksforgeeks.org/best-time-to-buy-and-sell-stock/", lc:"https://leetcode.com/problems/best-time-to-buy-and-sell-stock/" },
  { id:13, title:"Search in Rotated Sorted Array", difficulty:"medium", company:"Infosys, Wipro, Microsoft", topic:"Searching", gfg:"https://www.geeksforgeeks.org/search-an-element-in-a-sorted-and-pivoted-array/", lc:"https://leetcode.com/problems/search-in-rotated-sorted-array/" },
  { id:14, title:"Product of Array Except Self", difficulty:"medium", company:"Accenture, Google, Facebook", topic:"Arrays", gfg:"https://www.geeksforgeeks.org/a-product-array-puzzle/", lc:"https://leetcode.com/problems/product-of-array-except-self/" },
  { id:15, title:"Valid Anagram", difficulty:"easy", company:"TCS, Wipro, Amazon", topic:"Strings", gfg:"https://www.geeksforgeeks.org/check-whether-two-strings-are-anagram-of-each-other/", lc:"https://leetcode.com/problems/valid-anagram/" },
  { id:16, title:"Group Anagrams", difficulty:"medium", company:"Google, Amazon, Uber", topic:"Strings", gfg:"https://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together/", lc:"https://leetcode.com/problems/group-anagrams/" },
  { id:17, title:"Maximum Depth of Binary Tree", difficulty:"easy", company:"Accenture, Microsoft", topic:"Binary Tree", gfg:"https://www.geeksforgeeks.org/write-a-c-program-to-find-the-maximum-depth-or-height-of-a-tree/", lc:"https://leetcode.com/problems/maximum-depth-of-binary-tree/" },
  { id:18, title:"Longest Substring Without Repeating Characters", difficulty:"medium", company:"All Companies", topic:"Sliding Window", gfg:"https://www.geeksforgeeks.org/length-of-the-longest-substring-without-repeating-characters/", lc:"https://leetcode.com/problems/longest-substring-without-repeating-characters/" },
  { id:19, title:"3Sum", difficulty:"medium", company:"Google, Facebook, Amazon", topic:"Two Pointers", gfg:"https://www.geeksforgeeks.org/find-a-triplet-that-sum-to-a-given-value/", lc:"https://leetcode.com/problems/3sum/" },
  { id:20, title:"Word Search", difficulty:"medium", company:"Microsoft, Amazon, Apple", topic:"Backtracking", gfg:"https://www.geeksforgeeks.org/word-search-backtracking/", lc:"https://leetcode.com/problems/word-search/" },
  { id:21, title:"Merge Intervals", difficulty:"medium", company:"TCS, Infosys, Google", topic:"Arrays", gfg:"https://www.geeksforgeeks.org/merging-intervals/", lc:"https://leetcode.com/problems/merge-intervals/" },
  { id:22, title:"Non-overlapping Intervals", difficulty:"medium", company:"Google, Amazon", topic:"Greedy", gfg:"https://www.geeksforgeeks.org/select-maximum-number-of-activities-from-the-given-set-of-activities/", lc:"https://leetcode.com/problems/non-overlapping-intervals/" },
  { id:23, title:"House Robber", difficulty:"medium", company:"Wipro, Cognizant, Airbnb", topic:"Dynamic Programming", gfg:"https://www.geeksforgeeks.org/find-maximum-sum-such-that-no-two-elements-are-adjacent/", lc:"https://leetcode.com/problems/house-robber/" },
  { id:24, title:"Clone Graph", difficulty:"medium", company:"Google, Facebook", topic:"Graphs", gfg:"https://www.geeksforgeeks.org/clone-an-undirected-graph/", lc:"https://leetcode.com/problems/clone-graph/" },
  { id:25, title:"Median of Two Sorted Arrays", difficulty:"hard", company:"Google, Goldman Sachs", topic:"Searching", gfg:"https://www.geeksforgeeks.org/median-of-two-sorted-arrays-of-different-sizes/", lc:"https://leetcode.com/problems/median-of-two-sorted-arrays/" }
]

export default function AptitudePage() {
  const { language } = useStore()
  const t = T[language]
  const [tab, setTab] = useState('aptitude')
  const [diff, setDiff] = useState('all')
  const [topic, setTopic] = useState('all')
  const [answers, setAnswers] = useState({})

  const TABS = [{ key:'aptitude', icon:'🧮', label:t.aptitude }, { key:'coding', icon:'💻', label:t.coding }]

  const topics = ['all', ...new Set(APTITUDE_QS.map(q => q.topic))]
  const codingTopics = ['all', ...new Set(CODING_QS.map(q => q.topic))]

  const filteredApt = APTITUDE_QS.filter(q =>
    (diff === 'all' || q.difficulty === diff) &&
    (topic === 'all' || q.topic === topic)
  )
  const filteredCoding = CODING_QS.filter(q =>
    (diff === 'all' || q.difficulty === diff) &&
    (topic === 'all' || q.topic === topic)
  )

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      <div className="mb-6">
        <h1 className="section-title">🧮 {t.aptitudeTitle}</h1>
        <p className="section-sub">{t.aptitudeSub}</p>
      </div>

      <TabBar tabs={TABS} active={tab} onChange={t2 => { setTab(t2); setAnswers({}); setDiff('all'); setTopic('all') }} />

      {/* Filters */}
      <div className="card mb-5 flex flex-wrap gap-3 items-end">
        <div>
          <label className="label">Difficulty</label>
          <div className="flex gap-2">
            {['all','easy','medium','hard'].map(d => (
              <button key={d} onClick={() => setDiff(d)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all
                  ${diff === d ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-slate-600 border-slate-300 hover:border-indigo-400'}`}>
                {d.charAt(0).toUpperCase()+d.slice(1)}
              </button>
            ))}
          </div>
        </div>
        <div>
          <label className="label">Topic</label>
          <select className="input w-auto text-xs" value={topic} onChange={e => setTopic(e.target.value)}>
            {(tab === 'aptitude' ? topics : codingTopics).map(tp => (
              <option key={tp} value={tp}>{tp === 'all' ? 'All Topics' : tp}</option>
            ))}
          </select>
        </div>
        <div className="ml-auto flex gap-2">
          <a href="https://www.indiabix.com" target="_blank" rel="noreferrer" className="btn-secondary btn-sm text-xs">📚 IndiaBix ↗</a>
          <a href="https://www.careerride.com" target="_blank" rel="noreferrer" className="btn-secondary btn-sm text-xs">📖 CareerRide ↗</a>
        </div>
      </div>

      {tab === 'aptitude' && (
        <div className="space-y-4">
          {filteredApt.map((q, i) => (
            <div key={q.id} className="card">
              <div className="flex items-start justify-between gap-3 mb-4">
                <div className="font-semibold text-slate-800 text-sm flex-1">Q{i+1}. {q.question}</div>
                <div className="flex gap-1.5 shrink-0">
                  <Badge type={q.difficulty}>{q.difficulty}</Badge>
                  <Badge type="purple">{q.topic}</Badge>
                </div>
              </div>
              <div className="grid sm:grid-cols-2 gap-2">
                {q.options.map((opt, j) => {
                  const sel = answers[q.id]
                  let cls = 'bg-slate-50 border-slate-200 text-slate-700 hover:border-indigo-400 hover:bg-indigo-50 cursor-pointer'
                  if (sel !== undefined) {
                    if (j === q.correct) cls = 'bg-green-50 border-green-400 text-green-800 cursor-default'
                    else if (j === sel) cls = 'bg-red-50 border-red-400 text-red-800 cursor-default'
                    else cls = 'bg-slate-50 border-slate-200 text-slate-400 cursor-default'
                  }
                  return (
                    <button key={j} disabled={sel !== undefined}
                      onClick={() => setAnswers(a => ({...a, [q.id]: j}))}
                      className={`border rounded-xl px-4 py-2.5 text-sm text-left transition-all font-medium ${cls}`}>
                      {String.fromCharCode(65+j)}) {opt}
                    </button>
                  )
                })}
              </div>
              {answers[q.id] !== undefined && (
                <div className={`mt-3 p-3 rounded-xl text-xs font-medium ${answers[q.id] === q.correct ? 'bg-green-50 text-green-800 border border-green-200' : 'bg-red-50 text-red-800 border border-red-200'}`}>
                  {answers[q.id] === q.correct ? `✅ ${t.correct}` : `❌ ${t.wrong}`} — {q.explanation}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {tab === 'coding' && (
        <div className="space-y-3">
          {filteredCoding.map((q) => (
            <div key={q.id} className="card hover:border-indigo-200 hover:shadow-md transition-all">
              <div className="flex items-center justify-between mb-2">
                <div className="font-semibold text-slate-800 text-sm">💻 {q.title}</div>
                <div className="flex gap-1.5">
                  <Badge type={q.difficulty}>{q.difficulty}</Badge>
                  <Badge type="purple">{q.topic}</Badge>
                </div>
              </div>
              <div className="text-xs text-slate-500 mb-3">🏢 {q.company}</div>
              <div className="flex gap-3">
                <a href={q.gfg} target="_blank" rel="noreferrer"
                  className="inline-flex items-center gap-1 text-xs font-semibold text-green-700 bg-green-50 border border-green-200 px-3 py-1.5 rounded-lg hover:bg-green-100 transition-all">
                  🌱 GeeksforGeeks ↗
                </a>
                <a href={q.lc} target="_blank" rel="noreferrer"
                  className="inline-flex items-center gap-1 text-xs font-semibold text-orange-700 bg-orange-50 border border-orange-200 px-3 py-1.5 rounded-lg hover:bg-orange-100 transition-all">
                  💡 LeetCode ↗
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
