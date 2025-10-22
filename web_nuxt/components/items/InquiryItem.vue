<script setup lang="ts">
import type { Needs } from "@/types";

const props = defineProps<Needs>()
</script>

<template>
  <ElementsLabelValue label="Информация" :value="props.info" />
  <ElementsLabelValue label="Иннициатор" :value="props.initiator" />
  <ElementsLabelSlot v-if="props.created" label="Дата записи">
    <NuxtTime :datetime="props.created" />
  </ElementsLabelSlot>
</template>
