<script setup lang="ts">
import type { Verification } from "@/types";
import { Conclusions } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Verification>,
    required: true,
  },
});
</script>

<template>
  <ElementLabelValue
    label="Проверка по местам работы"
    :value="props.item.workplace"
  />
  <ElementLabelValue label="Проверка документов" :value="props.item.document" />
  <ElementLabelValue label="Проверка задолженностей" :value="props.item.debt" />
  <ElementLabelValue
    label="Проверка банкротства"
    :value="props.item.bankruptcy"
  />
  <ElementLabelValue label="Проверка по БКИ" :value="props.item.bki" />
  <ElementLabelValue
    label="Проверка судебных решений"
    :value="props.item.courts"
  />
  <ElementLabelValue
    label="Проверка аффилированности"
    :value="props.item.affilation"
  />
  <ElementLabelValue
    label="Проверка по списку террористов"
    :value="props.item.terrorist"
  />
  <ElementLabelValue
    label="Проверка в открытых источниках"
    :value="props.item.internet"
  />
  <ElementLabelValue label="Проверка Кронос" :value="props.item.cronos" />
  <ElementLabelValue
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <ElementLabelValue label="Комментарии" :value="props.item.comment" />
  <ElementLabelValue label="Результат">
    <UBadge
      :color="
        props.item.conclusion === Conclusions.agreed
          ? 'success'
          : props.item.conclusion === Conclusions.comments
          ? 'warning'
          : props.item.conclusion === Conclusions.cancel
          ? 'neutral'
          : 'error'
      "
      :label="props.item.conclusion"
    />
  </ElementLabelValue>
  <ElementLabelValue label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementLabelValue>
</template>
