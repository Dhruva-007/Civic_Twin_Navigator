export default function CivicIcon({
  size = 24,
  color = '#FFFFFF',
  style = {},
  className = '',
}) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="22 18 56 66"
      xmlns="http://www.w3.org/2000/svg"
      style={style}
      className={className}
      aria-hidden="true"
    >
      {/* Fingerprint */}
      <ellipse
        cx="50" cy="51" rx="8" ry="10"
        fill="none" stroke={color} strokeWidth="2.8" opacity="0.95"
      />
      <ellipse
        cx="50" cy="51" rx="14" ry="17"
        fill="none" stroke={color} strokeWidth="2.4" opacity="0.86"
      />
      <ellipse
        cx="50" cy="51" rx="20" ry="24"
        fill="none" stroke={color} strokeWidth="2.1" opacity="0.72"
      />
      <ellipse
        cx="50" cy="51" rx="26" ry="31"
        fill="none" stroke={color} strokeWidth="1.8" opacity="0.52"
      />

      {/* Ink mark dot */}
      <circle cx="50" cy="23" r="4.2" fill="#5B21B6" opacity="0.98" />

      {/* Tricolor accent */}
      <rect x="31" y="77" width="12.5" height="4" rx="2" fill="#FF9933" />
      <rect x="43.75" y="77" width="12.5" height="4" rx="2" fill="white" />
      <rect x="56.5" y="77" width="12.5" height="4" rx="2" fill="#138808" />
    </svg>
  )
}