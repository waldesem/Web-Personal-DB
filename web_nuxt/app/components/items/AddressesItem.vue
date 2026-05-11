<script setup lang="ts">
import type { Address, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Тип" },
  { key: "address", label: "Адрес", slot: true },
] as ItemField[];
</script>

<template>
  <ElementItemCard :fields="fields" :item="props.item">
    <template #address>
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
    </template>
  </ElementItemCard>
</template>
