const defaultTheme = require('tailwindcss/defaultTheme');
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
],
  theme: {
    extend: {
      fontFamily: {
        rubik: ['"Rubik"', ...defaultTheme.fontFamily.serif]
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ]
}

