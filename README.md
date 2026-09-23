# Scholr AI — Full Stack Project

AI-powered student learning platform for India.
6 languages · Student + Admin login · FastAPI backend · React frontend

---

## Project Structure

```
scholr-ai/
├── backend/
│   ├── main.py                         # FastAPI entry point
│   ├── requirements.txt
│   ├── .env.example                    # Copy to .env and fill values
│   └── app/
│       ├── core/
│       │   ├── config.py               # App settings from .env
│       │   ├── database.py             # SQLAlchemy + SQLite setup
│       │   └── security.py             # JWT auth + password hashing
│       ├── models/
│       │   ├── user.py                 # All DB models (User, Profile, Material...)
│       │   └── schemas.py              # Pydantic request/response schemas
│       ├── api/
│       │   ├── auth.py                 # /api/auth/register, /login, /me
│       │   ├── profile.py              # /api/profile/update, /dashboard
│       │   ├── learning.py             # /api/learning/* (marksheet, notes, QA...)
│       │   ├── other_routes.py         # /api/communication, /placement, /resources, /aptitude
│       │   └── admin.py                # /api/admin/* (stats, students, announcements)
│       └── services/
│           ├── ai_service.py           # All Anthropic API calls
│           └── file_service.py         # File upload + text extraction
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── App.jsx                     # Routes + auth guards
        ├── main.jsx                    # React entry point
        ├── index.css                   # Light theme Tailwind styles
        ├── store/
        │   └── useStore.js             # Zustand global state
        ├── utils/
        │   ├── api.js                  # Axios API client (all endpoints)
        │   └── translations.js         # 6 languages (EN/TA/TE/HI/ML/KN)
        ├── components/
        │   ├── auth/
        │   │   └── AuthPages.jsx       # Login + Register pages
        │   └── shared/
        │       ├── Header.jsx          # Top navigation bar
        │       └── UI.jsx              # Shared components (Spinner, Badge, Modal...)
        └── pages/
            ├── HomePage.jsx            # Landing page with module cards
            ├── LearningPage.jsx        # Planner, Notes, Flashcards, QA, Mock Test, Doubt
            ├── ResourcesPage.jsx       # Books (Class 1-12) + PYQ fetcher
            ├── PlacementPage.jsx       # Company-wise prep + Resume + Interview sim
            ├── AptitudePage.jsx        # Aptitude questions + Coding questions
            ├── CommunicationPage.jsx   # Speaking trainer + Writing analyser
            ├── DashboardPage.jsx       # Stats, progress, weekly chart, schedule
            └── AdminPage.jsx           # Admin: stats, manage students, announcements
```

---

## Setup & Run

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Edit .env → add your ANTHROPIC_API_KEY

uvicorn main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# Open: http://localhost:3000
```

---

## Features

| Module | Features |
|---|---|
| 🎯 Learning | Marksheet upload & analysis, AI study plan, AI notes, Flashcards from material, Q&A from material, Mock test, Doubt solver |
| 📚 Resources | Books for Class 1-12 (NCERT, RD Sharma, HC Verma...), Previous year board questions |
| 🏢 Placement | 6 companies (TCS, Infosys, Wipro, Accenture, Cognizant, Mr. Cooper), Resume analyser, AI interview simulator |
| 🧮 Aptitude | 10 aptitude questions with solutions, 10 coding questions with GFG + LeetCode links |
| 🎤 Communication | AI speaking feedback (grammar, filler words, pronunciation), AI writing analyser |
| 📊 Dashboard | Streak, score stats, subject progress, weekly activity chart, today's schedule |
| 🛡 Admin | Platform stats, student management (activate/deactivate/delete), announcements |

## Languages Supported
English · தமிழ் · తెలుగు · हिंदी · മലയാളം · ಕನ್ನಡ
