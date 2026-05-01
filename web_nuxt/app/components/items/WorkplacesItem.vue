<script setup lang="ts">
import { useExperience } from "@/composables/useExperience";
import { localStr } from "@/utils";
import type { Work } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    required: true,
  },
});

const workExperience = useExperience();

const experience = workExperience.experience(
  props.item.starts,
  props.item.finished,
  new Date().toDateString(),
);
</script>

<template>
  <ElementLabelValue
    label="Текущая работа"
    :value="!props.item.finished ? 'Да' : 'Нет'"
  />
  <ElementLabelValue
    label="Начало работы"
    :value="localStr(props.item.starts)"
  />
  <ElementLabelValue
    label="Окончание работы"
    :value="localStr(props.item.finished)"
  />
  <ElementLabelSlot v-if="experience" label="Стаж на рабочем месте">
    <UBadge
      variant="outline"
      :color="
        experience.years > 0
          ? 'success'
          : experience.months > 0
            ? 'info'
            : 'error'
      "
    >
      {{
        `${experience.years} г., ${experience.months} мес., ${experience.days} дн.`
      }}
    </UBadge>
  </ElementLabelSlot>
  <ElementLabelValue label="Место" :value="props.item.workplace" />
  <ElementLabelSlot v-if="props.item.address" label="Адрес">
    <div class="space-x-4">
      {{ props.item.address }}
      <UButton
        :to="`https://yandex.ru/maps/?text=${props.item.address}%10с%10`"
        target="_blank"
        title="Показать на Яндекс.Карте"
        variant="outline"
        icon="i-lucide-map-pinned"
      />
    </div>
  </ElementLabelSlot>
  <ElementLabelValue label="Должность" :value="props.item.position" />
  <ElementLabelValue label="Причина увольнения" :value="props.item.reason" />
</template>
