<script setup lang="ts">
import type { Verification } from '@/types';

const props = defineProps({
  item: {
    type: Object as () => Verification,
    default: {} as Verification,
  },
})
</script>

<template>
  <ElementsLabelSlot
    v-if="props.item.workplace"
    :label="'Проверка по местам работы'"
  >
    {{ props.item.workplace }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.document"
    :label="'Проверка документов'"
  >
    {{ props.item.document }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.debt"
    :label="'Проверка задолженностей'"
    >{{ props.item.debt }}</ElementsLabelSlot
  >
  <ElementsLabelSlot
    v-if="props.item.bankruptcy"
    :label="'Проверка банкротства'"
  >
    {{ props.item.bankruptcy }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.bki"
    :label="'Проверка БКИ'"
    >{{ props.item.bki }}</ElementsLabelSlot
  >
  <ElementsLabelSlot
    v-if="props.item.courts"
    :label="'Проверка судебных решений'"
  >
    {{ props.item.courts }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.affilation"
    :label="'Проверка аффилированности'"
  >
    {{ props.item.affilation }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.terrorist"
    :label="'Проверка по списку террористов'"
  >
    {{ props.item.terrorist }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.internet"
    :label="'Проверка в открытых источниках'"
  >
    {{ props.item.internet }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.cronos"
    :label="'Проверка Кронос'"
  >
    {{ props.item.cronos }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.addition"
    :label="'Дополнительная информация'"
  >
    {{ props.item.addition }}
  </ElementsLabelSlot>
  <ElementsLabelSlot
    v-if="props.item.comment"
    :label="'Комментарии'"
    >{{ props.item.comment }}
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Результат'">
    <UBadge
      :color="
        props.item.conclusion === 'СОГЛАСОВАНО'
          ? 'green'
          : props.item.conclusion === 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'
          ? 'primary'
          : 'red'
      "
      :label="props.item.conclusion"
      variant="solid"
    />
  </ElementsLabelSlot>
  <ElementsLabelSlot :label="'Дата записи'">
    {{ new Date(props.item.created).toLocaleString("ru-RU") }}
  </ElementsLabelSlot>
</template>
