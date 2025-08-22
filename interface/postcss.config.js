module.exports = {
  plugins: {
    'tailwindcss/nesting': {}, // Enables nesting
    'postcss-import': {}, // For @import rules
    tailwindcss: {},
    autoprefixer: {}, // Adds vendor prefixes
    ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {}) // Minification
  }
}