import { createContext, useContext, useState, useCallback } from 'react'
import { civicTwinAPI, journeyAPI, assessmentAPI, authAPI } from '../services/api'
import { getIdToken } from '../firebase'
import toast from 'react-hot-toast'

const CivicTwinContext = createContext(null)

export function CivicTwinProvider({ children }) {
  const [sessionId, setSessionId] = useState(
    () => localStorage.getItem('civic_session_id') || null
  )
  const [profile, setProfile] = useState(null)
  const [journey, setJourney] = useState(null)
  const [readinessScore, setReadinessScore] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [language, setLanguage] = useState(
    () => localStorage.getItem('civic_language') || 'en'
  )

  // Update language and persist
  const updateLanguage = useCallback((lang) => {
    setLanguage(lang)
    localStorage.setItem('civic_language', lang)
  }, [])

  // Create civic twin and link to authenticated user
  const createCivicTwin = useCallback(async (userInput, lang) => {
    setLoading(true)
    setError(null)
    try {
      const useLang = lang || language
      const response = await civicTwinAPI.create(userInput, useLang)
      const newSessionId = response.data.session_id
      const newProfile = response.data.profile

      setSessionId(newSessionId)
      setProfile(newProfile)
      localStorage.setItem('civic_session_id', newSessionId)

      // Link session to authenticated user if logged in
      try {
        const idToken = await getIdToken()
        if (idToken) {
          await authAPI.linkSession(newSessionId, idToken)
        }
      } catch (linkErr) {
        // Non-critical - session still works without linking
        console.warn('Could not link session to user:', linkErr)
      }

      toast.success('Your Civic Twin has been created!')
      return { success: true, sessionId: newSessionId, profile: newProfile }

    } catch (err) {
      setError(err.message)
      toast.error(err.message || 'Failed to create Civic Twin')
      return { success: false, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [language])

  // Load existing twin
  const loadCivicTwin = useCallback(async (sid) => {
    const id = sid || sessionId
    if (!id) return { success: false, error: 'No session ID' }

    setLoading(true)
    try {
      const response = await civicTwinAPI.get(id)
      setProfile(response.data.profile)
      setSessionId(id)
      localStorage.setItem('civic_session_id', id)
      return { success: true, profile: response.data.profile }
    } catch (err) {
      setError(err.message)
      return { success: false, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [sessionId])

  // Create journey
  const createJourney = useCallback(async () => {
    if (!sessionId) return { success: false, error: 'No session' }

    setLoading(true)
    try {
      const response = await journeyAPI.create(sessionId)
      setJourney(response.data.journey)
      toast.success('Your personalized journey is ready!')
      return { success: true, journey: response.data.journey }
    } catch (err) {
      toast.error(err.message || 'Failed to create journey')
      return { success: false, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [sessionId])

  // Load journey
  const loadJourney = useCallback(async () => {
    if (!sessionId) return

    try {
      const response = await journeyAPI.get(sessionId)
      setJourney(response.data.journey)
      return response.data.journey
    } catch (err) {
      return null
    }
  }, [sessionId])

  // Calculate readiness
  const calculateReadiness = useCallback(async () => {
    if (!sessionId) return { success: false }

    setLoading(true)
    try {
      const response = await assessmentAPI.calculateReadiness(sessionId)
      setReadinessScore(response.data.readiness_score)
      return { success: true, data: response.data }
    } catch (err) {
      toast.error(err.message || 'Assessment failed')
      return { success: false, error: err.message }
    } finally {
      setLoading(false)
    }
  }, [sessionId])

  // Clear session
  const clearSession = useCallback(() => {
    setSessionId(null)
    setProfile(null)
    setJourney(null)
    setReadinessScore(null)
    setError(null)
    localStorage.removeItem('civic_session_id')
  }, [])

  const value = {
    sessionId,
    profile,
    journey,
    readinessScore,
    loading,
    error,
    language,
    updateLanguage,
    createCivicTwin,
    loadCivicTwin,
    createJourney,
    loadJourney,
    calculateReadiness,
    clearSession,
    setProfile,
    setJourney,
    setReadinessScore,
  }

  return (
    <CivicTwinContext.Provider value={value}>
      {children}
    </CivicTwinContext.Provider>
  )
}

export function useCivicTwin() {
  const context = useContext(CivicTwinContext)
  if (!context) {
    throw new Error('useCivicTwin must be used within CivicTwinProvider')
  }
  return context
}

export default CivicTwinContext