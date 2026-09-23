import json, re
import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

LANG_NAMES = {
    "en": "English", "ta": "Tamil", "te": "Telugu",
    "hi": "Hindi", "ml": "Malayalam", "kn": "Kannada"
}

def _call(prompt: str, system: str = "", max_tokens: int = 4000) -> str:
    sys_msg = system or (
        "You are Scholr AI, an expert educational assistant for Indian students. "
        "Give clear, structured, practical responses."
    )
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=sys_msg
    )
    config = genai.GenerationConfig(
        max_output_tokens=max_tokens
    )
    try:
        response = model.generate_content(prompt, generation_config=config)
        if not response.candidates or not response.candidates[0].content.parts:
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                raise Exception(f"Request blocked by safety filters: {response.prompt_feedback.block_reason}")
            raise Exception("Response blocked or empty.")
        return response.text
    except Exception as e:
        print(f"Gemini API Error in _call: {e}")
        return "Sorry, I encountered an issue processing this request. Please try again."


def extract_balanced_json(text: str) -> str:
    start_idx = -1
    for i, char in enumerate(text):
        if char in ('{', '['):
            start_idx = i
            break
    if start_idx == -1:
        return text
    
    char_open = text[start_idx]
    char_close = '}' if char_open == '{' else ']'
    
    count = 0
    in_string = False
    escaped = False
    
    for i in range(start_idx, len(text)):
        char = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                in_string = False
        else:
            if char == '"':
                in_string = True
            elif char == char_open:
                count += 1
            elif char == char_close:
                count -= 1
                if count == 0:
                    return text[start_idx : i + 1]
    
    return text[start_idx:]


def _json_call(prompt: str, system: str = "") -> any:
    """Call AI and parse JSON response."""
    sys_msg = system or "You are an expert educator."
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=sys_msg
    )
    config = genai.GenerationConfig(
        response_mime_type="application/json",
        max_output_tokens=8192
    )
    try:
        response = model.generate_content(prompt, generation_config=config)
        if not response.candidates or not response.candidates[0].content.parts:
            raise Exception("Empty response or blocked by safety filters.")
        
        text = response.text.strip()
        clean = re.sub(r"```json|```", "", text).strip()
        
        # Try to parse directly
        try:
            return json.loads(clean)
        except Exception:
            # Fall back to extracting balanced JSON substring
            balanced = extract_balanced_json(clean)
            return json.loads(balanced)
    except Exception as e:
        print(f"Gemini API Error in _json_call: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            try:
                safe_text = response.text.encode('ascii', errors='backslashreplace').decode('ascii')
                print(f"Raw response text (escaped): {safe_text}")
            except Exception:
                pass
        return None


def _json_call_multimodal(contents: list, system: str = "") -> any:
    """Call AI with multimodal contents (text, images) and parse JSON response."""
    sys_msg = system or "You are an expert educator."
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=sys_msg
    )
    config = genai.GenerationConfig(
        response_mime_type="application/json",
        max_output_tokens=8192
    )
    try:
        response = model.generate_content(contents, generation_config=config)
        if not response.candidates or not response.candidates[0].content.parts:
            raise Exception("Empty response or blocked by safety filters.")
        
        text = response.text.strip()
        clean = re.sub(r"```json|```", "", text).strip()
        
        # Try to parse directly
        try:
            return json.loads(clean)
        except Exception:
            # Fall back to extracting balanced JSON substring
            balanced = extract_balanced_json(clean)
            return json.loads(balanced)
    except Exception as e:
        print(f"Gemini API Error in _json_call_multimodal: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            try:
                safe_text = response.text.encode('ascii', errors='backslashreplace').decode('ascii')
                print(f"Raw response text (escaped): {safe_text}")
            except Exception:
                pass
        return []


def parse_marksheet_with_ai(file_path: str, extension: str, extracted_text: str = "") -> list[dict]:
    """Parse subject-score pairs from marksheet image, PDF, or text using Gemini."""
    is_img = extension.lower() in (".png", ".jpg", ".jpeg")
    is_pdf = extension.lower() == ".pdf"
    
    prompt = """
Analyse this student marksheet and extract all subjects along with the marks/scores obtained by the student.
Return a JSON array of objects, where each object has:
- "name": the name of the subject (e.g. Mathematics, Physics, Chemistry, English, Computer Science, Biology, etc.)
- "score": the numerical score or marks obtained as a float or integer (out of 100. If the marks are out of a different total like 50, 70, 80, or 200, normalize the score to a 100-point scale so that it is out of 100).

Return ONLY a JSON array. Do not include any additional explanatory text.
Example structure:
[
  {"name": "Mathematics", "score": 85.5},
  {"name": "Physics", "score": 72.0}
]
"""
    subjects = []
    
    if is_img:
        try:
            from PIL import Image
            img = Image.open(file_path)
            # Call Gemini with the image and prompt
            subjects = _json_call_multimodal([prompt, img], "You are an expert OCR and marksheet analysis assistant.")
        except Exception as e:
            print(f"Error reading image for marksheet analysis: {e}")
            
    elif is_pdf:
        try:
            from pathlib import Path
            pdf_bytes = Path(file_path).read_bytes()
            pdf_data = {
                "mime_type": "application/pdf",
                "data": pdf_bytes
            }
            # Call Gemini with the PDF file and prompt directly
            subjects = _json_call_multimodal([prompt, pdf_data], "You are an expert OCR and marksheet analysis assistant.")
        except Exception as e:
            print(f"Error reading PDF for marksheet analysis: {e}")
    
    # If not an image/pdf, or if direct multimodal parsing returned nothing (e.g. rate limit / exception)
    if not subjects and extracted_text:
        text_prompt = f"""
{prompt}

Here is the extracted text from the marksheet:
\"\"\"
{extracted_text}
\"\"\"
"""
        subjects = _json_call(text_prompt, "You are an expert marksheet parser.")
        
    # If we still don't have subjects (e.g. both failed or are empty), use local regex parser
    if not subjects:
        try:
            from app.services import file_service
            subjects = file_service.parse_marksheet_text(extracted_text)
        except Exception as e:
            print(f"Error calling local parse_marksheet_text: {e}")
            
    return subjects


def get_study_plan_fallback(subjects: list[dict], style: str, hours: float, material_topics: list[dict] = None) -> dict:
    # Generate weekly study plan dynamically based on actual subjects!
    # Weak subjects (score < 70) get more time and priority
    weak = [s for s in subjects if s.get("score", 100) < 70]
    strong = [s for s in subjects if s.get("score", 0) >= 70]
    
    # default subjects if list is empty
    if not subjects:
        subjects = [{"name": "Mathematics", "score": 60}, {"name": "English", "score": 85}]
        weak = [subjects[0]]
        strong = [subjects[1]]
        
    cycle_subjects = []
    for s in subjects:
        weight = 2 if s.get("score", 100) < 70 else 1
        cycle_subjects.extend([s] * weight)
        
    if not cycle_subjects:
        cycle_subjects = [{"name": "Self Study", "score": 100}]
        
    weekly_plan = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    material_topics_list = []
    if material_topics:
        for item in material_topics:
            if isinstance(item, dict) and "topic" in item:
                t_name = item["topic"]
                subs = item.get("subtopics", [])
                if isinstance(subs, list) and subs:
                    for sub in subs:
                        material_topics_list.append((t_name, sub))
                else:
                    material_topics_list.append((t_name, ""))

    cycle_idx = 0
    # We distribute subjects across 4 weeks
    for w in ["week1", "week2", "week3", "week4"]:
        weekly_plan[w] = {}
        for day in days:
            day_schedule = []
            if day == "Sunday":
                day_schedule.append({
                    "time": "10:00 AM",
                    "subject": "Revision",
                    "topic": "Weekly Assessment & Flashcards",
                    "duration": "2.0h"
                })
            else:
                subj = cycle_subjects[cycle_idx % len(cycle_subjects)]
                cycle_idx += 1
                
                topic_str = f"Targeted Practice ({style} style)"
                if material_topics_list:
                    t_idx = cycle_idx % len(material_topics_list)
                    t_name, sub = material_topics_list[t_idx]
                    if sub:
                        topic_str = f"{t_name}: {sub} ({style} style)"
                    else:
                        topic_str = f"{t_name} ({style} style)"
                
                day_schedule.append({
                    "time": "09:00 AM",
                    "subject": subj["name"],
                    "topic": topic_str,
                    "duration": f"{hours}h"
                })
            weekly_plan[w][day] = day_schedule

    daily_targets = {}
    for s in subjects:
        if s["name"] in [w["name"] for w in weak]:
            daily_targets[s["name"]] = f"Solve 10 conceptual problems daily ({style} style)"
        else:
            daily_targets[s["name"]] = "Revise key formulas and summary cards weekly"
            
    tips = [
        "Study in 50-minute chunks with 10-minute active breaks (Pomodoro technique).",
        "Prioritize writing down derivations and solving weak topics first.",
        "Dedicate Sundays solely to active recall testing and revisions."
    ]
    
    resources = {}
    for s in subjects:
        resources[s["name"]] = [
            f"NCERT Class 12 {s['name']} Textbook",
            f"Recommended reference exercises for {s['name']}"
        ]

    return {
        "weekly_plan": weekly_plan,
        "daily_targets": daily_targets,
        "tips": tips,
        "resources": resources
    }



def get_marksheet_fallback(subjects: list[dict]) -> dict:
    weak = [s["name"] for s in subjects if s.get("score", 100) < 70]
    strong = [s["name"] for s in subjects if s.get("score", 0) >= 70]
    
    if not weak and subjects:
        sorted_subjs = sorted(subjects, key=lambda x: x.get("score", 100))
        weak = [s["name"] for s in sorted_subjs[:2]]
        strong = [s["name"] for s in sorted_subjs[2:]]
        
    analysis = "The student has demonstrated outstanding performance in strong subjects, but requires targeted practice and concept reinforcement in core analytical subjects."
    if weak:
        analysis = f"Based on the marksheet, the student is performing well in {', '.join(strong[:2])} but needs improvement in {', '.join(weak)}."
        
    priority_order = weak + strong
    
    improvement_tips = {}
    for w_subj in weak:
        improvement_tips[w_subj] = f"Focus on solving base concepts, NCERT exemplar questions, and practicing daily mock exercises."
    for s_subj in strong:
        improvement_tips[s_subj] = "Maintain current momentum and practice advanced-level question sheets."
        
    return {
        "weak_subjects": weak,
        "strong_subjects": strong,
        "analysis": analysis,
        "priority_order": priority_order,
        "improvement_tips": improvement_tips
    }


def get_flashcards_fallback(topic: str, count: int = 15) -> list[dict]:
    default_cards = [
        {"topic": topic, "question": f"What is the core definition of {topic}?", "answer": f"{topic} is a fundamental concept in this field of study, representing key theoretical frameworks.", "difficulty": "easy", "hint": "Think about core definitions"},
        {"topic": topic, "question": f"Can you explain the primary application of {topic}?", "answer": f"{topic} is widely applied to solve practical exercises, analyze systems, and build conceptual models.", "difficulty": "medium", "hint": "Think of real-world use cases"},
        {"topic": topic, "question": f"What is a common mistake when studying {topic}?", "answer": "Students often skip foundational formulas or definitions, leading to errors in complex derivations.", "difficulty": "easy", "hint": "Common oversight in derivations"},
        {"topic": topic, "question": f"Name one advanced topic related to {topic}.", "answer": f"Advanced modules build directly on {topic} to solve multi-variable and higher-order problems.", "difficulty": "hard", "hint": "Higher levels of complexity"},
        {"topic": topic, "question": f"How do we verify results in {topic}?", "answer": "By cross-checking boundary conditions, dimension analysis, or back-substituting values.", "difficulty": "medium", "hint": "Verification techniques"}
    ]
    cards = []
    for i in range(count):
        cards.append(default_cards[i % len(default_cards)])
    return cards


def get_qa_fallback(topic: str, count: int = 10) -> list[dict]:
    default_qa = [
        {
            "question": f"Which of the following is true about {topic}?",
            "options": ["A. It is constant", "B. It is variable", "C. It is both constant and variable", "D. None of the above"],
            "correct_index": 2,
            "explanation": f"{topic} exhibits properties that can be both constant under static conditions and variable under dynamic systems.",
            "topic": topic,
            "difficulty": "medium"
        },
        {
            "question": f"What is the first step in analyzing {topic}?",
            "options": ["A. Assume values", "B. Identify core parameters", "C. Graph the function", "D. None of the above"],
            "correct_index": 1,
            "explanation": "Identifying core parameters is the critical first step before applying any formulas or drawing representations.",
            "topic": topic,
            "difficulty": "easy"
        },
        {
            "question": f"Which rule governs the conservation of resources in {topic}?",
            "options": ["A. First Law", "B. Second Law", "C. Third Law", "D. All of the above"],
            "correct_index": 3,
            "explanation": "Resource conservation rules govern all phases of physical and theoretical systems under standard laws.",
            "topic": topic,
            "difficulty": "hard"
        }
    ]
    qa = []
    for i in range(count):
        qa.append(default_qa[i % len(default_qa)])
    return qa


def get_speaking_fallback(transcript: str, topic: str) -> dict:
    transcript_lower = transcript.lower()
    fillers = {"basically": 0, "like": 0, "um": 0, "uh": 0}
    for f in fillers.keys():
        fillers[f] = transcript_lower.count(f)
    filler_count = sum(fillers.values())
    
    return {
        "overall_score": 7.5,
        "grammar_errors": [
            {"error": "we everyday use it", "correction": "we use it everyday", "sentence": "basically we everyday use it"}
        ] if "everyday" in transcript_lower or "use" in transcript_lower else [],
        "filler_words": fillers,
        "filler_count": filler_count,
        "pronunciation_tips": [
            "Focus on clear pacing. Try to pause for breathing between complete clauses.",
            "Ensure proper stress on syllables in multi-syllabic terms."
        ],
        "vocabulary_suggestions": [
            {"word_used": "everyday", "better_word": "on a daily basis", "context": "we use it on a daily basis"},
            {"word_used": "important", "better_word": "essential", "context": "this is essential for"}
        ],
        "content_score": 8.0,
        "delivery_score": 7.0,
        "key_points_covered": [f"Basic description of {topic}.", "Why it is useful in daily life."],
        "missing_points": ["Specific real-world examples or analytical applications."],
        "top_improvements": [
            "Reduce the use of transition fillers like 'basically' or 'like'.",
            "Incorporate distinct pauses to structure your thoughts.",
            "Provide concrete examples to support your points."
        ],
        "positive_feedback": "You spoke with good confidence, and the core message of your transcript was clear and easy to follow."
    }


def get_writing_fallback(text: str, mode: str) -> dict:
    text_lower = text.lower()
    return {
        "overall_score": 7.0,
        "grammar_errors": [
            {"error": "Calculus are", "correction": "Calculus is", "line": "Calculus are a branch of maths"}
        ] if "calculus are" in text_lower or "are a branch" in text_lower else [],
        "spelling_mistakes": [{"wrong": "maths", "correct": "mathematics"}] if "maths" in text_lower else [],
        "vocabulary_improvements": [
            {"original": "useful", "suggestion": "indispensable", "reason": "more academic tone"}
        ],
        "readability_score": 8.0,
        "tone": "formal",
        "structure_feedback": f"The introductory sentence of this {mode} is clear but could be expanded with a brief overview of key arguments.",
        "corrected_version": text.replace("Calculus are", "Calculus is").replace("maths", "mathematics"),
        "strengths": ["Direct and clear writing style.", "Active voice usage."],
        "improvements": ["Ensure subject-verb agreement.", "Vocabulary expansion for professional context."]
    }


def get_resume_fallback(resume_text: str) -> dict:
    resume_lower = resume_text.lower()
    all_keys = ["python", "sql", "git", "docker", "aws", "gcp", "azure", "java", "javascript", "react", "fastapi"]
    found = [k.title() for k in all_keys if k in resume_lower]
    missing = [k.title() for k in all_keys if k not in resume_lower]
    
    return {
        "ats_score": 70 + len(found) * 2,
        "strengths": [
            f"Lists relevant technical skills: {', '.join(found[:4])}." if found else "Structured skills section.",
            "Clear layout with readable sections."
        ],
        "weaknesses": [
            "Lack of quantifiable metrics (e.g. percentages, outcomes) showing impact.",
            "Missing crucial developer keywords (like Git, Docker, cloud systems)."
        ],
        "missing_keywords": missing[:6],
        "format_issues": [
            "The header lacks a modern professional summary.",
            "Experience bullets should begin with strong action verbs."
        ],
        "suggestions": [
            {"section": "Experience", "suggestion": "Quantify outcomes: instead of 'worked on features', write 'designed REST endpoints reducing latency by 20%'."},
            {"section": "Skills", "suggestion": f"Add essential tools such as {', '.join(missing[:3])}." if missing else "Group skills into categories."},
            {"section": "Projects", "suggestion": "Add 2-3 technical projects outlining the problem solved and technologies used."}
        ],
        "overall_summary": "The resume has a solid baseline but needs enhancements to pass competitive ATS screenings. Adding version control, deployment tools, and quantifying achievements will significantly boost the score."
    }


INTERVIEW_TECHNICAL_POOL = [{'question': 'What is your understanding of the Software Development Life Cycle (SDLC), and which methodology do you prefer at {company}?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['SDLC is a structured process for software development consisting of planning, analysis, design, implementation, testing, and maintenance.', 'Agile Scrum is widely preferred for rapid iterations and regular feedback loops.'], 'sample_answer': "The SDLC is a structured process used to build high-quality software. It involves key phases: planning, analysis, design, coding, testing, and maintenance. I prefer Agile Scrum because it allows continuous collaboration and quick feedback loops, aligning with {company}'s focus on quality delivery.", 'what_not_to_say': ['Saying that testing is not a part of SDLC.', 'Failing to explain the difference between waterfall and agile models.'], 'follow_up_questions': ['What is the difference between waterfall and agile models?', 'How do you manage requirements change in agile?']}}, {'question': 'Can you explain the four pillars of Object-Oriented Programming (OOP) and give real-world examples?', 'type': 'Technical', 'difficulty': 'easy', 'model_answer': {'key_points': ['Abstraction (hiding complexity), Encapsulation (binding data and methods), Inheritance (reusing code), Polymorphism (multiple forms).'], 'sample_answer': 'OOP is based on four pillars. Encapsulation wraps data inside classes. Inheritance allows a subclass to inherit properties. Polymorphism lets methods behave differently based on the object. Abstraction hides internal implementation details.', 'what_not_to_say': ['Confusing compile-time polymorphism with runtime polymorphism.'], 'follow_up_questions': ['What is the difference between overloading and overriding?', 'Can we prevent inheritance in Java?']}}, {'question': 'What is a deadlock in Operating Systems, and how can it be prevented or resolved?', 'type': 'Technical', 'difficulty': 'hard', 'model_answer': {'key_points': ['Deadlock occurs when processes hold resources while waiting for others. Conditions: Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait.'], 'sample_answer': 'A deadlock happens when two or more processes are unable to proceed because each is waiting for the other to release resources. We can prevent it by breaking one of the four Coffman conditions, or resolve it using detection and termination.', 'what_not_to_say': ['Saying that deadlocks only happen in single-threaded systems.'], 'follow_up_questions': ["What is Banker's algorithm?", 'Difference between deadlock and starvation.']}}, {'question': 'Why is database normalization important, and can you explain the difference between 1NF, 2NF, and 3NF?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Normalization reduces data redundancy and improves data integrity. 1NF (atomic values), 2NF (no partial dependency), 3NF (no transitive dependency).'], 'sample_answer': 'Normalization organizes database columns to prevent anomalies. 1NF ensures all values are atomic. 2NF removes partial dependency on composite keys. 3NF removes transitive dependencies where non-prime attributes depend on other non-prime attributes.', 'what_not_to_say': ['Failing to explain when denormalization is preferred (performance).'], 'follow_up_questions': ['What is BCNF?', 'When should we denormalize a database?']}}, {'question': 'What is the difference between TCP and UDP protocols, and when would you choose one over the other?', 'type': 'Technical', 'difficulty': 'easy', 'model_answer': {'key_points': ['TCP is connection-oriented, reliable, slower. UDP is connectionless, faster, unreliable.'], 'sample_answer': 'TCP guarantees packet delivery via a three-way handshake, making it ideal for web browsing and databases. UDP sends packets without confirming receipt, making it faster and preferred for video streaming or gaming where minor packet loss is acceptable.', 'what_not_to_say': ['Saying UDP is always better because it is faster.'], 'follow_up_questions': ['How does TCP handle congestion control?', 'What is three-way handshake?']}}, {'question': 'Can you describe your final year project, the technologies used, and your role in it?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Explain project goal and scope. List tech stack (e.g. React, Node, Python). Outline your individual contribution and team dynamics.'], 'sample_answer': 'My final year project was an AI study planner. I designed the backend REST APIs using FastAPI and integrated database tables. It solved study scheduling challenges by creating customizable daily study targets for students.', 'what_not_to_say': ['Failing to explain what technologies were used.', 'Giving too generic a description without details of your own work.'], 'follow_up_questions': ['What was the most challenging bug you faced?', 'How did you design the database schema?']}}, {'question': 'What is the key difference between Agile and Waterfall models, and when is Waterfall preferred?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Waterfall is sequential, rigid, document-driven. Agile is iterative, flexible, collaborative. Waterfall is preferred when requirements are clear and fixed.'], 'sample_answer': 'Waterfall flows sequentially from requirements to deployment. Agile splits development into short sprints. Waterfall is preferred for projects with well-defined, static requirements where changes are unlikely.', 'what_not_to_say': ['Saying Waterfall is obsolete and never used.'], 'follow_up_questions': ['What is a sprint planning meeting?', 'Explain Scrum roles.']}}, {'question': 'What is cloud computing? Can you explain the difference between IaaS, PaaS, and SaaS?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Cloud computing offers on-demand IT resources. IaaS (infrastructure), PaaS (platform for coding), SaaS (ready software).'], 'sample_answer': 'Cloud computing delivers computing services over the internet. IaaS provides basic VM servers and storage. PaaS provides a pre-configured platform for coding and deployment. SaaS provides fully managed user applications.', 'what_not_to_say': ['Confusing host configurations with platform services.'], 'follow_up_questions': ['Name some services on AWS/Azure.', 'What is serverless computing?']}}, {'question': 'What are the different types of software testing? Explain Unit, Integration, and System testing.', 'type': 'Technical', 'difficulty': 'easy', 'model_answer': {'key_points': ['Unit testing (individual units), Integration testing (combined units), System testing (entire system).'], 'sample_answer': 'Software testing includes functional and non-functional tests. Unit testing validates individual methods or components. Integration testing ensures components interact correctly. System testing evaluates the complete integrated application.', 'what_not_to_say': ['Confusing manual testing with automated testing definitions.'], 'follow_up_questions': ['What is regression testing?', 'Difference between black-box and white-box testing.']}}, {'question': 'What is the difference between DELETE, TRUNCATE, and DROP commands in SQL?', 'type': 'Technical', 'difficulty': 'easy', 'model_answer': {'key_points': ['DELETE (DML, selective, slower, logged), TRUNCATE (DDL, removes all rows, faster), DROP (DDL, removes table structure).'], 'sample_answer': 'DELETE is a DML command that removes rows based on a WHERE clause and can be rolled back. TRUNCATE is a DDL command that removes all rows and releases storage space. DROP deletes the entire table structure from the database.', 'what_not_to_say': ['Saying TRUNCATE cannot be rolled back (it can under active transactions in some databases).'], 'follow_up_questions': ['What is DDL vs DML?', 'Explain database transaction ACID properties.']}}, {'question': 'What is the difference between fixed and variable interest rates on loans?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Fixed rate (remains constant throughout term), Variable rate (fluctuates with market indices).'], 'sample_answer': 'A fixed interest rate stays the same for the entire loan tenure, offering predictable payments. A variable rate changes based on market indices, which can lower or raise monthly payments over time.', 'what_not_to_say': ['Saying fixed rate is always cheaper than variable rate.'], 'follow_up_questions': ['What is LTV?', 'Explain mortgage amortization.']}}, {'question': 'What are microservices? How do they compare to a monolithic architecture?', 'type': 'Technical', 'difficulty': 'hard', 'model_answer': {'key_points': ['Monolithic (single database and codebase), Microservices (decoupled, independent databases, API communication).'], 'sample_answer': 'A monolithic app has all features compiled as a single unit. Microservices split features into autonomous services that communicate via APIs. Microservices offer better scalability and fault isolation but introduce deployment complexity.', 'what_not_to_say': ['Saying microservices should always be used (monolith is better for simple apps).'], 'follow_up_questions': ['What is API Gateway?', 'How do microservices communicate?']}}, {'question': 'What are the core design principles of a RESTful API?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Statelessness, Client-Server architecture, Cacheability, Uniform Interface, Layered System.'], 'sample_answer': 'RESTful APIs are stateless, meaning every request must contain all context needed to process it. They use standard HTTP methods (GET, POST, PUT, DELETE) and return standard status codes (e.g. 200 OK, 404 Not Found) for resources.', 'what_not_to_say': ['Confusing PUT with POST definitions.'], 'follow_up_questions': ['Difference between PUT and PATCH.', 'What is idempotency?']}}, {'question': 'How does Garbage Collection work in programming languages like Java or Python?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Garbage collection manages memory by freeing unreachable objects. Java (generational heap, mark-and-sweep), Python (reference counting).'], 'sample_answer': 'Garbage collection automatically deallocates memory occupied by objects that are no longer referenced. Java uses generational sweep processes to find and clear dead objects. Python primarily uses reference counting along with cyclic garbage detectors.', 'what_not_to_say': ["Saying GC prevents all memory leaks (it doesn't prevent leak of referenced but unused memory)."], 'follow_up_questions': ['What is a memory leak?', 'Can we force garbage collection manually?']}}, {'question': 'Why is Big O notation important, and what are the time complexities of Binary Search and QuickSort?', 'type': 'Technical', 'difficulty': 'easy', 'model_answer': {'key_points': ['Big O measures worst-case run time relative to input size. Binary Search (O(log n)), QuickSort (O(n log n) average, O(n^2) worst case).'], 'sample_answer': 'Big O notation measures the scalability and efficiency of an algorithm. Binary Search splits search space in half, resulting in O(log n) complexity. QuickSort averages O(n log n) but can degrade to O(n^2) if pivot choices are poor.', 'what_not_to_say': ['Confusing average-case with worst-case complexities.'], 'follow_up_questions': ['What is space complexity?', 'Time complexity of MergeSort worst case?']}}, {'question': 'What is the difference between a process and a thread? What is multi-threading?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Process (independent execution unit with memory), Thread (lightweight subset sharing process memory).'], 'sample_answer': 'A process is a program in execution with its own isolated memory space. A thread is a path of execution within a process that shares memory with other threads. Multi-threading allows concurrent execution of tasks within a single program.', 'what_not_to_say': ['Saying threads are completely isolated from each other.'], 'follow_up_questions': ['What is a race condition?', 'How to achieve synchronization?']}}, {'question': 'What is the difference between symmetric and asymmetric encryption? Give examples of both.', 'type': 'Technical', 'difficulty': 'hard', 'model_answer': {'key_points': ['Symmetric (same key for encryption/decryption, faster), Asymmetric (public key to encrypt, private key to decrypt, slower).'], 'sample_answer': 'Symmetric encryption uses a single shared secret key, such as AES, making it fast and suitable for bulk data. Asymmetric encryption uses a key pair (public and private), such as RSA, which is secure for key exchange and digital signatures.', 'what_not_to_say': ['Confusing hashing with encryption (hashing is one-way).'], 'follow_up_questions': ['What is a hash function?', 'How does HTTPS work?']}}, {'question': 'What is the difference between SQL and NoSQL databases, and when would you choose which?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['SQL is relational (tables), NoSQL is non-relational (documents/keys).', 'SQL scales vertically, NoSQL scales horizontally.', 'SQL uses structured query language, NoSQL schemas are dynamic.'], 'sample_answer': 'SQL databases are relational, table-based, and scale vertically, making them ideal for structured data with complex query needs. NoSQL databases are non-relational, document or key-value based, and scale horizontally, making them suitable for unstructured data and rapid development.', 'what_not_to_say': ['Saying SQL is always better or NoSQL is always better without context.'], 'follow_up_questions': ['What is transaction ACID compliance?', 'When would you choose MongoDB over MySQL?']}}, {'question': 'Can you explain the concept of Virtual Memory and Paging in Operating Systems?', 'type': 'Technical', 'difficulty': 'hard', 'model_answer': {'key_points': ['Virtual memory extends physical RAM using hard disk space.', 'Paging splits memory into fixed-size logical pages.', 'Page tables map logical addresses to physical RAM page frames.'], 'sample_answer': 'Virtual Memory is a memory management technique that makes a system appear to have more physical memory than it actually does by using disk space as an extension. Paging divides memory into fixed-size pages, mapping logical addresses to physical page frames to prevent external fragmentation.', 'what_not_to_say': ['Confusing virtual memory with cache memory.', 'Failing to explain page faults.'], 'follow_up_questions': ['What is a page fault and how is it handled?', 'Explain Thrashing in operating systems.']}}, {'question': 'What is a MVC (Model-View-Controller) architecture, and how is it used in web development?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Model handles database data and business rules.', 'View renders output to the user interface.', 'Controller processes user inputs and updates Model/View.'], 'sample_answer': 'MVC is a design pattern that separates an application into three components: Model (data structure), View (user interface), and Controller (business logic). This separation of concerns improves codebase maintainability and makes parallel development easier.', 'what_not_to_say': ['Saying MVC is only used in frontend frameworks.', 'Mixing business logic directly into the View component.'], 'follow_up_questions': ['What is the difference between MVC and MVVM?', 'How does request routing relate to the Controller?']}}, {'question': 'What is the purpose of indexes in a database, and how do they speed up query execution?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Indexes speed up SELECT queries by creating lookup indices.', 'They are usually stored as B-Trees or B+ Trees.', 'Indexes slow down INSERT/UPDATE/DELETE writes due to index updates.'], 'sample_answer': 'A database index is a data structure, typically a B-Tree or Hash index, that improves the speed of data retrieval operations on a table at the cost of additional write speed and storage space. It avoids full table scans during lookup queries.', 'what_not_to_say': ['Indexing every single column in a table.', 'Failing to explain the overhead of indexing.'], 'follow_up_questions': ['Difference between clustered and non-clustered index?', 'What is a composite index?']}}, {'question': 'Explain the concept of recursion and state its advantages and disadvantages.', 'type': 'Technical', 'difficulty': 'easy', 'model_answer': {'key_points': ['Recursion occurs when a function calls itself directly or indirectly.', 'It requires a base case to terminate execution.', 'It has call stack space overhead of O(n) compared to O(1) iterative loops.'], 'sample_answer': 'Recursion is a programming technique where a function calls itself to solve smaller subproblems. The main advantage is cleaner, simpler code for problems like tree traversals. The main disadvantage is high memory usage due to call stack frames, potentially leading to stack overflow.', 'what_not_to_say': ['Saying recursion is always faster than iteration.', 'Forgetting the base case (results in infinite loops).'], 'follow_up_questions': ['What is Tail Recursion?', 'How does call stack manage recursive functions?']}}, {'question': 'What are design patterns? Can you explain the Singleton and Factory design patterns?', 'type': 'Technical', 'difficulty': 'medium', 'model_answer': {'key_points': ['Singleton ensures exactly one instance exists (e.g. database pool).', 'Factory pattern decouples object creation logic from client code.', 'Creational patterns help manage object instantiation lifecycle.'], 'sample_answer': 'Singleton restricts class instantiation to a single instance and provides global access to it. Factory pattern defines an interface for creating objects but lets subclasses decide which class to instantiate, promoting loose coupling.', 'what_not_to_say': ['Saying Singleton is always thread-safe without explicit locking.', 'Confusing Factory Method with Abstract Factory pattern.'], 'follow_up_questions': ['How do you make a Singleton thread-safe in Java/Python?', 'What are the drawbacks of Singleton pattern?']}}, {'question': 'How does the Git version control system work? Explain the difference between git merge and git rebase.', 'type': 'Technical', 'difficulty': 'easy', 'model_answer': {'key_points': ['Merge keeps original commit logs and creates a merge commit.', 'Rebase rewrites commit history by applying commits on top of the target branch.', 'Rebase should never be used on public/shared branches.'], 'sample_answer': 'Git merge combines changes from different branches by creating a new merge commit, preserving the historical sequence of commits. Git rebase moves the base of a branch to a new starting point, flattening the commit history for a cleaner timeline.', 'what_not_to_say': ['Saying rebase is always better because it leaves no merge commits.', 'Not knowing that rebase alters commit hashes.'], 'follow_up_questions': ['What is a fast-forward merge?', 'How do you resolve merge conflicts?']}}, {'question': 'What is Cross-Site Scripting (XSS) in web security, and how can it be prevented?', 'type': 'Technical', 'difficulty': 'hard', 'model_answer': {'key_points': ["XSS injects scripts that execute in the user's browser context.", 'Types include Stored, Reflected, and DOM-based XSS.', 'Prevention requires input validation, output encoding, and CSP headers.'], 'sample_answer': 'XSS is a security vulnerability where an attacker injects malicious scripts into trusted websites viewed by other users. We prevent it by sanitizing and escaping all user inputs, implementing Content Security Policy (CSP) headers, and using modern framework features that automatically escape HTML content.', 'what_not_to_say': ['Saying HTTPS prevents XSS (HTTPS only secures transport).', 'Relying purely on client-side validation.'], 'follow_up_questions': ['What is the difference between XSS and CSRF?', 'Explain what Content Security Policy (CSP) does.']}}]
INTERVIEW_HR_POOL = [{'question': 'Tell me about yourself. What motivated you to pursue a career in technology?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Introduce background and qualifications. Highlight passion for problem-solving and programming. Connect skills to company goals.'], 'sample_answer': 'I am a passionate software engineering student specializing in building responsive web applications. Solving complex logical challenges drew me to technology. I want to bring my programming skills to {company} to build scalable solutions.', 'what_not_to_say': ['Reciting the entire resume line-by-line.', 'Speaking too much about personal hobbies instead of professional highlights.'], 'follow_up_questions': ['What is your biggest achievement in college?', 'Why did you choose this stream?']}}, {'question': 'What are your greatest strengths and weaknesses? How do you work on improving your weaknesses?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Strength: problem-solving, team player, fast learner. Weakness: public speaking, over-analysing. Show self-awareness and how you are fixing it.'], 'sample_answer': 'My greatest strength is my capability to learn new tech stacks quickly. My weakness is public speaking. To improve this, I actively participate in college presentations and practice speech sessions.', 'what_not_to_say': ["Giving a cliché weakness like 'I am a perfectionist' or 'I work too hard'.", 'Mentioning a weakness that is a critical job requirement.'], 'follow_up_questions': ['Give an example of when you demonstrated this strength.', 'How does your weakness affect your team?']}}, {'question': 'Why do you want to join {company}? What do you know about our work culture?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ["Highlight company reputation, client base, and technical achievements. Connect personal growth to the company's innovation goals."], 'sample_answer': 'I want to join {company} because of your focus on innovation and strong learning culture. Working here will give me exposure to large-scale projects and help me learn industry best practices.', 'what_not_to_say': ["Saying 'I need a job' or focusing solely on salary and perks.", 'Showing no knowledge of what the company actually does.'], 'follow_up_questions': ['What other companies are you interviewing with?', 'Where do you see yourself in 5 years?']}}, {'question': 'Are you comfortable relocating, and what are your salary expectations?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Confirm relocation flexibility. Keep salary expectation open and industry-standard.'], 'sample_answer': 'I am fully comfortable relocating to any of your office hubs. Regarding salary, I am open to standard entry-level packages offered by the company for this role.', 'what_not_to_say': ['Demanding rigid numbers without negotiation room.', 'Stating that you cannot relocate if the job description requires it.'], 'follow_up_questions': ['Which city is your preferred location?', 'How soon can you join if selected?']}}, {'question': 'Tell me about a time you had a conflict with a team member. How did you resolve it?', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Explain the conflict context calmly. Emphasize active listening, objective discussion, and finding a win-win compromise.'], 'sample_answer': 'During a hackathon, a teammate and I disagreed on the database choice. Instead of arguing, we listed the pros and cons of SQL vs NoSQL for our app. We decided on SQL which fit our relational data best.', 'what_not_to_say': ['Blaming the other person or showing anger.', 'Saying you never have conflicts (unrealistic).'], 'follow_up_questions': ['How do you handle pressure?', 'What makes a good team leader?']}}, {'question': 'How do you handle a situation where a client changes software requirements at the last minute?', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Evaluate impact on timeline and resources. Discuss with team and project manager. Communicate transparently with client on compromises.'], 'sample_answer': 'I would stay calm and analyze the requested change. I would discuss the technical feasibility and impact on the timeline with my team. We would then communicate the trade-offs clearly to the client to align on delivery.', 'what_not_to_say': ['Refusing to adapt or complaining about the client.', 'Agreeing to last-minute changes without evaluating the impact first.'], 'follow_up_questions': ['How do you handle deadlines?', 'Describe your project management style.']}}, {'question': 'Where do you see yourself in 5 years? What are your career aspirations?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ["Show long-term commitment. Aspire to technical growth (Senior Developer / Tech Lead) and mentorship. Align with the company's growth."], 'sample_answer': 'In 5 years, I see myself as a Senior Software Engineer leading development modules. I want to build deep technical expertise in cloud technologies and guide junior team members to deliver high-quality solutions.', 'what_not_to_say': ["Saying 'I want to be the CEO' (unrealistic) or 'I want to leave this company'."], 'follow_up_questions': ['What skills do you need to reach this goal?', 'How does this role help you?']}}, {'question': 'Describe a difficult technical challenge you faced and how you overcame it.', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Explain technical challenge clearly. Outline the structured debugging process. Share what you learned from resolving it.'], 'sample_answer': 'In a web app project, we faced a database deadlock under load. I monitored queries and found that concurrent transactions updated rows in different orders. By sorting updates, we eliminated the deadlock completely.', 'what_not_to_say': ['Saying you solved it by random trials.', 'Not mentioning the specific steps taken to debug and analyze.'], 'follow_up_questions': ['What tools did you use to debug?', 'How did you verify the fix?']}}, {'question': 'How do you handle work pressure or tight deadlines? Give a real-world example from your college life.', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Prioritize tasks objectively.', 'Maintain open communication about delays.', 'Focus on time-management and structured scheduling.'], 'sample_answer': 'When facing tight deadlines, I prioritize tasks using a matrix, break them down into smaller action items, and maintain transparent communication with my team. For example, during my college project submission week, I worked in scheduled blocks and successfully met all deadlines.', 'what_not_to_say': ['Saying you never feel pressure.', 'Admitting you miss deadlines regularly without communicating.'], 'follow_up_questions': ['How do you handle unexpected delays?', 'Give an example of a time you worked under pressure.']}}, {'question': 'Why should we hire you over other candidates? What unique value do you bring?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Connect technical skills to the job requirements.', 'Highlight soft skills (fast learner, team player).', "Show enthusiasm for the company's business model."], 'sample_answer': "You should hire me because I have a strong foundation in core software engineering, hands-on experience building practical projects, and a quick learning curve. I am highly motivated to align my programming skills with your team's goals to deliver quality results.", 'what_not_to_say': ["Giving a generic answer like 'I need a job' or 'I am the best'.", 'Failing to connect your skills to the specific job profile.'], 'follow_up_questions': ['What unique skill do you bring?', 'Why do you think you fit this role?']}}, {'question': 'Tell me about a time you failed. What did you learn from that experience?', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Choose a genuine, work-related setback, not a personal one.', 'Take responsibility for the failure.', 'Focus on the learning outcome and subsequent improvement.'], 'sample_answer': 'In a college web project, I spent too long trying to implement a complex feature myself instead of asking for help, which delayed our progress. I learned the importance of collaboration, timely escalation, and dividing tasks efficiently. We finished the project successfully by teaming up to complete the delayed parts.', 'what_not_to_say': ['Saying you have never failed in your life.', 'Blaming others for your failure.'], 'follow_up_questions': ['How did your team react?', 'What changes did you implement in your next project?']}}, {'question': 'How do you keep yourself updated with the latest technologies and industry trends?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Mention concrete resources (blogs, podcasts, GitHub, newsletters).', 'Talk about hands-on experimentation.', 'Show natural curiosity and a learning mindset.'], 'sample_answer': 'I keep myself updated by reading tech blogs like Medium and Dev.to, subscribing to developer newsletters, and building small personal projects to experiment with new frameworks. I also participate in local developer forums and hackathons.', 'what_not_to_say': ['Saying you only learn what is taught in college classes.', 'Stating that you do not follow tech news because it changes too fast.'], 'follow_up_questions': ['What is the most interesting tech trend you followed recently?', 'Have you built any project with a new technology?']}}, {'question': "If you are given a task you don't know how to do, what steps would you take to complete it?", 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Demonstrate self-reliance and research habits.', 'Show understanding of when to ask for help (avoiding stuck loops).', 'Approach the challenge with structured learning.'], 'sample_answer': 'If given an unfamiliar task, I start by doing quick research on the concepts, reading documentation, and looking for standard examples. If I am still stuck after trying, I construct specific questions and seek guidance from my mentor or team members to avoid wasting time.', 'what_not_to_say': ['Giving up immediately or asking for help before doing any research.', 'Pretending you know how to do it and delivering poor work.'], 'follow_up_questions': ['How long do you try before asking for help?', 'Describe a time you had to learn something new quickly.']}}, {'question': 'How do you prioritize your tasks when you have multiple assignments or projects due at the same time?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Use tools like calendars, lists, or Kanban boards.', 'Evaluate urgency vs importance.', 'Communicate early if deadlines might conflict.'], 'sample_answer': 'I prioritize tasks based on their urgency and impact on the project timeline. I use todo lists to track tasks, allocate specific time blocks for deep work, and communicate with stakeholders if conflicting priorities arise to align on expectations.', 'what_not_to_say': ['Saying you work on whatever you feel like doing first.', 'Failing to check deadlines or milestones.'], 'follow_up_questions': ['How do you handle tasks with the same deadline?', 'How do you manage distraction?']}}, {'question': 'Describe a situation where you had to work with someone whose personality was very different from yours.', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Emphasize adaptability and emotional intelligence.', 'Focus on objective communication and empathy.', 'Keep discussions professional and task-focused.'], 'sample_answer': 'I focus on professional respect, active listening, and open communication. I understand that everyone has different working styles. By focusing on shared project goals rather than personal differences, I find it easy to work with diverse team members.', 'what_not_to_say': ["Saying you avoid people you don't like.", 'Detailing personal conflicts that reflect poorly on your teamwork.'], 'follow_up_questions': ['Have you ever had a disagreement with a senior?', 'How do you build trust in a team?']}}, {'question': 'What is your leadership style? Give an example of a time you led a team or project.', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Mention democratic, collaborative, or servant leadership.', 'Focus on organization, empathy, and clear goal-setting.', 'Provide a brief example of coordination.'], 'sample_answer': "My leadership style is collaborative and supportive. I believe in setting clear goals, listening to team members' ideas, and dividing work based on individual strengths. During a class group project, I helped keep the team organized and motivated, which led to a high grade.", 'what_not_to_say': ["Describing an authoritarian style ('I tell everyone what to do').", 'Claiming to do all the work yourself instead of delegating.'], 'follow_up_questions': ['How do you resolve conflict as a leader?', 'How do you delegate tasks?']}}, {'question': 'How do you define success?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Balance personal growth with business outcomes.', 'Define success in terms of quality delivery and problem-solving.', 'Keep it realistic and professional.'], 'sample_answer': "For me, success is delivering high-quality results that solve real problems, while continuously learning and growing as an engineer. Meeting project milestones and contributing positively to the team's goals constitutes success.", 'what_not_to_say': ['Defining success purely in terms of salary, promotions, or titles.', 'Giving a very abstract definition that lacks professional relevance.'], 'follow_up_questions': ['Can you share a time you felt successful?', 'How do you handle failure?']}}, {'question': 'What are your hobbies and interests outside of work? How do they help you in your professional life?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Choose active, positive, or creative hobbies.', 'Explain how they help you recharge or develop useful soft skills.', 'Keep the explanation brief.'], 'sample_answer': 'Outside of programming, I enjoy playing chess, which keeps my analytical thinking sharp, and playing football, which teaches me team coordination. These activities help me recharge and maintain a healthy work-life balance.', 'what_not_to_say': ["Saying 'I have no hobbies' or 'I only write code'.", 'Mentioning controversial topics or passive habits like sleeping.'], 'follow_up_questions': ['How often do you play chess?', 'How do you manage your time for hobbies?']}}, {'question': 'Are you planning to pursue higher education (like MS, MTech, or MBA) in the near future?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Confirm commitment to starting work immediately.', 'Frame learning in terms of professional experience.', 'Do not promise absolute certainty, but show interest in the current job opportunity.'], 'sample_answer': 'Currently, my primary focus is to start my professional career, gain hands-on industry experience, and contribute to your team. While I am committed to continuous learning, I do not have immediate plans for full-time higher education.', 'what_not_to_say': ['Saying you plan to leave in 1 year to pursue an MBA.', 'Appearing uninterested in long-term career growth in the company.'], 'follow_up_questions': ['Would you pursue part-time certifications?', 'What skills do you want to learn first?']}}, {'question': 'How do you handle feedback or constructive criticism from your peers or mentors?', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Show coachability and a growth mindset.', 'Stay calm and analytical under critique.', 'Give an example (like code reviews or project feedback).'], 'sample_answer': 'I welcome constructive feedback as an opportunity to improve. I listen objectively, analyze the suggestions without taking them personally, and implement corrections. During code reviews, feedback from senior peers has helped me write cleaner, more efficient code.', 'what_not_to_say': ['Becoming defensive or taking feedback as a personal attack.', 'Ignoring feedback or pretending you are always correct.'], 'follow_up_questions': ['Can you give an example of feedback you implemented?', 'How do you handle criticism you disagree with?']}}, {'question': 'Tell me about a time you went above and beyond what was expected of you for a project.', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Describe taking initiative to solve a problem.', 'Emphasize team spirit and quality mindset.', 'Show that you did it without neglecting your main duties.'], 'sample_answer': 'In my last project, after completing my assigned API modules, I noticed that our UI styling had alignment issues in mobile views. I spent extra time fixing the responsive layout classes, ensuring a seamless user experience across devices.', 'what_not_to_say': ["Claiming to do someone else's job because they were incompetent.", 'Exaggerating details that seem unrealistic.'], 'follow_up_questions': ['How did your team leader react?', 'Would you do it again?']}}, {'question': 'If your team leader asks you to do something that violates company policy, how would you handle it?', 'type': 'HR', 'difficulty': 'hard', 'model_answer': {'key_points': ['Prioritize integrity and compliance.', 'Polite refusal first, followed by formal escalation.', 'Show understanding of corporate governance.'], 'sample_answer': 'If asked to do something that violates company policy, I would politely decline and point out the specific policy guidelines. If the pressure persists, I would escalate the matter to my manager or the HR department through the official reporting channels.', 'what_not_to_say': ['Saying you would do it to please your senior.', 'Stating that you would ignore it and do nothing.'], 'follow_up_questions': ['What if it is a minor violation?', 'How would you handle conflict resulting from this?']}}, {'question': 'What does teamwork mean to you, and what role do you typically play in a team?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Define teamwork as collaboration and support.', 'Explain your typical role (contributor, mediator, coordinator).', 'Emphasize mutual respect.'], 'sample_answer': "To me, teamwork means collaborative effort towards a common goal, where team members support each other's strengths and cover weaknesses. I usually play a supportive role, completing my tasks on time and helping peers with debugging when needed.", 'what_not_to_say': ['Saying you prefer working alone because others are slow.', 'Describing yourself as always being the boss in every team.'], 'follow_up_questions': ["Describe a time a teammate wasn't contributing.", 'How do you handle disagreements on task division?']}}, {'question': 'Describe a time you had to explain a complex technical concept to a non-technical person.', 'type': 'HR', 'difficulty': 'medium', 'model_answer': {'key_points': ['Use analogies/metaphors.', 'Avoid acronyms and jargon.', "Focus on the 'why' and user benefits, not details."], 'sample_answer': "When explaining technical concepts to non-technical stakeholders, I avoid jargon, use real-world analogies, and focus on the business impact. For example, I compared database indexing to a textbook's index to help a client understand why query speeds improved.", 'what_not_to_say': ['Using complex terms and assuming the listener will understand.', 'Appearing patronizing or impatient.'], 'follow_up_questions': ['How do you check if they understood?', 'Describe a time you had to do this.']}}, {'question': 'Do you have any questions for us?', 'type': 'HR', 'difficulty': 'easy', 'model_answer': {'key_points': ['Always have questions prepared.', 'Ask about role expectations, team challenges, or company growth.', 'Avoid asking about salary or benefits in early rounds.'], 'sample_answer': "I would ask: 'What do the first 90 days look like for a successful candidate in this role?' and 'What is the team's biggest challenge at the moment that this candidate can help solve?'", 'what_not_to_say': ["Saying 'No, I don't have any questions' (signals lack of interest).", 'Asking about salary, leave policies, or performance bonuses immediately.'], 'follow_up_questions': ['Why are you interested in these aspects?', 'How do you prepare questions for interviews?']}}]

def get_interview_fallback(company: str, round_type: str) -> list[dict]:
    import random
    import json
    
    # Deep copy and format company names
    def format_company(q_list):
        formatted = []
        for q in q_list:
            # Deep copy
            copied = json.loads(json.dumps(q))
            copied["question"] = copied["question"].replace("{company}", company)
            if "model_answer" in copied:
                ma = copied["model_answer"]
                if "sample_answer" in ma:
                    ma["sample_answer"] = ma["sample_answer"].replace("{company}", company)
            formatted.append(copied)
        return formatted

    # Filter based on round_type
    if round_type.lower() == "technical":
        selected = format_company(INTERVIEW_TECHNICAL_POOL)
        random.shuffle(selected)
        return selected[:25]
    elif round_type.lower() == "hr":
        selected = format_company(INTERVIEW_HR_POOL)
        random.shuffle(selected)
        return selected[:25]
    else:
        # Mixed round
        t_sel = format_company(INTERVIEW_TECHNICAL_POOL)
        h_sel = format_company(INTERVIEW_HR_POOL)
        random.shuffle(t_sel)
        random.shuffle(h_sel)
        mixed = t_sel[:13] + h_sel[:12]
        random.shuffle(mixed)
        return mixed[:25]


def generate_model_answer(question: str, language: str = "en") -> dict:
    import json
    # Try to find a matching question in fallback pools
    tech_pool = INTERVIEW_TECHNICAL_POOL
    hr_pool = INTERVIEW_HR_POOL
    
    # Substring matching
    q_norm = question.strip().lower()
    match = None
    for q in tech_pool + hr_pool:
        if q["question"].strip().lower() in q_norm or q_norm in q["question"].strip().lower():
            match = q
            break
            
    if match:
        return match
        
    lang = LANG_NAMES.get(language, "English")
    # If no matching fallback, run Gemini or return default
    prompt = f"""
For the following interview question:
"{question}"

Generate a realistic model answer. Respond in {lang}.
Return JSON:
{{
  "question": "{question}",
  "type": "Technical",
  "difficulty": "medium",
  "model_answer": {{
    "key_points": ["point1", "point2"],
    "sample_answer": "well-structured model answer",
    "what_not_to_say": ["avoid1"],
    "follow_up_questions": ["followup1"]
  }}
}}
"""
    res = _json_call(prompt, "You are a senior interviewer at an Indian tech company.")
    if res is not None:
        return res
        
    # Generic high-quality fallback
    return {{
        "question": question,
        "type": "Technical",
        "difficulty": "medium",
        "model_answer": {{
            "key_points": [
                "Analyze the question carefully and structure your thoughts.",
                "Use the STAR method (Situation, Task, Action, Result) if situational.",
                "Reference industry standard terms and practical experiences."
            ],
            "sample_answer": "To answer this effectively, I would first outline the core concepts, state the key challenges associated with it, and then explain my structured approach to resolving or implementing it in a team environment.",
            "what_not_to_say": ["Giving an unstructured or overly brief answer.", "Saying you do not know without attempting to reason through it."],
            "follow_up_questions": ["Can you give a practical example?", "What is the alternative solution?"]
        }}
    }}


def analyse_marksheet(extracted_text: str, subjects: list[dict], language: str = "en") -> dict:
    lang = LANG_NAMES.get(language, "English")
    prompt = f"""
Analyse these student exam results and provide educational guidance.
Subjects & Scores: {json.dumps(subjects)}
Extracted text from marksheet: {extracted_text[:2000]}

Respond in {lang}. Return JSON:
{{
  "weak_subjects": ["subject1", "subject2"],
  "strong_subjects": ["subject3"],
  "analysis": "2-3 sentence overall analysis",
  "priority_order": ["subject ordered by urgency"],
  "improvement_tips": {{"SubjectName": "specific tip"}}
}}
"""
    res = _json_call(prompt, "You are an expert Indian academic counselor.")
    if res is None:
        return get_marksheet_fallback(subjects)
    return res


# ── Study Plan ────────────────────────────────────────────────────────────────
def generate_study_plan(subjects: list[dict], style: str, hours: float, language: str = "en", material_text: str = "", material_topics: list[dict] = None) -> dict:
    lang = LANG_NAMES.get(language, "English")
    weak = [s for s in subjects if s.get("score", 0) < 70]
    
    context = ""
    if material_text or material_topics:
        context = "\n=== REFERENCE STUDY MATERIAL DETAILS ===\n"
        if material_topics:
            context += f"Uploaded Study Material Chapters & Topics:\n{json.dumps(material_topics, indent=2)}\n"
        if material_text:
            context += f"Reference Text Snippet (first 3500 chars):\n{material_text[:3500]}\n"
        context += "========================================\n"

    prompt = f"""
Create a detailed 4-week study plan for an Indian student.
Subjects & Scores: {json.dumps(subjects)}
Weak subjects (need most focus): {json.dumps(weak)}
Learning style: {style}
Available study hours per day: {hours}
Respond in {lang}.
{context}

CRITICAL REQUIREMENTS:
1. The study plan MUST ONLY schedule subjects that are present in the provided list of Subjects & Scores above. Do not include any default or placeholder subjects (like "Maths", "Physics", or "Calculus") unless they are actually present in the input list.
2. If there are no subjects in the input list, you can use default subjects.
3. Every subject in the input list should be scheduled at least once, with weak subjects scheduled more frequently.
4. If "REFERENCE STUDY MATERIAL DETAILS" is provided above, you MUST align the topics, subtopics, and daily targets scheduled in the study plan directly with the chapters and concepts found in that reference study material. Prioritize covering the topics/subtopics from the reference material in the weeks of study.

Return JSON in this format:
{{
  "weekly_plan": {{
    "week1": {{
      "Monday": [
        {{
          "time": "09:00 AM",
          "subject": "Name of subject from the input list",
          "topic": "Topic to study in that subject",
          "duration": "1.5h"
        }}
      ],
      "Tuesday": [],
      "Wednesday": [],
      "Thursday": [],
      "Friday": [],
      "Saturday": [],
      "Sunday": [
        {{
          "time": "10:00 AM",
          "subject": "Revision",
          "topic": "Weekly Assessment & Flashcards",
          "duration": "2.0h"
        }}
      ]
    }},
    "week2": {{}}, "week3": {{}}, "week4": {{}}
  }},
  "daily_targets": {{
    "SubjectNameFromList": "Specific target description"
  }},
  "tips": [
    "Useful study tips tailored to this student's needs"
  ],
  "resources": {{
    "SubjectNameFromList": [
      "Resource 1",
      "Resource 2"
    ]
  }}
}}
"""
    res = _json_call(prompt, "You are an expert Indian academic counselor.")
    if res is None:
        return get_study_plan_fallback(subjects, style, hours, material_topics=material_topics)
    return res



# ── AI Notes ──────────────────────────────────────────────────────────────────
def generate_notes(topic: str, material_text: str = "", language: str = "en") -> str:
    lang = LANG_NAMES.get(language, "English")
    context = f"\nBase these notes on this uploaded study material:\n{material_text[:3000]}" if material_text else ""
    prompt = f"""
Generate comprehensive study notes on "{topic}" for Indian students (Class 11-12 / college level).
Respond in {lang}.{context}

Structure:
## Introduction
## Key Concepts
## Important Definitions
## Formulas / Rules (if applicable)
## Examples with Solutions
## Common Mistakes to Avoid
## Quick Summary (bullet points)
## Exam Tips
"""
    return _call(prompt, "You are an expert Indian educator. Create clear, exam-focused study notes.")


# ── Flashcards from Material ──────────────────────────────────────────────────
def generate_flashcards_from_material(material_text: str, topic: str = "", count: int = 15) -> list[dict]:
    """Generate 10-15 flashcards based on uploaded digital material."""
    prompt = f"""
Read this study material and generate exactly {count} flashcards covering the most important concepts.
Study Material:
{material_text[:4000]}

{"Topic focus: " + topic if topic else "Cover all major topics in the material."}

Return JSON array of exactly {count} objects:
[
  {{
    "topic": "chapter/topic name",
    "question": "Clear question",
    "answer": "Complete answer with explanation (2-3 sentences)",
    "difficulty": "easy|medium|hard",
    "hint": "one-line hint"
  }}
]

Make questions varied: definitions, explain-why, fill-in-blank, what-happens-when.
"""
    res = _json_call(prompt, "You are an expert educator creating study flashcards from course material.")
    if res is None:
        return get_flashcards_fallback(topic or "Study Material", count)
    return res


# ── Q&A from Material ────────────────────────────────────────────────────────
def generate_qa_from_material(material_text: str, count: int = 10, language: str = "en") -> list[dict]:
    """Generate MCQ questions strictly based on uploaded material."""
    lang = LANG_NAMES.get(language, "English")
    prompt = f"""
Read this study material carefully and generate {count} multiple-choice questions STRICTLY based on its content.
Study Material:
{material_text[:4000]}

Respond in {lang}. Return JSON array:
[
  {{
    "question": "question text",
    "options": ["A. option1", "B. option2", "C. option3", "D. option4"],
    "correct_index": 0,
    "explanation": "why this answer is correct (from the material)",
    "topic": "topic this question is from",
    "difficulty": "easy|medium|hard"
  }}
]
"""
    res = _json_call(prompt, f"You are an expert educator. Respond in {lang}.")
    if res is None:
        return get_qa_fallback("Study Material", count)
    return res


# ── Doubt Solver ──────────────────────────────────────────────────────────────
def solve_doubt(question: str, material_text: str = "", language: str = "en") -> str:
    lang = LANG_NAMES.get(language, "English")
    context = f"\nUse this uploaded study material as reference:\n{material_text[:2000]}" if material_text else ""
    prompt = f"""
A student asks: "{question}"
Respond in {lang}.{context}

Provide:
1. Direct answer
2. Step-by-step explanation  
3. Example if applicable
4. Related concepts to study
"""
    return _call(prompt, f"You are a patient Indian tutor. Respond in {lang}.")


# ── Topic Analysis from Material ──────────────────────────────────────────────
def analyse_topics_from_material(material_text: str) -> list[dict]:
    """Identify topics and their exam weightage from uploaded material."""
    prompt = f"""
Read this study material and identify all topics/chapters. 
Estimate exam weightage based on content depth and importance.
Material: {material_text[:3000]}

Return JSON array:
[
  {{
    "topic": "topic name",
    "subtopics": ["subtopic1", "subtopic2"],
    "weightage": "high|medium|low",
    "estimated_marks": 8,
    "pages_approx": 5
  }}
]
"""
    res = _json_call(prompt, "You are an expert exam analyst.")
    if res is None:
        return [
            {"topic": "Foundations & Introduction", "subtopics": ["Key Concepts", "Basic definitions"], "weightage": "high", "estimated_marks": 12, "pages_approx": 10},
            {"topic": "Theoretical Implementations", "subtopics": ["Formulas", "Core rules"], "weightage": "medium", "estimated_marks": 8, "pages_approx": 8},
            {"topic": "Advanced Applications", "subtopics": ["Case studies", "Advanced exercises"], "weightage": "medium", "estimated_marks": 6, "pages_approx": 6}
        ]
    return res


# ── Speaking Feedback ─────────────────────────────────────────────────────────
def analyse_speaking(transcript: str, topic: str, language: str = "en") -> dict:
    lang = LANG_NAMES.get(language, "English")
    prompt = f"""
Analyse this student speech transcript on topic "{topic}":
"{transcript}"

Respond in {lang}. Return JSON:
{{
  "overall_score": 7.5,
  "grammar_errors": [{{"error": "incorrect usage", "correction": "correct form", "sentence": "original"}}],
  "filler_words": {{"um": 3, "like": 5, "basically": 2}},
  "filler_count": 10,
  "pronunciation_tips": ["tip1", "tip2"],
  "vocabulary_suggestions": [{{"word_used": "big", "better_word": "significant", "context": "..."}}],
  "content_score": 7,
  "delivery_score": 6,
  "key_points_covered": ["point1", "point2"],
  "missing_points": ["what was not covered"],
  "top_improvements": ["improvement1", "improvement2", "improvement3"],
  "positive_feedback": "what they did well"
}}
"""
    res = _json_call(prompt, "You are an expert communication trainer for Indian students.")
    if res is None:
        return get_speaking_fallback(transcript, topic)
    return res


# ── Writing Feedback ──────────────────────────────────────────────────────────
def analyse_writing(text: str, mode: str = "essay", language: str = "en") -> dict:
    lang = LANG_NAMES.get(language, "English")
    prompt = f"""
Analyse this student {mode} writing:
"{text}"

Respond in {lang}. Return JSON:
{{
  "overall_score": 7,
  "grammar_errors": [{{"error": "mistake", "correction": "fix", "line": "original text"}}],
  "spelling_mistakes": [{{"wrong": "recieve", "correct": "receive"}}],
  "vocabulary_improvements": [{{"original": "good", "suggestion": "excellent", "reason": "stronger word"}}],
  "readability_score": 7.5,
  "tone": "formal|informal|mixed",
  "structure_feedback": "paragraph structure analysis",
  "corrected_version": "full corrected text",
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"]
}}
"""
    res = _json_call(prompt, "You are an expert English writing coach for Indian students.")
    if res is None:
        return get_writing_fallback(text, mode)
    return res


# ── Resume Analysis ───────────────────────────────────────────────────────────
def analyse_resume(resume_text: str, language: str = "en") -> dict:
    lang = LANG_NAMES.get(language, "English")
    prompt = f"""
Analyse this resume for an Indian student applying to tech companies:
{resume_text}

Respond in {lang}. Return JSON with "ats_score" as an integer between 0 and 100:
{{
  "ats_score": 75,
  "strengths": ["strength1", "strength2"],
  "weaknesses": ["weakness1", "weakness2"],
  "missing_keywords": ["Python", "SQL", "Agile"],
  "format_issues": ["issue1"],
  "suggestions": [{{"section": "Experience", "suggestion": "Use action verbs"}}],
  "overall_summary": "2-3 sentence assessment"
}}
"""
    res = _json_call(prompt, "You are an expert HR and ATS specialist for Indian tech companies.")
    if res is None:
        return get_resume_fallback(resume_text)
    return res


def clean_question_typos(text: str) -> str:
    import re
    typos = {
        r"\bwat\b": "what",
        r"\bpptterns\b": "patterns",
        r"\bppttern\b": "pattern",
        r"\besign\b": "design",
        r"\byouuexplain\b": "you explain",
        r"\byouexplain\b": "you explain",
        r"\ban you\b": "can you",
        r"\ban we\b": "can we",
        r"\ban I\b": "can I",
        r"\ban they\b": "can they",
        r"\ban it\b": "can it",
        r"\ban a\b": "can a",
        r"\ban the\b": "can the",
        r"\bcna\b": "can",
        r"\bteh\b": "the",
        r"\bnormalizatoin\b": "normalization",
        r"\bnormalisation\b": "normalization",
        r"\bsingelton\b": "singleton",
        r"\bsingelton's\b": "singleton's",
    }
    cleaned = text
    for typo, correction in typos.items():
        cleaned = re.sub(typo, correction, cleaned, flags=re.IGNORECASE)
    return cleaned


# ── Interview Simulation ──────────────────────────────────────────────────────
def generate_interview_question(company: str, round_type: str = "technical", difficulty: str = "medium", resume_text: str = "", language: str = "en") -> list[dict]:
    lang = LANG_NAMES.get(language, "English")
    resume_context = f"\nTailor the questions to assess the candidate's resume, skills, and experience: {resume_text}" if resume_text else ""
    # We now return a list of 25 questions
    prompt = f"""
Generate 5 realistic, highly customized {round_type} interview questions of {difficulty} difficulty specifically tailored for {company} (an Indian tech company).{resume_context}
Respond in {lang}. All text values (question, type, key_points, sample_answer, what_not_to_say, follow_up_questions) MUST be in {lang}.
Even if the candidate's resume contains spelling mistakes, typos, abbreviations, or grammatical errors, you must correct them. Do NOT propagate any typos or spelling mistakes from the resume into the generated questions or model answers. All output text must use perfect, grammatically correct, professional English with proper spelling. Double check that every word is spelled correctly. Ensure proper casing, spacing, and punctuation throughout the response.
Return a JSON array of exactly 5 objects, each having this schema:
[
  {{
    "question": "the interview question",
    "type": "HR|Technical",
    "difficulty": "easy|medium|hard",
    "model_answer": {{
      "key_points": ["point1", "point2"],
      "sample_answer": "detailed model answer",
      "what_not_to_say": ["avoid1"],
      "follow_up_questions": ["followup1"]
    }}
  }}
]
"""
    res = _json_call(prompt, "You are a senior interviewer at an Indian tech company. You must write clear, professional, grammatically correct English with absolutely zero spelling mistakes, typos, or grammatical errors.")
    
    fallback_list = get_interview_fallback(company, round_type)
    
    if res is None:
        return fallback_list
        
    try:
        # Check if response has standard questions list
        if isinstance(res, dict) and "questions" in res:
            res = res["questions"]
        if not isinstance(res, list):
            return fallback_list
            
        custom_qs = []
        for q in res:
            if isinstance(q, dict) and "question" in q:
                q["question"] = clean_question_typos(q["question"])
                ma = q.get("model_answer", {})
                if not isinstance(ma, dict):
                    ma = {}
                q["model_answer"] = {
                    "key_points": [clean_question_typos(kp) for kp in ma.get("key_points", ["Understand the concepts deeply."])],
                    "sample_answer": clean_question_typos(ma.get("sample_answer", "Here is a standard approach to solving this question.")),
                    "what_not_to_say": [clean_question_typos(wn) for wn in ma.get("what_not_to_say", ["Failing to explain clearly."])],
                    "follow_up_questions": [clean_question_typos(fu) for fu in ma.get("follow_up_questions", ["Can you elaborate?"])]
                }
                q["type"] = q.get("type", round_type.capitalize())
                q["difficulty"] = q.get("difficulty", "medium")
                custom_qs.append(q)
                
        if not custom_qs:
            return fallback_list
            
        # Combine custom questions and fallback questions to get exactly 25 questions.
        combined = list(custom_qs)
        for fq in fallback_list:
            if len(combined) >= 25:
                break
            # Check if similar question already exists
            dup = False
            for cq in combined:
                if cq["question"].lower()[:20] in fq["question"].lower() or fq["question"].lower()[:20] in cq["question"].lower():
                    dup = True
                    break
            if not dup:
                combined.append(fq)
                
        # If we still have less than 25 (e.g. due to duplicates), pad it out
        for fq in fallback_list:
            if len(combined) >= 25:
                break
            if fq not in combined:
                combined.append(fq)
                
        return combined[:25]
    except Exception as e:
        import sys
        print(f"Error merging AI questions: {e}", file=sys.stderr)
        return fallback_list


def extract_details_locally(text: str) -> dict:
    import re
    # 1. Extract skills using keyword matching
    common_skills = [
        "Go (Golang)", "Golang", "Go", "Python", "Java", "C++", "C#", "Ruby", "PHP", 
        "JavaScript", "TypeScript", "React", "Angular", "Vue", "Node.js", "Express",
        "Django", "Flask", "FastAPI", "Spring Boot", "SQL", "MySQL", "PostgreSQL", 
        "MongoDB", "Redis", "SQLite", "Docker", "Kubernetes", "AWS", "Azure", "GCP", 
        "Terraform", "Ansible", "Jenkins", "GitHub Actions", "CI/CD", "Git", "GitHub", 
        "REST APIs", "RESTful APIs", "GraphQL", "Microservices", "JWT", "OAuth",
        "HTML", "CSS", "Tailwind CSS", "Linux", "Nginx", "Apache", "Kafka", "RabbitMQ"
    ]
    
    found_skills = []
    text_lower = text.lower()
    for skill in common_skills:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if skill.lower() == "go (golang)":
            if "go (golang)" in text_lower or ("golang" in text_lower and "go" in text_lower):
                found_skills.append("Go (Golang)")
        elif skill.lower() in ("go", "c"):
            if re.search(r'\b' + skill.lower() + r'\b', text_lower):
                found_skills.append(skill)
        else:
            if re.search(pattern, text_lower):
                found_skills.append(skill)
                
    final_skills = []
    seen = set()
    for s in found_skills:
        s_norm = s.lower()
        if s_norm == "go" and "Go (Golang)" in final_skills:
            continue
        if s_norm == "golang" and "Go (Golang)" in final_skills:
            continue
        if s_norm not in seen:
            seen.add(s_norm)
            final_skills.append(s)
            
    if not final_skills:
        final_skills = ["Python", "SQL", "JavaScript"]

    # 2. Extract projects
    projects = []
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    
    project_section = False
    for line in lines:
        if re.search(r'^(projects|personal projects|key projects|academic projects|experience|work experience)$', line.lower()):
            project_section = True
            continue
        if project_section:
            if re.search(r'^(skills|education|certificates|languages|contact|summary|objective|achievements)$', line.lower()):
                project_section = False
                continue
            if len(line) < 50 and not line.startswith(("-", "•", "*", "o", "■")):
                if len(line) > 5 and not re.search(r'^(19|20)\d{2}', line) and not re.search(r'^(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', line.lower()):
                    projects.append(line)
            if len(projects) >= 5:
                break
                
    if not projects:
        for line in lines[:40]:
            if len(line) < 40 and any(keyword in line.lower() for keyword in ["system", "platform", "app", "application", "website", "manager", "tool", "bot"]):
                projects.append(line)
                if len(projects) >= 2:
                    break
                    
    if not projects:
        projects = ["Massive Golang Microservices Platform", "Movie Recommendation System"]

    # 3. Extract role
    role = "Software Engineer"
    for line in lines[:15]:
        if len(line) < 40 and any(keyword in line.lower() for keyword in ["developer", "engineer", "designer", "architect", "analyst", "specialist", "scientist"]):
            role = line
            break

    # 4. Extract summary
    summary = "Experienced developer with focus on software development and design."
    for line in lines[:30]:
        if 20 < len(line) < 120 and any(keyword in line.lower() for keyword in ["developed", "built", "implemented", "designed", "responsible", "created"]):
            summary = line
            break

    return {
        "role": role,
        "summary": summary,
        "projects": projects[:3],
        "skills": final_skills[:12]
    }


def extract_resume_details(resume_text: str) -> dict:
    prompt = f"""
Analyze the following resume text and extract:
1. A suggested job role/profile title (max 5 words).
2. A short 1-sentence summary of experience or core focus (max 15 words).
3. A list of key projects mentioned.
4. A list of technical skills mentioned.

Return a JSON object with this exact schema:
{{
  "role": "extracted job role",
  "summary": "1-sentence summary",
  "projects": ["Project Name 1", "Project Name 2"],
  "skills": ["Skill 1", "Skill 2"]
}}

Resume text:
{resume_text}
"""
    res = _json_call(prompt, "You are an expert ATS parser. You must strictly output valid JSON with the exact lowercase keys: 'role', 'summary', 'projects', 'skills'.")
    
    if res is None or not isinstance(res, dict):
        try:
            return extract_details_locally(resume_text)
        except Exception:
            return {
                "role": "Software Developer",
                "summary": "Experience in software development and systems design.",
                "projects": ["General Software Development"],
                "skills": ["Python", "SQL"]
            }
        
    try:
        normalized = {}
        fallback = {
            "role": "Software Developer",
            "summary": "Experience in software development and systems design.",
            "projects": ["General Software Development"],
            "skills": ["Python", "SQL"]
        }
        
        # Extract role
        role_key = next((k for k in res if "role" in str(k).lower() or str(k).lower() in ("profile", "title", "job")), None)
        normalized["role"] = res.get(role_key, fallback["role"]) if role_key else fallback["role"]
        if not normalized["role"]:
            normalized["role"] = fallback["role"]
            
        # Extract summary
        summary_key = next((k for k in res if "summary" in str(k).lower() or "experience" in str(k).lower() or "focus" in str(k).lower()), None)
        normalized["summary"] = res.get(summary_key, fallback["summary"]) if summary_key else fallback["summary"]
        if not normalized["summary"]:
            normalized["summary"] = fallback["summary"]
            
        # Extract projects
        projects_key = next((k for k in res if "project" in str(k).lower() or "work" in str(k).lower()), None)
        projects_val = res.get(projects_key, fallback["projects"]) if projects_key else fallback["projects"]
        if not projects_val:
            projects_val = fallback["projects"]
        normalized["projects"] = projects_val if isinstance(projects_val, list) else [str(projects_val)]
        
        # Extract skills
        skills_key = next((k for k in res if "skill" in str(k).lower() or str(k).lower() in ("keywords", "technologies", "tech")), None)
        skills_val = res.get(skills_key, fallback["skills"]) if skills_key else fallback["skills"]
        if not skills_val:
            skills_val = fallback["skills"]
        normalized["skills"] = skills_val if isinstance(skills_val, list) else [str(skills_val)]
        
        return normalized
    except Exception as parse_error:
        print(f"Error parsing Gemini response in extract_resume_details: {parse_error}")
        return extract_details_locally(resume_text)


def grade_interview_answers(questions: list[dict], answers: dict, language: str = "en") -> dict:
    import json
    lang = LANG_NAMES.get(language, "English")
    
    # 1. Build prompt for Gemini grading
    q_a_pairs = []
    for idx, q in enumerate(questions):
        ans = answers.get(str(idx), "").strip()
        q_text = q.get("question", "")
        sample_ans = q.get("model_answer", {}).get("sample_answer", "")
        key_points = q.get("model_answer", {}).get("key_points", [])
        q_a_pairs.append({
            "index": idx,
            "question": q_text,
            "candidate_answer": ans,
            "sample_answer": sample_ans,
            "key_points": key_points
        })
        
    prompt = f"""
You are a senior tech interviewer grading a candidate's mock interview responses.
Grade the candidate strictly. Marks (10 marks) are ONLY awarded if their answer is correct and covers the core technical aspects. Vague, off-topic, empty, or incorrect answers get 0 marks.
Evaluate the following QA list:
{json.dumps(q_a_pairs, indent=2)}

Respond in {lang}. All text values (feedback, strengths, improvements) MUST be in {lang}.
Return a JSON object with this exact schema:
{{
  "overall_score": 75,
  "knowledge_level": "Beginner|Intermediate|Advanced",
  "questions_graded": [
    {{
      "index": 0,
      "is_correct": true,
      "marks": 10,
      "correct_answer": "the model sample answer",
      "feedback": "constructive feedback"
    }}
  ],
  "strengths": ["strength1", "strength2"],
  "improvements": ["improvement1", "improvement2"]
}}
"""
    # Call Gemini
    res = _json_call(prompt, "You are a strict technical grader for mock interviews.")
    
    # Check if Gemini returned a valid response
    if res is not None:
        try:
            if "overall_score" in res and "questions_graded" in res:
                return res
        except Exception:
            pass
            
    # 2. Local Fallback Grader (Strict Rule-based)
    print("Falling back to local strict grader due to quota limits or API errors")
    graded = []
    total_score = 0
    correct_count = 0
    
    for idx, q in enumerate(questions):
        ans = answers.get(str(idx), "").strip()
        q_text = q.get("question", "")
        sample_ans = q.get("model_answer", {}).get("sample_answer", "")
        key_points = q.get("model_answer", {}).get("key_points", [])
        
        # Check correctness strictly
        # Threshold: must be at least 15 characters AND contain at least one key word/phrase from key_points
        is_correct = False
        feedback = "No answer provided or answer is too short to evaluate."
        
        if len(ans) >= 15:
            # Normalize words
            ans_lower = ans.lower()
            matched_keywords = []
            for kp in key_points:
                words = [w.strip(".,;:?!'\"()").lower() for w in kp.split() if len(w) > 4]
                for w in words:
                    if w in ans_lower and w not in matched_keywords:
                        matched_keywords.append(w)
            
            # Check matching words in sample answer
            sample_words = [w.strip(".,;:?!'\"()").lower() for w in sample_ans.split() if len(w) > 5]
            for w in sample_words[:15]:
                if w in ans_lower and w not in matched_keywords:
                    matched_keywords.append(w)
            
            # Strict logic: needs at least 2 matched key terms OR 1 matched key term + >40 chars length
            if len(matched_keywords) >= 2 or (len(matched_keywords) >= 1 and len(ans) >= 40):
                is_correct = True
                feedback = "Good attempt. Your answer covers core technical concepts."
            else:
                feedback = "Answer does not cover the required key concepts of this topic."
        
        marks = 10 if is_correct else 0
        if is_correct:
            correct_count += 1
            total_score += 10
            
        graded.append({
            "index": idx,
            "is_correct": is_correct,
            "marks": marks,
            "correct_answer": sample_ans,
            "feedback": feedback
        })
        
    overall_score = round((correct_count / len(questions)) * 100) if len(questions) > 0 else 0
    
    if overall_score >= 76:
        knowledge_level = "Advanced"
    elif overall_score >= 41:
        knowledge_level = "Intermediate"
    else:
        knowledge_level = "Beginner"
        
    return {
        "overall_score": overall_score,
        "knowledge_level": knowledge_level,
        "questions_graded": graded,
        "strengths": [
            "Attempted key questions relative to the technical standard.",
            "Demonstrated willingness to detail answers."
        ],
        "improvements": [
            "Focus more on core keywords and technical definitions.",
            "Elaborate your answers with examples to hit key scoring criteria."
        ]
    }
