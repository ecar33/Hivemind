/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './hivemind/templates/**/*.html', // Matches all HTML files in templates and subdirectories
    './hivemind/static/js/**/*.js',   // Matches all JS files in static/js and subdirectories
  ],
  theme: {
    extend: {}, // Add any customizations here
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui : {
    themes: ['retro', 'cyberpunk', 'wireframe', 'dark']
  },

};

