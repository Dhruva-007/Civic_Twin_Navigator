<div align="center">

<img src="https://img.shields.io/badge/Google%20Vertex%20AI-Gemini%202.5%20Flash-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" />
<img src="https://img.shields.io/badge/Firebase-Authentication%20%2B%20Firestore-FF6F00?style=for-the-badge&logo=firebase&logoColor=white" />
<img src="https://img.shields.io/badge/BigQuery-Analytics-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" />
<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black" />


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


## 🎯 Problem Statement

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

| Feature | Generic Chatbots | Civic Twin Navigator |
| :--- | :--- | :--- |
| **Brain** | Static AI | **10-agent AI system** |
| **Personalization** | Generic info | **Tailored per user profile** |
| **Language** | English only | **12 Indian languages** |
| **Interface** | Text only | **Voice input + output** |
| **Accounts** | Temporary | **Permanent Firebase accounts** |
| **Reliability** | Untested | **81 automated tests** |
| **Security** | Basic | **CSP + Rate limits + Validation** |
| **Integration** | 1-2 APIs | **9 Deeply integrated Google services** |
| **Approach** | Reactive | **Proactive risk prediction** |
| **Ethics** | No filter | **AI Safety Agent verification** |

---

## 🏗️ System Architecture

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/architecture.png" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/architecture.png" />
    <img
      src="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/architecture.png"
      alt="Civic Twin Navigator - System Architecture: Frontend (React + Vite) → FastAPI Backend with 10 AI Agents → 9 Google Cloud Services"
      width="900"
      style="background-color: white; padding: 20px; border-radius: 12px;"
    />
  </picture>
  <br/><br/>
  <b>System Architecture</b>
  <br/>
  <sub>Frontend → Security Middleware → 10 AI Agents → 6 API Routes → 9 Google Cloud Services</sub>
</div>

---

## 🤖 AI Agent System

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/agents.png" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/agents.png" />
    <img
      src="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/agents.png"
      alt="Civic Twin Navigator - 10 AI Agent Pipeline: Safety → Intent → Consistency → Policy → Journey → Simulation → Assessment → Prediction → Accessibility → Evidence Logger"
      width="900"
      style="background-color: white; padding: 20px; border-radius: 12px;"
    />
  </picture>
  <br/><br/>
  <b>10 AI Agents — Single Responsibility Principle</b>
  <br/>
  <sub>Each agent has one job • All powered by Vertex AI Gemini 2.5 Flash • Prompts centralized in prompt_templates.py</sub>
</div>

---

## ☁️ Google Services Integration

| # | Service | Integration | Purpose |
| :--- | :--- | :---: | :--- |
| 1 | **Vertex AI — Gemini 2.5 Flash** | **Deep** | Powers all 10 AI agents — reasoning, generation, simulation |
| 2 | **Firebase Firestore** | **Deep** | All data — profiles, journeys, missions, scores, logs |
| 3 | **Firebase Authentication** | **Deep** | Email/password + Google Sign-In + permanent accounts |
| 4 | **Google Maps Platform** | **Meaningful** | Polling station finder, geocoding, directions |
| 5 | **Cloud Translation API** | **Deep** | 12 Indian languages localization in real-time |
| 6 | **Text-to-Speech API** | **Meaningful** | Voice output in 9 Indian language voices |
| 7 | **Speech-to-Text API** | **Meaningful** | Voice input for low-literacy users |
| 8 | **BigQuery** | **Meaningful** | 8 event types tracked — creation, missions, scores, languages |
| 9 | **Application Default Credentials** | **Deep** | Zero hardcoded secrets anywhere |

---

## 🗺️ User Journey

1.  **Sign Up / Login** ─── Firebase Auth (Email or Google)
2.  **Describe Yourself** ── "I am a 19-year-old student in Hyderabad, hostel resident, first-time voter"
3.  **Safety Check** ──────── AI Safety Agent validates input (No bias, no misinformation)
4.  **Civic Twin Created** ── Intent Agent builds your profile; Consistency Agent verifies it
5.  **Journey Generated** ─── Journey Planner creates 5-phase plan tailored to your situation
6.  **Complete Missions** ─── 5 interactive missions with quizzes, what-if scenarios, and recovery steps
7.  **Get Scored** ────────── Assessment Agent calculates 0-100; Prediction Agent flags risks
8.  **Proof Generated** ───── Readiness certificate issued; Evidence Logger records everything
9.  **Analytics Logged** ──── BigQuery tracks all events linked to your account
10. **Vote with Confidence** ✅

---

## ✨ Features

### 🧬 Civic Twin Profile
Type one sentence about yourself. The AI builds a complete voter profile — location, age, voter status, documents, risk factors — instantly.

### 🗺️ Personalized Journey
A 5-phase election journey generated specifically for your situation, removing irrelevant steps and surfacing what matters most.

### 🎯 5 Interactive Missions
1.  **Eligibility & Registration Understanding**
2.  **Document Preparation Guidance**
3.  **Timeline & Deadline Awareness**
4.  **Poll Day Process Walkthrough**
5.  **Disruption Scenarios & Edge Cases**

### ⚡ What-If Scenarios
- *"What if I miss the registration deadline?"*
- *"What if my name is not on the voter list?"*
- *"What if I forgot my voter ID on poll day?"*

### 📊 Readiness Score — 4 Dimensions
| Dimension | Measures |
| :--- | :--- |
| **Legal Readiness** | Eligibility and citizenship status |
| **Document Readiness** | Required documents availability |
| **Timeline Readiness** | Deadline awareness and registration status |
| **Poll Day Readiness** | Preparation for voting day procedures |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
| :--- | :--- |
| **Python 3.11** | Core language |
| **FastAPI** | REST API framework |
| **Uvicorn** | ASGI server |
| **Pydantic v2** | Data validation with ConfigDict |
| **google-genai** | Vertex AI Gemini SDK |
| **firebase-admin** | Firebase Admin SDK |
| **google-cloud-bigquery** | Analytics tracking |
| **google-cloud-translate** | Translation API |
| **google-cloud-speech** | Speech-to-Text |
| **google-cloud-texttospeech** | Text-to-Speech |
| **googlemaps** | Maps Platform |
| **pytest** | **81 automated tests** |

### Frontend
| Technology | Purpose |
| :--- | :--- |
| **React 18** | UI framework |
| **Vite** | Build tool |
| **React Router v6** | Client-side routing |
| **Firebase JS SDK v11** | Authentication |
| **Axios** | HTTP client |
| **Lucide React** | Icons |
| **react-hot-toast** | Notifications |
| **Inter Font** | Typography |

---

## 📁 Project Structure

```text
Civic_Twin_Navigator/
│
├── backend/
│   ├── agents/                    # 10 specialized AI agents
│   ├── services/                  # Google Cloud service wrappers
│   ├── routes/                    # FastAPI route handlers
│   ├── models/                    # Pydantic data models
│   ├── utils/                     # Utilities & Prompt Templates
│   ├── config/                    # Pydantic settings
│   └── main.py                    # Entry point
│
├── frontend/
│   ├── src/
│   │   ├── components/            # UI components
│   │   ├── context/               # Auth & App state
│   │   ├── hooks/                 # Translation hooks
│   │   ├── pages/                 # Route pages
│   │   ├── services/              # API client
│   │   ├── App.jsx                # Router + providers
│   │   ├── main.jsx               # React entry point
│   │   ├── index.css              # Global styles
│   │   └── firebase.js            # Initialisation
│   └── public/                    # Static assets
│
├── tests/
│   └── backend/                   # 74 automated backend tests
│
└── README.md
```

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/structure.png" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/structure.png" />
    <img
      src="https://raw.githubusercontent.com/Dhruva-007/Civic_Twin_Navigator/main/docs/structure.png"
      alt="Civic Twin Navigator - Project Structure: backend (agents, services, routes, models, utils) + frontend (pages, components, context, hooks) + tests"
      width="800"
      style="background-color: white; padding: 20px; border-radius: 12px;"
    />
  </picture>
  <br/><br/>
  <b>Project Structure</b>
  <br/>
  <sub>10 agents • 9 services • 6 routes • 4 models • 7 pages • 74 tests</sub>
</div>

---

## ⚙️ Setup & Installation

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Google Cloud CLI**

### 1. Google Cloud Setup
```bash
# Set project and authenticate
gcloud config set project civic-twin-navigator
gcloud auth application-default login

# Enable required APIs
gcloud services enable aiplatform.googleapis.com firestore.googleapis.com firebase.googleapis.com translate.googleapis.com speech.googleapis.com texttospeech.googleapis.com maps-backend.googleapis.com bigquery.googleapis.com run.googleapis.com
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

---

## ▶️ Running the Application

### Terminal 1 — Backend
```bash
cd backend
python main.py
# Runs at http://localhost:8000 | API docs at http://localhost:8000/docs
```

### Terminal 2 — Frontend
```bash
cd frontend
npm run dev
# Runs at http://localhost:5173
```

---

## 🧪 Testing

```bash
# Full test suite (81 tests)
cd tests/backend
pytest -v --tb=short

# Fast tests only (no AI calls)
pytest -v -k "health or auth or security or translate" --tb=short
```

---

## 🔒 Security

| Feature | Implementation |
| :--- | :--- |
| **Authentication** | Firebase Auth — no passwords in our database |
| **Zero Secrets** | Application Default Credentials (ADC) used |
| **Validation** | Strict length limits and Pydantic validation |
| **Size Limit** | 1MB max body — prevents payload attacks |
| **Rate Limiting** | 200 req/min standard |
| **Headers** | X-Frame-Options, CSP, XSS protection |
| **Safety Agent** | AI-powered political bias detection |

---

## ♿ Accessibility

- **12 Indian Languages**: Real-time localization.
- **Voice Interface**: Native TTS/STT support.
- **Simple Language**: Adapts to user literacy levels.
- **ARIA & Keyboard**: Full screen reader and keyboard support.
- **Responsive**: Fully optimized for mobile and desktop.

---

## 📈 BigQuery Analytics

We track 8 critical event types in real-time to analyze election readiness:
- `civic_twin_created`, `journey_created`, `mission_completed`, `readiness_assessed`, `scenario_run`, `proof_generated`, `language_selected`, `user_login`.

---

## ⚠️ Disclaimer

> [!CAUTION]

✅ Completely politically neutral  
✅ Not affiliated with the Election Commission of India  
✅ Information sourced from official ECI guidelines  
✅ Always verify at [eci.gov.in](https://eci.gov.in) for latest updates

Official voter registration: [voters.eci.gov.in](https://voters.eci.gov.in) | Voter helpline: **1950**

<br></br>

<div align="center">

Built with ❤️ for Indian Democracy

**Civic Twin Navigator — Empowering every Indian to vote with confidence**

Powered by **Google Vertex AI (Gemini 2.5 Flash)**  

</div>
