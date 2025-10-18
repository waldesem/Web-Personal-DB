// @ts-check
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt(
  // Your custom configs here
  {
    files: ["app.vue", "error.vue", "pages/**/*.vue", "layouts/**/*.vue"],
    rules: {
      // disable the rule for these files
      "vue/multi-word-component-names": "off",
    },
  }
);
