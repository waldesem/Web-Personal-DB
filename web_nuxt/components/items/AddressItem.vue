<script setup lang="ts">
import type { Address } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    default: () => ({}),
  },
});
</script>

<template>
  <ElementsLabelValue label="Тип" :value="props.item.view" />
  <ElementsLabelSlot v-if="props.item.address" label="Адрес">
    {{ props.item.address }}
    <UButton
      :to="`https://yandex.ru/maps/?text=${props.item.address}%10с%10`"
      target="_blank"
      title="Показать на Яндекс.Карте"
      variant="outline"
      trailing-icon="i-lucide-map-pinned"
      class="ms-4"
    />
  </ElementsLabelSlot>
</template>
