import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCivicTwin } from '../context/CivicTwinContext'
import Navbar from '../components/Common/Navbar'
import LoadingSpinner from '../components/Common/LoadingSpinner'
import ScoreCard from '../components/Common/ScoreCard'
import TranslatableText from '../components/Common/TranslatableText'
import { assessmentAPI } from '../services/api'
import {
  Award, RefreshCw, Shield, AlertTriangle,
  CheckCircle, TrendingUp, FileText,
  ExternalLink, Clock
} from 'lucide-react'
import toast from 'react-hot-toast'

function ReadinessReport() {
  const { sessionId, profile } = useCivicTwin()
  const navigate = useNavigate()

  const [readiness, setReadiness] = useState(null)
  const [predictions, setPredictions] = useState(null)
  const [proof, setProof] = useState(null)
  const [pageLoading, setPageLoading] = useState(true)
  const [proofLoading, setProofLoading] = useState(false)

  // Prevent double API calls from React StrictMode
  const hasFetched = useRef(false)

  useEffect(() => {
    if (!sessionId) { navigate('/'); return }
    if (hasFetched.current) return
    hasFetched.current = true
    loadReport()
  }, [sessionId])

  const loadReport = async () => {
    setPageLoading(true)
    try {
      const r = await assessmentAPI.calculateReadiness(sessionId)
      setReadiness(r.data.readiness_score)
      setPredictions(r.data.predictions)
    } catch {
      toast.error('Failed to load report')
    } finally {
      setPageLoading(false)
    }
  }

  const generateProof = async () => {
    setProofLoading(true)
    try {
      const r = await assessmentAPI.generateProof(sessionId)
      setProof(r.data.proof)
      toast.success('Proof of Readiness generated!')
    } catch (err) {
      toast.error(err.message || 'Failed to generate proof')
    } finally {
      setProofLoading(false)
    }
  }

  const getConfig = (score) => {
    if (score >= 80) return { color: '#2E844A', label: 'Excellent', bg: '#EEF6EC', border: '#C8E6C2' }
    if (score >= 60) return { color: '#0176D3', label: 'Good', bg: '#EAF3FF', border: '#C7E0F4' }
    if (score >= 40) return { color: '#A07900', label: 'Fair', bg: '#FEF7E6', border: '#F9E4A2' }
    return { color: '#C23934', label: 'Needs Work', bg: '#FEEFEC', border: '#F5BCB9' }
  }

  if (pageLoading) {
    return (
      <div style={{ background: '#F4F8FF', minHeight: '100vh' }}>
        <Navbar />
        <LoadingSpinner message="Generating your readiness report..." />
      </div>
    )
  }

  const score = readiness?.overall_score || 0
  const cfg = getConfig(score)

  return (
    <div style={{ background: '#F4F8FF', minHeight: '100vh' }}>
      <Navbar />

      <div className="container" style={{ paddingTop: '36px', paddingBottom: '48px' }}>

        {/* Header */}
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
              text="Readiness Report"
              as="h2"
              style={{ fontSize: '24px', fontWeight: '700', color: '#1E1E1E', marginBottom: '4px' }}
            />
            <TranslatableText
              text="Your comprehensive election preparation assessment"
              as="p"
              style={{ fontSize: '14px', color: '#5F6B7A' }}
            />
          </div>
          <button onClick={loadReport} className="btn-ghost btn-sm">
            <RefreshCw size={14} />
            <TranslatableText text="Refresh" />
          </button>
        </div>

        {/* Score Hero */}
        <div
          className="animate-scale-in"
          style={{
            background: '#FFFFFF',
            border: '1px solid #E5EBF2',
            borderRadius: '16px',
            padding: '40px',
            marginBottom: '24px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '40px', flexWrap: 'wrap' }}>

            {/* SVG Ring */}
            <div className="score-ring-container" style={{ flexShrink: 0 }}>
              <svg width="160" height="160" viewBox="0 0 160 160">
                <circle cx="80" cy="80" r="68" fill="none" stroke="#E5EBF2" strokeWidth="8" />
                <circle
                  cx="80" cy="80" r="68" fill="none"
                  stroke={cfg.color}
                  strokeWidth="8"
                  strokeLinecap="round"
                  strokeDasharray={`${score * 4.27} ${427 - score * 4.27}`}
                  strokeDashoffset="107"
                  style={{ transition: 'stroke-dasharray 1.2s cubic-bezier(0.4, 0, 0.2, 1)' }}
                />
              </svg>
              <div
                style={{
                  position: 'absolute',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                }}
              >
                <span style={{ fontSize: '36px', fontWeight: '800', color: cfg.color, lineHeight: 1 }}>
                  {score}
                </span>
                <TranslatableText
                  text="out of 100"
                  as="span"
                  style={{ fontSize: '12px', color: '#9BAFC4', marginTop: '2px' }}
                />
              </div>
            </div>

            {/* Info */}
            <div style={{ flex: 1, minWidth: '220px' }}>
              <span
                className="badge"
                style={{
                  background: cfg.bg,
                  color: cfg.color,
                  border: `1px solid ${cfg.border}`,
                  fontSize: '13px',
                  padding: '5px 14px',
                  marginBottom: '16px',
                  display: 'inline-flex',
                }}
              >
                <TranslatableText text={`${cfg.label} Readiness`} />
              </span>

              <TranslatableText
                text={readiness?.overall_status?.replace(/_/g, ' ') || 'Assessment Complete'}
                as="h2"
                style={{
                  fontSize: '20px',
                  fontWeight: '700',
                  color: '#1E1E1E',
                  marginBottom: '10px',
                  textTransform: 'capitalize',
                }}
              />

              <TranslatableText
                text="Your readiness is scored across 4 key dimensions. Focus on the areas marked for improvement to increase your score."
                as="p"
                style={{
                  fontSize: '14px',
                  color: '#5F6B7A',
                  lineHeight: '1.7',
                  marginBottom: '24px',
                  maxWidth: '380px',
                }}
              />

              <button
                onClick={generateProof}
                disabled={proofLoading}
                className="btn-primary"
                style={{ height: '44px', fontSize: '14px' }}
              >
                {proofLoading ? (
                  <>
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
                    <TranslatableText text="Generating..." />
                  </>
                ) : (
                  <>
                    <Award size={15} />
                    <TranslatableText text="Generate Proof of Readiness" />
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Two Column Layout */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 340px',
            gap: '24px',
            alignItems: 'start',
          }}
        >

          {/* Left Column */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

            {/* Score Breakdown */}
            <div
              style={{
                background: '#FFFFFF',
                border: '1px solid #E5EBF2',
                borderRadius: '14px',
                padding: '24px',
              }}
            >
              <TranslatableText
                text="Score Breakdown"
                as="h3"
                style={{ fontSize: '15px', fontWeight: '600', color: '#1E1E1E', marginBottom: '16px' }}
              />
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '14px' }}>
                {readiness?.scores && Object.entries(readiness.scores).map(([key, val]) => (
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

            {/* Priority Actions */}
            {readiness?.key_improvement_areas?.length > 0 && (
              <div
                style={{
                  background: '#FFFFFF',
                  border: '1px solid #E5EBF2',
                  borderRadius: '14px',
                  padding: '24px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
                  <AlertTriangle size={15} color="#A07900" />
                  <TranslatableText
                    text="Priority Actions"
                    as="h3"
                    style={{ fontSize: '15px', fontWeight: '600', color: '#1E1E1E' }}
                  />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {readiness.key_improvement_areas.map((area, i) => (
                    <div
                      key={i}
                      style={{
                        display: 'flex',
                        alignItems: 'flex-start',
                        gap: '12px',
                        padding: '12px 14px',
                        borderRadius: '10px',
                        background: '#FEF7E6',
                        border: '1px solid #F9E4A2',
                      }}
                    >
                      <div
                        style={{
                          width: '24px',
                          height: '24px',
                          borderRadius: '6px',
                          background: '#F9E4A2',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          flexShrink: 0,
                          fontSize: '12px',
                          fontWeight: '700',
                          color: '#A07900',
                        }}
                      >
                        {i + 1}
                      </div>
                      <TranslatableText
                        text={area}
                        as="p"
                        style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.6' }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* How to Improve */}
            {readiness?.improvement_tips?.length > 0 && (
              <div
                style={{
                  background: '#FFFFFF',
                  border: '1px solid #E5EBF2',
                  borderRadius: '14px',
                  padding: '24px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
                  <TrendingUp size={15} color="#0176D3" />
                  <TranslatableText
                    text="How to Improve"
                    as="h3"
                    style={{ fontSize: '15px', fontWeight: '600', color: '#1E1E1E' }}
                  />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {readiness.improvement_tips.map((tip, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
                      <CheckCircle size={15} color="#2E844A" style={{ flexShrink: 0, marginTop: '1px' }} />
                      <TranslatableText
                        text={tip}
                        as="p"
                        style={{ fontSize: '13px', color: '#5F6B7A', lineHeight: '1.6' }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right Column */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

            {/* Quick Wins */}
            {readiness?.quick_wins?.length > 0 && (
              <div
                style={{
                  background: '#EEF6EC',
                  border: '1px solid #C8E6C2',
                  borderRadius: '14px',
                  padding: '20px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
                  <CheckCircle size={15} color="#2E844A" />
                  <TranslatableText
                    text="What You Have Ready"
                    as="h3"
                    style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E' }}
                  />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {readiness.quick_wins.map((win, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#2E844A', flexShrink: 0 }} />
                      <TranslatableText
                        text={win}
                        as="p"
                        style={{ fontSize: '13px', color: '#5F6B7A' }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Risk Predictions */}
            {predictions?.risk_assessment?.risk_factors?.length > 0 && (
              <div
                style={{
                  background: '#FFFFFF',
                  border: '1px solid #E5EBF2',
                  borderRadius: '14px',
                  padding: '20px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <Shield size={15} color="#C23934" />
                  <TranslatableText
                    text="Risk Predictions"
                    as="h3"
                    style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E' }}
                  />
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {predictions.risk_assessment.risk_factors.map((risk, i) => (
                    <div
                      key={i}
                      style={{
                        background: '#F4F8FF',
                        border: '1px solid #E5EBF2',
                        borderRadius: '10px',
                        padding: '12px',
                      }}
                    >
                      <div
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'space-between',
                          marginBottom: '6px',
                        }}
                      >
                        <TranslatableText
                          text={risk.factor}
                          as="p"
                          style={{ fontSize: '12px', fontWeight: '600', color: '#1E1E1E' }}
                        />
                        <span className={`badge ${
                          risk.risk_level === 'high' ? 'badge-red' :
                          risk.risk_level === 'medium' ? 'badge-yellow' : 'badge-green'
                        }`}>
                          <TranslatableText text={risk.risk_level} />
                        </span>
                      </div>
                      <TranslatableText
                        text={risk.preventive_action}
                        as="p"
                        style={{ fontSize: '12px', color: '#9BAFC4', lineHeight: '1.5' }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Proof of Readiness */}
            {proof && (
              <div
                className="animate-scale-in"
                style={{
                  background: '#FFFFFF',
                  border: '1.5px solid #0176D3',
                  borderRadius: '14px',
                  padding: '20px',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
                  <FileText size={15} color="#0176D3" />
                  <TranslatableText
                    text="Proof of Readiness"
                    as="h3"
                    style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E' }}
                  />
                </div>

                <div
                  style={{
                    padding: '8px 12px',
                    borderRadius: '8px',
                    background: '#EAF3FF',
                    marginBottom: '14px',
                    fontFamily: 'monospace',
                    fontSize: '12px',
                    color: '#0176D3',
                    wordBreak: 'break-all',
                  }}
                >
                  {proof.certificate_id}
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '14px' }}>
                  {proof.verified_areas?.map((area, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <CheckCircle size={13} color="#2E844A" style={{ flexShrink: 0 }} />
                      <TranslatableText
                        text={area}
                        as="p"
                        style={{ fontSize: '12px', color: '#5F6B7A' }}
                      />
                    </div>
                  ))}
                  {proof.pending_actions?.map((action, i) => (
                    <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <AlertTriangle size={13} color="#A07900" style={{ flexShrink: 0 }} />
                      <TranslatableText
                        text={action}
                        as="p"
                        style={{ fontSize: '12px', color: '#5F6B7A' }}
                      />
                    </div>
                  ))}
                </div>

                <div
                  style={{
                    paddingTop: '12px',
                    borderTop: '1px solid #E5EBF2',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                    <Clock size={11} color="#9BAFC4" />
                    <span style={{ fontSize: '11px', color: '#9BAFC4' }}>
                      {proof.issued_at?.slice(0, 10)}
                    </span>
                  </div>
                  <div style={{ display: 'flex', gap: '10px' }}>
                    {proof.official_references?.map((ref, i) => (
                      <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <ExternalLink size={11} color="#0176D3" />
                        <span style={{ fontSize: '11px', color: '#0176D3', fontWeight: '500' }}>
                          {ref}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Official Resources */}
            <div
              style={{
                background: '#EAF3FF',
                border: '1px solid #C7E0F4',
                borderRadius: '14px',
                padding: '20px',
              }}
            >
              <TranslatableText
                text="Official Resources"
                as="h3"
                style={{ fontSize: '14px', fontWeight: '600', color: '#1E1E1E', marginBottom: '14px' }}
              />
              {[
                { label: 'Election Commission of India', url: 'https://eci.gov.in' },
                { label: 'Voter Registration Portal', url: 'https://voters.eci.gov.in' },
                { label: 'Voter Helpline: 1950', url: 'tel:1950' },
              ].map(({ label, url }, i) => (
                <a
                  key={i}
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '10px 0',
                    borderBottom: i < 2 ? '1px solid #C7E0F4' : 'none',
                    color: '#0176D3',
                    textDecoration: 'none',
                    fontSize: '13px',
                    fontWeight: '500',
                    transition: 'opacity 0.2s ease',
                  }}
                  onMouseEnter={e => e.currentTarget.style.opacity = '0.7'}
                  onMouseLeave={e => e.currentTarget.style.opacity = '1'}
                >
                  <TranslatableText text={label} />
                  <ExternalLink size={13} />
                </a>
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
        @media (max-width: 1024px) {
          .report-grid { grid-template-columns: 1fr !important; }
        }
        @media (max-width: 768px) {
          .score-grid { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  )
}

export default ReadinessReport