/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        purple: {
          600: '#7c3aed', // Primary brand color
          700: '#6d28d9', // Darker shade for hover states
        },
        gray: {
          800: '#1f2937', // Dark backgrounds
          700: '#374151', // Borders
          600: '#4b5563', // Scrollbar
          400: '#9ca3af', // Secondary text
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms')({
      strategy: 'class', // Only generate classes
    }),
  ],
}