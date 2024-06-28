<script setup lang="ts">
const props = defineProps({
  divClass: {
    type: String,
    default: "pt-3",
  },
  tblClass: {
    type: String,
    default: "table align-middle caption-top",
  },
})
</script>

<template>
  <div :class="props.divClass">
    <table :class="props.tblClass">
      <caption>
        <slot name="caption"></slot>
      </caption>
      <thead>
        <slot name="thead"></slot>
      </thead>
      <tbody>
        <slot name="tbody"></slot>
      </tbody>
    </table>
  </div>
</template>