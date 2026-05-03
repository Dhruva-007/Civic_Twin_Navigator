import { useState, useRef } from 'react'
import { Mic, MicOff, Loader } from 'lucide-react'
import toast from 'react-hot-toast'

function VoiceButton({ onTranscript, language = 'en' }) {
  const [isRecording, setIsRecording] = useState(false)
  const [loading, setLoading] = useState(false)
  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data)
      }
      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/mp3' })
        await processAudio(blob)
        stream.getTracks().forEach(t => t.stop())
      }
      mediaRecorder.start()
      setIsRecording(true)
      toast('🎙️ Recording... Click again to stop', {
        duration: 2000,
        style: { background: '#1E1E1E', color: '#FFFFFF', borderRadius: '8px' },
      })
    } catch {
      toast.error('Microphone access denied')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const processAudio = async (blob) => {
    setLoading(true)
    try {
      const reader = new FileReader()
      reader.onloadend = async () => {
        try {
          const base64 = reader.result.split(',')[1]
          const response = await fetch(
            `${import.meta.env.VITE_API_BASE_URL}/twin/speech-to-text`,
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ audio_base64: base64, language }),
            }
          )
          if (response.ok) {
            const data = await response.json()
            const transcript = data?.data?.transcript
            if (transcript?.trim() && onTranscript) {
              onTranscript(transcript)
              toast.success('Voice captured!')
            } else {
              toast('Could not understand. Please type instead.', {
                style: { background: '#1E1E1E', color: '#FFFFFF', borderRadius: '8px' },
              })
            }
          } else {
            toast('Type your message to continue.', {
              style: { background: '#1E1E1E', color: '#FFFFFF', borderRadius: '8px' },
            })
          }
        } catch {
          toast('Type your message to continue.', {
            style: { background: '#1E1E1E', color: '#FFFFFF', borderRadius: '8px' },
          })
        } finally {
          setLoading(false)
        }
      }
      reader.readAsDataURL(blob)
    } catch {
      toast.error('Voice processing failed')
      setLoading(false)
    }
  }

  return (
    <>
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        style={{
          position: 'absolute',
          width: '1px',
          height: '1px',
          padding: 0,
          margin: '-1px',
          overflow: 'hidden',
          clip: 'rect(0,0,0,0)',
          border: 0,
        }}
      >
        {isRecording ? 'Recording started. Click again to stop.' : ''}
        {loading ? 'Processing voice input.' : ''}
      </div>

      <button
        type="button"
        onClick={loading ? undefined : isRecording ? stopRecording : startRecording}
        disabled={loading}
        aria-label={isRecording ? 'Stop voice recording' : 'Start voice input'}
        role="button"
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '36px',
          height: '36px',
          borderRadius: '8px',
          border: `1.5px solid ${isRecording ? '#F5BCB9' : '#E5EBF2'}`,
          background: isRecording ? '#FEEFEC' : '#F4F6F9',
          cursor: loading ? 'not-allowed' : 'pointer',
          transition: 'all 0.2s ease',
          flexShrink: 0,
        }}
        onMouseEnter={e => {
          if (!loading && !isRecording) {
            e.currentTarget.style.background = '#EAF3FF'
            e.currentTarget.style.borderColor = '#C7E0F4'
          }
        }}
        onMouseLeave={e => {
          if (!isRecording) {
            e.currentTarget.style.background = '#F4F6F9'
            e.currentTarget.style.borderColor = '#E5EBF2'
          }
        }}
        title={isRecording ? 'Stop recording' : 'Voice input'}
      >
        {loading ? (
          <Loader
            size={14}
            style={{ color: '#0176D3', animation: 'spin 0.8s linear infinite' }}
            aria-hidden="true"
          />
        ) : isRecording ? (
          <MicOff size={14} style={{ color: '#C23934' }} aria-hidden="true" />
        ) : (
          <Mic size={14} style={{ color: '#5F6B7A' }} aria-hidden="true" />
        )}
        <style>{`
          @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
          }
        `}</style>
      </button>
    </>
  )
}

export default VoiceButton