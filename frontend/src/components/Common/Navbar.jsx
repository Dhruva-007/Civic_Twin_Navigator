import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useCivicTwin } from '../../context/CivicTwinContext'
import { useAuth } from '../../context/AuthContext'
import LanguageSelector from './LanguageSelector'
import TranslatableText from './TranslatableText'
import CivicIcon from '../ui/CivicIcon'
import {
  Home, LayoutDashboard, Target, Award,
  LogOut, User, Menu, X
} from 'lucide-react'
import { useState } from 'react'

function Navbar() {
  const { sessionId, clearSession, language, updateLanguage } = useCivicTwin()
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const [mobileOpen, setMobileOpen] = useState(false)

  const navLinks = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { path: '/missions', label: 'Missions', icon: Target },
    { path: '/report', label: 'Report', icon: Award },
  ]

  const handleLogout = async () => {
    clearSession()
    await logout()
    navigate('/login')
    setMobileOpen(false)
  }

  const isActive = (path) => location.pathname === path

  const displayName = user?.displayName
    || user?.email?.split('@')[0]
    || 'User'

  const initials = user?.displayName
    ? user.displayName.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    : user?.email?.[0]?.toUpperCase() || 'U'

  return (
    <header className="navbar" role="banner">
      <div className="container">
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            height: '64px',
          }}
        >
          {/* Logo */}
          <Link
            to="/"
            onClick={() => setMobileOpen(false)}
            aria-label="Civic Twin Navigator - Go to home"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              textDecoration: 'none',
            }}
          >
            <div
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                background: 'linear-gradient(135deg, #0176D3, #0EA5E9)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0,
                transition: 'transform 0.2s ease',
              }}
              onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.05)'}
              onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
            >
              <CivicIcon size={16} color="#FFFFFF" />
            </div>
            <span
              style={{
                fontWeight: '700',
                fontSize: '15px',
                color: '#1E1E1E',
                whiteSpace: 'nowrap',
              }}
            >
              Civic Twin{' '}
              <span style={{ color: '#0176D3' }}>Navigator</span>
            </span>
          </Link>

          {/* Desktop Nav Links */}
          {user && (
            <nav
              aria-label="Main navigation"
              style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
              className="hidden-mobile"
            >
              {navLinks.map(({ path, label, icon: Icon }) => (
                <Link
                  key={path}
                  to={path}
                  aria-label={`Go to ${label}`}
                  aria-current={isActive(path) ? 'page' : undefined}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '8px 14px',
                    borderRadius: '8px',
                    fontSize: '14px',
                    fontWeight: '500',
                    textDecoration: 'none',
                    transition: 'all 0.2s ease',
                    color: isActive(path) ? '#0176D3' : '#5F6B7A',
                    background: isActive(path) ? '#EAF3FF' : 'transparent',
                    whiteSpace: 'nowrap',
                  }}
                  onMouseEnter={e => {
                    if (!isActive(path)) {
                      e.currentTarget.style.color = '#1E1E1E'
                      e.currentTarget.style.background = '#F4F6F9'
                    }
                  }}
                  onMouseLeave={e => {
                    if (!isActive(path)) {
                      e.currentTarget.style.color = '#5F6B7A'
                      e.currentTarget.style.background = 'transparent'
                    }
                  }}
                >
                  <Icon size={15} aria-hidden="true" />
                  <TranslatableText text={label} />
                </Link>
              ))}
            </nav>
          )}

          {/* Right Side */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div className="hidden-mobile">
              <LanguageSelector selected={language} onChange={updateLanguage} />
            </div>

            {user ? (
              <>
                {/* User Avatar + Name */}
                <div
                  className="hidden-mobile"
                  aria-label={`Signed in as ${displayName}`}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '5px 12px 5px 5px',
                    borderRadius: '10px',
                    background: '#F4F6F9',
                    border: '1px solid #E5EBF2',
                  }}
                >
                  {user.photoURL ? (
                    <img
                      src={user.photoURL}
                      alt={`${displayName}'s profile picture`}
                      style={{
                        width: '28px',
                        height: '28px',
                        borderRadius: '50%',
                        objectFit: 'cover',
                        flexShrink: 0,
                      }}
                    />
                  ) : (
                    <div
                      aria-hidden="true"
                      style={{
                        width: '28px',
                        height: '28px',
                        borderRadius: '50%',
                        background: 'linear-gradient(135deg, #0176D3, #0EA5E9)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '11px',
                        fontWeight: '700',
                        color: '#FFFFFF',
                        flexShrink: 0,
                      }}
                    >
                      {initials}
                    </div>
                  )}
                  <span
                    style={{
                      fontSize: '13px',
                      fontWeight: '500',
                      color: '#5F6B7A',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {displayName}
                  </span>
                </div>

                {/* Sign Out */}
                <button
                  onClick={handleLogout}
                  aria-label="Sign out of your account"
                  className="btn-ghost btn-sm hidden-mobile"
                  style={{ color: '#C23934', height: '36px' }}
                  onMouseEnter={e => {
                    e.currentTarget.style.background = '#FEEFEC'
                    e.currentTarget.style.color = '#C23934'
                    e.currentTarget.style.borderColor = '#F5BCB9'
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.background = 'transparent'
                    e.currentTarget.style.color = '#C23934'
                    e.currentTarget.style.borderColor = 'transparent'
                  }}
                >
                  <LogOut size={14} aria-hidden="true" />
                  <TranslatableText text="Sign Out" />
                </button>

                {/* Mobile Hamburger */}
                <button
                  onClick={() => setMobileOpen(!mobileOpen)}
                  aria-label={mobileOpen ? 'Close navigation menu' : 'Open navigation menu'}
                  aria-expanded={mobileOpen}
                  aria-controls="mobile-nav"
                  className="show-mobile"
                  style={{
                    display: 'none',
                    alignItems: 'center',
                    justifyContent: 'center',
                    width: '40px',
                    height: '40px',
                    borderRadius: '8px',
                    border: '1.5px solid #E5EBF2',
                    background: '#FFFFFF',
                    cursor: 'pointer',
                    color: '#5F6B7A',
                    transition: 'all 0.2s ease',
                    flexShrink: 0,
                  }}
                  onMouseEnter={e => {
                    e.currentTarget.style.background = '#F4F6F9'
                    e.currentTarget.style.borderColor = '#C9D5E3'
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.background = '#FFFFFF'
                    e.currentTarget.style.borderColor = '#E5EBF2'
                  }}
                >
                  {mobileOpen
                    ? <X size={18} aria-hidden="true" />
                    : <Menu size={18} aria-hidden="true" />
                  }
                </button>
              </>
            ) : (
              <div style={{ display: 'flex', gap: '8px' }}>
                <Link to="/login" aria-label="Sign in to your account">
                  <button className="btn-ghost btn-sm" style={{ height: '36px' }}>
                    Sign In
                  </button>
                </Link>
                <Link to="/signup" aria-label="Create a new account">
                  <button className="btn-primary btn-sm">
                    Get Started
                  </button>
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Nav Drawer */}
        {mobileOpen && user && (
          <div
            id="mobile-nav"
            className="animate-slide-up"
            role="navigation"
            aria-label="Mobile navigation"
            style={{
              borderTop: '1px solid #E5EBF2',
              paddingTop: '12px',
              paddingBottom: '16px',
            }}
          >
            {/* User info in mobile */}
            <div
              aria-label={`Signed in as ${displayName}`}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                padding: '10px 16px',
                marginBottom: '8px',
                borderRadius: '10px',
                background: '#F4F6F9',
              }}
            >
              {user.photoURL ? (
                <img
                  src={user.photoURL}
                  alt={`${displayName}'s profile picture`}
                  style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    objectFit: 'cover',
                  }}
                />
              ) : (
                <div
                  aria-hidden="true"
                  style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #0176D3, #0EA5E9)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '12px',
                    fontWeight: '700',
                    color: '#FFFFFF',
                  }}
                >
                  {initials}
                </div>
              )}
              <div>
                <p style={{ fontSize: '13px', fontWeight: '600', color: '#1E1E1E' }}>
                  {displayName}
                </p>
                <p style={{ fontSize: '11px', color: '#9BAFC4' }}>
                  {user.email}
                </p>
              </div>
            </div>

            {navLinks.map(({ path, label, icon: Icon }) => (
              <Link
                key={path}
                to={path}
                onClick={() => setMobileOpen(false)}
                aria-label={`Go to ${label}`}
                aria-current={isActive(path) ? 'page' : undefined}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '12px 16px',
                  borderRadius: '10px',
                  marginBottom: '4px',
                  fontSize: '14px',
                  fontWeight: '500',
                  textDecoration: 'none',
                  color: isActive(path) ? '#0176D3' : '#5F6B7A',
                  background: isActive(path) ? '#EAF3FF' : 'transparent',
                  transition: 'all 0.2s ease',
                }}
              >
                <Icon size={16} aria-hidden="true" />
                <TranslatableText text={label} />
              </Link>
            ))}

            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginTop: '12px',
                paddingTop: '12px',
                borderTop: '1px solid #F4F6F9',
              }}
            >
              <LanguageSelector selected={language} onChange={updateLanguage} />
              <button
                onClick={handleLogout}
                aria-label="Sign out of your account"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '8px 16px',
                  borderRadius: '8px',
                  border: 'none',
                  background: '#FEEFEC',
                  color: '#C23934',
                  fontSize: '14px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  fontFamily: 'inherit',
                }}
              >
                <LogOut size={15} aria-hidden="true" />
                <TranslatableText text="Sign Out" />
              </button>
            </div>
          </div>
        )}
      </div>

      <style>{`
        @media (max-width: 768px) {
          .hidden-mobile { display: none !important; }
          .show-mobile { display: flex !important; }
        }
        @media (min-width: 769px) {
          .show-mobile { display: none !important; }
          .hidden-mobile { display: flex !important; }
        }
      `}</style>
    </header>
  )
}

export default Navbar