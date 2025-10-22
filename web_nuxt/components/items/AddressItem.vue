<script setup lang="ts">
import type { Address } from "@/types";

const props = defineProps<Address>();
</script>

<template>
  <ElementsLabelValue label="Тип" :value="props.view" />
  <ElementsLabelSlot v-if="props.address" label="Адрес">
    {{ props.address }}
    <UButton
      :to="`https://yandex.ru/maps/?text=${props.address}%10с%10`"
      target="_blank"
      title="Показать на Яндекс.Карте"
      variant="outline"
      trailing-icon="i-lucide-map-pinned"
      class="ms-4"
    />
  </ElementsLabelSlot>
</template>
