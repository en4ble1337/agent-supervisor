/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class', // We use 'class' so we can force dark mode or rely on user preference, we'll just set it to 'class' and force it in HTML
  theme: {
    extend: {
      colors: {
        background: '#0d1117',
        surface: '#161b22',
        border: '#30363d',
        text: '#c9d1d9',
        muted: '#8b949e',
        accent: '#58a6ff',
        success: '#3fb950',
        error: '#f85149',
        warning: '#d29922'
      },
      fontFamily: {
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', "Liberation Mono", "Courier New", 'monospace'],
      },
    },
  },
  plugins: [],
}
