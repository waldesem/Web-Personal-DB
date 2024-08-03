import pluginVue from 'eslint-plugin-vue'
export default [
  // add more generic rulesets here, such as:
  // js.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  ...pluginVue.configs['plugin-vue/recommended'],
  ...pluginVue.configs['plugin-vue/essential'],
  ...pluginVue.configs['plugin-vue/strongly-recommended'],
  {
    rules: {
      // override/add rules settings here, such as:
      // 'vue/no-unused-vars': 'error'
    }
  }
]