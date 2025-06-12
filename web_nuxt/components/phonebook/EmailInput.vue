<script setup lang="ts">
import type { Phone } from "@/types";

const props = defineProps<{ email: PropType<Phone["email"]> }>();

const email = ref(props.email as unknown as Phone["email"]);
</script>

<template>
  <UFormField label="Email" name="email" type="email">
    <UInput
      v-model.lazy.trim="email"
      placeholder="Email"
      maxlength="255"
      required
      type="email"
    />
  </UFormField>
</template>
