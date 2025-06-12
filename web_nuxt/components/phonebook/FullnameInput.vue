<script setup lang="ts">
import type { Phone } from "@/types";

const props = defineProps<{ fullname: PropType<Phone["fullname"]> }>();

const fullname = ref(props.fullname as unknown as Phone["fullname"]);
</script>

<template>
  <UFormField label="Полное имя" name="fullname" required>
    <UInput
      v-model.lazy.trim="fullname"
      placeholder="Полное имя"
      maxlength="255"
      required
      @input="fullname = $event.target.value"
    />
  </UFormField>
</template>
