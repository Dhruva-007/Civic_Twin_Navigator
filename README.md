<div align="center">

<img src="https://img.shields.io/badge/Google%20Vertex%20AI-Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" />
<img src="https://img.shields.io/badge/Firebase-Authentication%20%2B%20Firestore-FF6F00?style=for-the-badge&logo=firebase&logoColor=white" />
<img src="https://img.shields.io/badge/BigQuery-Analytics-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black" />

<br /><br />

<h1>🗳️ Civic Twin Navigator</h1>

<h3>AI-Powered Election Learning & Readiness Assistant</h3>

<p>
  Civic Twin Navigator transforms election education into a personalized, interactive journey —
  helping first-time voters in India understand every step, timeline, and requirement
  through guided missions, real-life scenarios, and verified insights.
</p>

<br />

[![Tests](https://img.shields.io/badge/Tests-74%20Passing-2E844A?style=flat-square)](tests/)
[![Google Services](https://img.shields.io/badge/Google%20Services-9%20Integrated-4285F4?style=flat-square)](docs/)
[![Languages](https://img.shields.io/badge/Languages-12%20Indian-FF6F00?style=flat-square)](docs/)
[![License](https://img.shields.io/badge/License-Educational-5F6B7A?style=flat-square)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Why Civic Twin Navigator](#-why-civic-twin-navigator)
- [Architecture](#-architecture)
- [Google Services Integration](#-google-services-integration)
- [AI Agent System](#-ai-agent-system)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Security](#-security)
- [Accessibility](#-accessibility)
- [Evaluation Criteria Alignment](#-evaluation-criteria-alignment)
- [Disclaimer](#-disclaimer)

---

## 🎯 Problem Statement

> **Create an assistant that helps users understand the election process, timelines, and steps in an interactive and easy-to-follow way.**

India has over 900 million eligible voters. A significant portion — especially first-time voters, students, migrants, and rural citizens — face confusion about:

- How to register to vote
- What documents are required
- Where and when to vote
- What to do if something goes wrong

Static government websites and information pamphlets fail to address the **personalized, interactive, and accessible** nature of learning that modern users need.

---

## 💡 Solution Overview

Civic Twin Navigator builds a **"Civic Twin"** — a dynamic, AI-powered representation of each user — and transforms complex Indian election procedures into:

| Feature | Description |
|---------|-------------|
| 🧬 **Civic Twin Profile** | Personalized voter profile built from natural language input |
| 🗺️ **Journey Planner** | 5-phase election journey with deadlines and dependencies |
| 🎯 **Mission Mode** | Interactive quizzes and real election scenarios |
| ⚡ **What-If Scenarios** | Simulate disruptions and learn recovery steps |
| 📊 **Readiness Score** | 0–100 score across 4 dimensions with explanations |
| 🏆 **Proof of Readiness** | Structured certificate of election preparation |
| 🔮 **Risk Prediction** | Proactive identification of potential failure points |
| 🌐 **Multilingual** | 12 Indian languages via Google Cloud Translation |
| 🎙️ **Voice Support** | Text-to-Speech and Speech-to-Text via Google APIs |
| 🛡️ **Safety Agent** | Political bias and misinformation detection |
| 📈 **BigQuery Analytics** | Real-time usage and engagement tracking |

---

## 🚀 Why Civic Twin Navigator
❌ Not just a chatbot → Full multi-agent AI system
❌ Not static information → Context-aware adaptive journey
❌ Not generic content → Personalized per user profile
❌ Not reactive only → Proactive risk prediction
❌ Not English only → 12 Indian languages
❌ Not text only → Voice input and output
❌ Not temporary sessions → Permanent user accounts via Firebase Auth
❌ Not untested → 74 automated tests passing
❌ Not unsecured → CSP, rate limiting, input validation
❌ Not superficial Google → 9 Google services deeply integrated

text


---

## 🏗️ Architecture
┌──────────────────────────────────────────────────────────────────┐
│ Frontend (React + Vite) │
│ │
│ ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────┐ │
│ │ Home │ │ Dashboard │ │ Missions │ │ Report │ │
│ └──────────┘ └───────────┘ └──────────┘ └──────────────┘ │
│ │
│ Firebase Auth │ Context API │ Translation │ Voice UI │
└────────────────────────────────┬─────────────────────────────────┘
│ REST API (HTTPS)
┌────────────────────────────────▼─────────────────────────────────┐
│ Backend (FastAPI + Python) │
│ │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │ 10 AI Agents │ │
│ │ │ │
│ │ 1. Intent & Context Agent 6. Assessment Agent │ │
│ │ 2. Policy Retrieval Agent 7. Prediction Agent │ │
│ │ 3. Consistency Agent 8. Accessibility Agent │ │
│ │ 4. Journey Planner Agent 9. Safety Agent │ │
│ │ 5. Simulation Agent 10. Evidence Logger Agent │ │
│ └────────────────────────────────────────────────────────────┘ │
│ │
│ ┌─────────────┐ ┌──────────────┐ ┌───────────────────────┐ │
│ │ Rate Limit │ │ Input Valid. │ │ Security Headers │ │
│ │ Middleware │ │ Middleware │ │ CSP + Permissions │ │
│ └─────────────┘ └──────────────┘ └───────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
│
┌────────────────────────────────▼─────────────────────────────────┐
│ Google Cloud Services │
│ │
│ Vertex AI ─── Firebase ─── BigQuery ─── Maps ─── Translation │
│ (Gemini 2.5) Auth+DB Analytics Platform + TTS/STT │
└──────────────────────────────────────────────────────────────────┘

text


---

## ☁️ Google Services Integration

| # | Service | Integration | Purpose |
|---|---------|-------------|---------|
| 1 | **Vertex AI (Gemini 2.5 Flash)** | Deep | Powers all 10 AI agents for reasoning, personalization, simulation |
| 2 | **Firebase Firestore** | Deep | Stores profiles, journeys, scores, missions, evidence logs |
| 3 | **Firebase Authentication** | Deep | Email/password and Google Sign-In for permanent user accounts |
| 4 | **Google Maps Platform** | Meaningful | Polling station finder, geocoding, directions |
| 5 | **Cloud Translation API** | Deep | 12 Indian languages — Hindi, Marathi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Bengali, Punjabi, Odia, Assamese |
| 6 | **Text-to-Speech API** | Meaningful | Voice output for accessibility — all 12 languages |
| 7 | **Speech-to-Text API** | Meaningful | Voice input for low-literacy users |
| 8 | **BigQuery** | Meaningful | Analytics — tracks civic twin creation, missions, readiness scores, language usage |
| 9 | **Application Default Credentials** | Deep | Secure authentication — no hardcoded secrets anywhere |

---

## 🤖 AI Agent System

Each agent has a single responsibility (Single Responsibility Principle):
┌─────────────────────────────────────────────────────────┐
│ Agent │ Responsibility │
├───────────────────────────┼──────────────────────────────┤
│ Intent & Context │ Parse user input, build │
│ │ Civic Twin profile │
├───────────────────────────┼──────────────────────────────┤
│ Policy Retrieval │ Fetch ECI election rules, │
│ │ documents, timelines │
├───────────────────────────┼──────────────────────────────┤
│ Consistency Verification │ Cross-check data, detect │
│ │ contradictions │
├───────────────────────────┼──────────────────────────────┤
│ Journey Planner │ Build personalized 5-phase │
│ │ election journey │
├───────────────────────────┼──────────────────────────────┤
│ Simulation │ Generate missions, run │
│ │ what-if scenarios │
├───────────────────────────┼──────────────────────────────┤
│ Assessment │ Calculate 0-100 readiness │
│ │ score with explanations │
├───────────────────────────┼──────────────────────────────┤
│ Prediction │ Predict failure risks, │
│ │ suggest corrective actions │
├───────────────────────────┼──────────────────────────────┤
│ Accessibility │ Simplify language, enable │
│ │ multilingual support │
├───────────────────────────┼──────────────────────────────┤
│ Safety │ Detect political bias, │
│ │ flag misinformation │
├───────────────────────────┼──────────────────────────────┤
│ Evidence Logger │ Audit trail — log all │
│ │ sources and actions │
└───────────────────────────┴──────────────────────────────┘

text


**All prompts are centralized in `backend/utils/prompt_templates.py`** for maintainability.

---

## ✨ Features

### 🧬 Civic Twin Profile
Tell the app about yourself in plain language. The AI builds a personalized voter profile capturing your location, age, voter status, document situation, and risk factors.

### 🗺️ Personalized Journey
A 5-phase election journey is generated specifically for your situation — removing irrelevant steps and highlighting what matters to you.

### 🎯 Interactive Mission Mode
Five interactive missions covering:
1. Eligibility & Registration Understanding
2. Document Preparation Guidance
3. Timeline & Deadline Awareness
4. Poll Day Process Walkthrough
5. Disruption Scenarios & Edge Cases

### ⚡ What-If Scenarios
Simulate disruptions:
- *"What if I miss the registration deadline?"*
- *"What if my name is not on the voter list?"*
- *"What if I forgot my voter ID on poll day?"*

### 📊 Readiness Score
A detailed 0–100 score broken down across:
- **Legal Readiness** — eligibility and citizenship
- **Document Readiness** — required documents availability
- **Timeline Readiness** — deadline awareness
- **Poll Day Readiness** — preparation for voting day

### 🏆 Proof of Readiness
A structured certificate showing:
- Completed steps
- Pending actions
- Confidence level
- Official references

### 🔮 Risk Prediction
Proactive identification of risks based on similar user profiles with preventive missions automatically created.

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.10+ | Core language |
| FastAPI | Latest | REST API framework |
| Uvicorn | Latest | ASGI server |
| Pydantic | v2 | Data validation |
| google-genai | Latest | Vertex AI SDK |
| firebase-admin | Latest | Firebase Admin SDK |
| google-cloud-bigquery | Latest | BigQuery analytics |
| google-cloud-translate | Latest | Translation API |
| google-cloud-speech | Latest | Speech-to-Text |
| google-cloud-texttospeech | Latest | Text-to-Speech |
| googlemaps | Latest | Maps Platform |
| pytest | Latest | Testing framework |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18+ | UI framework |
| Vite | Latest | Build tool |
| React Router | v6 | Client-side routing |
| Firebase JS SDK | v11 | Authentication |
| Axios | Latest | HTTP client |
| Lucide React | Latest | Icons |
| react-hot-toast | Latest | Notifications |
| Inter Font | - | Typography |

---

## 📁 Project Structure
civic-twin-navigator/
│
├── backend/
│ ├── agents/ # 10 specialized AI agents
│ │ ├── init.py
│ │ ├── intent_context_agent.py
│ │ ├── policy_retrieval_agent.py
│ │ ├── consistency_verification_agent.py
│ │ ├── journey_planner_agent.py
│ │ ├── simulation_agent.py
│ │ ├── assessment_agent.py
│ │ ├── prediction_agent.py
│ │ ├── accessibility_agent.py
│ │ ├── safety_agent.py
│ │ └── evidence_logger_agent.py
│ │
│ ├── services/ # Google Cloud service wrappers
│ │ ├── init.py
│ │ ├── vertex_ai_service.py # Gemini 2.5 Flash
│ │ ├── firebase_service.py # Firestore
│ │ ├── auth_service.py # Firebase Auth
│ │ ├── bigquery_service.py # Analytics
│ │ ├── maps_service.py # Maps Platform
│ │ ├── translation_service.py # Cloud Translation
│ │ └── speech_service.py # TTS + STT
│ │
│ ├── routes/ # FastAPI route handlers
│ │ ├── init.py
│ │ ├── twin_routes.py # Civic Twin CRUD
│ │ ├── journey_routes.py # Journey management
│ │ ├── mission_routes.py # Missions & scenarios
│ │ ├── assessment_routes.py # Readiness scoring
│ │ ├── translate_routes.py # Translation
│ │ └── auth_routes.py # Authentication
│ │
│ ├── models/ # Pydantic data models
│ │ ├── init.py
│ │ ├── civic_twin.py
│ │ ├── journey.py
│ │ ├── mission.py
│ │ └── readiness_score.py
│ │
│ ├── utils/ # Utility functions
│ │ ├── init.py
│ │ ├── helpers.py # Common helpers
│ │ ├── validators.py # Input validation
│ │ ├── rate_limiter.py # Rate limiting
│ │ ├── cache.py # Response caching
│ │ └── prompt_templates.py # All AI prompts
│ │
│ ├── config/
│ │ ├── init.py
│ │ └── settings.py # Pydantic settings
│ │
│ └── main.py # FastAPI application entry
│
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ │ ├── Common/ # Reusable components
│ │ │ │ ├── Navbar.jsx
│ │ │ │ ├── LoadingSpinner.jsx
│ │ │ │ ├── ScoreCard.jsx
│ │ │ │ ├── LanguageSelector.jsx
│ │ │ │ ├── VoiceButton.jsx
│ │ │ │ ├── TranslatableText.jsx
│ │ │ │ └── ProtectedRoute.jsx
│ │ │ └── ui/
│ │ │ └── CivicIcon.jsx # Custom SVG icon
│ │ │
│ │ ├── context/
│ │ │ ├── AuthContext.jsx # Firebase Auth state
│ │ │ └── CivicTwinContext.jsx # App state
│ │ │
│ │ ├── hooks/
│ │ │ └── useTranslation.js # Translation hook
│ │ │
│ │ ├── pages/
│ │ │ ├── Home.jsx # Landing + input
│ │ │ ├── Dashboard.jsx # Journey tracker
│ │ │ ├── MissionMode.jsx # Interactive missions
│ │ │ ├── ReadinessReport.jsx # Score + certificate
│ │ │ ├── Login.jsx # Authentication
│ │ │ ├── Signup.jsx # Registration
│ │ │ └── ForgotPassword.jsx # Password reset
│ │ │
│ │ ├── services/
│ │ │ └── api.js # Axios API client
│ │ │
│ │ ├── firebase.js # Firebase initialization
│ │ ├── App.jsx # Router + providers
│ │ ├── main.jsx # React entry point
│ │ └── index.css # Global styles
│ │
│ └── public/
│
├── tests/
│ └── backend/
│ ├── conftest.py # pytest fixtures
│ ├── pytest.ini # pytest configuration
│ ├── test_health.py # Health endpoint tests
│ ├── test_twin.py # Civic Twin tests
│ ├── test_journey.py # Journey tests
│ ├── test_mission.py # Mission tests
│ ├── test_assessment.py # Assessment tests
│ ├── test_translate.py # Translation tests
│ ├── test_auth.py # Auth tests
│ └── test_security.py # Security tests
│
└── README.md

text


---

## ⚙️ Setup & Installation

### Prerequisites

| Requirement | Version | Check |
|------------|---------|-------|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| Google Cloud CLI | Latest | `gcloud --version` |
| Git | Latest | `git --version` |

### Google Cloud Requirements

```bash
# 1. Create or select project
gcloud config set project civic-twin-navigator

# 2. Authenticate with Application Default Credentials
gcloud auth application-default login

# 3. Enable all required APIs
gcloud services enable aiplatform.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable firebase.googleapis.com
gcloud services enable translate.googleapis.com
gcloud services enable speech.googleapis.com
gcloud services enable texttospeech.googleapis.com
gcloud services enable maps-backend.googleapis.com
gcloud services enable bigquery.googleapis.com
Backend Setup
Bash

# Clone repository
git clone https://github.com/your-repo/civic-twin-navigator
cd civic-twin-navigator

# Create virtual environment
cd backend
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Environment Configuration
Create backend/.env:

env

# Google Cloud
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Vertex AI
VERTEX_AI_MODEL=gemini-2.5-flash
VERTEX_AI_MAX_TOKENS=8192
VERTEX_AI_TEMPERATURE=0.7

# Google Maps
GOOGLE_MAPS_API_KEY=your-maps-api-key

# Firebase
FIREBASE_PROJECT_ID=your-firebase-project-id

# App
APP_NAME=Civic Twin Navigator
APP_VERSION=1.0.0
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# CORS
FRONTEND_URL=http://localhost:5173

# Rate Limiting
MAX_REQUESTS_PER_MINUTE=200
Frontend Setup
Bash

cd frontend

# Install dependencies
npm install

# Configure environment
# Create frontend/.env with Firebase config
Create frontend/.env:

env

VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Civic Twin Navigator

# Firebase Configuration
VITE_FIREBASE_API_KEY=your-api-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
Firebase Setup
text

1. Go to console.firebase.google.com
2. Select your project
3. Enable Authentication → Email/Password + Google
4. Create Firestore Database (Native mode)
5. Register Web App → Copy firebaseConfig
BigQuery Setup
Bash

# Enable BigQuery and create dataset
gcloud services enable bigquery.googleapis.com

# Create dataset in Google Cloud Console:
# BigQuery → Create Dataset → civic_twin_analytics
# Then run:
python create_table.py
▶️ Running the Application
Start Backend
Bash

cd backend
venv\Scripts\activate    # Windows
python main.py
Backend runs at: http://localhost:8000
API Documentation: http://localhost:8000/docs

Start Frontend
Bash

cd frontend
npm run dev
Frontend runs at: http://localhost:5173

📖 API Documentation
Full interactive API docs available at http://localhost:8000/docs

Core Endpoints
text

POST   /api/twin/create              Create Civic Twin profile
GET    /api/twin/{session_id}        Get Civic Twin profile
POST   /api/twin/query               Ask election question

POST   /api/journey/create           Create personalized journey
GET    /api/journey/{session_id}     Get journey
PUT    /api/journey/step/update      Mark step complete

POST   /api/mission/start            Start interactive mission
POST   /api/mission/answer           Submit mission answer
POST   /api/mission/scenario         Run what-if scenario

POST   /api/assessment/readiness     Calculate readiness score
POST   /api/assessment/proof-of-readiness  Generate certificate

POST   /api/translate                Translate to Indian language
POST   /api/translate/batch          Batch translation

POST   /api/auth/verify              Verify Firebase token
POST   /api/auth/link-session        Link session to user
GET    /api/auth/profile/{user_id}   Get user profile
Response Format
All endpoints return consistent JSON:

JSON

{
  "success": true,
  "timestamp": "2024-01-01T00:00:00.000000+00:00",
  "message": "Operation successful",
  "data": {},
  "error": ""
}
🧪 Testing
Run Full Test Suite
Bash

cd tests/backend
pytest -v --tb=short
Test Coverage
text

test_health.py      4 tests  → Health and root endpoints
test_twin.py       10 tests  → Civic Twin CRUD operations
test_journey.py     9 tests  → Journey planning and progress
test_mission.py     7 tests  → Missions and scenarios
test_assessment.py  7 tests  → Readiness scoring
test_translate.py   7 tests  → Translation API
test_auth.py        6 tests  → Authentication security
test_security.py   24 tests  → Security headers, validation, edge cases
─────────────────────────────
Total              74 tests  → All passing ✅
Quick Test (Fast, No AI Calls)
Bash

pytest -v -k "health or auth or security or translate" --tb=short
🔒 Security
Implementation
Security Feature	Implementation
Authentication	Firebase Auth — no passwords stored in our DB
Zero Hardcoded Secrets	Application Default Credentials (ADC)
Environment Variables	All keys in .env — never committed
Input Sanitization	All user inputs sanitized before processing
Input Length Limits	2000 chars user input, 5000 chars translation, 500 chars scenario
Request Size Limit	1MB max body size — prevents payload attacks
Rate Limiting	200 req/min standard, 300 req/min for translation
Security Headers	X-Content-Type-Options, X-Frame-Options, XSS Protection
Content Security Policy	Strict CSP preventing XSS and injection
Permissions Policy	Only microphone allowed — all others denied
Safety Agent	AI-powered political bias and misinformation detection
Prompt Injection	Dangerous patterns filtered before AI processing
CORS	Strictly configured for known origins only
Security Headers Applied
text

X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: microphone=self
Content-Security-Policy: default-src 'self'; ...
♿ Accessibility
Feature	Implementation
12 Indian Languages	Hindi, Marathi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Bengali, Punjabi, Odia, Assamese, English
Voice Input	Speech-to-Text via Google API — type or speak
Voice Output	Text-to-Speech — listen to all content
Simple Language Mode	Adapts to basic, intermediate, advanced literacy
Skip to Content	Screen reader keyboard navigation support
ARIA Labels	All interactive elements properly labeled
ARIA Roles	nav, main, banner, listbox, option, alert
ARIA Live Regions	Dynamic error messages announced to screen readers
Keyboard Navigation	Full keyboard support throughout
High Contrast	Light theme with WCAG compliant contrast ratios
Focus Indicators	Visible focus outlines on all interactive elements
Mobile Responsive	Works on all screen sizes
Quick Prompts	Pre-written examples for low-literacy users

🗺️ User Journey
text

Step 1: User signs up or logs in (Firebase Auth)
          ↓
Step 2: Describes situation in plain language
        "I am a 20-year-old student in Pune, hostel, first-time voter"
          ↓
Step 3: Safety Agent validates input (no bias/misinformation)
          ↓
Step 4: Intent Agent extracts profile → Civic Twin created
          ↓
Step 5: Consistency Agent verifies profile
          ↓
Step 6: Journey Planner creates 5-phase personalized plan
          ↓
Step 7: User completes interactive missions (5 missions)
          ↓
Step 8: What-If Scenarios prepare for disruptions
          ↓
Step 9: Assessment Agent calculates readiness score (0-100)
          ↓
Step 10: Proof of Readiness certificate generated
          ↓
Step 11: All data logged to BigQuery for analytics
          ↓
Step 12: User data permanently linked to Firebase account
📈 BigQuery Analytics
Events tracked in real-time:

Event	Tracked Fields
civic_twin_created	location, language, voter_status
journey_created	location, voter_status, total_phases
mission_completed	mission_number, score, correct_answers
readiness_assessed	overall_score, location, voter_status
scenario_run	scenario_type, is_recoverable
proof_generated	certificate_id, confidence_level
language_selected	language code
user_login	sign_in_provider, is_new_user
🤝 Data Sources
All election information is sourced from official government sources:

Election Commission of India — eci.gov.in
National Voters' Service Portal — voters.eci.gov.in
Voter Helpline — 1950
⚠️ Disclaimer
text

This is an educational tool built for a hackathon.

✅ Completely politically neutral
✅ No affiliation with any political party
✅ No affiliation with Election Commission of India
✅ Information sourced from official ECI guidelines
✅ Always verify at eci.gov.in for latest updates

For official voter registration, visit: voters.eci.gov.in
For voter helpline: 1950
<div align="center">
Built with ❤️ for Indian Democracy

Civic Twin Navigator — Empowering every Indian to vote with confidence

<br />
Powered by Google Vertex AI (Gemini 2.5 Flash)

</div> ```