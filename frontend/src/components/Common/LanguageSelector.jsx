import { useState } from 'react'
import { Globe, ChevronDown, Check } from 'lucide-react'

const LANGUAGES = [
  { code: 'en', name: 'English', native: 'English' },
  { code: 'hi', name: 'Hindi', native: 'हिंदी' },
  { code: 'mr', name: 'Marathi', native: 'मराठी' },
  { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
  { code: 'te', name: 'Telugu', native: 'తెలుగు' },
  { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
  { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
  { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
  { code: 'bn', name: 'Bengali', native: 'বাংলা' },
  { code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ' },
]

function LanguageSelector({ selected = 'en', onChange }) {
  const [isOpen, setIsOpen] = useState(false)
  const selectedLang = LANGUAGES.find(l => l.code === selected) || LANGUAGES[0]

  return (
    <div style={{ position: 'relative' }} role="navigation" aria-label="Language selection">
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-label={`Select language, currently ${selectedLang.name}`}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '6px',
          padding: '6px 12px',
          borderRadius: '8px',
          border: '1.5px solid #E5EBF2',
          background: '#F4F6F9',
          color: '#5F6B7A',
          fontSize: '13px',
          fontWeight: '500',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
          whiteSpace: 'nowrap',
          height: '36px',
          fontFamily: 'inherit',
        }}
        onMouseEnter={e => {
          e.currentTarget.style.background = '#E5EBF2'
          e.currentTarget.style.color = '#1E1E1E'
        }}
        onMouseLeave={e => {
          e.currentTarget.style.background = '#F4F6F9'
          e.currentTarget.style.color = '#5F6B7A'
        }}
      >
        <Globe size={13} aria-hidden="true" />
        {selectedLang.native}
        <ChevronDown
          size={12}
          aria-hidden="true"
          style={{
            transform: isOpen ? 'rotate(180deg)' : 'rotate(0)',
            transition: 'transform 0.2s ease',
          }}
        />
      </button>

      {isOpen && (
        <>
          <div
            style={{ position: 'fixed', inset: 0, zIndex: 40 }}
            onClick={() => setIsOpen(false)}
            aria-hidden="true"
          />
          <div
            className="animate-scale-in"
            role="listbox"
            aria-label="Available languages"
            style={{
              position: 'absolute',
              right: 0,
              top: 'calc(100% + 6px)',
              width: '200px',
              background: '#FFFFFF',
              border: '1px solid #E5EBF2',
              borderRadius: '12px',
              boxShadow: '0 8px 28px rgba(0,0,0,0.10)',
              zIndex: 50,
              overflow: 'hidden',
              padding: '6px',
            }}
          >
            {LANGUAGES.map(lang => (
              <button
                key={lang.code}
                role="option"
                aria-selected={selected === lang.code}
                onClick={() => { onChange(lang.code); setIsOpen(false) }}
                style={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  border: 'none',
                  background: selected === lang.code ? '#EAF3FF' : 'transparent',
                  color: selected === lang.code ? '#0176D3' : '#5F6B7A',
                  fontSize: '13px',
                  fontWeight: '500',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.15s ease',
                  fontFamily: 'inherit',
                  marginBottom: '2px',
                }}
                onMouseEnter={e => {
                  if (selected !== lang.code) {
                    e.currentTarget.style.background = '#F4F6F9'
                    e.currentTarget.style.color = '#1E1E1E'
                  }
                }}
                onMouseLeave={e => {
                  if (selected !== lang.code) {
                    e.currentTarget.style.background = 'transparent'
                    e.currentTarget.style.color = '#5F6B7A'
                  }
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span>{lang.native}</span>
                  <span style={{ color: '#C9D5E3', fontSize: '11px' }}>
                    {lang.name}
                  </span>
                </div>
                {selected === lang.code && (
                  <Check size={13} style={{ color: '#0176D3' }} aria-hidden="true" />
                )}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

export default LanguageSelector