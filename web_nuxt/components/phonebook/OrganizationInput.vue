<script setup lang="ts">
import type { Phone } from "@/types";

const props = defineProps({
  organization: {
    type: String as PropType<Phone["organization"]>,
    default: () => "",
  },
  items: {
    type: Array,
    default: () => [],
  },
});

const organization = ref(
  props.organization as unknown as Phone["organization"]
);
const items = ref(props.items as string[]);
</script>

<template>
  <UFormField label="Название организации" name="organization" required>
    <UInputMenu
      v-model="organization"
      create-item
      :items="items"
      class="w-48"
      placeholder="Название организации"
      maxlength="255"
      required
      @input="organization = $event.target.value"
    />
  </UFormField>
</template>
