<script setup lang="ts">
import type { Phone } from "@/types";

const props = defineProps<{ phone: PropType<Phone["phone"]> }>();

const phone = ref(props.phone as unknown as Phone["phone"]);
</script>

<template>
  <UFormField label="Телефон" name="phone">
    <UInput
      v-model.lazy.trim="phone"
      placeholder="Телефон"
      maxlength="255"
      @input="phone = $event.target.value"
    />
  </UFormField>
</template>
