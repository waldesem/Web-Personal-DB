<script setup lang="ts">
import type { Education } from "@/types";

const props = defineProps<Education>()
</script>

<template>
  <ElementsLabelValue label="Уровень образования" :value="props.view" />
  <ElementsLabelValue
    label="Учебное заведение"
    :value="props.institution"
  />
  <ElementsLabelValue label="Год окончания" :value="props.finished" />
  <ElementsLabelValue label="Специальность" :value="props.specialty" />
</template>
