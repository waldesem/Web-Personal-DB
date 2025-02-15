<script setup lang="ts">
import type { Needs } from "@/types";

const emit = defineEmits(["delete", "update", "cancel"]);

const props = defineProps({
  item: {
    type: Object as () => Needs,
    default: {} as Needs,
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
    <ElementsLabelSlot :label="'Информация'">{{
      props.item.info
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Иннициатор'">{{
      props.item.initiator
    }}</ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата записи'">
      {{ new Date(props.item.created).toLocaleString("ru-RU") }}
    </ElementsLabelSlot>
    <template v-if="editable" #footer>
      <ElementsTabMenu
        :item="'inquiries'"
        @delete="emit('delete', props.item.id, index)"
        @update="emit('update')"
        @cancel="emit('cancel')"
      />
    </template>
  </ElementsCardDiv>
</template>