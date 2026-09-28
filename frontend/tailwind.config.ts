import type { Config } from 'tailwindcss'

export default {
  theme: {
    extend: {
      colors: {
        cream: '#FBFBF9',
        sand: '#F4EFE8',
        mist: '#F3F5F3',
        blush: '#FBF6EF',
        fog: '#F2F4F2',
        forest: {
          DEFAULT: '#0A3D36',
          deep: '#072E29',
          soft: '#E7F2EE'
        },
        ink: '#16332E',
        mute: '#6E7A76',
        gold: '#E6A11A',
        sun: '#F5C518'
      },
      fontFamily: {
        sans: ['Outfit', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Fraunces', 'Georgia', 'ui-serif', 'serif']
      },
      boxShadow: {
        card: '0 18px 40px -28px rgba(10, 61, 54, 0.45)'
      }
    }
  }
} satisfies Config
