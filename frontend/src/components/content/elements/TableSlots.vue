<script setup lang="ts">
const props = defineProps({
  divClass: {
    type: String,
    default: "table-responsive",
  },
  tblClass: {
    type: String,
    default: "table align-middle",
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