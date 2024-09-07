/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'selector',
  content: [
    "./**/*.py",
  ],
  theme: {
    extend: {
      screens: {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
      },
    },
  },
  plugins: [],
  extract: {
    python: (content) => {
      return content.match(/cls\s*=\s*f?["'](?:\{[^}]+\}|[^"'{}])*["']/g) || [];
    }
  }
}

