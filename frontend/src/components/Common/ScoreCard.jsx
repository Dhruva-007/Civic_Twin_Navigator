import TranslatableText from './TranslatableText'

function ScoreCard({ label, score, status, explanation }) {
  const getConfig = (s) => {
    switch (s) {
      case 'good':
        return { color: '#2E844A', bg: '#EEF6EC', border: '#C8E6C2' }
      case 'needs_attention':
        return { color: '#A07900', bg: '#FEF7E6', border: '#F9E4A2' }
      case 'needs_improvement':
        return { color: '#E07A00', bg: '#FEF7E6', border: '#F9E4A2' }
      case 'early_stage':
        return { color: '#5F6B7A', bg: '#F4F6F9', border: '#E5EBF2' }
      default:
        return { color: '#0176D3', bg: '#EAF3FF', border: '#C7E0F4' }
    }
  }

  const c = getConfig(status)

  return (
    <div
      style={{
        background: c.bg,
        border: `1px solid ${c.border}`,
        borderRadius: '12px',
        padding: '16px',
        transition: 'all 0.2s ease',
      }}
    >
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          marginBottom: '10px',
        }}
      >
        <TranslatableText
          text={label?.replace(/_/g, ' ') || ''}
          as="span"
          style={{
            fontSize: '13px',
            fontWeight: '500',
            color: '#1E1E1E',
            textTransform: 'capitalize',
          }}
        />
        <span
          style={{
            fontSize: '18px',
            fontWeight: '700',
            color: c.color,
            lineHeight: 1,
          }}
        >
          {score}%
        </span>
      </div>

      <div className="progress-bar" style={{ background: 'rgba(255,255,255,0.7)' }}>
        <div
          className="progress-fill"
          style={{
            width: `${score}%`,
            background: `linear-gradient(90deg, ${c.color}80, ${c.color})`,
          }}
        />
      </div>

      {explanation && (
        <TranslatableText
          text={explanation}
          as="p"
          style={{
            fontSize: '12px',
            color: '#5F6B7A',
            marginTop: '8px',
            lineHeight: '1.5',
          }}
        />
      )}
    </div>
  )
}

export default ScoreCard