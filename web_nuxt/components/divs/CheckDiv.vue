<script setup lang="ts">
import type { Verification } from '@/types';

const emit = defineEmits(["delete", "update", "cancel"]);

const props = defineProps({
  item: {
    type: Object as () => Verification,
    default: {} as Verification,
  },
  index: {
    type: Number,
    default: 0,
  },
  editable: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <ElementsCardDiv>
    <ElementsLabelSlot
      v-if="props.item.workplace"
      :label="'Проверка по местам работы'"
    >
      {{ props.item.workplace }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.document"
      :label="'Проверка паспорта'"
    >
      {{ props.item.document }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.inn"
      :label="'Проверка ИНН'"
      >{{ props.item.inn }}</ElementsLabelSlot
    >
    <ElementsLabelSlot
      v-if="props.item.debt"
      :label="'Проверка ФССП'"
      >{{ props.item.debt }}</ElementsLabelSlot
    >
    <ElementsLabelSlot
      v-if="props.item.bankruptcy"
      :label="'Проверка банкротства'"
    >
      {{ props.item.bankruptcy }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.bki"
      :label="'Проверка БКИ'"
      >{{ props.item.bki }}</ElementsLabelSlot
    >
    <ElementsLabelSlot
      v-if="props.item.courts"
      :label="'Проверка судебных решений'"
    >
      {{ props.item.courts }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.affilation"
      :label="'Проверка аффилированности'"
    >
      {{ props.item.affilation }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.terrorist"
      :label="'Проверка по списку террористов'"
    >
      {{ props.item.terrorist }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.mvd"
      :label="'Проверка в розыск'"
      >{{ props.item.mvd }}</ElementsLabelSlot
    >
    <ElementsLabelSlot
      v-if="props.item.internet"
      :label="'Проверка в открытых источниках'"
    >
      {{ props.item.internet }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.cronos"
      :label="'Проверка Кронос'"
    >
      {{ props.item.cronos }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.addition"
      :label="'Дополнительная информация'"
    >
      {{ props.item.addition }}
    </ElementsLabelSlot>
    <ElementsLabelSlot
      v-if="props.item.comment"
      :label="'Комментарии'"
      >{{ props.item.comment }}
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Результат'">
      <UBadge
        :color="
          props.item.conclusion === 'СОГЛАСОВАНО'
            ? 'green'
            : props.item.conclusion === 'СОГЛАСОВАНО С КОММЕНТАРИЕМ'
            ? 'primary'
            : 'red'
        "
        :label="props.item.conclusion"
        variant="solid"
      />
    </ElementsLabelSlot>
    <ElementsLabelSlot :label="'Дата записи'">
      {{ new Date(props.item.created).toLocaleString("ru-RU") }}
    </ElementsLabelSlot>
    <template v-if="editable" #footer>
      <ElementsTabMenu
        :item="'checks'"
        @cancel="emit('cancel')"
        @update="emit('update')"
        @delete="emit('delete', props.item.id, index)"
      />
    </template>
  </ElementsCardDiv>
</template>
