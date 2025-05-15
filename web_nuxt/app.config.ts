export default defineAppConfig({
  ui: {
    colors: {
      primary: 'blue',
      neutral: 'zinc'
    },
    input: {
      slots: {
        root: 'w-full',
      },
    },
    modal: {
      content: 'overflow-y-auto'
    },
    textarea: {
      slots: {
        root: 'w-full',
      },
    },
  }
})