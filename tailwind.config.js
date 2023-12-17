/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      flexGrow: { 10:'10', 4:'4', 5:'5',
        2: '2'},
      fontFamily:{
        enfont:['Nunito'],farsi:['Vazirmatn']
      },
    },
  },
  plugins: [],
}

