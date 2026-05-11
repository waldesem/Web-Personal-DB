<script setup lang="ts">
import { useExperience } from "@/composables/useExperience";
import { localStr } from "@/utils";
import type { ItemField, Work } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Work>,
    required: true,
  },
});

const workExperience = useExperience();

const work = computed(() => {
  return {
    ...props.item,
    experience: workExperience.experience(
      props.item.starts,
      props.item.finished,
      new Date().toDateString(),
    ),
    nowWork: props.item.finished ? "Нет" : "Да",
    starts: localStr(props.item.starts),
    finished: localStr(props.item.finished),
  };
});

const fields = [
  { key: "nowWork", label: "Текущая работа" },
  { key: "starts", label: "Начало работы" },
  { key: "finished", label: "Дата увольнения" },
  { key: "experience", label: "Стаж", slot: true },
  { key: "workplace", label: "Организация" },
  { key: "address", label: "Организация", slot: true },
  { key: "position", label: "Должность" },
  { key: "reason", label: "Причина увольнения" },
] as ItemField[];
</script>

<template>
  <ElementItemCard :fields="fields" :item="work">
    <template #experience>
      <UBadge
        variant="outline"
        :color="
          work.experience.years > 0
            ? 'success'
            : work.experience.months > 0
              ? 'info'
              : 'error'
        "
      >
        {{
          `${work.experience.years} г., ${work.experience.months} мес., ${work.experience.days} дн.`
        }}
      </UBadge>
    </template>
    <template #address>
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
    </template>
  </ElementItemCard>
</template>
