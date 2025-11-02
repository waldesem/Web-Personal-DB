<script setup lang="ts">
import type { Work } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    required: true,
  },
});

const experience = computed(() => {
  const duration = {
    years: 0,
    months: 0,
    days: 0,
  };
  const end = props.item.finished
    ? new Date(props.item.finished)
    : new Date(props.item.created);
  if (!props.item.starts) {
    return duration;
  }
  const start = new Date(props.item.starts);

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
    :value="props.item.now_work ? 'Да' : 'Нет'"
  />
  <ElementsLabelValue v-if="props.item.starts" label="Начало работы">
    <NuxtTime :datetime="props.item.starts" />
  </ElementsLabelValue>
  <ElementsLabelValue v-if="props.item.finished" label="Окончание работы">
    <NuxtTime :datetime="props.item.finished" />
  </ElementsLabelValue>
  <ElementsLabelValue v-if="experience" label="Стаж на рабочем месте">
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
  </ElementsLabelValue>
  <ElementsLabelValue label="Место" :value="props.item.workplace" />
  <ElementsLabelValue label="Адрес">
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
  </ElementsLabelValue>
  <ElementsLabelValue label="Должность" :value="props.item.position" />
  <ElementsLabelValue label="Причина увольнения" :value="props.item.reason" />
</template>
