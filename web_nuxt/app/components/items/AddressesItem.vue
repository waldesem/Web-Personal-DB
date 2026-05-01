<script setup lang="ts">
import type { Address } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue label="Тип" :value="props.item.view" />
  <ElementLabelSlot v-if="props.item.address" label="Адрес">
    <div class="space-x-4">
      {{ props.item.address }}
      <UButton
        :to="`https://yandex.ru/maps/?text=${props.item.address}%10с%10`"
        target="_blank"
        title="Показать на Яндекс.Карте"
        variant="outline"
        trailing-icon="i-lucide-map-pinned"
      />
    </div>
  </ElementLabelSlot>
</template>
