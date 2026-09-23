from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.schemas import (SpeakingFeedbackRequest, WritingFeedbackRequest,
                                 ResumeRequest, InterviewSimulateRequest, InterviewGradeRequest)
from app.services import ai_service

# ── Communication ─────────────────────────────────────────────────────────────
comm_router = APIRouter(prefix="/api/communication", tags=["communication"])

@comm_router.post("/speaking-feedback")
def speaking_feedback(data: SpeakingFeedbackRequest,
                      current_user: User = Depends(get_current_user)):
    feedback = ai_service.analyse_speaking(data.transcript, data.topic, data.language)
    return feedback

@comm_router.post("/writing-feedback")
def writing_feedback(data: WritingFeedbackRequest,
                     current_user: User = Depends(get_current_user)):
    feedback = ai_service.analyse_writing(data.text, data.mode, data.language)
    return feedback


# ── Placement ─────────────────────────────────────────────────────────────────
placement_router = APIRouter(prefix="/api/placement", tags=["placement"])

COMPANIES_DATA = [
    {
        "id": 1, "name": "TCS", "logo": "T",
        "process": "Online Test (Quant+Verbal+Reasoning+Coding) → Technical Interview (TR) → Managerial (MR) → HR",
        "package": "3.6–7.2 LPA (Ninja & Digital & Prime Roles)", "eligibility": "60%+ in 10th, 12th, UG/PG. Max 1 active backlog allowed at time of test.",
        "aptitude_topics": ["Number System", "Speed & Distance", "Time & Work", "Profit & Loss", "Logical Reasoning", "Data Interpretation", "Probability", "Permutations"],
        "coding_questions": [
            {"title": "Two Sum", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/check-if-a-pair-with-given-sum-exists-in-array/",
             "lc": "https://leetcode.com/problems/two-sum/"},
            {"title": "Reverse a String", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/reverse-a-string-in-java/",
             "lc": "https://leetcode.com/problems/reverse-string/"},
            {"title": "Find duplicate in array", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/find-duplicates-in-on-time-and-constant-extra-space/",
             "lc": "https://leetcode.com/problems/find-the-duplicate-number/"},
            {"title": "Maximum Subarray (Kadane)", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/",
             "lc": "https://leetcode.com/problems/maximum-subarray/"},
            {"title": "Merge Sorted Array", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/merge-two-sorted-arrays/",
             "lc": "https://leetcode.com/problems/merge-sorted-array/"},
            {"title": "LinkedList Cycle", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/detect-loop-in-a-linked-list/",
             "lc": "https://leetcode.com/problems/linked-list-cycle/"},
            {"title": "Product of Array Except Self", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/a-product-array-puzzle/",
             "lc": "https://leetcode.com/problems/product-of-array-except-self/"},
            {"title": "Container With Most Water", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/container-with-most-water/",
             "lc": "https://leetcode.com/problems/container-with-most-water/"},
            {"title": "Subarray Sum Equals K", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/number-of-subarrays-having-sum-exactly-equal-to-k/",
             "lc": "https://leetcode.com/problems/subarray-sum-equals-k/"},
            {"title": "House Robber", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/find-maximum-sum-such-that-no-two-elements-are-adjacent/",
             "lc": "https://leetcode.com/problems/house-robber/"},
            {"title": "Merge Intervals", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/merging-intervals/",
             "lc": "https://leetcode.com/problems/merge-intervals/"}
        ],
        "interview_questions": [
            "Tell me about yourself and your final year project in detail.",
            "Explain the difference between call by value and call by reference in Java/C++.",
            "What is normalization in DBMS? Explain 1NF, 2NF, 3NF and BCNF.",
            "What is a dangling pointer? How can you avoid it?",
            "Explain static polymorphism vs dynamic polymorphism with code examples.",
            "What is the difference between primary key, unique key, and candidate key?",
            "What are the phases of SDLC (Software Development Life Cycle)?",
            "Explain ACID properties in DBMS.",
            "Why do you want to join TCS over other service-based companies?",
            "Are you comfortable with relocation and working in night shifts?"
        ],
    },
    {
        "id": 2, "name": "Infosys", "logo": "I",
        "process": "Online Assessment (Reasoning, Mathematical, Verbal, Pseudocode, Puzzle) → Technical + HR Interview",
        "package": "3.6–8.0 LPA (System Engineer & Specialist Programmer Roles)", "eligibility": "65%+ or 6.5+ CGPA aggregate in UG. Max 2 backlogs allowed.",
        "aptitude_topics": ["Data Interpretation", "Cryptarithmetic", "Logical Reasoning", "Verbal Ability", "Sentence Completion", "Puzzles", "Data Sufficiency"],
        "coding_questions": [
            {"title": "Palindrome Check", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/check-whether-a-number-is-palindrome-or-not/",
             "lc": "https://leetcode.com/problems/valid-palindrome/"},
            {"title": "Fibonacci Series", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/program-for-nth-fibonacci-number/",
             "lc": "https://leetcode.com/problems/fibonacci-number/"},
            {"title": "Longest Common Subsequence", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/",
             "lc": "https://leetcode.com/problems/longest-common-subsequence/"},
            {"title": "Valid Anagram", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/check-whether-two-strings-are-anagram-of-each-other/",
             "lc": "https://leetcode.com/problems/valid-anagram/"},
            {"title": "Climbing Stairs", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/count-ways-reach-nth-stair/",
             "lc": "https://leetcode.com/problems/climbing-stairs/"},
            {"title": "Search in Rotated Sorted Array", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/search-an-element-in-a-sorted-and-pivoted-array/",
             "lc": "https://leetcode.com/problems/search-in-rotated-sorted-array/"},
            {"title": "Group Anagrams", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/given-a-sequence-of-words-print-all-anagrams-together/",
             "lc": "https://leetcode.com/problems/group-anagrams/"},
            {"title": "Jump Game", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/minimum-number-jumps-reach-end-array/",
             "lc": "https://leetcode.com/problems/jump-game/"},
            {"title": "Rotate Image", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/rotate-a-matrix-by-90-degree-in-clockwise-direction-without-using-any-extra-space/",
             "lc": "https://leetcode.com/problems/rotate-image/"},
            {"title": "Kth Largest Element in an Array", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/k-largest-elements-in-an-array/",
             "lc": "https://leetcode.com/problems/kth-largest-element-in-an-array/"},
            {"title": "Unique Paths", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/count-possible-paths-top-left-bottom-right-nxm-matrix/",
             "lc": "https://leetcode.com/problems/unique-paths/"}
        ],
        "interview_questions": [
            "What was your role in your final year project and what challenges did you face?",
            "Explain OOP concepts in detail: Encapsulation, Inheritance, Polymorphism, Abstraction.",
            "What is a pointer in C++? Explain the difference between pointer and reference.",
            "Explain the concept of virtual functions and abstract classes.",
            "What is a database transaction? Explain commit, rollback, and savepoint.",
            "What is an index in DBMS? How does it improve query performance?",
            "What is the difference between abstract class and interface in Java?",
            "Write a SQL query to find the second highest salary of an employee.",
            "What are your career plans for the next 5 years?",
            "How do you deal with conflicts in a project team?"
        ],
    },
    {
        "id": 3, "name": "Wipro", "logo": "W",
        "process": "Wipro Elite National Talent Hunt (Aptitude + Written English + Coding) → TR Interview → HR Interview",
        "package": "3.5–6.5 LPA", "eligibility": "60%+ in 10th, 12th, and 60% or 6.0 CGPA in graduation. No active backlogs.",
        "aptitude_topics": ["Time & Work", "Percentages", "Series Completion", "Syllogisms", "Data Sufficiency", "Blood Relations", "Algebra"],
        "coding_questions": [
            {"title": "Reverse a Linked List", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/reverse-a-linked-list/",
             "lc": "https://leetcode.com/problems/reverse-linked-list/"},
            {"title": "Valid Parentheses", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/",
             "lc": "https://leetcode.com/problems/valid-parentheses/"},
            {"title": "Binary Search", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/binary-search/",
             "lc": "https://leetcode.com/problems/binary-search/"},
            {"title": "Merge Two Sorted Lists", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/merge-two-sorted-linked-lists/",
             "lc": "https://leetcode.com/problems/merge-two-sorted-lists/"},
            {"title": "Invert Binary Tree", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/write-an-efficient-c-function-to-convert-a-tree-into-its-mirror-tree/",
             "lc": "https://leetcode.com/problems/invert-binary-tree/"},
            {"title": "Detect Cycle in Directed Graph", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/detect-cycle-in-a-graph/",
             "lc": "https://leetcode.com/problems/course-schedule/"},
            {"title": "Word Search", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/word-search-board-of-characters/",
             "lc": "https://leetcode.com/problems/word-search/"},
            {"title": "Min Stack", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/design-a-stack-that-supports-getmin-in-o1-time-and-o1-extra-space/",
             "lc": "https://leetcode.com/problems/min-stack/"},
            {"title": "3Sum", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/find-a-triplet-that-sum-to-a-given-value/",
             "lc": "https://leetcode.com/problems/3sum/"},
            {"title": "Set Matrix Zeroes", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/a-boolean-matrix-question/",
             "lc": "https://leetcode.com/problems/set-matrix-zeroes/"}
        ],
        "interview_questions": [
            "Explain the difference between structure and union in C.",
            "What is a memory leak? How can it be prevented in programming?",
            "Explain stack vs heap memory allocation.",
            "What is a join in SQL? Explain Inner, Left, Right, and Full joins.",
            "Explain exception handling keywords in Java/Python (try, catch/except, finally, throw).",
            "What is a constructor? Explain default, parameterized, and copy constructors.",
            "What is the difference between multiprocessing and multithreading?",
            "Write a program to count the number of vowels and consonants in a string.",
            "Describe a situation where you had to learn a new skill quickly.",
            "Why should Wipro hire you? What value do you bring?"
        ],
    },
    {
        "id": 4, "name": "Accenture", "logo": "A",
        "process": "Cognitive & Technical Assessment → Coding Round (2 Questions) → Communication Test → Interview",
        "package": "4.5–8.5 LPA (Associate Software Engineer & Advanced ASE Roles)", "eligibility": "60%+ or 6.0 CGPA aggregate. No active backlogs. All branches eligible.",
        "aptitude_topics": ["Attention to Detail", "Abstract Reasoning", "Quantitative Aptitude", "Verbal Comprehension", "MS Office Basics", "Pseudocoding"],
        "coding_questions": [
            {"title": "Binary Search", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/binary-search/",
             "lc": "https://leetcode.com/problems/binary-search/"},
            {"title": "Merge Two Sorted Arrays", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/merge-two-sorted-arrays/",
             "lc": "https://leetcode.com/problems/merge-sorted-array/"},
            {"title": "Two Sum", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/given-an-array-a-and-a-number-x-check-for-pair-in-a-with-sum-as-x/",
             "lc": "https://leetcode.com/problems/two-sum/"},
            {"title": "Valid Anagram", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/check-whether-two-strings-are-anagram-of-each-other/",
             "lc": "https://leetcode.com/problems/valid-anagram/"},
            {"title": "Best Time to Buy and Sell Stock", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/best-time-to-buy-and-sell-stock/",
             "lc": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
            {"title": "Spiral Matrix", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/print-a-given-matrix-in-spiral-form/",
             "lc": "https://leetcode.com/problems/spiral-matrix/"},
            {"title": "Search a 2D Matrix", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/search-in-a-row-wise-and-column-wise-sorted-matrix/",
             "lc": "https://leetcode.com/problems/search-a-2d-matrix/"},
            {"title": "Implement Trie (Prefix Tree)", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/trie-insert-and-search/",
             "lc": "https://leetcode.com/problems/implement-trie-prefix-tree/"},
            {"title": "Non-overlapping Intervals", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/activity-selection-problem-greedy-algo-1/",
             "lc": "https://leetcode.com/problems/non-overlapping-intervals/"},
            {"title": "Valid Sudoku", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/check-if-given-sudoku-board-configuration-is-valid-or-not/",
             "lc": "https://leetcode.com/problems/valid-sudoku/"}
        ],
        "interview_questions": [
            "Explain Cloud Computing and its service models (IaaS, PaaS, SaaS).",
            "What is Agile methodology? How does it differ from the Waterfall model?",
            "What is Git? Explain commands like clone, commit, push, pull, merge, and rebase.",
            "What is a primary key vs foreign key? How do they establish relationships?",
            "Explain the difference between abstract class and interface with respect to multiple inheritance.",
            "What is an API? Explain REST API constraints and HTTP methods (GET, POST, PUT, DELETE).",
            "Write a pseudocode to check if a number is prime.",
            "How do you prioritize tasks when you have tight deadlines for multiple projects?",
            "Explain a project where you worked in a team. What was your main contribution?",
            "How do you handle feedback or constructive criticism?"
        ],
    },
    {
        "id": 5, "name": "Cognizant", "logo": "C",
        "process": "GenC & GenC Elevate Assessment (Quantitative, Logical, English, Coding/Automata Fix) → Technical Interview → HR Interview",
        "package": "4.0–7.5 LPA", "eligibility": "60%+ in 10th, 12th, and UG. Max 1 active backlog. Year of graduation eligibility criteria applies.",
        "aptitude_topics": ["Number Series", "Blood Relations", "Direction Sense", "Coding Decoding", "Quantitative Aptitude", "Data Sufficiency"],
        "coding_questions": [
            {"title": "Invert Binary Tree", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/write-an-efficient-c-function-to-convert-a-tree-into-its-mirror-tree/",
             "lc": "https://leetcode.com/problems/invert-binary-tree/"},
            {"title": "Maximum Depth of Binary Tree", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/write-a-c-program-to-find-the-maximum-depth-or-height-of-a-tree/",
             "lc": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"},
            {"title": "LinkedList Cycle", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/detect-loop-in-a-linked-list/",
             "lc": "https://leetcode.com/problems/linked-list-cycle/"},
            {"title": "Climbing Stairs", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/count-ways-reach-nth-stair/",
             "lc": "https://leetcode.com/problems/climbing-stairs/"},
            {"title": "Maximum Subarray (Kadane)", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/",
             "lc": "https://leetcode.com/problems/maximum-subarray/"},
            {"title": "Longest Consecutive Sequence", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/longest-consecutive-subsequence/",
             "lc": "https://leetcode.com/problems/longest-consecutive-sequence/"},
            {"title": "Valid Palindrome II", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/check-if-a-string-can-be-converted-to-a-palindrome-by-removing-at-most-one-character/",
             "lc": "https://leetcode.com/problems/valid-palindrome-ii/"},
            {"title": "Coin Change", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/coin-change-dp-7/",
             "lc": "https://leetcode.com/problems/coin-change/"},
            {"title": "Daily Temperatures", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/next-greater-element/",
             "lc": "https://leetcode.com/problems/daily-temperatures/"},
            {"title": "Number of Islands", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/find-number-of-islands/",
             "lc": "https://leetcode.com/problems/number-of-islands/"}
        ],
        "interview_questions": [
            "Explain Software Development Life Cycle (SDLC) models: Waterfall, Spiral, and V-Model.",
            "What is DBMS? Explain the difference between DBMS and RDBMS.",
            "What is normalization and denormalization? Why do we normalize databases?",
            "Explain what is a join. Write a query to join three tables.",
            "Explain garbage collection in Java. How does JVM manage heap memory?",
            "What is the difference between final, finally, and finalize in Java?",
            "Write a program to swap two numbers without using a third variable.",
            "Write a program to check if an input string is a palindrome.",
            "Tell me about a time you had a disagreement with a team member and how you resolved it.",
            "Why do you want to join Cognizant? What are your expectations?"
        ],
    },
    {
        "id": 6, "name": "Mr. Cooper", "logo": "M",
        "process": "Online Aptitude & Coding Test → Technical Round (Core CS + DSA) → Technical Round 2 → HR Interview",
        "package": "5.5–9.5 LPA", "eligibility": "65%+ or 6.5 CGPA aggregate. CS/IT/ECE branches preferred. Strong programming skills required.",
        "aptitude_topics": ["Data Interpretation", "Logical Reasoning", "Quantitative Aptitude", "Probability & Combinatorics", "Mortgage & Financial Basics"],
        "coding_questions": [
            {"title": "Two Sum", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/given-an-array-a-and-a-number-x-check-for-pair-in-a-with-sum-as-x/",
             "lc": "https://leetcode.com/problems/two-sum/"},
            {"title": "Valid Parentheses", "difficulty": "easy",
             "gfg": "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/",
             "lc": "https://leetcode.com/problems/valid-parentheses/"},
            {"title": "Search in Rotated Sorted Array", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/search-an-element-in-a-sorted-and-pivoted-array/",
             "lc": "https://leetcode.com/problems/search-in-rotated-sorted-array/"},
            {"title": "Longest Substring Without Repeating Characters", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/length-of-the-longest-substring-without-repeating-characters/",
             "lc": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
            {"title": "LRU Cache", "difficulty": "hard",
             "gfg": "https://www.geeksforgeeks.org/lru-cache-implementation/",
             "lc": "https://leetcode.com/problems/lru-cache/"},
            {"title": "Maximum Product Subarray", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/maximum-product-subarray/",
             "lc": "https://leetcode.com/problems/maximum-subarray/"},
            {"title": "House Robber II", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/find-maximum-sum-such-that-no-two-elements-are-adjacent/",
             "lc": "https://leetcode.com/problems/house-robber-ii/"},
            {"title": "Word Break", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/word-break-problem-dp-32/",
             "lc": "https://leetcode.com/problems/word-break/"},
            {"title": "Design Add and Search Words Data Structure", "difficulty": "medium",
             "gfg": "https://www.geeksforgeeks.org/trie-insert-and-search/",
             "lc": "https://leetcode.com/problems/design-add-and-search-words-data-structure/"},
            {"title": "Edit Distance", "difficulty": "hard",
             "gfg": "https://www.geeksforgeeks.org/edit-distance-dp-5/",
             "lc": "https://leetcode.com/problems/edit-distance/"}
        ],
        "interview_questions": [
            "Explain core principles of Object-Oriented Programming (OOP) in detail.",
            "What is a smart pointer in C++? Explain unique_ptr, shared_ptr, and weak_ptr.",
            "What is a primary key, foreign key, and unique constraint? Explain database indexes.",
            "What is a transaction? Explain ACID properties and transaction isolation levels.",
            "What is the difference between SQL and NoSQL databases? When would you choose which?",
            "Explain the difference between a process and a thread. What is thread synchronization?",
            "What is a deadlock? What are the four necessary conditions for deadlock to occur?",
            "Write a function to find the middle element of a singly linked list in a single traversal.",
            "Write a function to detect a loop in a linked list and return the starting node.",
            "Why are you interested in Mr. Cooper? (Note: Mr. Cooper is a leading mortgage service provider in the US)."
        ],
    }
]

@placement_router.get("/companies")
def get_companies():
    return [{"id": c["id"], "name": c["name"], "logo": c["logo"],
             "package": c["package"], "process": c["process"]} for c in COMPANIES_DATA]

@placement_router.get("/companies/{company_id}")
def get_company(company_id: int, _: User = Depends(get_current_user)):
    company = next((c for c in COMPANIES_DATA if c["id"] == company_id), None)
    if not company:
        from fastapi import HTTPException
        raise HTTPException(404, "Company not found")
    
    from app.api.placement_questions import get_company_aptitude, get_company_coding
    company_copy = dict(company)
    company_copy["aptitude_questions"] = get_company_aptitude(company["name"])
    company_copy["coding_questions"] = get_company_coding(company["name"])
    return company_copy

def extract_text_from_pdf(file_bytes: bytes) -> str:
    import io
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    import io
    import docx
    doc = docx.Document(io.BytesIO(file_bytes))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

@placement_router.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...), _: User = Depends(get_current_user)):
    try:
        content_type = file.content_type
        filename = file.filename.lower()
        file_bytes = await file.read()
        text = ""
        if filename.endswith(".pdf") or content_type == "application/pdf":
            try:
                text = extract_text_from_pdf(file_bytes)
            except Exception as e:
                print(f"PDF extraction failed, falling back to empty text: {e}")
                text = ""
        elif filename.endswith(".docx") or content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            try:
                text = extract_text_from_docx(file_bytes)
            except Exception as e:
                print(f"DOCX extraction failed, falling back to empty text: {e}")
                text = ""
        elif filename.endswith(".txt") or content_type.startswith("text/"):
            try:
                text = file_bytes.decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"Text decoding failed, falling back to empty text: {e}")
                text = ""
        else:
            return {"error": "Unsupported file type. Please upload a PDF, DOCX, or TXT file."}
        
        try:
            parsed = ai_service.extract_resume_details(text.strip())
        except Exception as parse_err:
            print(f"Error in extract_resume_details: {parse_err}")
            parsed = {
                "role": "Software Developer",
                "summary": "Experience in software development and systems design.",
                "projects": ["General Software Development"],
                "skills": ["Python", "SQL"]
            }
        return {"resume_text": text.strip(), "parsed_details": parsed}
    except Exception as outer_err:
        print(f"Critical error in upload_resume endpoint: {outer_err}")
        return {"error": f"Internal parser error: {str(outer_err)}"}

@placement_router.post("/resume-analyse")
def analyse_resume(data: ResumeRequest, language: str = "en", _: User = Depends(get_current_user)):
    return ai_service.analyse_resume(data.resume_text, language)

@placement_router.post("/interview-simulate")
def simulate_interview(data: InterviewSimulateRequest, language: str = "en",
                       _: User = Depends(get_current_user)):
    return ai_service.generate_interview_question(
        data.company_name, data.round_type, data.difficulty, data.resume_text, language
    )

@placement_router.post("/interview-model-answer")
def get_interview_model_answer(question: str, language: str = "en", _: User = Depends(get_current_user)):
    return ai_service.generate_model_answer(question, language)


@placement_router.post("/interview-grade")
def grade_interview(data: InterviewGradeRequest, language: str = "en", _: User = Depends(get_current_user)):
    return ai_service.grade_interview_answers(data.questions, data.answers, language)


# ── Resources ─────────────────────────────────────────────────────────────────
resources_router = APIRouter(prefix="/api/resources", tags=["resources"])

BOOKS_DATA = {
    "12": {
        "Mathematics": ["NCERT Maths Part 1 & 2", "RD Sharma Class 12", "NCERT Exemplar Maths", "Arihant Skills in Mathematics"],
        "Physics": ["NCERT Physics Part 1 & 2", "HC Verma Concepts of Physics Vol 1 & 2", "DC Pandey", "Arihant Physics"],
        "Chemistry": ["NCERT Chemistry Part 1 & 2", "OP Tandon Physical Chemistry", "MS Chauhan Organic Chemistry", "VK Jaiswal Inorganic"],
        "Biology": ["NCERT Biology", "Trueman's Biology Vol 1 & 2", "Pradeep Biology", "MTG NCERT at your Fingertips"],
        "Computer Science": ["NCERT Computer Science", "Sumita Arora Python", "Preeti Arora"],
        "English": ["NCERT Flamingo & Vistas", "Wren & Martin Grammar"],
        "Accountancy": ["NCERT Accountancy Part 1 & 2", "DK Goel", "TS Grewal"],
        "Business Studies": ["NCERT Business Studies", "Poonam Gandhi"],
        "Economics": ["NCERT Economics", "TR Jain & VK Ohri"],
    },
    "11": {
        "Mathematics": ["NCERT Maths", "RD Sharma Class 11", "SL Loney Trigonometry", "Hall & Knight Higher Algebra"],
        "Physics": ["NCERT Physics Part 1 & 2", "HC Verma Vol 1", "DC Pandey", "IE Irodov (advanced)"],
        "Chemistry": ["NCERT Chemistry Part 1 & 2", "OP Tandon", "NCERT Exemplar Chemistry"],
        "Biology": ["NCERT Biology", "Trueman's Biology", "Pradeep Biology"],
        "Computer Science": ["NCERT Computer Science", "Sumita Arora C++/Python"],
    },
    "10": {
        "Mathematics": ["NCERT Maths", "RS Aggarwal", "RD Sharma Class 10", "Exam Idea Maths"],
        "Science": ["NCERT Science", "Lakhmir Singh Physics/Chemistry/Biology", "Exam Idea Science"],
        "Social Science": ["NCERT SST (all 4 books)", "Together with Social Science"],
        "English": ["NCERT First Flight & Footprints", "Wren & Martin"],
        "Hindi": ["NCERT Kshitij & Kritika"],
    },
    "9": {
        "Mathematics": ["NCERT Maths", "RD Sharma Class 9", "RS Aggarwal"],
        "Science": ["NCERT Science", "Lakhmir Singh"],
        "Social Science": ["NCERT SST (4 books)"],
        "English": ["NCERT Beehive & Moments"],
    },
}

@resources_router.get("/books")
def get_books(class_level: str = "12"):
    return {"class": class_level, "books": BOOKS_DATA.get(class_level, {})}

@resources_router.get("/books/all-classes")
def get_all_books():
    return BOOKS_DATA

@resources_router.post("/pyq")
async def get_pyq(subject: str, chapter: str = "", year: str = "recent",
                  language: str = "en", _: User = Depends(get_current_user)):
    import google.generativeai as genai
    from app.core.config import settings
    genai.configure(api_key=settings.GEMINI_API_KEY)
    lang = {"en": "English", "ta": "Tamil", "te": "Telugu",
            "hi": "Hindi", "ml": "Malayalam", "kn": "Kannada"}.get(language, "English")
    prompt = f"""List 10 important previous year CBSE board exam questions on:
Subject: {subject}
{"Chapter: " + chapter if chapter else ""}
Time period: {year} board exams

Respond in {lang}.
Format each question with:
- Year (approximate)
- Marks weightage
- The question
- Key points for answer (2-3 bullets)
Number them 1-10."""
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    config = genai.GenerationConfig(max_output_tokens=4000)
    response = model.generate_content(prompt, generation_config=config)
    return {"questions": response.text}


# ── Aptitude ──────────────────────────────────────────────────────────────────
aptitude_router = APIRouter(prefix="/api/aptitude", tags=["aptitude"])

APTITUDE_QUESTIONS = [
    {"id": 1, "question": "A train 150m long passes a pole in 15 seconds. What is the speed of the train in km/hr?",
     "options": ["30 km/h", "36 km/h", "42 km/h", "45 km/h"], "correct": 1,
     "topic": "Speed & Distance", "difficulty": "easy", "explanation": "Speed = Distance/Time = 150/15 = 10 m/s. Convert to km/h: 10 * (18/5) = 36 km/h."},
    {"id": 2, "question": "If 15 workers can complete a job in 48 days, how many workers are needed to complete it in 30 days?",
     "options": ["20", "22", "24", "26"], "correct": 2,
     "topic": "Time & Work", "difficulty": "medium", "explanation": "Workers × Days = total work constant. 15 × 48 = X × 30. X = 720 / 30 = 24 workers."},
    {"id": 3, "question": "What is 30% of 25% of 400?",
     "options": ["25", "30", "35", "40"], "correct": 1,
     "topic": "Percentages", "difficulty": "easy", "explanation": "25% of 400 = 100. 30% of 100 = 30."},
    {"id": 4, "question": "A man buys an article for ₹800 and sells it for ₹1000. What is his profit percentage?",
     "options": ["20%", "25%", "30%", "15%"], "correct": 1,
     "topic": "Profit & Loss", "difficulty": "easy", "explanation": "Profit = Selling Price - Cost Price = 1000 - 800 = ₹200. Profit% = (Profit/Cost Price) * 100 = (200/800) * 100 = 25%."},
    {"id": 5, "question": "Find the next number in the series: 2, 6, 12, 20, 30, ?",
     "options": ["40", "42", "44", "45"], "correct": 1,
     "topic": "Number Series", "difficulty": "medium", "explanation": "Differences between consecutive numbers: 6-2=4, 12-6=6, 20-12=8, 30-20=10. The difference increases by 2 each time. Next difference is 12. Next number = 30 + 12 = 42."},
    {"id": 6, "question": "If A:B = 3:4 and B:C = 5:6. Find the ratio A:B:C.",
     "options": ["15:20:24", "12:16:20", "9:12:16", "3:4:6"], "correct": 0,
     "topic": "Ratios & Proportions", "difficulty": "medium", "explanation": "To equate B, multiply A:B by 5 and B:C by 4. A:B = 15:20. B:C = 20:24. Hence, A:B:C = 15:20:24."},
    {"id": 7, "question": "Find the simple interest on ₹5000 at 8% per annum for 3 years.",
     "options": ["₹1000", "₹1200", "₹1500", "₹1800"], "correct": 1,
     "topic": "Simple Interest", "difficulty": "easy", "explanation": "Simple Interest = (Principal * Rate * Time)/100 = (5000 * 8 * 3)/100 = ₹1200."},
    {"id": 8, "question": "A can do a piece of work in 20 days and B in 30 days. How many days will they take if they work together?",
     "options": ["10 days", "12 days", "14 days", "15 days"], "correct": 1,
     "topic": "Time & Work", "difficulty": "easy", "explanation": "Together rate = 1/20 + 1/30 = (3+2)/60 = 5/60 = 1/12. So they take 12 days working together."},
    {"id": 9, "question": "A sum of money doubles itself in 5 years at compound interest. In how many years will it become 8 times itself?",
     "options": ["10 years", "15 years", "20 years", "25 years"], "correct": 1,
     "topic": "Compound Interest", "difficulty": "hard", "explanation": "Let initial principal be P. P becomes 2P in 5 years. 2P becomes 4P in another 5 years (total 10 years). 4P becomes 8P in another 5 years (total 15 years)."},
    {"id": 10, "question": "Two cards are drawn from a pack of 52 cards. What is the probability that both are kings?",
     "options": ["1/221", "2/221", "3/221", "4/221"], "correct": 0,
     "topic": "Probability", "difficulty": "hard", "explanation": "Number of kings in a pack = 4. Probability of 1st King = 4/52. Probability of 2nd King = 3/51. Probability of both Kings = (4/52) * (3/51) = (1/13) * (1/17) = 1/221."},
    {"id": 11, "question": "A man rows upstream 13 km and downstream 28 km, taking 5 hours each time. What is the velocity of the current?",
     "options": ["1.2 km/h", "1.5 km/h", "1.8 km/h", "2.0 km/h"], "correct": 1,
     "topic": "Speed & Distance", "difficulty": "medium", "explanation": "Upstream speed = 13/5 = 2.6 km/h. Downstream speed = 28/5 = 5.6 km/h. Speed of current = (Downstream speed - Upstream speed)/2 = (5.6 - 2.6)/2 = 1.5 km/h."},
    {"id": 12, "question": "A bag contains 6 black and 8 white balls. One ball is drawn at random. What is the probability that the ball drawn is black?",
     "options": ["3/7", "4/7", "1/2", "3/14"], "correct": 0,
     "topic": "Probability", "difficulty": "easy", "explanation": "Total balls = 6 + 8 = 14. Black balls = 6. Probability = 6/14 = 3/7."},
    {"id": 13, "question": "The average of 5 consecutive numbers is 20. What is the largest of these numbers?",
     "options": ["20", "21", "22", "24"], "correct": 2,
     "topic": "Averages", "difficulty": "easy", "explanation": "Let consecutive numbers be x-2, x-1, x, x+1, x+2. Average = x = 20. Largest number = x+2 = 20+2 = 22."},
    {"id": 14, "question": "A person crosses a 600m long street in 5 minutes. What is his speed in km per hour?",
     "options": ["3.6 km/h", "7.2 km/h", "8.4 km/h", "10 km/h"], "correct": 1,
     "topic": "Speed & Distance", "difficulty": "easy", "explanation": "Speed = Distance/Time = 600m / (5 * 60)s = 2 m/s. Convert to km/h: 2 * (18/5) = 7.2 km/h."},
    {"id": 15, "question": "If 6 men and 8 boys can do a piece of work in 10 days while 26 men and 48 boys can do the same in 2 days, what is the time taken by 15 men and 20 boys in doing the same work?",
     "options": ["4 days", "5 days", "6 days", "7 days"], "correct": 0,
     "topic": "Time & Work", "difficulty": "hard", "explanation": "Let 1 man's 1 day work = M and 1 boy's 1 day work = B. 10(6M + 8B) = 2(26M + 48B) => 60M + 80B = 52M + 96B => 8M = 16B => 1M = 2B. Total work = 10(6M + 8B) = 10(12B + 8B) = 200 boy-days. 15 men + 20 boys = 15(2B) + 20B = 50B. Days required = 200B / 50B = 4 days."},
    {"id": 16, "question": "What is the angle between the hour hand and the minute hand of a clock at 3:40?",
     "options": ["120 degrees", "130 degrees", "140 degrees", "145 degrees"], "correct": 1,
     "topic": "Clocks", "difficulty": "medium", "explanation": "Angle = |(30 * Hour) - (5.5 * Minute)| = |(30 * 3) - (5.5 * 40)| = |90 - 220| = 130 degrees."},
    {"id": 17, "question": "How many times do the hands of a clock coincide in a day?",
     "options": ["20", "21", "22", "24"], "correct": 2,
     "topic": "Clocks", "difficulty": "easy", "explanation": "The hands coincide once every 65 5/11 minutes. In a 24-hour day, they coincide exactly 22 times."},
    {"id": 18, "question": "A vendor bought toffees at 6 for a rupee. How many for a rupee must he sell to gain 20%?",
     "options": ["3", "4", "5", "6"], "correct": 2,
     "topic": "Profit & Loss", "difficulty": "medium", "explanation": "Cost Price of 6 toffees = Re 1 => CP of 1 toffee = 1/6. To gain 20%, Selling Price of 1 toffee = (1/6) * 1.20 = 1.2/6 = 1/5. Thus, he must sell 5 toffees for Re 1."},
    {"id": 19, "question": "A and B invest in a business in the ratio 3:2. If 5% of the total profit goes to charity and A's share is ₹855, what is the total profit?",
     "options": ["₹1425", "₹1500", "₹1575", "₹1600"], "correct": 1,
     "topic": "Partnership", "difficulty": "medium", "explanation": "Let total profit be P. Profit remaining after charity = 0.95P. A's share = 3/5 of remaining profit => (3/5) * 0.95P = 855 => 0.57P = 855 => P = 1500."},
    {"id": 20, "question": "In how many different ways can the letters of the word 'LEADING' be arranged in such a way that the vowels always come together?",
     "options": ["360", "480", "720", "1440"], "correct": 2,
     "topic": "Permutations", "difficulty": "hard", "explanation": "Word 'LEADING' has 7 letters. Vowels are E, A, I (3 vowels). Consonants are L, D, N, G (4 consonants). Treat 3 vowels as 1 unit. Total units to arrange = 4 + 1 = 5 units. 5 units can be arranged in 5! = 120 ways. The 3 vowels within their unit can be arranged in 3! = 6 ways. Total arrangements = 120 * 6 = 720 ways."}
]

CODING_QUESTIONS = [
    {"id": 1, "title": "Two Sum", "difficulty": "easy", "company": "TCS, Infosys, Amazon, Mr. Cooper",
     "gfg": "https://www.geeksforgeeks.org/given-an-array-a-and-a-number-x-check-for-pair-in-a-with-sum-as-x/",
     "lc": "https://leetcode.com/problems/two-sum/", "topic": "Arrays"},
    {"id": 2, "title": "Reverse a Linked List", "difficulty": "easy", "company": "Wipro, Cognizant, Microsoft",
     "gfg": "https://www.geeksforgeeks.org/reverse-a-linked-list/",
     "lc": "https://leetcode.com/problems/reverse-linked-list/", "topic": "Linked List"},
    {"id": 3, "title": "Valid Parentheses", "difficulty": "easy", "company": "Wipro, Accenture, Mr. Cooper",
     "gfg": "https://www.geeksforgeeks.org/check-for-balanced-parentheses-in-an-expression/",
     "lc": "https://leetcode.com/problems/valid-parentheses/", "topic": "Stack"},
    {"id": 4, "title": "Binary Search", "difficulty": "easy", "company": "TCS, Wipro, Accenture, Google",
     "gfg": "https://www.geeksforgeeks.org/binary-search/",
     "lc": "https://leetcode.com/problems/binary-search/", "topic": "Searching"},
    {"id": 5, "title": "Maximum Subarray (Kadane's Algorithm)", "difficulty": "medium", "company": "TCS, Cognizant, Amazon",
     "gfg": "https://www.geeksforgeeks.org/largest-sum-contiguous-subarray/",
     "lc": "https://leetcode.com/problems/maximum-subarray/", "topic": "Dynamic Programming"},
    {"id": 6, "title": "Longest Common Subsequence", "difficulty": "medium", "company": "Infosys, Wipro, Google",
     "gfg": "https://www.geeksforgeeks.org/longest-common-subsequence-dp-4/",
     "lc": "https://leetcode.com/problems/longest-common-subsequence/", "topic": "Dynamic Programming"},
    {"id": 7, "title": "Number of Islands (BFS/DFS)", "difficulty": "medium", "company": "Cognizant, Amazon, Microsoft",
     "gfg": "https://www.geeksforgeeks.org/find-number-of-islands/",
     "lc": "https://leetcode.com/problems/number-of-islands/", "topic": "Graphs"},
    {"id": 8, "title": "Merge K Sorted Lists", "difficulty": "hard", "company": "Google, Amazon, Microsoft",
     "gfg": "https://www.geeksforgeeks.org/merge-k-sorted-linked-lists/",
     "lc": "https://leetcode.com/problems/merge-k-sorted-lists/", "topic": "Linked List"},
    {"id": 9, "title": "Trapping Rain Water", "difficulty": "hard", "company": "Google, Amazon",
     "gfg": "https://www.geeksforgeeks.org/trapping-rain-water/",
     "lc": "https://leetcode.com/problems/trapping-rain-water/", "topic": "Arrays"},
    {"id": 10, "title": "LRU Cache", "difficulty": "hard", "company": "Amazon, Microsoft, Mr. Cooper",
     "gfg": "https://www.geeksforgeeks.org/lru-cache-implementation/",
     "lc": "https://leetcode.com/problems/lru-cache/", "topic": "Design"},
    {"id": 11, "title": "Valid Anagram", "difficulty": "easy", "company": "Infosys, Accenture, Amazon",
     "gfg": "https://www.geeksforgeeks.org/check-whether-two-strings-are-anagram-of-each-other/",
     "lc": "https://leetcode.com/problems/valid-anagram/", "topic": "Strings"},
    {"id": 12, "title": "Climbing Stairs", "difficulty": "easy", "company": "Infosys, Cognizant, Wipro",
     "gfg": "https://www.geeksforgeeks.org/count-ways-reach-nth-stair/",
     "lc": "https://leetcode.com/problems/climbing-stairs/", "topic": "Dynamic Programming"},
    {"id": 13, "title": "Search in Rotated Sorted Array", "difficulty": "medium", "company": "Infosys, Mr. Cooper, Uber",
     "gfg": "https://www.geeksforgeeks.org/search-an-element-in-a-sorted-and-pivoted-array/",
     "lc": "https://leetcode.com/problems/search-in-rotated-sorted-array/", "topic": "Searching"},
    {"id": 14, "title": "Longest Substring Without Repeating Characters", "difficulty": "medium", "company": "Mr. Cooper, Amazon, Microsoft",
     "gfg": "https://www.geeksforgeeks.org/length-of-the-longest-substring-without-repeating-characters/",
     "lc": "https://leetcode.com/problems/longest-substring-without-repeating-characters/", "topic": "Strings"},
    {"id": 15, "title": "Merge Sorted Array", "difficulty": "easy", "company": "TCS, Accenture, Adobe",
     "gfg": "https://www.geeksforgeeks.org/merge-two-sorted-arrays/",
     "lc": "https://leetcode.com/problems/merge-sorted-array/", "topic": "Arrays"},
    {"id": 16, "title": "LinkedList Cycle", "difficulty": "easy", "company": "TCS, Cognizant, Qualcomm",
     "gfg": "https://www.geeksforgeeks.org/detect-loop-in-a-linked-list/",
     "lc": "https://leetcode.com/problems/linked-list-cycle/", "topic": "Linked List"},
    {"id": 17, "title": "Invert Binary Tree", "difficulty": "easy", "company": "Wipro, Cognizant, Google",
     "gfg": "https://www.geeksforgeeks.org/write-an-efficient-c-function-to-convert-a-tree-into-its-mirror-tree/",
     "lc": "https://leetcode.com/problems/invert-binary-tree/", "topic": "Trees"},
    {"id": 18, "title": "Maximum Depth of Binary Tree", "difficulty": "easy", "company": "Cognizant, Microsoft, Facebook",
     "gfg": "https://www.geeksforgeeks.org/write-a-c-program-to-find-the-maximum-depth-or-height-of-a-tree/",
     "lc": "https://leetcode.com/problems/maximum-depth-of-binary-tree/", "topic": "Trees"},
    {"id": 19, "title": "Best Time to Buy and Sell Stock", "difficulty": "easy", "company": "Accenture, Goldman Sachs, Amazon",
     "gfg": "https://www.geeksforgeeks.org/best-time-to-buy-and-sell-stock/",
     "lc": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/", "topic": "Arrays"},
    {"id": 20, "title": "Merge Two Sorted Lists", "difficulty": "easy", "company": "Wipro, Microsoft, Yahoo",
     "gfg": "https://www.geeksforgeeks.org/merge-two-sorted-linked-lists/",
     "lc": "https://leetcode.com/problems/merge-two-sorted-lists/", "topic": "Linked List"}
]

@aptitude_router.get("/questions")
def get_aptitude(topic: str = "", difficulty: str = ""):
    qs = APTITUDE_QUESTIONS
    if topic:
        qs = [q for q in qs if topic.lower() in q["topic"].lower()]
    if difficulty:
        qs = [q for q in qs if q["difficulty"] == difficulty]
    return qs

@aptitude_router.get("/coding")
def get_coding(difficulty: str = "", topic: str = ""):
    qs = CODING_QUESTIONS
    if difficulty:
        qs = [q for q in qs if q["difficulty"] == difficulty]
    if topic:
        qs = [q for q in qs if topic.lower() in q["topic"].lower()]
    return qs
