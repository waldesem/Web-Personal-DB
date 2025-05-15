export default defineAppConfig({
  ui: {
    alert: {
      slots: {
        icon: "size-10",
      },
    },
    colors: {
      primary: "blue",
      neutral: "zinc",
    },
    formField: {
      slots: {
        root: "mb-3",
      },
    },
    input: {
      slots: {
        root: "w-full",
      },
    },
    modal: {
      slots: {
        content: "overflow-y-auto",
      },
    },
    textarea: {
      slots: {
        root: "w-full",
      },
    },
  },
});
