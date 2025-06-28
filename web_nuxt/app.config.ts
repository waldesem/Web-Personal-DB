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
        // content: "overflow-y-auto sm:max-w-4xl",
        header: "p-3",
      },
    },
    textarea: {
      slots: {
        root: "w-full",
      },
    },
  },
});
