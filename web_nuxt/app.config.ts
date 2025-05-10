export default defineAppConfig({
  ui: {
    fonts: false,
    colors: {
      primary: 'blue',
      neutral: 'zinc'
    },
    input: {
      slots: {
        root: 'w-full',
      },
    },
    textarea: {
      slots: {
        root: 'w-full',
      },
    },
  }
})