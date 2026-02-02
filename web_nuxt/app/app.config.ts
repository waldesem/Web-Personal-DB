export default defineAppConfig({
  ui: {
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
    pageHeader: {
      slots: {
        root: "relative border-none py-4",
        title: "text-2xl sm:text-3xl",
      },
    },
    textarea: {
      slots: {
        root: "w-full",
      },
    },
  },
});
