<script setup lang="ts">
import type { Inquisition } from "@/types";

const props = defineProps<Inquisition>()
</script>

<template>
  <ElementsLabelValue label="Тема проверки" :value="props.theme" />
  <ElementsLabelValue label="Информация" :value="props.info" />
  <ElementsLabelSlot v-if="props.created" label="Дата записи">
    <NuxtTime :datetime="props.created" />
  </ElementsLabelSlot>
</template>
