import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import {
  signUpWithEmail,
  signInWithEmail,
  signInWithGoogle,
  logOut,
  resetPassword,
  onAuthChange,
  getIdToken,
} from '../firebase'
import { authAPI } from '../services/api'
import toast from 'react-hot-toast'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [authLoading, setAuthLoading] = useState(true)
  const [authError, setAuthError] = useState(null)

  useEffect(() => {
    // Safety timeout - if Firebase does not respond in 5s stop loading
    const timeout = setTimeout(() => {
      console.warn('Firebase auth timeout - proceeding without auth')
      setAuthLoading(false)
    }, 5000)

    let unsubscribe = () => {}

    try {
      unsubscribe = onAuthChange(async (firebaseUser) => {
        clearTimeout(timeout)
        setUser(firebaseUser)
        setAuthLoading(false)

        // Verify with backend when user logs in
        if (firebaseUser) {
          try {
            const token = await firebaseUser.getIdToken()
            await authAPI.verifyToken(token)
          } catch (err) {
            // Non-critical - frontend auth still works
            console.warn('Backend verification warning:', err.message)
          }
        }
      })
    } catch (err) {
      console.error('Firebase auth error:', err)
      clearTimeout(timeout)
      setAuthLoading(false)
    }

    return () => {
      clearTimeout(timeout)
      unsubscribe()
    }
  }, [])

  // Sign up with email
  const signup = useCallback(async (email, password, displayName) => {
    setAuthError(null)
    try {
      const result = await signUpWithEmail(email, password, displayName)
      toast.success(`Welcome, ${displayName || email}!`)
      return { success: true, user: result.user }
    } catch (err) {
      const message = getErrorMessage(err.code)
      setAuthError(message)
      toast.error(message)
      return { success: false, error: message }
    }
  }, [])

  // Sign in with email
  const login = useCallback(async (email, password) => {
    setAuthError(null)
    try {
      const result = await signInWithEmail(email, password)
      toast.success('Welcome back!')
      return { success: true, user: result.user }
    } catch (err) {
      const message = getErrorMessage(err.code)
      setAuthError(message)
      toast.error(message)
      return { success: false, error: message }
    }
  }, [])

  // Sign in with Google
  const loginWithGoogle = useCallback(async () => {
    setAuthError(null)
    try {
      const result = await signInWithGoogle()
      const isNew = result._tokenResponse?.isNewUser
      toast.success(isNew
        ? `Welcome, ${result.user.displayName}!`
        : `Welcome back, ${result.user.displayName}!`
      )
      return { success: true, user: result.user }
    } catch (err) {
      if (err.code === 'auth/popup-closed-by-user') {
        return { success: false, error: 'Popup closed' }
      }
      const message = getErrorMessage(err.code)
      setAuthError(message)
      toast.error(message)
      return { success: false, error: message }
    }
  }, [])

  // Logout
  const logout = useCallback(async () => {
    try {
      // Notify backend about logout
      if (user) {
        try {
          await authAPI.logout(user.uid)
        } catch (err) {
          console.warn('Backend logout warning:', err.message)
        }
      }
      await logOut()
      toast.success('Signed out successfully')
      return { success: true }
    } catch (err) {
      toast.error('Logout failed')
      return { success: false }
    }
  }, [user])

  // Reset password
  const forgotPassword = useCallback(async (email) => {
    try {
      await resetPassword(email)
      toast.success('Password reset email sent!')
      return { success: true }
    } catch (err) {
      const message = getErrorMessage(err.code)
      toast.error(message)
      return { success: false, error: message }
    }
  }, [])

  // Get current ID token for backend calls
  const getToken = useCallback(async () => {
    return await getIdToken()
  }, [])

  const value = {
    user,
    authLoading,
    authError,
    signup,
    login,
    loginWithGoogle,
    logout,
    forgotPassword,
    getToken,
    isAuthenticated: !!user,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

function getErrorMessage(code) {
  const errors = {
    'auth/email-already-in-use': 'This email is already registered.',
    'auth/invalid-email': 'Please enter a valid email address.',
    'auth/operation-not-allowed': 'Email/password login is not enabled.',
    'auth/weak-password': 'Password must be at least 6 characters.',
    'auth/user-disabled': 'This account has been disabled.',
    'auth/user-not-found': 'No account found with this email.',
    'auth/wrong-password': 'Incorrect password. Please try again.',
    'auth/invalid-credential': 'Invalid email or password.',
    'auth/too-many-requests': 'Too many attempts. Please try again later.',
    'auth/network-request-failed': 'Network error. Check your connection.',
    'auth/popup-blocked': 'Popup blocked. Please allow popups for this site.',
    'auth/cancelled-popup-request': 'Sign-in cancelled.',
    'auth/account-exists-with-different-credential': 'Account exists with different login method.',
  }
  return errors[code] || 'Something went wrong. Please try again.'
}

export default AuthContext