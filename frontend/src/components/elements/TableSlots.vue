<script setup lang="ts">
const props = defineProps({
  divClass: {
    type: String,
    default: "table-responsive mt-3",
  },
  tblClass: {
    type: String,
    default: "table align-middle",
  },
  tblCaption: {
    type: String,
    default: "",
  },
})
</script>

<template>
  <div :class="props.divClass">
    <table :class="props.tblClass">
      <caption>{{ props.tblClass }}</caption>
      <thead>
        <slot name="thead"></slot>
      </thead>
      <tbody>
        <slot name="tbody"></slot>
      </tbody>
    </table>
  </div>
</template>