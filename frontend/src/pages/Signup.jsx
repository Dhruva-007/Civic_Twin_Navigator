import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Mail, Lock, Eye, EyeOff, User, ArrowRight } from 'lucide-react'
import CivicIcon from '../components/ui/CivicIcon'

function Signup() {
  const { signup, loginWithGoogle } = useAuth()
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [googleLoading, setGoogleLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSignup = async (e) => {
    e.preventDefault()
    if (!name.trim() || !email.trim() || !password.trim()) return

    if (password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters.')
      return
    }

    setError('')
    setLoading(true)
    const result = await signup(email, password, name)
    setLoading(false)

    if (result.success) {
      navigate('/')
    } else {
      setError(result.error || 'Signup failed')
    }
  }

  const handleGoogleSignup = async () => {
    setError('')
    setGoogleLoading(true)
    const result = await loginWithGoogle()
    setGoogleLoading(false)

    if (result.success) {
      navigate('/')
    } else if (result.error !== 'Popup closed') {
      setError(result.error || 'Google sign-in failed')
    }
  }

  const inputStyle = {
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
  }

  const handleFocus = (e) => {
    e.currentTarget.style.borderColor = '#0176D3'
    e.currentTarget.style.boxShadow = '0 0 0 3px rgba(1,118,211,0.1)'
  }

  const handleBlur = (e) => {
    e.currentTarget.style.borderColor = '#E5EBF2'
    e.currentTarget.style.boxShadow = 'none'
  }

  const isFormValid = name.trim() && email.trim() && password.trim() && confirmPassword.trim()

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
          <Link
            to="/"
            style={{
              textDecoration: 'none',
              display: 'inline-flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '12px',
            }}
          >
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

        {/* Card */}
        <div
          style={{
            background: '#FFFFFF',
            border: '1px solid #E5EBF2',
            borderRadius: '20px',
            padding: '36px',
            boxShadow: '0 8px 40px rgba(0,0,0,0.08)',
          }}
        >
          <h2 style={{ fontSize: '22px', fontWeight: '700', color: '#1E1E1E', marginBottom: '6px' }}>
            Create your account
          </h2>
          <p style={{ fontSize: '14px', color: '#5F6B7A', marginBottom: '28px' }}>
            Start your personalized election readiness journey
          </p>

          {/* Error */}
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

          {/* Google */}
          <button
            onClick={handleGoogleSignup}
            disabled={googleLoading || loading}
            style={{
              width: '100%',
              height: '46px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '10px',
              borderRadius: '10px',
              border: '1.5px solid #E5EBF2',
              background: '#FFFFFF',
              color: '#1E1E1E',
              fontSize: '14px',
              fontWeight: '600',
              cursor: googleLoading || loading ? 'not-allowed' : 'pointer',
              transition: 'all 0.2s ease',
              fontFamily: 'inherit',
              marginBottom: '20px',
              opacity: googleLoading || loading ? 0.7 : 1,
            }}
            onMouseEnter={e => {
              if (!googleLoading && !loading) {
                e.currentTarget.style.background = '#F4F6F9'
                e.currentTarget.style.borderColor = '#C9D5E3'
              }
            }}
            onMouseLeave={e => {
              e.currentTarget.style.background = '#FFFFFF'
              e.currentTarget.style.borderColor = '#E5EBF2'
            }}
          >
            {googleLoading ? (
              <div
                style={{
                  width: '18px',
                  height: '18px',
                  borderRadius: '50%',
                  border: '2px solid #E5EBF2',
                  borderTopColor: '#0176D3',
                  animation: 'spin 0.8s linear infinite',
                }}
              />
            ) : (
              <svg width="18" height="18" viewBox="0 0 48 48">
                <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
              </svg>
            )}
            Continue with Google
          </button>

          {/* Divider */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              marginBottom: '20px',
            }}
          >
            <div style={{ flex: 1, height: '1px', background: '#E5EBF2' }} />
            <span style={{ fontSize: '12px', color: '#9BAFC4', fontWeight: '500' }}>
              or continue with email
            </span>
            <div style={{ flex: 1, height: '1px', background: '#E5EBF2' }} />
          </div>

          {/* Form */}
          <form onSubmit={handleSignup}>

            {/* Name */}
            <div style={{ marginBottom: '14px' }}>
              <label style={{ fontSize: '13px', fontWeight: '600', color: '#1E1E1E', display: 'block', marginBottom: '6px' }}>
                Full name
              </label>
              <div style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }}>
                  <User size={15} color="#9BAFC4" />
                </div>
                <input
                  type="text"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  placeholder="Your full name"
                  required
                  disabled={loading || googleLoading}
                  style={inputStyle}
                  onFocus={handleFocus}
                  onBlur={handleBlur}
                />
              </div>
            </div>

            {/* Email */}
            <div style={{ marginBottom: '14px' }}>
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
                  disabled={loading || googleLoading}
                  style={inputStyle}
                  onFocus={handleFocus}
                  onBlur={handleBlur}
                />
              </div>
            </div>

            {/* Password */}
            <div style={{ marginBottom: '14px' }}>
              <label style={{ fontSize: '13px', fontWeight: '600', color: '#1E1E1E', display: 'block', marginBottom: '6px' }}>
                Password
              </label>
              <div style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }}>
                  <Lock size={15} color="#9BAFC4" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  placeholder="At least 6 characters"
                  required
                  disabled={loading || googleLoading}
                  style={{ ...inputStyle, paddingRight: '46px' }}
                  onFocus={handleFocus}
                  onBlur={handleBlur}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '14px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    padding: 0,
                    color: '#9BAFC4',
                    display: 'flex',
                    alignItems: 'center',
                  }}
                >
                  {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>

            {/* Confirm Password */}
            <div style={{ marginBottom: '24px' }}>
              <label style={{ fontSize: '13px', fontWeight: '600', color: '#1E1E1E', display: 'block', marginBottom: '6px' }}>
                Confirm password
              </label>
              <div style={{ position: 'relative' }}>
                <div style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }}>
                  <Lock size={15} color="#9BAFC4" />
                </div>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={e => setConfirmPassword(e.target.value)}
                  placeholder="Repeat your password"
                  required
                  disabled={loading || googleLoading}
                  style={{
                    ...inputStyle,
                    borderColor: confirmPassword && password !== confirmPassword ? '#C23934' : '#E5EBF2',
                  }}
                  onFocus={handleFocus}
                  onBlur={handleBlur}
                />
              </div>
              {confirmPassword && password !== confirmPassword && (
                <p style={{ fontSize: '12px', color: '#C23934', marginTop: '4px' }}>
                  Passwords do not match
                </p>
              )}
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading || googleLoading || !isFormValid}
              style={{
                width: '100%',
                height: '46px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                borderRadius: '10px',
                border: 'none',
                background: loading || !isFormValid ? '#C9D5E3' : '#0176D3',
                color: '#FFFFFF',
                fontSize: '15px',
                fontWeight: '600',
                cursor: loading || !isFormValid ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s ease',
                fontFamily: 'inherit',
              }}
              onMouseEnter={e => {
                if (!loading && isFormValid) {
                  e.currentTarget.style.background = '#0161B5'
                  e.currentTarget.style.boxShadow = '0 4px 14px rgba(1,118,211,0.3)'
                }
              }}
              onMouseLeave={e => {
                e.currentTarget.style.background = loading || !isFormValid ? '#C9D5E3' : '#0176D3'
                e.currentTarget.style.boxShadow = 'none'
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
                <>
                  Create Account
                  <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>

          {/* Login Link */}
          <p style={{ textAlign: 'center', marginTop: '24px', fontSize: '14px', color: '#5F6B7A' }}>
            Already have an account?{' '}
            <Link
              to="/login"
              style={{ color: '#0176D3', fontWeight: '600', textDecoration: 'none' }}
              onMouseEnter={e => e.currentTarget.style.textDecoration = 'underline'}
              onMouseLeave={e => e.currentTarget.style.textDecoration = 'none'}
            >
              Sign in
            </Link>
          </p>
        </div>

        <p style={{ textAlign: 'center', marginTop: '24px', fontSize: '12px', color: '#9BAFC4' }}>
          By creating an account, you agree to use this for election education only.
        </p>
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

export default Signup