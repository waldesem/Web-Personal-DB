<script setup lang="ts">
import type { Staff } from "@/types";

const props = defineProps<Staff>()
</script>

<template>
  <ElementsLabelValue label="Должность" :value="props.position" />
  <ElementsLabelValue label="Департамент" :value="props.department" />
</template>
