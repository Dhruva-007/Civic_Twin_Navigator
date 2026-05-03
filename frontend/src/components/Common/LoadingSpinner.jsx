function LoadingSpinner({ message = 'Loading...', size = 'md' }) {
  const sizes = {
    sm: { outer: 24, border: 2 },
    md: { outer: 44, border: 3 },
    lg: { outer: 60, border: 4 },
  }
  const s = sizes[size] || sizes.md

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '80px 24px',
        gap: '16px',
      }}
    >
      <div style={{ position: 'relative', width: s.outer, height: s.outer }}>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            borderRadius: '50%',
            border: `${s.border}px solid #E5EBF2`,
          }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            borderRadius: '50%',
            border: `${s.border}px solid transparent`,
            borderTopColor: '#0176D3',
            animation: 'spin 0.8s linear infinite',
          }}
        />
      </div>
      {message && (
        <p style={{ color: '#9BAFC4', fontSize: '14px' }}>
          {message}
        </p>
      )}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  )
}

export default LoadingSpinner