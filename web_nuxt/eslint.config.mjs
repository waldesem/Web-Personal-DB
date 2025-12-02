// @ts-check
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt({
  files: [
    "app.vue",
    "app/error.vue",
    "app/pages/**/*.vue",
    "app/layouts/**/*.vue",
  ],
  rules: {
    // disable the rule for these files
    "vue/multi-word-component-names": "off",
  },
});
