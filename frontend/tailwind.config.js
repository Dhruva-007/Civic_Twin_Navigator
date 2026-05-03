/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EAF3FF',
          100: '#C7E0F4',
          200: '#9DC6EE',
          300: '#6EA8E8',
          400: '#3D8FE0',
          500: '#0176D3',
          600: '#0161B5',
          700: '#014E96',
          800: '#013A76',
          900: '#012856',
        },
        neutral: {
          50: '#F4F6F9',
          100: '#E5EBF2',
          200: '#C9D5E3',
          300: '#9BAFC4',
          400: '#7A93AA',
          500: '#5F6B7A',
          600: '#4A5568',
          700: '#374151',
          800: '#1F2937',
          900: '#1E1E1E',
        },
        success: {
          light: '#EEF6EC',
          DEFAULT: '#2E844A',
          dark: '#1D5C32',
        },
        warning: {
          light: '#FEF7E6',
          DEFAULT: '#A07900',
          dark: '#7A5C00',
        },
        danger: {
          light: '#FEEFEC',
          DEFAULT: '#C23934',
          dark: '#8E2828',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'SF Pro Display', 'system-ui', 'sans-serif'],
      },
      fontSize: {
        'xs': ['12px', { lineHeight: '1.5' }],
        'sm': ['14px', { lineHeight: '1.6' }],
        'base': ['15px', { lineHeight: '1.7' }],
        'lg': ['17px', { lineHeight: '1.6' }],
        'xl': ['20px', { lineHeight: '1.5' }],
        '2xl': ['24px', { lineHeight: '1.4' }],
        '3xl': ['30px', { lineHeight: '1.3' }],
        '4xl': ['36px', { lineHeight: '1.2' }],
        '5xl': ['48px', { lineHeight: '1.1' }],
      },
      spacing: {
        '18': '4.5rem',
        '22': '5.5rem',
        '100': '25rem',
        '120': '30rem',
      },
      borderRadius: {
        'xl': '12px',
        '2xl': '16px',
        '3xl': '24px',
      },
      boxShadow: {
        'card': '0 2px 8px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.04)',
        'card-hover': '0 8px 32px rgba(0, 0, 0, 0.10), 0 2px 8px rgba(0, 0, 0, 0.06)',
        'blue': '0 4px 16px rgba(1, 118, 211, 0.24)',
        'input': '0 0 0 3px rgba(1, 118, 211, 0.12)',
        'nav': '0 1px 3px rgba(0, 0, 0, 0.08)',
        'dropdown': '0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.06)',
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease forwards',
        'slide-up': 'slideUp 0.4s ease forwards',
        'scale-in': 'scaleIn 0.3s ease forwards',
        'shimmer': 'shimmer 1.5s infinite',
        'spin-slow': 'spin 2s linear infinite',
      },
    },
  },
  plugins: [],
}