<script setup lang="ts">
import { useClipboard } from "@vueuse/core";
import type { ItemField, Person } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Person>,
    default: () => {},
  },
});

const { copy, copied } = useClipboard();

const fields = [
  { key: "surname", label: "Фамилия" },
  { key: "firstname", label: "Имя" },
  { key: "patronymic", label: "Отчество" },
  { key: "birthday", label: "Дата рождения" },
  { key: "birthplace", label: "Место рождения" },
  { key: "citizenship", label: "Гражданство" },
  { key: "dual", label: "Двойное гражданство", slot: true },
  { key: "snils", label: "СНИЛС" },
  { key: "inn", label: "ИНН" },
  { key: "marital", label: "Семейное положение" },
  { key: "created", label: "Дата записи" },
  { key: "addition", label: "Дополнительная информация" },
  { key: "destination", label: "Материалы проверок", slot: true },
] as ItemField[];

const person = computed(() => {
  return {
    ...props.item,
    birthday: localStr(props.item.birthday),
    created: localStr(props.item.updated_at),
  };
});
</script>

<template>
  <ElementItemCard :fields="fields" :item="person">
    <template v-if="props.item.dual" #dual>
      <UBadge variant="outline" color="info" :label="props.item.dual" />
    </template>
    <template v-if="props.item.destination" #destination>
      <UButton
        variant="outline"
        :color="!copied ? 'info' : 'success'"
        size="sm"
        :label="!copied ? 'Копировать ссылку' : 'Скопировано'"
        @click="copy(props.item.destination)"
      />
    </template>
  </ElementItemCard>
</template>
