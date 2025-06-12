<script setup lang="ts">
import type { Phone } from "@/types";

const props = defineProps<{ comments: PropType<Phone["comments"]> }>();

const comments = ref(props.comments as unknown as Phone["comments"]);
</script>

<template>
  <UFormField label="Комментарий" name="comments">
    <UTextarea
      v-model.lazy="comments"
      autoresize
      @input="comments = $event.target.value"
    />
  </UFormField>
</template>
