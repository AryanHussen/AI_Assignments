/** @type {import('tailwindcss').Config} */
// Provides IntelliSense/auto-completion for Tailwind configuration options
export default {
  // Specifies the paths to all of your template files
  // Tailwind will scan these files to generate the necessary CSS classes
  content: [
    "./index.html",                // Scans the main HTML file
    "./src/**/*.{js,ts,jsx,tsx}",  // Scans all JS, TS, and React files in the src folder
  ],
  
  // Used to customize the default design system (colors, fonts, spacing, etc.)
  theme: {
    // Allows you to add new styles without overriding the default Tailwind theme
    extend: {},
  },

  // Allows you to add third-party plugins (like forms or typography libraries)
  plugins: [],
}
