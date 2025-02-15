<script setup lang="ts">
import type { Inquisition } from "@/types";

const emit = defineEmits(["delete", "update", "cancel"]);

const props = defineProps({
  item: {
    type: Object as () => Inquisition,
    default: {} as Inquisition,
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
    <ElementsLabelSlot :label="'Информация'">{{
      props.item.info
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата записи'">
      {{ new Date(props.item.created).toLocaleString("ru-RU") }}
    </ElementsLabelSlot>
    <template v-if="editable" #footer>
      <ElementsTabMenu
        :item="'investigations'"
        @cancel="emit('cancel')"
        @update="emit('update')"
        @delete="emit('delete', props.item.id, index)"
      />
    </template>
  </ElementsCardDiv>
</template>