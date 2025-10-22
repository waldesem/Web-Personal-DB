<script setup lang="ts">
import type { Work } from "@/types";

const props = defineProps<Work>()

const experience = computed(() => {
  const duration = {
    years: 0,
    months: 0,
    days: 0,
  };
  const end = props.finished
    ? new Date(props.finished)
    : new Date(props.created);
  if (!props.starts) {
    return duration;
  }
  const start = new Date(props.starts);

  duration.years = end.getFullYear() - start.getFullYear();
  duration.months = end.getMonth() - start.getMonth();
  duration.days = end.getDate() - start.getDate();

  // Коррекция дней, если конечная дата меньше начальной по дням
  if (duration.days < 0) {
    duration.months--;
    const lastDayOfPrevMonth = new Date(
      end.getFullYear(),
      end.getMonth(),
      0
    ).getDate();
    duration.days += lastDayOfPrevMonth;
  }

  // Коррекция месяцев, если они отрицательные
  if (duration.months < 0) {
    duration.years--;
    duration.months += 12;
  }

  return duration;
});
</script>

<template>
  <ElementsLabelValue
    label="Текущая работа"
    :value="props.now_work ? 'Да' : 'Нет'"
  />
  <ElementsLabelSlot v-if="props.starts" label="Начало работы">
    <NuxtTime :datetime="props.starts" />
  </ElementsLabelSlot>
  <ElementsLabelSlot v-if="props.finished" label="Окончание работы">
    <NuxtTime :datetime="props.finished" />
  </ElementsLabelSlot>
  <ElementsLabelSlot label="Стаж на рабочем месте">
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
        `${experience.years} лет, ${experience.months} месяцев, ${experience.days} дней`
      }}
    </UBadge>
  </ElementsLabelSlot>
  <ElementsLabelValue label="Место" :value="props.workplace" />
  <ElementsLabelSlot v-if="props.address" label="Адрес">
    {{ props.address }}
    <UButton
      :to="`https://yandex.ru/maps/?text=${props.address}%10с%10`"
      target="_blank"
      title="Показать на Яндекс.Карте"
      variant="outline"
      icon="i-lucide-map-pinned"
      class="ms-4"
    />
  </ElementsLabelSlot>
  <ElementsLabelValue label="Должность" :value="props.position" />
  <ElementsLabelValue label="Причина увольнения" :value="props.reason" />
</template>
