<script setup lang="ts">
import { useClipboard } from "@vueuse/core";
import { localStr } from "@/utils";
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
    :value="localStr(props.item.birthday)"
  />
  <ElementLabelValue label="Место рождения" :value="props.item.birthplace" />
  <ElementLabelValue label="Гражданство" :value="props.item.citizenship" />
  <ElementLabelSlot v-if="props.item.dual" label="Двойное гражданство">
    <UBadge variant="outline" color="info" :label="props.item.dual" />
  </ElementLabelSlot>
  <ElementLabelValue label="СНИЛС" :value="props.item.snils" />
  <ElementLabelValue label="ИНН" :value="props.item.inn" />
  <ElementLabelValue label="Семейное положение" :value="props.item.marital" />
  <ElementLabelValue
    label="Дата записи"
    :value="localStr(props.item.created_at)"
  />
  <ElementLabelValue
    label="Дата обновления"
    :value="localStr(props.item.updated_at)"
  />
  <ElementLabelValue
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <ElementLabelSlot v-if="props.item.destination" label="Материалы проверок">
    <UButton
      variant="outline"
      :color="!copied ? 'info' : 'success'"
      size="sm"
      :label="!copied ? 'Копировать ссылку' : 'Скопировано'"
      @click="copy(props.item.destination)"
    />
  </ElementLabelSlot>
</template>
