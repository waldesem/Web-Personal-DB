<script setup lang="ts">
import { useClipboard } from "@vueuse/core";
import type { Person } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Person>,
    default: () => {},
  },
});

const { copy, copied } = useClipboard();
</script>

<template>
  <ElementLabelValue label="Фамилия" :value="props.item.surname" />
  <ElementLabelValue label="Имя" :value="props.item.firstname" />
  <ElementLabelValue label="Отчество" :value="props.item.patronymic" />
  <ElementLabelValue
    label="Дата рождения"
    :value="new Date(props.item.birthday).toLocaleDateString()"
  />
  <ElementLabelValue label="Место рождения" :value="props.item.birthplace" />
  <ElementLabelValue label="Гражданство" :value="props.item.citizenship" />
  <ElementLabelValue v-if="props.item.dual" label="Двойное гражданство">
    <UBadge variant="outline" color="info" :label="props.item.dual" />
  </ElementLabelValue>
  <ElementLabelValue label="СНИЛС" :value="props.item.snils" />
  <ElementLabelValue label="ИНН" :value="props.item.inn" />
  <ElementLabelValue label="Семейное положение" :value="props.item.marital" />
  <ElementLabelValue
    label="Дата записи"
    :value="new Date(props.item.created_at).toLocaleDateString()"
  />
  <ElementLabelValue
    label="Дата обновления"
    :value="new Date(props.item.updated_at).toLocaleDateString()"
  />
  <ElementLabelValue
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <ElementLabelValue v-if="props.item.destination" label="Материалы проверок">
    <UButton
      variant="outline"
      :color="!copied ? 'info' : 'success'"
      size="sm"
      :label="!copied ? 'Копировать ссылку' : 'Скопировано'"
      @click="copy(props.item.destination)"
    />
  </ElementLabelValue>
</template>
