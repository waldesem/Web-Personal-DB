<script setup lang="ts">
import type { Pfo } from "@/types";

const emit = defineEmits(["delete", "update", "cancel"]);

const props = defineProps({
  item: {
    type: Object as () => Pfo,
    default: {} as Pfo,
  },
  index: {
    type: Number,
    default: 0,
  },
  editable: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <ElementsCardDiv>
    <ElementsLabelSlot :label="'Тема проверки'">{{
      props.item.theme
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Результат'">
      <UBadge
        :color="
          props.item.conclusion === 'БЕЗ ЗАМЕЧАНИЙ'
            ? 'green'
            : props.item.conclusion === 'С КОММЕНТАРИЯМИ'
            ? 'primary'
            : 'red'
        "
        :label="props.item.conclusion"
        variant="soft"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата записи'">
      {{ new Date(props.item.created).toLocaleString("ru-RU") }}
    </ElementsLabelSlot>
    <template v-if="editable" #footer>
      <ElementsTabMenu
        :item="'poligrafs'"
        @cancel="emit('cancel')"
        @update="emit('update')"
        @delete="emit('delete', props.item.id, index)"
      />
    </template>
  </ElementsCardDiv>
</template>