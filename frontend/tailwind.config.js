/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        expense: '#ef4444',
        income: '#22c55e',
      },
    },
  },
  plugins: [],
}
