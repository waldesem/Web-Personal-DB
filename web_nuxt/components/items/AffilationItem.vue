<script setup lang="ts">
import type { Affilation } from '@/types';

const props = defineProps<Affilation>()
</script>

<template>
  <ElementsLabelValue label="Тип участия" :value="props.view" />
  <ElementsLabelValue label="Организация" :value="props.organization" />
  <ElementsLabelValue label="ИНН" :value="props.inn" />
</template>
