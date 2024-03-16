<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { Robot } from "@/interfaces/interface";

const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);

const emit = defineEmits(["delete"]);

const props = defineProps({
  robots:  {
    type: Array as () => Array<Robot>,
    default: {},
  },
});
</script>

<template>
  <div v-if="props.robots.length">
    <CollapseDiv
      v-for="(item, idx) in props.robots"
      :key="idx"
      :id="'check' + idx"
      :idx="idx.toString()"
      :label="'Робот #' + (idx + 1)"
    >
      <LabelSlot>
        <a
          href="#"
          @click="emit('delete', item['id'].toString(), 'robot')"
          title="Удалить"
        >
          <i class="bi bi-trash"></i>
        </a>
      </LabelSlot>
      <LabelValue
        :label="'Проверка по кадровым данным<'"
        :value="item['employee']"
      />
      <LabelValue :label="'Проверка ИНН'" :value="item['inn']" />
      <LabelValue :label="'Проверка ФССП'" :value="item['debt']" />
      <LabelValue
        :label="'Проверка банкротства'"
        :value="item['bankruptcy']"
      />
      <LabelValue :label="'Проверка БКИ'" :value="item['bki']" />
      <LabelValue :label="'Проверка судебных дел'" :value="item['courts']" />
      <LabelValue
        :label="'Проверка по списку террористов'"
        :value="item['terrorist']"
      />
      <LabelValue
        :label="'Проверка нахождения в розыске'"
        :value="item['mvd']"
      />
      <LabelValue
        :label="'Дата'"
        :value="new Date(String(item['deadline'])).toLocaleDateString('ru-RU')"
      />
    </CollapseDiv>
  </div>
</template>
