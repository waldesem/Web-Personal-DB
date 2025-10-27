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
  <ElementsLabelValue label="Дата рождения">
    <NuxtTime :datetime="props.item.birthday" />
  </ElementsLabelValue>
  <ElementsLabelValue label="Место рождения" :value="props.item.birthplace" />
  <ElementsLabelValue label="Гражданство" :value="props.item.citizenship" />
  <ElementsLabelValue label="Двойное гражданство">
    <UBadge variant="outline" color="info" :label="props.item.dual" />
  </ElementsLabelValue>
  <ElementsLabelValue label="СНИЛС" :value="props.item.snils" />
  <ElementsLabelValue label="ИНН" :value="props.item.inn" />
  <ElementsLabelValue label="Семейное положение" :value="props.item.marital" />
  <ElementsLabelValue label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementsLabelValue>
  <ElementsLabelValue
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <ElementsLabelValue label="Материалы проверок">
    <UButton
      variant="outline"
      :color="!copied ? 'info' : 'success'"
      size="sm"
      :label="!copied ? 'Копировать ссылку' : 'Скопировано'"
      @click="copy(props.item.destination)"
    />
  </ElementsLabelValue>
</template>
