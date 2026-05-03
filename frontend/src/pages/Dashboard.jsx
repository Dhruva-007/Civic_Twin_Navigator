import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCivicTwin } from '../context/CivicTwinContext'
import Navbar from '../components/Common/Navbar'
import LoadingSpinner from '../components/Common/LoadingSpinner'
import ScoreCard from '../components/Common/ScoreCard'
import TranslatableText from '../components/Common/TranslatableText'
import { journeyAPI, civicTwinAPI, assessmentAPI } from '../services/api'
import {
  CheckCircle, ChevronRight, Target, Award,
  MapPin, User, AlertTriangle, RefreshCw,
  Send, TrendingUp, FileText, Clock, BookOpen
} from 'lucide-react'
import toast from 'react-hot-toast'

function Dashboard() {
  const { sessionId, profile, loadCivicTwin } = useCivicTwin()
  const navigate = useNavigate()

  const [journeyData, setJourneyData] = useState(null)
  const [summary, setSummary] = useState(null)
  const [readiness, setReadiness] = useState(null)
  const [queryInput, setQueryInput] = useState('')
  const [queryAnswer, setQueryAnswer] = useState(null)
  const [queryLoading, setQueryLoading] = useState(false)
  const [pageLoading, setPageLoading] = useState(true)

  // Prevent double API calls from React StrictMode
  const hasFetched = useRef(false)

  useEffect(() => {
    if (!sessionId) { navigate('/'); return }
    if (hasFetched.current) return
    hasFetched.current = true
    initializeDashboard()
  }, [sessionId])

  const initializeDashboard = async () => {
    setPageLoading(true)
    try {
      if (!profile) await loadCivicTwin(sessionId)
      try {
        const r = await journeyAPI.get(sessionId)
        setJourneyData(r.data.journey)
      } catch {
        const r = await journeyAPI.create(sessionId)
        setJourneyData(r.data.journey)
      }
      try {
        const r = await journeyAPI.getSummary(sessionId)
        setSummary(r.data)
      } catch {}
      try {
        const r = await assessmentAPI.calculateReadiness(sessionId)
        setReadiness(r.data.readiness_score)
      } catch {}
    } catch {
      toast.error('Failed to load dashboard')
    } finally {
      setPageLoading(false)
    }
  }

  const handleStepToggle = async (phaseId, stepId, current) => {
    try {
      await journeyAPI.updateStep(sessionId, phaseId, stepId, !current)
      toast.success(!current ? '✓ Step completed!' : 'Step unmarked')
      const r = await journeyAPI.get(sessionId)
      setJourneyData(r.data.journey)
      const s = await journeyAPI.getSummary(sessionId)
      setSummary(s.data)
    } catch {
      toast.error('Failed to update step')
    }
  }

  const handleQuery = async (e) => {
    e.preventDefault()
    if (!queryInput.trim()) return
    setQueryLoading(true)
    try {
      const r = await civicTwinAPI.query(queryInput, sessionId)
      setQueryAnswer(r.data.answer)
    } catch (err) {
      toast.error(err.message || 'Query failed')
    } finally {
      setQueryLoading(false)
    }
  }

  if (pageLoading) {
    return (
      <div style={{ background: '#F4F8FF', minHeight: '100vh' }}>
        <Navbar />
        <LoadingSpinner message="Loading your dashboard..." />
      </div>
    )
  }

  const phases = journeyData?.phases || []
  const progress = summary?.progress_percentage || 0
  const completedSteps = summary?.completed_steps || 0
  const totalSteps = summary?.total_steps || 0

  const STAT_CARDS = [
    { label: 'Overall Progress', value: `${Math.round(progress)}%`, icon: TrendingUp, color: '#0176D3', bg: '#EAF3FF' },
    { label: 'Steps Completed', value: `${completedSteps} / ${totalSteps}`, icon: CheckCircle, color: '#2E844A', bg: '#EEF6EC' },
    { label: 'Location', value: profile?.personal_info?.location || 'N/A', icon: MapPin, color: '#E07A00', bg: '#FEF7E6' },
    { label: 'Voter Status', value: profile?.voter_profile?.voter_status?.replace(/_/g, ' ') || 'N/A', icon: User, color: '#8B5CF6', bg: '#F3F0FF' },
  ]

  return (
    <div style={{ background: '#F4F8FF', minHeight: '100vh' }}>
      <Navbar />

      <div className="container" style={{ paddingTop: '36px', paddingBottom: '48px' }}>

        {/* Page Header */}
        <div
          className="animate-fade-in"
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            marginBottom: '28px',
          }}
        >
          <div>
            <TranslatableText
              text="Your Election Dashboard"
              as="h2"
              style={{ fontSize: '24px', fontWeight: '700', color: '#1E1E1E', marginBottom: '4px' }}
            />
            <TranslatableText
              text="Track your progress and complete your voter readiness journey"
              as="p"
              style={{ fontSize: '14px', color: '#5F6B7A' }}
            />
          </div>
          <button onClick={initializeDashboard} className="btn-ghost btn-sm">
            <RefreshCw size={14} />
            <TranslatableText text="Refresh" />
          </button>
        </div>

        {/* Stat Cards */}
        <div
          className="stagger-children"
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(4, 1fr)',
            gap: '16px',
            marginBottom: '28px',
          }}
        >
          {STAT_CARDS.map(({ label, value, icon: Icon, color, bg }, i) => (
            <div
              key={i}
              className="animate-slide-up card-flat"
              style={{ padding: '20px' }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  marginBottom: '10px',
                }}
              >
                <div
                  style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '8px',
                    background: bg,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                  }}
                >
                  <Icon size={15} color={color} />
                </div>
                <TranslatableText
                  text={label}
                  as="span"
                  style={{ fontSize: '12px', fontWeight: '500', color: '#5F6B7A' }}
                />
              </div>
              <p
                style={{
                  fontSize: '15px',
                  fontWeight: '700',
                  color: '#1E1E1E',
                  textTransform: 'capitalize',
                }}
              >
                {value}
              </p>
            </div>
          ))}
        </div>

        {/* Main Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 360px',
            gap: '24px',
            alignItems: 'start',
          }}
        >

          {/* Left – Journey */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

            {/* Progress Bar Card */}
            <div className="card-flat" style={{ padding: '20px' }}>
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '12px',
                }}
              >
                <TranslatableText
                  text="Journey Progress"
                  as="h3"
                  style={{ fontSize: '15px', fontWeight: '600', color: '#1E1E1E' }}
                />
                <span className="badge badge-blue">
                  {Math.round(progress)}% <TranslatableText text="Complete" />
                </span>
              </div>
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${progress}%` }} />
              </div>
              <TranslatableText
                text={`${completedSteps} of ${totalSteps} steps completed`}
                as="p"
                style={{ fontSize: '12px', color: '#9BAFC4', marginTop: '8px' }}
              />
            </div>

            {/* Phases */}
            {phases.map((phase) => (
              <div key={phase.phase_id} className="card-flat" style={{ padding: '20px' }}>

                {/* Phase Header */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    marginBottom: '16px',
                  }}
                >
                  <div
                    style={{
                      width: '36px',
                      height: '36px',
                      borderRadius: '10px',
                      background: phase.status === 'completed' ? '#EEF6EC' : '#EAF3FF',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: '13px',
                      fontWeight: '700',
                      color: phase.status === 'completed' ? '#2E844A' : '#0176D3',
                      flexShrink: 0,
                    }}
                  >
                    {phase.status === 'completed'
                      ? <CheckCircle size={16} />
                      : phase.phase_number
                    }
                  </div>
                  <div style={{ flex: 1 }}>
                    <TranslatableText
                      text={phase.title}
                      as="h3"
                      style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E', marginBottom: '2px' }}
                    />
                    <TranslatableText
                      text={phase.description || ''}
                      as="p"
                      style={{ fontSize: '12px', color: '#9BAFC4' }}
                    />
                  </div>
                  <span className={`badge ${
                    phase.status === 'completed' ? 'badge-green' :
                    phase.status === 'in_progress' ? 'badge-blue' : 'badge-gray'
                  }`}>
                    <TranslatableText text={phase.status?.replace(/_/g, ' ') || ''} />
                  </span>
                </div>

                {/* Steps */}
                <div style={{ paddingLeft: '8px' }}>
                  {(phase.steps || []).map((step, si) => (
                    <div
                      key={step.step_id}
                      style={{
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: '12px',
                        padding: '12px 0',
                        borderBottom: si < phase.steps.length - 1 ? '1px solid #F4F6F9' : 'none',
                      }}
                    >
                      <button
                        onClick={() => handleStepToggle(phase.phase_id, step.step_id, step.is_completed)}
                        className="step-dot"
                        style={{
                          marginTop: '2px',
                          background: step.is_completed ? '#2E844A' : '#FFFFFF',
                          borderColor: step.is_completed ? '#2E844A' : '#C9D5E3',
                        }}
                      >
                        {step.is_completed && (
                          <CheckCircle size={12} color="#FFFFFF" />
                        )}
                      </button>
                      <div style={{ flex: 1 }}>
                        <TranslatableText
                          text={step.title}
                          as="p"
                          style={{
                            fontSize: '14px',
                            fontWeight: '500',
                            color: step.is_completed ? '#9BAFC4' : '#1E1E1E',
                            textDecoration: step.is_completed ? 'line-through' : 'none',
                            marginBottom: '3px',
                          }}
                        />
                        <TranslatableText
                          text={step.action || ''}
                          as="p"
                          style={{ fontSize: '12px', color: '#9BAFC4', lineHeight: '1.5' }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Right Panel */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

            {/* Quick Actions */}
            <div className="card-flat" style={{ padding: '20px' }}>
              <TranslatableText
                text="Quick Actions"
                as="h3"
                style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E', marginBottom: '14px' }}
              />
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {[
                  { icon: Target, label: 'Start Interactive Missions', path: '/missions', color: '#0176D3', bg: '#EAF3FF' },
                  { icon: Award, label: 'View Readiness Report', path: '/report', color: '#2E844A', bg: '#EEF6EC' },
                  { icon: BookOpen, label: 'Learn Election Process', path: '/missions', color: '#8B5CF6', bg: '#F3F0FF' },
                ].map(({ icon: Icon, label, path, color, bg }, i) => (
                  <button
                    key={i}
                    onClick={() => navigate(path)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '10px',
                      padding: '12px',
                      borderRadius: '10px',
                      border: '1px solid #E5EBF2',
                      background: '#FFFFFF',
                      color: '#1E1E1E',
                      fontSize: '13px',
                      fontWeight: '500',
                      cursor: 'pointer',
                      textAlign: 'left',
                      width: '100%',
                      transition: 'all 0.2s ease',
                      fontFamily: 'inherit',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.background = bg
                      e.currentTarget.style.borderColor = color + '30'
                      e.currentTarget.style.color = color
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.background = '#FFFFFF'
                      e.currentTarget.style.borderColor = '#E5EBF2'
                      e.currentTarget.style.color = '#1E1E1E'
                    }}
                  >
                    <div
                      style={{
                        width: '28px',
                        height: '28px',
                        borderRadius: '7px',
                        background: bg,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexShrink: 0,
                      }}
                    >
                      <Icon size={14} color={color} />
                    </div>
                    <TranslatableText text={label} as="span" style={{ flex: 1 }} />
                    <ChevronRight size={14} color="#C9D5E3" />
                  </button>
                ))}
              </div>
            </div>

            {/* Readiness Score */}
            {readiness && (
              <div className="card-flat" style={{ padding: '20px' }}>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '16px',
                  }}
                >
                  <TranslatableText
                    text="Readiness Score"
                    as="h3"
                    style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E' }}
                  />
                  <span
                    style={{
                      fontSize: '22px',
                      fontWeight: '800',
                      color: '#0176D3',
                      lineHeight: 1,
                    }}
                  >
                    {readiness.overall_score}%
                  </span>
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {readiness.scores && Object.entries(readiness.scores).map(([key, val]) => (
                    <ScoreCard
                      key={key}
                      label={key}
                      score={val.score}
                      status={val.status}
                      explanation={val.explanation}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Risk Alerts */}
            {profile?.risk_factors?.length > 0 && (
              <div
                style={{
                  background: '#FEF7E6',
                  border: '1px solid #F9E4A2',
                  borderRadius: '14px',
                  padding: '20px',
                }}
              >
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    marginBottom: '12px',
                  }}
                >
                  <AlertTriangle size={15} color="#A07900" />
                  <TranslatableText
                    text="Risk Alerts"
                    as="h3"
                    style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E' }}
                  />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {profile.risk_factors.map((risk, i) => (
                    <div
                      key={i}
                      style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}
                    >
                      <div
                        style={{
                          width: '6px',
                          height: '6px',
                          borderRadius: '50%',
                          background: '#A07900',
                          marginTop: '6px',
                          flexShrink: 0,
                        }}
                      />
                      <TranslatableText
                        text={typeof risk === 'string' ? risk.replace(/_/g, ' ') : String(risk)}
                        as="p"
                        style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.5' }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Ask a Question */}
            <div className="card-flat" style={{ padding: '20px' }}>
              <TranslatableText
                text="Ask a Question"
                as="h3"
                style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E', marginBottom: '12px' }}
              />
              <form onSubmit={handleQuery}>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <input
                    type="text"
                    value={queryInput}
                    onChange={(e) => setQueryInput(e.target.value)}
                    placeholder="Ask about voter registration..."
                    className="input-field"
                    style={{ fontSize: '13px', height: '40px', flex: 1 }}
                    disabled={queryLoading}
                  />
                  <button
                    type="submit"
                    disabled={!queryInput.trim() || queryLoading}
                    className="btn-primary"
                    style={{ height: '40px', width: '40px', padding: 0, flexShrink: 0 }}
                  >
                    {queryLoading ? (
                      <div
                        style={{
                          width: '14px',
                          height: '14px',
                          borderRadius: '50%',
                          border: '2px solid rgba(255,255,255,0.3)',
                          borderTopColor: '#FFFFFF',
                          animation: 'spin 0.8s linear infinite',
                        }}
                      />
                    ) : (
                      <Send size={14} />
                    )}
                  </button>
                </div>
              </form>

              {queryAnswer && (
                <div
                  className="animate-slide-up"
                  style={{
                    marginTop: '12px',
                    padding: '14px',
                    borderRadius: '10px',
                    background: '#F4F8FF',
                    border: '1px solid #E5EBF2',
                  }}
                >
                  <TranslatableText
                    text={queryAnswer.answer || JSON.stringify(queryAnswer)}
                    as="p"
                    style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.6' }}
                  />
                  {queryAnswer.official_source && (
                    <TranslatableText
                      text={`Source: ${queryAnswer.official_source}`}
                      as="p"
                      style={{ fontSize: '12px', color: '#0176D3', marginTop: '8px', fontWeight: '500' }}
                    />
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @media (max-width: 1024px) {
          .dashboard-grid { grid-template-columns: 1fr !important; }
        }
        @media (max-width: 768px) {
          .stat-grid { grid-template-columns: repeat(2, 1fr) !important; }
        }
      `}</style>
    </div>
  )
}

export default Dashboard