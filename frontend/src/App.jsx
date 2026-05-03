import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { CivicTwinProvider } from './context/CivicTwinContext'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/Common/ProtectedRoute'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import MissionMode from './pages/MissionMode'
import ReadinessReport from './pages/ReadinessReport'
import Login from './pages/Login'
import Signup from './pages/Signup'
import ForgotPassword from './pages/ForgotPassword'

function App() {
  return (
    <AuthProvider>
      <CivicTwinProvider>
        <Router>
          <div style={{ minHeight: '100vh', background: '#FFFFFF' }}>

            {/* Skip to main content link for screen reader accessibility */}
            <a
              href="#main-content"
              aria-label="Skip to main content"
              style={{
                position: 'absolute',
                top: '-48px',
                left: '0',
                background: '#0176D3',
                color: '#FFFFFF',
                padding: '10px 20px',
                borderRadius: '0 0 8px 0',
                fontSize: '14px',
                fontWeight: '600',
                fontFamily: 'Inter, sans-serif',
                textDecoration: 'none',
                zIndex: 9999,
                transition: 'top 0.2s ease',
                outline: '2px solid transparent',
              }}
              onFocus={e => {
                e.currentTarget.style.top = '0'
                e.currentTarget.style.outline = '2px solid #FFFFFF'
              }}
              onBlur={e => {
                e.currentTarget.style.top = '-48px'
                e.currentTarget.style.outline = '2px solid transparent'
              }}
            >
              Skip to main content
            </a>

            {/* Toast notifications */}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 3000,
                style: {
                  background: '#1E1E1E',
                  color: '#FFFFFF',
                  borderRadius: '10px',
                  fontSize: '14px',
                  fontFamily: 'Inter, sans-serif',
                  boxShadow: '0 8px 32px rgba(0,0,0,0.2)',
                },
                success: {
                  iconTheme: { primary: '#2E844A', secondary: '#FFFFFF' },
                },
                error: {
                  iconTheme: { primary: '#C23934', secondary: '#FFFFFF' },
                },
              }}
            />

            {/* Main content landmark for accessibility */}
            <main id="main-content" role="main">
              <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/forgot-password" element={<ForgotPassword />} />

                {/* Protected Routes */}
                <Route
                  path="/"
                  element={
                    <ProtectedRoute>
                      <Home />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/missions"
                  element={
                    <ProtectedRoute>
                      <MissionMode />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/report"
                  element={
                    <ProtectedRoute>
                      <ReadinessReport />
                    </ProtectedRoute>
                  }
                />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
          </div>
        </Router>
      </CivicTwinProvider>
    </AuthProvider>
  )
}

export default App