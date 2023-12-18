/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      flexGrow: {
        10: '10',
        4: '4',
        5: '5',
        2: '2'
      },
      fontFamily: {
        enfont: ['Nunito'],
        farsi: ['Vazirmatn']
      },
      colors: {
        cafe: {
          black: '#0b0c10',
          blue: '#45a29e',
          cyan: '#66fcf1',
          lime: '#49c5b6',
          gray: '#1f2833',
          white: '#c5c6c7',
        },
      },
    },
  },
  plugins: [],
};
