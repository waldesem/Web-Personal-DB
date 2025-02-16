<script setup lang="ts">
import type { Persons } from "@/types";

const props = defineProps({
  person: {
    type: Object as () => Persons,
    default: {} as Persons,
  },
})
</script>

<template>
  <ElementsLabelSlot :label="'Фамилия'">
    {{ props.person.surname }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Имя'">
    {{ props.person.firstname }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Отчество'">
    {{ props.person.patronymic }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Дата рождения'">
    {{ new Date(props.person.birthday).toLocaleDateString("ru-RU") }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Место рождения'">
    {{ props.person.birthplace }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Гражданство'">
    {{ props.person.citizenship }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.dual" :label="'Двойное гражданство'">
    {{ props.person.dual }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.snils" :label="'СНИЛС'">
    {{ props.person.snils }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.inn" :label="'ИНН'">
    {{ props.person.inn }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.marital" :label="'Семейное положение'">
    {{ props.person.marital }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Дата записи'">
    {{ new Date(props.person.created).toLocaleString("ru-RU") }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.person.addition"
    :label="'Дополнительная информация'"
  >
    {{ props.person.addition }}
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.person.destination" :label="'Материалы'">
    {{ props.person.destination }}
  </ElementsLabelSlot>
</template>
