import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCivicTwin } from '../context/CivicTwinContext'
import Navbar from '../components/Common/Navbar'
import LoadingSpinner from '../components/Common/LoadingSpinner'
import TranslatableText from '../components/Common/TranslatableText'
import { missionAPI } from '../services/api'
import {
  Target, CheckCircle, XCircle, ArrowRight,
  ArrowLeft, HelpCircle, Zap, BookOpen,
  AlertCircle, Trophy, Play, Send, MessageSquare
} from 'lucide-react'
import toast from 'react-hot-toast'

const MISSIONS = [
  { id: 1, title: 'Eligibility & Registration', desc: 'Learn who can vote and how to register.', icon: BookOpen, color: '#0176D3', bg: '#EAF3FF' },
  { id: 2, title: 'Document Preparation', desc: 'Know exactly which documents you need.', icon: Target, color: '#8B5CF6', bg: '#F3F0FF' },
  { id: 3, title: 'Timeline & Deadlines', desc: 'Never miss an important election date.', icon: Zap, color: '#E07A00', bg: '#FEF7E6' },
  { id: 4, title: 'Poll Day Walkthrough', desc: 'Step-by-step guide for election day.', icon: CheckCircle, color: '#2E844A', bg: '#EEF6EC' },
  { id: 5, title: 'Disruption Scenarios', desc: 'Handle unexpected situations confidently.', icon: AlertCircle, color: '#C23934', bg: '#FEEFEC' },
]

const QUICK_SCENARIOS = [
  "What if my name is not on voter list?",
  "What if I forgot my voter ID on poll day?",
  "What if I miss the registration deadline?",
]

function MissionMode() {
  const { sessionId, profile } = useCivicTwin()
  const navigate = useNavigate()

  const [currentMission, setCurrentMission] = useState(null)
  const [currentQIndex, setCurrentQIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [answerResult, setAnswerResult] = useState(null)
  const [missionScore, setMissionScore] = useState({ correct: 0, total: 0 })
  const [missionLoading, setMissionLoading] = useState(false)
  const [showHint, setShowHint] = useState(false)
  const [missionCompleted, setMissionCompleted] = useState(false)
  const [activeTab, setActiveTab] = useState('missions')
  const [scenarioInput, setScenarioInput] = useState('')
  const [scenarioResult, setScenarioResult] = useState(null)
  const [scenarioLoading, setScenarioLoading] = useState(false)

  const hasFetched = useRef(false)

  useEffect(() => {
    if (!sessionId) { navigate('/'); return }
    hasFetched.current = true
  }, [sessionId])

  const startMission = async (num) => {
    setMissionLoading(true)
    setCurrentQIndex(0)
    setSelectedAnswer(null)
    setAnswerResult(null)
    setMissionScore({ correct: 0, total: 0 })
    setMissionCompleted(false)
    setShowHint(false)
    try {
      const r = await missionAPI.start(sessionId, num)
      setCurrentMission(r.data.mission)
    } catch (err) {
      toast.error(err.message || 'Failed to start mission')
    } finally {
      setMissionLoading(false)
    }
  }

  const submitAnswer = async () => {
    if (!selectedAnswer || !currentMission) return
    const q = currentMission.questions[currentQIndex]
    try {
      const r = await missionAPI.submitAnswer(
        sessionId, currentMission.mission_id,
        q.question_id, selectedAnswer, q.correct_answer, q.explanation
      )
      setAnswerResult(r.data.result)
      setMissionScore(p => ({
        correct: p.correct + (r.data.result.is_correct ? 1 : 0),
        total: p.total + 1,
      }))
    } catch {
      toast.error('Failed to submit answer')
    }
  }

  const nextQuestion = () => {
    const qs = currentMission?.questions || []
    if (currentQIndex + 1 < qs.length) {
      setCurrentQIndex(p => p + 1)
      setSelectedAnswer(null)
      setAnswerResult(null)
      setShowHint(false)
    } else {
      setMissionCompleted(true)
      missionAPI.completeMission(sessionId, currentMission.mission_id)
      toast.success('🎉 Mission Completed!')
    }
  }

  const handleScenario = async (e) => {
    e.preventDefault()
    if (!scenarioInput.trim()) return
    setScenarioLoading(true)
    try {
      const r = await missionAPI.runScenario(sessionId, scenarioInput)
      setScenarioResult(r.data.scenario)
    } catch (err) {
      toast.error(err.message || 'Scenario failed')
    } finally {
      setScenarioLoading(false)
    }
  }

  if (!sessionId) return null

  const questions = currentMission?.questions || []
  const currentQ = questions[currentQIndex]

  return (
    <div style={{ background: '#F4F8FF', minHeight: '100vh' }}>
      <Navbar />

      <div className="container" style={{ paddingTop: '36px', paddingBottom: '48px' }}>

        {/* Header */}
        <div className="animate-fade-in" style={{ marginBottom: '28px' }}>
          <TranslatableText
            text="Interactive Missions"
            as="h2"
            style={{ fontSize: '24px', fontWeight: '700', color: '#1E1E1E', marginBottom: '4px' }}
          />
          <TranslatableText
            text="Learn about elections through guided missions and what-if scenarios"
            as="p"
            style={{ fontSize: '14px', color: '#5F6B7A' }}
          />
        </div>

        {/* Tabs */}
        <div
          style={{
            display: 'inline-flex',
            background: '#FFFFFF',
            border: '1px solid #E5EBF2',
            borderRadius: '10px',
            padding: '4px',
            marginBottom: '28px',
            gap: '4px',
          }}
        >
          {[
            { id: 'missions', label: 'Missions', icon: Target },
            { id: 'scenarios', label: 'What-If Scenarios', icon: MessageSquare },
          ].map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '8px 18px',
                borderRadius: '7px',
                border: 'none',
                background: activeTab === id ? '#EAF3FF' : 'transparent',
                color: activeTab === id ? '#0176D3' : '#5F6B7A',
                fontSize: '14px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                fontFamily: 'inherit',
              }}
            >
              <Icon size={15} />
              <TranslatableText text={label} />
            </button>
          ))}
        </div>

        {/* ── Missions Tab ── */}
        {activeTab === 'missions' && (
          <>
            {/* Mission Grid */}
            {!currentMission && !missionLoading && (
              <div
                className="stagger-children"
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(3, 1fr)',
                  gap: '20px',
                }}
              >
                {MISSIONS.map(({ id, title, desc, icon: Icon, color, bg }) => (
                  <div
                    key={id}
                    className="mission-card animate-slide-up"
                    onClick={() => startMission(id)}
                  >
                    <div
                      style={{
                        width: '48px',
                        height: '48px',
                        borderRadius: '12px',
                        background: bg,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        marginBottom: '16px',
                        flexShrink: 0,
                      }}
                    >
                      <Icon size={22} color={color} />
                    </div>
                    <span
                      className="badge badge-gray"
                      style={{ marginBottom: '10px', fontSize: '11px' }}
                    >
                      <TranslatableText text={`Mission ${id}`} />
                    </span>
                    <TranslatableText
                      text={title}
                      as="h3"
                      style={{ fontSize: '15px', fontWeight: '600', color: '#1E1E1E', marginBottom: '8px' }}
                    />
                    <TranslatableText
                      text={desc}
                      as="p"
                      style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.6', marginBottom: '20px', flex: 1 }}
                    />
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                        fontSize: '13px',
                        fontWeight: '600',
                        color,
                      }}
                    >
                      <Play size={13} />
                      <TranslatableText text="Start Mission" />
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Loading */}
            {missionLoading && <LoadingSpinner message="Generating your mission..." />}

            {/* Mission Complete */}
            {missionCompleted && (
              <div style={{ maxWidth: '440px', margin: '0 auto' }} className="animate-scale-in">
                <div
                  style={{
                    background: '#FFFFFF',
                    border: '1px solid #E5EBF2',
                    borderRadius: '20px',
                    padding: '48px 40px',
                    textAlign: 'center',
                    boxShadow: '0 8px 40px rgba(0,0,0,0.08)',
                  }}
                >
                  <div
                    style={{
                      width: '64px',
                      height: '64px',
                      borderRadius: '16px',
                      background: '#EEF6EC',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: '0 auto 24px',
                    }}
                  >
                    <Trophy size={28} color="#2E844A" />
                  </div>
                  <TranslatableText
                    text="Mission Complete!"
                    as="h2"
                    style={{ fontSize: '22px', fontWeight: '700', color: '#1E1E1E', marginBottom: '8px' }}
                  />
                  <div style={{ fontSize: '40px', fontWeight: '800', color: '#0176D3', margin: '16px 0' }}>
                    {missionScore.correct}/{missionScore.total}
                  </div>
                  <TranslatableText
                    text="Questions answered correctly"
                    as="p"
                    style={{ fontSize: '14px', color: '#5F6B7A', marginBottom: '32px' }}
                  />
                  <div style={{ display: 'flex', gap: '12px' }}>
                    <button
                      onClick={() => { setCurrentMission(null); setMissionCompleted(false) }}
                      className="btn-secondary"
                      style={{ flex: 1, height: '44px' }}
                    >
                      <ArrowLeft size={15} />
                      <TranslatableText text="All Missions" />
                    </button>
                    <button
                      onClick={() => navigate('/report')}
                      className="btn-primary"
                      style={{ flex: 1, height: '44px' }}
                    >
                      <TranslatableText text="View Report" />
                      <ArrowRight size={15} />
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Active Mission */}
            {currentMission && !missionCompleted && !missionLoading && currentQ && (
              <div style={{ maxWidth: '640px', margin: '0 auto' }} className="animate-slide-up">

                {/* Mission Header */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '20px',
                  }}
                >
                  <button onClick={() => setCurrentMission(null)} className="btn-ghost btn-sm">
                    <ArrowLeft size={14} />
                    <TranslatableText text="Back" />
                  </button>
                  <span style={{ fontSize: '13px', color: '#9BAFC4' }}>
                    <TranslatableText text={`Question ${currentQIndex + 1} of ${questions.length}`} />
                  </span>
                  <span className="badge badge-blue">
                    {missionScore.correct}/{missionScore.total} <TranslatableText text="correct" />
                  </span>
                </div>

                {/* Progress */}
                <div className="progress-bar" style={{ marginBottom: '24px' }}>
                  <div
                    className="progress-fill"
                    style={{ width: `${((currentQIndex + 1) / questions.length) * 100}%` }}
                  />
                </div>

                {/* Question Card */}
                <div
                  style={{
                    background: '#FFFFFF',
                    border: '1px solid #E5EBF2',
                    borderRadius: '16px',
                    padding: '28px',
                    marginBottom: '16px',
                    boxShadow: '0 4px 16px rgba(0,0,0,0.05)',
                  }}
                >
                  <TranslatableText
                    text={currentQ.question}
                    as="p"
                    style={{
                      fontSize: '16px',
                      fontWeight: '600',
                      color: '#1E1E1E',
                      lineHeight: '1.5',
                      marginBottom: '24px',
                    }}
                  />

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    {(currentQ.options || []).map((option, idx) => {
                      const isSelected = selectedAnswer === option
                      const isCorrect = answerResult && option === currentQ.correct_answer
                      const isWrong = answerResult && isSelected && !answerResult.is_correct

                      return (
                        <button
                          key={idx}
                          onClick={() => !answerResult && setSelectedAnswer(option)}
                          disabled={!!answerResult}
                          style={{
                            width: '100%',
                            textAlign: 'left',
                            padding: '14px 16px',
                            borderRadius: '10px',
                            border: `1.5px solid ${
                              isCorrect ? '#2E844A' : isWrong ? '#C23934' :
                              isSelected ? '#0176D3' : '#E5EBF2'
                            }`,
                            background: isCorrect ? '#EEF6EC' : isWrong ? '#FEEFEC' :
                              isSelected ? '#EAF3FF' : '#FAFBFC',
                            color: isCorrect ? '#2E844A' : isWrong ? '#C23934' :
                              isSelected ? '#0176D3' : '#1E1E1E',
                            fontSize: '14px',
                            fontWeight: '500',
                            cursor: answerResult ? 'default' : 'pointer',
                            transition: 'all 0.2s ease',
                            fontFamily: 'inherit',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '10px',
                          }}
                          onMouseEnter={e => {
                            if (!answerResult && !isSelected) {
                              e.currentTarget.style.borderColor = '#0176D3'
                              e.currentTarget.style.background = '#EAF3FF'
                              e.currentTarget.style.color = '#0176D3'
                            }
                          }}
                          onMouseLeave={e => {
                            if (!answerResult && !isSelected) {
                              e.currentTarget.style.borderColor = '#E5EBF2'
                              e.currentTarget.style.background = '#FAFBFC'
                              e.currentTarget.style.color = '#1E1E1E'
                            }
                          }}
                        >
                          {isCorrect && <CheckCircle size={16} style={{ flexShrink: 0 }} />}
                          {isWrong && <XCircle size={16} style={{ flexShrink: 0 }} />}
                          <TranslatableText text={option} />
                        </button>
                      )
                    })}
                  </div>
                </div>

                {/* Hint */}
                {!answerResult && currentQ.hint && (
                  <button
                    onClick={() => setShowHint(!showHint)}
                    className="btn-ghost btn-sm"
                    style={{ marginBottom: '12px' }}
                  >
                    <HelpCircle size={14} />
                    <TranslatableText text={showHint ? 'Hide Hint' : 'Show Hint'} />
                  </button>
                )}
                {showHint && !answerResult && (
                  <div
                    className="animate-slide-up"
                    style={{
                      padding: '14px 16px',
                      borderRadius: '10px',
                      background: '#FEF7E6',
                      border: '1px solid #F9E4A2',
                      marginBottom: '14px',
                    }}
                  >
                    <TranslatableText
                      text={`💡 ${currentQ.hint}`}
                      as="p"
                      style={{ fontSize: '13px', color: '#A07900' }}
                    />
                  </div>
                )}

                {/* Answer Result */}
                {answerResult && (
                  <div
                    className="animate-scale-in"
                    style={{
                      padding: '16px',
                      borderRadius: '12px',
                      background: answerResult.is_correct ? '#EEF6EC' : '#FEEFEC',
                      border: `1px solid ${answerResult.is_correct ? '#C8E6C2' : '#F5BCB9'}`,
                      marginBottom: '16px',
                    }}
                  >
                    <TranslatableText
                      text={answerResult.is_correct ? '✅ Correct!' : '❌ Incorrect'}
                      as="p"
                      style={{
                        fontWeight: '600',
                        fontSize: '14px',
                        marginBottom: '6px',
                        color: answerResult.is_correct ? '#2E844A' : '#C23934',
                      }}
                    />
                    <TranslatableText
                      text={answerResult.explanation}
                      as="p"
                      style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.6' }}
                    />
                  </div>
                )}

                {/* Submit / Next */}
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  {!answerResult ? (
                    <button
                      onClick={submitAnswer}
                      disabled={!selectedAnswer}
                      className="btn-primary"
                      style={{ height: '44px' }}
                    >
                      <TranslatableText text="Submit Answer" />
                      <ArrowRight size={15} />
                    </button>
                  ) : (
                    <button onClick={nextQuestion} className="btn-primary" style={{ height: '44px' }}>
                      <TranslatableText
                        text={currentQIndex + 1 < questions.length ? 'Next Question' : 'Complete Mission'}
                      />
                      <ArrowRight size={15} />
                    </button>
                  )}
                </div>
              </div>
            )}
          </>
        )}

        {/* ── Scenarios Tab ── */}
        {activeTab === 'scenarios' && (
          <div style={{ maxWidth: '640px', margin: '0 auto' }} className="animate-fade-in">

            {/* Input Card */}
            <div
              style={{
                background: '#FFFFFF',
                border: '1px solid #E5EBF2',
                borderRadius: '16px',
                padding: '28px',
                marginBottom: '20px',
                boxShadow: '0 4px 16px rgba(0,0,0,0.05)',
              }}
            >
              <TranslatableText
                text="What-If Scenario Simulator"
                as="h3"
                style={{ fontSize: '16px', fontWeight: '600', color: '#1E1E1E', marginBottom: '6px' }}
              />
              <TranslatableText
                text="Ask what would happen in different election situations"
                as="p"
                style={{ fontSize: '13px', color: '#5F6B7A', marginBottom: '20px' }}
              />

              <form onSubmit={handleScenario}>
                <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
                  <input
                    value={scenarioInput}
                    onChange={e => setScenarioInput(e.target.value)}
                    placeholder='e.g., "What if I miss voter registration deadline?"'
                    className="input-field"
                    style={{ fontSize: '14px' }}
                    disabled={scenarioLoading}
                  />
                  <button
                    type="submit"
                    disabled={!scenarioInput.trim() || scenarioLoading}
                    className="btn-primary"
                    style={{ height: '42px', width: '42px', padding: 0, flexShrink: 0 }}
                  >
                    {scenarioLoading ? (
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
                      <Send size={15} />
                    )}
                  </button>
                </div>
              </form>

              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {QUICK_SCENARIOS.map((s, i) => (
                  <button
                    key={i}
                    onClick={() => setScenarioInput(s)}
                    type="button"
                    style={{
                      padding: '6px 12px',
                      borderRadius: '8px',
                      border: '1px solid #E5EBF2',
                      background: '#F4F6F9',
                      color: '#5F6B7A',
                      fontSize: '12px',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                      fontFamily: 'inherit',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.background = '#EAF3FF'
                      e.currentTarget.style.borderColor = '#C7E0F4'
                      e.currentTarget.style.color = '#0176D3'
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.background = '#F4F6F9'
                      e.currentTarget.style.borderColor = '#E5EBF2'
                      e.currentTarget.style.color = '#5F6B7A'
                    }}
                  >
                    <TranslatableText text={s} />
                  </button>
                ))}
              </div>
            </div>

            {/* Scenario Result */}
            {scenarioResult && (
              <div
                className="animate-slide-up"
                style={{
                  background: '#FFFFFF',
                  border: '1px solid #E5EBF2',
                  borderRadius: '16px',
                  padding: '28px',
                  boxShadow: '0 4px 16px rgba(0,0,0,0.05)',
                }}
              >
                <TranslatableText
                  text={scenarioResult.scenario}
                  as="h3"
                  style={{ fontSize: '15px', fontWeight: '600', color: '#1E1E1E', marginBottom: '16px' }}
                />

                <div
                  style={{
                    padding: '14px 16px',
                    borderRadius: '10px',
                    background: '#FEF7E6',
                    border: '1px solid #F9E4A2',
                    marginBottom: '20px',
                  }}
                >
                  <TranslatableText
                    text="⚡ Immediate Impact"
                    as="p"
                    style={{ fontSize: '12px', fontWeight: '600', color: '#A07900', marginBottom: '4px' }}
                  />
                  <TranslatableText
                    text={scenarioResult.immediate_impact}
                    as="p"
                    style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.6' }}
                  />
                </div>

                <TranslatableText
                  text="Recovery Steps"
                  as="h4"
                  style={{ fontSize: '13px', fontWeight: '600', color: '#1E1E1E', marginBottom: '12px' }}
                />
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '20px' }}>
                  {scenarioResult.recovery_steps?.map((step, i) => (
                    <div
                      key={i}
                      style={{
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: '12px',
                        padding: '12px 14px',
                        borderRadius: '10px',
                        background: '#F4F8FF',
                        border: '1px solid #E5EBF2',
                      }}
                    >
                      <div
                        style={{
                          width: '24px',
                          height: '24px',
                          borderRadius: '6px',
                          background: '#EAF3FF',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexShrink: 0,
                          fontSize: '12px',
                          fontWeight: '700',
                          color: '#0176D3',
                        }}
                      >
                        {step.step}
                      </div>
                      <div>
                        <TranslatableText
                          text={step.action}
                          as="p"
                          style={{ fontSize: '13px', fontWeight: '500', color: '#1E1E1E', marginBottom: '3px' }}
                        />
                        <TranslatableText
                          text={`⏱ ${step.timeframe}`}
                          as="p"
                          style={{ fontSize: '12px', color: '#9BAFC4' }}
                        />
                      </div>
                    </div>
                  ))}
                </div>

                {scenarioResult.prevention_tips?.length > 0 && (
                  <div
                    style={{
                      padding: '16px',
                      borderRadius: '10px',
                      background: '#EEF6EC',
                      border: '1px solid #C8E6C2',
                    }}
                  >
                    <TranslatableText
                      text="Prevention Tips"
                      as="p"
                      style={{ fontSize: '13px', fontWeight: '600', color: '#2E844A', marginBottom: '8px' }}
                    />
                    {scenarioResult.prevention_tips.map((tip, i) => (
                      <TranslatableText
                        key={i}
                        text={`• ${tip}`}
                        as="p"
                        style={{ fontSize: '13px', color: '#5F6B7A', marginBottom: '4px' }}
                      />
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @media (max-width: 768px) {
          .mission-grid { grid-template-columns: 1fr !important; }
        }
        @media (max-width: 1024px) {
          .mission-grid { grid-template-columns: repeat(2, 1fr) !important; }
        }
      `}</style>
    </div>
  )
}

export default MissionMode