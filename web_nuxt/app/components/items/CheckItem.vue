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
  <ElementsLabelValue
    label="Проверка по местам работы"
    :value="props.item.workplace"
  />
  <ElementsLabelValue
    label="Проверка документов"
    :value="props.item.document"
  />
  <ElementsLabelValue
    label="Проверка задолженностей"
    :value="props.item.debt"
  />
  <ElementsLabelValue
    label="Проверка банкротства"
    :value="props.item.bankruptcy"
  />
  <ElementsLabelValue label="Проверка по БКИ" :value="props.item.bki" />
  <ElementsLabelValue
    label="Проверка судебных решений"
    :value="props.item.courts"
  />
  <ElementsLabelValue
    label="Проверка аффилированности"
    :value="props.item.affilation"
  />
  <ElementsLabelValue
    label="Проверка по списку террористов"
    :value="props.item.terrorist"
  />
  <ElementsLabelValue
    label="Проверка в открытых источниках"
    :value="props.item.internet"
  />
  <ElementsLabelValue label="Проверка Кронос" :value="props.item.cronos" />
  <ElementsLabelValue
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <ElementsLabelValue label="Комментарии" :value="props.item.comment" />
  <ElementsLabelValue label="Результат">
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
  </ElementsLabelValue>
  <ElementsLabelValue label="Дата записи">
    <NuxtTime :datetime="props.item.created" />
  </ElementsLabelValue>
</template>
