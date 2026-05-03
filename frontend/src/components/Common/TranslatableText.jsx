import { useState, useEffect, useRef } from 'react'
import { useTranslation } from '../../hooks/useTranslation'
import { useCivicTwin } from '../../context/CivicTwinContext'

function TranslatableText({ text, as = 'span', style = {}, className = '', ...props }) {
  const { language } = useCivicTwin()
  const { translate } = useTranslation(language)
  const [displayText, setDisplayText] = useState(text || '')
  const prevLangRef = useRef(language)
  const prevTextRef = useRef(text)
  const timerRef = useRef(null)

  useEffect(() => {
    // Update immediately when text changes in English
    if (language === 'en') {
      setDisplayText(text || '')
      prevTextRef.current = text
      prevLangRef.current = language
      return
    }

    // Skip if nothing changed
    if (prevLangRef.current === language && prevTextRef.current === text) {
      return
    }

    prevLangRef.current = language
    prevTextRef.current = text

    if (!text) {
      setDisplayText('')
      return
    }

    // Clear any pending timer
    if (timerRef.current) {
      clearTimeout(timerRef.current)
    }

    let cancelled = false

    // Small random delay to stagger requests and avoid hitting rate limit
    const delay = Math.random() * 200

    timerRef.current = setTimeout(async () => {
      try {
        const result = await translate(text)
        if (!cancelled) {
          setDisplayText(result || text)
        }
      } catch {
        if (!cancelled) {
          setDisplayText(text)
        }
      }
    }, delay)

    return () => {
      cancelled = true
      if (timerRef.current) {
        clearTimeout(timerRef.current)
      }
    }
  }, [text, language, translate])

  // Keep display text in sync when text prop changes and language is English
  useEffect(() => {
    if (language === 'en') {
      setDisplayText(text || '')
    }
  }, [text, language])

  const Tag = as

  return (
    <Tag style={style} className={className} {...props}>
      {displayText || text || ''}
    </Tag>
  )
}

export default TranslatableText