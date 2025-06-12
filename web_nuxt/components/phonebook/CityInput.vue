<script setup lang="ts">
import type { Phone } from "@/types";

const props = defineProps({
  city: {
    type: String as PropType<Phone["city"]>,
    default: () => "",
  },
  items: {
    type: Array,
    default: () => [],
  },
});

const city = ref(
  props.city as unknown as Phone["city"]
);
const items = ref(props.items as string[]);
</script>

<template>
  <UFormField label="city" name="city" required>
    <UInputMenu
      v-model="city"
      create-item
      :items="items"
      class="w-48"
      placeholder="city"
      maxlength="255"
      @input="city = $event.target.value"
    />
  </UFormField>
</template>
