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
    v-if="props.item.workplace"
    label="Проверка по местам работы"
    :value="props.item.workplace"
  />
  <ElementLabelValue
    v-if="props.item.document"
    label="Проверка документов"
    :value="props.item.document"
  />
  <ElementLabelValue
    v-if="props.item.debt"
    label="Проверка задолженностей"
    :value="props.item.debt"
  />
  <ElementLabelValue
    label="Проверка банкротства"
    :value="props.item.bankruptcy"
  />
  <ElementLabelValue
    v-if="props.item.bki"
    label="Проверка по БКИ"
    :value="props.item.bki"
  />
  <ElementLabelValue
    label="Проверка судебных решений"
    :value="props.item.courts"
  />
  <ElementLabelValue
    v-if="props.item.affilation"
    label="Проверка аффилированности"
    :value="props.item.affilation"
  />
  <ElementLabelValue
    v-if="props.item.terrorist"
    label="Проверка по списку террористов"
    :value="props.item.terrorist"
  />
  <ElementLabelValue
    v-if="props.item.internet"
    label="Проверка в открытых источниках"
    :value="props.item.internet"
  />
  <ElementLabelValue
    v-if="props.item.cronos"
    label="Проверка Кронос"
    :value="props.item.cronos"
  />
  <ElementLabelValue
    v-if="props.item.addition"
    label="Дополнительная информация"
    :value="props.item.addition"
  />
  <ElementLabelValue
    v-if="props.item.comment"
    label="Комментарии"
    :value="props.item.comment"
  />
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
  <ElementLabelValue
    label="Дата записи"
    :value="new Date(props.item.created_at).toLocaleDateString()"
  />
</template>
