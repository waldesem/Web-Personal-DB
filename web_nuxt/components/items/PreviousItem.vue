<script setup lang="ts">
import type { Previous } from "@/types";

const props = defineProps<Previous>()
</script>

<template>
  <ElementsLabelValue label="Фамилия" :value="props.surname" />
  <ElementsLabelValue label="Имя" :value="props.firstname" />
  <ElementsLabelValue label="Отчество" :value="props.patronymic" />
  <ElementsLabelValue label="Год изменения" :value="props.changed" />
  <ElementsLabelValue label="Причина" :value="props.reason" />
</template>
