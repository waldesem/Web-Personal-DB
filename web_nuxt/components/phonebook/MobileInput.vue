<script setup lang="ts">
import type { Phone } from "@/types";

const props = defineProps<{ mobile: PropType<Phone["mobile"]> }>();

const mobile = ref(props.mobile as unknown as Phone["mobile"]);
</script>

<template>
  <UFormField label="Мобильный номер" name="mobile">
    <UInput
      v-model.lazy.trim="mobile"
      placeholder="Мобильный номер"
      maxlength="255"
      @input="mobile = $event.target.value"
    />
  </UFormField>
</template>
