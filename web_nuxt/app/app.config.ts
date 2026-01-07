export default defineAppConfig({
  ui: {
    alert: {
      slots: {
        icon: "size-10",
      },
    },
    colors: {
      primary: "blue",
      neutral: "gray",
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
        header: "p-3",
        content: "sm:max-w-xl",
      },
    },
    textarea: {
      slots: {
        root: "w-full",
      },
    },
  },
});
