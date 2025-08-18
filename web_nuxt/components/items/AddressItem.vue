<script setup lang="ts">
import type { Address } from "@/types";

const UButton = resolveComponent("UButton");

const props = defineProps({
  item: {
    type: Object as PropType<Address>,
    default: () => ({}),
  },
});

const address = {
  Тип: props.item.view,
  Адрес: h("div", [
    props.item.address,
    h(UButton, {
      to: `https://yandex.ru/maps/?text=${props.item.address}%10с%10`,
      target: "_blank",
      title: "Показать на Яндекс.Карте",
      variant: "outline",
      icon: "i-lucide-map-pinned",
      class: "ms-4"
    }),
  ]),
};
</script>

<template>
  <div v-for="(value, key) in address" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
