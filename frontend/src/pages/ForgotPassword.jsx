import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Mail, ArrowLeft, CheckCircle } from 'lucide-react'
import CivicIcon from '../components/ui/CivicIcon'

function ForgotPassword() {
  const { forgotPassword } = useAuth()
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [sent, setSent] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email.trim()) return

    setError('')
    setLoading(true)
    const result = await forgotPassword(email)
    setLoading(false)

    if (result.success) {
      setSent(true)
    } else {
      setError(result.error || 'Failed to send reset email')
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(180deg, #EAF3FF 0%, #FFFFFF 60%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '24px',
      }}
    >
      <div style={{ width: '100%', maxWidth: '420px' }}>

        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: '32px' }}>
          <Link to="/" style={{ textDecoration: 'none', display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
            <div
              style={{
                width: '52px',
                height: '52px',
                borderRadius: '14px',
                background: 'linear-gradient(135deg, #0176D3, #0EA5E9)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                boxShadow: '0 8px 24px rgba(1,118,211,0.25)',
              }}
            >
              <CivicIcon size={24} color="#FFFFFF" />
            </div>
            <span style={{ fontSize: '18px', fontWeight: '700', color: '#1E1E1E' }}>
              Civic Twin <span style={{ color: '#0176D3' }}>Navigator</span>
            </span>
          </Link>
        </div>

        <div
          style={{
            background: '#FFFFFF',
            border: '1px solid #E5EBF2',
            borderRadius: '20px',
            padding: '36px',
            boxShadow: '0 8px 40px rgba(0,0,0,0.08)',
          }}
        >
          {!sent ? (
            <>
              <h2 style={{ fontSize: '22px', fontWeight: '700', color: '#1E1E1E', marginBottom: '6px' }}>
                Reset your password
              </h2>
              <p style={{ fontSize: '14px', color: '#5F6B7A', marginBottom: '28px' }}>
                Enter your email and we will send you a reset link
              </p>

              {error && (
                <div
                  style={{
                    padding: '12px 16px',
                    borderRadius: '10px',
                    background: '#FEEFEC',
                    border: '1px solid #F5BCB9',
                    marginBottom: '20px',
                  }}
                >
                  <p style={{ fontSize: '13px', color: '#C23934' }}>{error}</p>
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '24px' }}>
                  <label style={{ fontSize: '13px', fontWeight: '600', color: '#1E1E1E', display: 'block', marginBottom: '6px' }}>
                    Email address
                  </label>
                  <div style={{ position: 'relative' }}>
                    <div style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }}>
                      <Mail size={15} color="#9BAFC4" />
                    </div>
                    <input
                      type="email"
                      value={email}
                      onChange={e => setEmail(e.target.value)}
                      placeholder="you@example.com"
                      required
                      disabled={loading}
                      style={{
                        width: '100%',
                        height: '46px',
                        paddingLeft: '42px',
                        paddingRight: '16px',
                        borderRadius: '10px',
                        border: '1.5px solid #E5EBF2',
                        background: '#FFFFFF',
                        fontSize: '14px',
                        fontFamily: 'inherit',
                        color: '#1E1E1E',
                        outline: 'none',
                        transition: 'all 0.2s ease',
                        boxSizing: 'border-box',
                      }}
                      onFocus={e => {
                        e.currentTarget.style.borderColor = '#0176D3'
                        e.currentTarget.style.boxShadow = '0 0 0 3px rgba(1,118,211,0.1)'
                      }}
                      onBlur={e => {
                        e.currentTarget.style.borderColor = '#E5EBF2'
                        e.currentTarget.style.boxShadow = 'none'
                      }}
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading || !email.trim()}
                  style={{
                    width: '100%',
                    height: '46px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px',
                    borderRadius: '10px',
                    border: 'none',
                    background: loading || !email.trim() ? '#C9D5E3' : '#0176D3',
                    color: '#FFFFFF',
                    fontSize: '15px',
                    fontWeight: '600',
                    cursor: loading || !email.trim() ? 'not-allowed' : 'pointer',
                    transition: 'all 0.2s ease',
                    fontFamily: 'inherit',
                    marginBottom: '20px',
                  }}
                >
                  {loading ? (
                    <div
                      style={{
                        width: '18px',
                        height: '18px',
                        borderRadius: '50%',
                        border: '2px solid rgba(255,255,255,0.3)',
                        borderTopColor: '#FFFFFF',
                        animation: 'spin 0.8s linear infinite',
                      }}
                    />
                  ) : (
                    'Send Reset Link'
                  )}
                </button>
              </form>

              <Link
                to="/login"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '6px',
                  fontSize: '14px',
                  color: '#5F6B7A',
                  fontWeight: '500',
                  textDecoration: 'none',
                }}
                onMouseEnter={e => e.currentTarget.style.color = '#0176D3'}
                onMouseLeave={e => e.currentTarget.style.color = '#5F6B7A'}
              >
                <ArrowLeft size={15} />
                Back to Sign In
              </Link>
            </>
          ) : (
            <div style={{ textAlign: 'center' }}>
              <div
                style={{
                  width: '56px',
                  height: '56px',
                  borderRadius: '14px',
                  background: '#EEF6EC',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 20px',
                }}
              >
                <CheckCircle size={26} color="#2E844A" />
              </div>
              <h2 style={{ fontSize: '20px', fontWeight: '700', color: '#1E1E1E', marginBottom: '8px' }}>
                Check your email
              </h2>
              <p style={{ fontSize: '14px', color: '#5F6B7A', marginBottom: '24px', lineHeight: '1.6' }}>
                We sent a password reset link to<br />
                <strong style={{ color: '#1E1E1E' }}>{email}</strong>
              </p>
              <Link
                to="/login"
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '6px',
                  fontSize: '14px',
                  color: '#0176D3',
                  fontWeight: '600',
                  textDecoration: 'none',
                }}
              >
                <ArrowLeft size={15} />
                Back to Sign In
              </Link>
            </div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

export default ForgotPassword