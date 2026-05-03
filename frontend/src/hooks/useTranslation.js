import { useState, useCallback, useRef } from 'react'
import { translationAPI } from '../services/api'

// Global cache shared across all components
const translationCache = {}
const pendingRequests = {}

function getCacheKey(text, lang) {
  if (!text) return ''
  return `${lang}:${text.substring(0, 100)}`
}

export function useTranslation(language = 'en') {
  const [translating, setTranslating] = useState(false)

  const translate = useCallback(async (text) => {
    // No translation needed
    if (!text || !text.trim()) return text
    if (language === 'en') return text
    if (!text || text.length < 1) return text

    const cacheKey = getCacheKey(text, language)

    // Return from cache if available
    if (translationCache[cacheKey]) {
      return translationCache[cacheKey]
    }

    // If same request is already pending, wait for it
    if (pendingRequests[cacheKey]) {
      try {
        return await pendingRequests[cacheKey]
      } catch {
        return text
      }
    }

    // Create new translation request
    const requestPromise = (async () => {
      try {
        setTranslating(true)
        const result = await translationAPI.translate(text, language, 'en')

        if (result?.data?.translated_text) {
          translationCache[cacheKey] = result.data.translated_text
          return result.data.translated_text
        }
        return text
      } catch (err) {
        // On rate limit or any error, return original text silently
        return text
      } finally {
        setTranslating(false)
        delete pendingRequests[cacheKey]
      }
    })()

    pendingRequests[cacheKey] = requestPromise
    return requestPromise

  }, [language])


  const translateBatch = useCallback(async (texts) => {
    if (!texts || texts.length === 0) return texts
    if (language === 'en') return texts

    // Check cache first
    const results = [...texts]
    const uncached = []
    const uncachedIndexes = []

    texts.forEach((text, i) => {
      if (!text) return
      const cacheKey = getCacheKey(text, language)
      if (translationCache[cacheKey]) {
        results[i] = translationCache[cacheKey]
      } else {
        uncached.push(text)
        uncachedIndexes.push(i)
      }
    })

    if (uncached.length === 0) return results

    try {
      setTranslating(true)
      const response = await translationAPI.translateBatch(uncached, language, 'en')

      if (response?.data?.translations) {
        response.data.translations.forEach((t, i) => {
          const originalIndex = uncachedIndexes[i]
          const translated = t.translated || t.original || uncached[i]
          results[originalIndex] = translated
          const cacheKey = getCacheKey(uncached[i], language)
          translationCache[cacheKey] = translated
        })
      }
      return results
    } catch {
      return results
    } finally {
      setTranslating(false)
    }
  }, [language])


  return { translate, translateBatch, translating }
}