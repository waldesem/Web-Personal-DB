<script setup lang="ts">
import type { Passport } from "@/types";

const props = defineProps<Passport>()
</script>

<template>
  <ElementsLabelValue label="Вид документа" :value="props.view" />
  <ElementsLabelValue label="Серия документа" :value="props.series" />
  <ElementsLabelValue label="Номер документа" :value="props.digits" />
  <ElementsLabelSlot v-if="props.issue" label="Дата выдачи">
    <NuxtTime :datetime="props.issue" />
  </ElementsLabelSlot>
  <ElementsLabelValue label="Кем выдан" :value="props.agency" />
</template>
