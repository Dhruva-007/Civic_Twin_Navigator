import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCivicTwin } from '../context/CivicTwinContext'
import Navbar from '../components/Common/Navbar'
import VoiceButton from '../components/Common/VoiceButton'
import TranslatableText from '../components/Common/TranslatableText'
import LanguageSelector from '../components/Common/LanguageSelector'
import {
  ArrowRight, Shield, Map, Target, Award,
  Sparkles, FileCheck, HelpCircle,
  CheckCircle, Star
} from 'lucide-react'
import CivicIcon from '../components/ui/CivicIcon'

const FEATURES = [
  { icon: Sparkles, title: 'Civic Twin Profile', desc: 'AI builds your personalized voter profile from a simple description in seconds.' },
  { icon: Map, title: 'Personalized Journey', desc: 'Get a step-by-step election journey tailored specifically to your situation.' },
  { icon: Target, title: 'Interactive Missions', desc: 'Learn through guided missions, quizzes, and real election scenarios.' },
  { icon: Shield, title: 'Safety & Accuracy', desc: 'All information is verified against ECI guidelines. Fully politically neutral.' },
  { icon: Award, title: 'Readiness Score', desc: 'Understand exactly how prepared you are with a detailed 0–100 score.' },
  { icon: HelpCircle, title: 'What-If Scenarios', desc: 'Simulate disruptions like missed deadlines or lost voter ID with recovery steps.' },
]

const STEPS = [
  { num: '01', title: 'Describe yourself', desc: 'Share your location, age, and voter status in plain language.' },
  { num: '02', title: 'Get your journey', desc: 'AI creates a personalized 5-phase election readiness plan for you.' },
  { num: '03', title: 'Complete missions', desc: 'Interactive learning with quizzes and real-world scenarios.' },
  { num: '04', title: 'Check readiness', desc: 'Get your readiness score and proof of preparation.' },
]

const QUICK_PROMPTS = [
  "First-time voter in Pune, student in hostel",
  "Need voter ID, 19 years old, Mumbai",
  "Moved to Bangalore, need to update registration",
  "Unsure about address proof documents",
]

const TRUST_ITEMS = [
  'ECI Verified Information',
  'No Political Bias',
  '12 Indian Languages',
  'Voice Accessible',
]

const STATS = [
  { value: '12+', label: 'Indian Languages' },
  { value: '10', label: 'AI Agents' },
  { value: '5', label: 'Learning Missions' },
  { value: '100%', label: 'Politically Neutral' },
]

function Home() {
  const [userInput, setUserInput] = useState('')
  const [selectedLanguage, setSelectedLanguage] = useState('en')
  const { createCivicTwin, loading, sessionId } = useCivicTwin()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!userInput.trim()) return
    const result = await createCivicTwin(userInput, selectedLanguage)
    if (result.success) navigate('/dashboard')
  }

  // Returning user screen
  if (sessionId) {
    return (
      <div style={{ background: '#FFFFFF', minHeight: '100vh' }}>
        <Navbar />
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: 'calc(100vh - 64px)',
            padding: '24px',
          }}
        >
          <div
            className="animate-slide-up"
            style={{
              textAlign: 'center',
              maxWidth: '420px',
              width: '100%',
              background: '#FFFFFF',
              border: '1px solid #E5EBF2',
              borderRadius: '20px',
              padding: '48px 40px',
              boxShadow: '0 8px 40px rgba(0,0,0,0.08)',
            }}
          >
            <div
              style={{
                width: '48px',
                height: '48px',
                borderRadius: '12px',
                background: 'linear-gradient(135deg, #0176D3, #0EA5E9)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 24px',
              }}
            >
              <CivicIcon size={30} color="#FFFFFF" />
            </div>

            <TranslatableText
              text="Welcome Back!"
              as="h2"
              style={{ fontSize: '22px', fontWeight: '700', color: '#1E1E1E', marginBottom: '8px' }}
            />

            <TranslatableText
              text="Continue your election readiness journey."
              as="p"
              style={{ fontSize: '14px', color: '#5F6B7A', marginBottom: '32px', lineHeight: '1.5' }}
            />

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <button
                onClick={() => navigate('/dashboard')}
                className="btn-primary"
                style={{ width: '100%', height: '46px', fontSize: '15px' }}
              >
                <TranslatableText text="Continue to Dashboard" />
                <ArrowRight size={16} />
              </button>
              <button
                onClick={() => {
                  localStorage.removeItem('civic_session_id')
                  window.location.reload()
                }}
                className="btn-secondary"
                style={{ width: '100%', height: '46px', fontSize: '15px' }}
              >
                <TranslatableText text="Start New Session" />
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div style={{ background: '#FFFFFF' }}>
      <Navbar />

      {/* ─── Hero ─── */}
      <section className="hero-gradient" style={{ padding: '80px 0 100px' }}>
        <div className="container">
          <div
            className="animate-fade-in"
            style={{ textAlign: 'center', maxWidth: '720px', margin: '0 auto' }}
          >
            {/* Tag */}
            <div style={{ marginBottom: '24px' }}>
              <span className="badge badge-blue" style={{ fontSize: '12px', padding: '5px 14px' }}>
                <Star size={11} />
                Powered by Google Vertex AI
              </span>
            </div>

            {/* Headline */}
            <h1
              style={{
                fontSize: 'clamp(2rem, 5vw, 3.2rem)',
                fontWeight: '800',
                color: '#1E1E1E',
                lineHeight: '1.15',
                letterSpacing: '-0.03em',
                marginBottom: '20px',
              }}
            >
              <TranslatableText text="Your Personal Guide to" as="span" />
              <br />
              <TranslatableText
                text="Voting in India"
                as="span"
                style={{ color: '#0176D3' }}
              />
            </h1>

            {/* Subheadline */}
            <TranslatableText
              text="Civic Twin Navigator is an AI-powered assistant that helps first-time voters understand every step, timeline, and document needed to vote with confidence."
              as="p"
              style={{
                fontSize: '17px',
                color: '#5F6B7A',
                lineHeight: '1.7',
                maxWidth: '560px',
                margin: '0 auto 48px',
              }}
            />

            {/* Input Card */}
            <div
              className="animate-slide-up"
              style={{
                background: '#FFFFFF',
                border: '1.5px solid #E5EBF2',
                borderRadius: '18px',
                boxShadow: '0 8px 40px rgba(0,0,0,0.09)',
                overflow: 'hidden',
                maxWidth: '680px',
                margin: '0 auto 24px',
              }}
            >
              <form onSubmit={handleSubmit}>
                <textarea
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  placeholder="Tell us about yourself... e.g., I'm a 20-year-old student in Pune, living in a hostel, and want to register to vote for the first time."
                  rows={4}
                  disabled={loading}
                  style={{
                    width: '100%',
                    background: 'transparent',
                    border: 'none',
                    outline: 'none',
                    resize: 'none',
                    padding: '20px 20px 0',
                    fontSize: '15px',
                    fontFamily: 'inherit',
                    color: '#1E1E1E',
                    lineHeight: '1.6',
                    minHeight: '110px',
                  }}
                />

                {/* Action Bar */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 16px',
                    borderTop: '1px solid #F4F6F9',
                    background: '#FAFBFC',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <VoiceButton
                      onTranscript={(t) => setUserInput(t)}
                      language={selectedLanguage}
                    />
                    <LanguageSelector
                      selected={selectedLanguage}
                      onChange={setSelectedLanguage}
                    />
                  </div>

                  {loading ? (
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '8px 16px',
                        borderRadius: '8px',
                        background: '#EAF3FF',
                      }}
                    >
                      <div
                        style={{
                          width: '16px',
                          height: '16px',
                          borderRadius: '50%',
                          border: '2px solid #C7E0F4',
                          borderTopColor: '#0176D3',
                          animation: 'spin 0.8s linear infinite',
                        }}
                      />
                      <span style={{ fontSize: '14px', fontWeight: '500', color: '#0176D3' }}>
                        Creating...
                      </span>
                    </div>
                  ) : (
                    <button
                      type="submit"
                      disabled={!userInput.trim()}
                      className="btn-primary"
                      style={{ height: '40px', fontSize: '14px', padding: '0 20px' }}
                    >
                      <TranslatableText text="Create My Civic Twin" />
                      <ArrowRight size={15} />
                    </button>
                  )}
                </div>
              </form>
            </div>

            {/* Quick Prompts */}
            <div>
              <TranslatableText
                text="Try an example:"
                as="p"
                style={{ fontSize: '13px', color: '#9BAFC4', marginBottom: '12px' }}
              />
              <div
                style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  justifyContent: 'center',
                  gap: '8px',
                }}
              >
                {QUICK_PROMPTS.map((p, i) => (
                  <button
                    key={i}
                    onClick={() => setUserInput(p)}
                    type="button"
                    style={{
                      padding: '7px 14px',
                      borderRadius: '8px',
                      border: '1px solid #E5EBF2',
                      background: '#FFFFFF',
                      color: '#5F6B7A',
                      fontSize: '13px',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                      fontFamily: 'inherit',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.borderColor = '#0176D3'
                      e.currentTarget.style.color = '#0176D3'
                      e.currentTarget.style.background = '#EAF3FF'
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.borderColor = '#E5EBF2'
                      e.currentTarget.style.color = '#5F6B7A'
                      e.currentTarget.style.background = '#FFFFFF'
                    }}
                  >
                    <TranslatableText text={p} />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
        <style>{`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}</style>
      </section>

      {/* ─── Stats ─── */}
      <section
        style={{
          padding: '48px 0',
          borderTop: '1px solid #E5EBF2',
          borderBottom: '1px solid #E5EBF2',
        }}
      >
        <div className="container">
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '24px',
            }}
          >
            {STATS.map(({ value, label }, i) => (
              <div key={i} style={{ textAlign: 'center' }}>
                <div
                  className="gradient-text"
                  style={{
                    fontSize: '32px',
                    fontWeight: '800',
                    marginBottom: '4px',
                    lineHeight: 1.2,
                  }}
                >
                  {value}
                </div>
                <TranslatableText
                  text={label}
                  as="p"
                  style={{ fontSize: '13px', color: '#5F6B7A' }}
                />
              </div>
            ))}
          </div>
        </div>
        <style>{`
          @media (max-width: 640px) {
            .stats-grid { grid-template-columns: repeat(2, 1fr) !important; }
          }
        `}</style>
      </section>

      {/* ─── Features ─── */}
      <section className="section">
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '56px' }}>
            <TranslatableText
              text="Everything you need to vote confidently"
              as="h2"
              style={{ fontSize: '28px', fontWeight: '700', color: '#1E1E1E', marginBottom: '12px' }}
            />
            <TranslatableText
              text="Six powerful features that guide you from confusion to confidence."
              as="p"
              style={{ fontSize: '16px', color: '#5F6B7A', maxWidth: '480px', margin: '0 auto' }}
            />
          </div>

          <div
            className="stagger-children"
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '20px',
            }}
          >
            {FEATURES.map(({ icon: Icon, title, desc }, i) => (
              <div key={i} className="card animate-slide-up">
                <div
                  style={{
                    width: '44px',
                    height: '44px',
                    borderRadius: '12px',
                    background: '#EAF3FF',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '16px',
                    flexShrink: 0,
                  }}
                >
                  <Icon size={20} color="#0176D3" />
                </div>
                <TranslatableText
                  text={title}
                  as="h3"
                  style={{ fontSize: '15px', fontWeight: '600', color: '#1E1E1E', marginBottom: '8px' }}
                />
                <TranslatableText
                  text={desc}
                  as="p"
                  style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.7' }}
                />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── How It Works ─── */}
      <section className="section" style={{ background: '#F4F8FF' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '56px' }}>
            <TranslatableText
              text="How it works"
              as="h2"
              style={{ fontSize: '28px', fontWeight: '700', color: '#1E1E1E', marginBottom: '12px' }}
            />
            <TranslatableText
              text="Four simple steps to go from confused to completely ready to vote."
              as="p"
              style={{ fontSize: '16px', color: '#5F6B7A', maxWidth: '420px', margin: '0 auto' }}
            />
          </div>

          <div
            className="stagger-children"
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '20px',
            }}
          >
            {STEPS.map(({ num, title, desc }, i) => (
              <div
                key={i}
                className="animate-slide-up"
                style={{
                  background: '#FFFFFF',
                  border: '1px solid #E5EBF2',
                  borderRadius: '14px',
                  padding: '28px 24px',
                  boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
                }}
              >
                <div
                  style={{
                    fontSize: '36px',
                    fontWeight: '800',
                    color: '#C7E0F4',
                    lineHeight: 1,
                    marginBottom: '16px',
                  }}
                >
                  {num}
                </div>
                <TranslatableText
                  text={title}
                  as="h3"
                  style={{ fontSize: '15px', fontWeight: '600', color: '#1E1E1E', marginBottom: '8px' }}
                />
                <TranslatableText
                  text={desc}
                  as="p"
                  style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.7' }}
                />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ─── Trust Section ─── */}
      <section className="section">
        <div className="container">
          <div
            style={{
              background: 'linear-gradient(135deg, #EAF3FF 0%, #F4F8FF 100%)',
              border: '1px solid #C7E0F4',
              borderRadius: '20px',
              padding: '64px 48px',
              textAlign: 'center',
            }}
          >
            <TranslatableText
              text="Trusted information, not opinions"
              as="h2"
              style={{ fontSize: '26px', fontWeight: '700', color: '#1E1E1E', marginBottom: '12px' }}
            />
            <TranslatableText
              text="All information is sourced from the Election Commission of India. We are completely politically neutral and non-partisan."
              as="p"
              style={{
                fontSize: '15px',
                color: '#5F6B7A',
                maxWidth: '500px',
                margin: '0 auto 36px',
                lineHeight: '1.7',
              }}
            />
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                justifyContent: 'center',
                gap: '12px',
              }}
            >
              {TRUST_ITEMS.map((item, i) => (
                <div
                  key={i}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '10px 18px',
                    borderRadius: '10px',
                    background: '#FFFFFF',
                    border: '1px solid #E5EBF2',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.05)',
                  }}
                >
                  <CheckCircle size={15} color="#2E844A" />
                  <TranslatableText
                    text={item}
                    as="span"
                    style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E' }}
                  />
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ─── Footer ─── */}
      <footer style={{ borderTop: '1px solid #E5EBF2', padding: '32px 0' }}>
        <div className="container">
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '16px',
              textAlign: 'center',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div
                style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: '7px',
                  background: 'linear-gradient(135deg, #0176D3, #0EA5E9)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <CivicIcon size={22} color="#FFFFFF" />
              </div>
              <span style={{ fontWeight: '700', fontSize: '14px', color: '#1E1E1E' }}>
                Civic Twin Navigator
              </span>
            </div>
            <TranslatableText
              text="Powered by Google Vertex AI (Gemini 2.5 Flash) • Data from Election Commission of India"
              as="p"
              style={{ fontSize: '12px', color: '#9BAFC4' }}
            />
            <TranslatableText
              text="Educational tool only. Not affiliated with any political party or ECI."
              as="p"
              style={{ fontSize: '12px', color: '#C9D5E3' }}
            />
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home