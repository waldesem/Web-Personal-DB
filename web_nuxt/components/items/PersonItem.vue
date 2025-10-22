<script setup lang="ts">
import { useClipboard } from "@vueuse/core";
import type { Persons } from "@/types";

const props = defineProps<Persons>();

const { copy, copied } = useClipboard();
</script>

<template>
  <ElementsLabelValue label="Фамилия" :value="props.surname" />
  <ElementsLabelValue label="Имя" :value="props.firstname" />
  <ElementsLabelValue label="Отчество" :value="props.patronymic" />
  <ElementsLabelSlot v-if="props.birthday" label="Дата рождения">
    <NuxtTime :datetime="props.birthday" />
  </ElementsLabelSlot>
  <ElementsLabelValue label="Место рождения" :value="props.birthplace" />
  <ElementsLabelValue label="Гражданство" :value="props.citizenship" />
  <ElementsLabelSlot v-if="props.dual" label="Двойное гражданство">
    <UBadge variant="outline" color="error" :label="props.dual" />
  </ElementsLabelSlot>
  <ElementsLabelValue label="СНИЛС" :value="props.snils" />
  <ElementsLabelValue label="ИНН" :value="props.inn" />
  <ElementsLabelValue label="Семейное положение" :value="props.marital" />
  <ElementsLabelSlot v-if="props.created" label="Дата записи">
    <NuxtTime :datetime="props.created" />
  </ElementsLabelSlot>
  <ElementsLabelValue
    label="Дополнительная информация"
    :value="props.addition"
  />
  <ElementsLabelSlot v-if="props.destination" label="Материалы проверок">
    <UButton
      variant="outline"
      :color="!copied ? 'info' : 'success'"
      size="sm"
      :label="!copied ? 'Копировать ссылку' : 'Скопировано'"
      @click="copy(props.destination)"
    />
  </ElementsLabelSlot>
</template>
