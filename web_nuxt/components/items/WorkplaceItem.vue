<script setup lang="ts">
import type { Work } from "@/types";

const NuxtTime = resolveComponent("NuxtTime");
const UBadge = resolveComponent("UBadge");
const UButton = resolveComponent("UButton");

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    default: () => ({}),
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

const workplace = {
  "Текущая работа": props.item.now_work ? "Да" : "Нет",
  "Начало работы": props.item.starts
    ? h(NuxtTime, {
        datetime: props.item.starts,
      })
    : "",
  "Окончание работы": props.item.finished
    ? h(NuxtTime, {
        datetime: props.item.finished,
      })
    : "",
  "Стаж на рабочем месте": h(
    UBadge,
    {
      variant: "outline",
      color:
        experience.value.years > 0
          ? "success"
          : experience.value.months > 0
          ? "info"
          : "danger",
    },
    {
      default: () =>
        `${experience.value.years} лет, ${experience.value.months} месяцев, ${experience.value.days} дней`,
    }
  ),
  Место: props.item.workplace,
  Адрес: props.item.address
    ? h("div", [
        props.item.address,
        h(UButton, {
          to: `https://yandex.ru/maps/?text=${props.item.address}%10с%10`,
          target: "_blank",
          title: "Показать на Яндекс.Карте",
          variant: "outline",
          icon: "i-lucide-map-pinned",
          class: "ms-4",
        }),
      ])
    : "",
  Должность: props.item.position,
  "Причина увольнения": props.item.reason,
};
</script>

<template>
  <div v-for="(value, key) in workplace" :key="key">
    <ElementsLabelValue :label="key" :value="value" />
  </div>
</template>
