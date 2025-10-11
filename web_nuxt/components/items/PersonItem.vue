<script setup lang="ts">
import type { Persons } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Persons>,
    default: () => ({}),
  },
});

function handleClick() {
  if (props.item.destination) {
    navigator.clipboard.writeText(props.item.destination).then(() => {
      useToasts("success", "Адрес скопирован!");
    });
  }
}
</script>

<template>
  <ElementsLabelValue label="Фамилия" :value="props.item.surname" />
  <ElementsLabelValue label="Имя" :value="props.item.firstname" />
  <ElementsLabelValue label="Отчество" :value="props.item.patronymic" />
  <ElementsLabelSlot v-if="props.item.birthday" label="Дата рождения">
    <NuxtTime :datetime="props.item.birthday" />
  </ElementsLabelSlot>
  <ElementsLabelValue label="Место рождения" :value="props.item.birthplace" />
  <ElementsLabelValue label="Гражданство" :value="props.item.citizenship" />
  <ElementsLabelSlot v-if="props.item.dual" label="Двойное гражданство">
    <UBadge variant="outline" color="error" :label="props.item.dual" />
  </ElementsLabelSlot>
  <ElementsLabelValue label="СНИЛС" :value="props.item.snils" />
  <ElementsLabelValue label="ИНН" :value="props.item.inn" />
  <ElementsLabelValue label="Семейное положение" :value="props.item.marital" />
  <ElementsLabelSlot v-if="props.item.created" label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementsLabelSlot>
  <ElementsLabelValue
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <ElementsLabelSlot v-if="props.item.destination" label="Материалы проверок">
    <UButton
      variant="outline"
      color="info"
      size="sm"
      label="Копировать ссылку"
      @click="handleClick"
    />
  </ElementsLabelSlot>
</template>
