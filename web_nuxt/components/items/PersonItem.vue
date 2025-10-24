<script setup lang="ts">
import { useClipboard } from "@vueuse/core";
import type { Persons } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Persons>,
    required: true,
  },
});

const { copy, copied } = useClipboard();
</script>

<template>
  <ElementsLabelValue label="Фамилия" :value="props.item.surname" />
  <ElementsLabelValue label="Имя" :value="props.item.firstname" />
  <ElementsLabelValue label="Отчество" :value="props.item.patronymic" />
  <ElementsLabelValue v-if="props.item.birthday" label="Дата рождения">
    <template #value>
      <NuxtTime :datetime="props.item.birthday" />
    </template>
  </ElementsLabelValue>
  <ElementsLabelValue
    label="Место рождения"
    :value="props.item.birthplace"
  />
  <ElementsLabelValue label="Гражданство" :value="props.item.citizenship" />
  <ElementsLabelValue v-if="props.item.dual" label="Двойное гражданство">
    <template #value>
      <UBadge variant="outline" color="error" :label="props.item.dual" />
    </template>
  </ElementsLabelValue>
  <ElementsLabelValue label="СНИЛС" :value="props.item.snils" />
  <ElementsLabelValue label="ИНН" :value="props.item.inn" />
  <ElementsLabelValue
    label="Семейное положение"
    :value="props.item.marital"
  />
  <ElementsLabelValue v-if="props.item.created" label="Дата записи">
    <template #value>
      <NuxtTime :datetime="props.item.created" />
    </template>
  </ElementsLabelValue>
  <ElementsLabelValue
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <ElementsLabelValue
    v-if="props.item.destination"
    label="Материалы проверок"
  >
    <template #value>
      <UButton
        variant="outline"
        :color="!copied ? 'info' : 'success'"
        size="sm"
        :label="!copied ? 'Копировать ссылку' : 'Скопировано'"
        @click="copy(props.item.destination)"
      />
    </template>
  </ElementsLabelValue>
</template>
