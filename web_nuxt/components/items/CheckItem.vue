<script setup lang="ts">
import type { Verification } from "@/types";
import { Conclusions } from "@/types";

const props = defineProps<Verification>()
</script>

<template>
  <ElementsLabelValue
    label="Проверка по местам работы"
    :value="props.workplace"
  />
  <ElementsLabelValue
    label="Проверка документов"
    :value="props.document"
  />
  <ElementsLabelValue
    label="Проверка задолженностей"
    :value="props.debt"
  />
  <ElementsLabelValue
    label="Проверка банкротства"
    :value="props.bankruptcy"
  />
  <ElementsLabelValue label="Проверка по БКИ" :value="props.bki" />
  <ElementsLabelValue
    label="Проверка судебных решений"
    :value="props.courts"
  />
  <ElementsLabelValue
    label="Проверка аффилированности"
    :value="props.affilation"
  />
  <ElementsLabelValue
    label="Проверка по списку террористов"
    :value="props.terrorist"
  />
  <ElementsLabelValue
    label="Проверка в открытых источниках"
    :value="props.internet"
  />
  <ElementsLabelValue label="Проверка Кронос" :value="props.cronos" />
  <ElementsLabelValue
    label="Дополнительная информация"
    :value="props.addition"
  />
  <ElementsLabelValue label="Комментарии" :value="props.comment" />
  <ElementsLabelSlot v-if="props.conclusion" label="Результат">
    <UBadge
      :color="
        props.conclusion === Conclusions.agreed
          ? 'success'
          : props.conclusion === Conclusions.comments
          ? 'warning'
          : props.conclusion === Conclusions.cancel
          ? 'neutral'
          : 'error'
      "
      :label="props.conclusion"
    />
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.created" label="Дата записи">
    <NuxtTime :datetime="props.created" />
  </ElementsLabelSlot>
</template>
