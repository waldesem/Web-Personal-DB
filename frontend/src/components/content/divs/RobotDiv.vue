<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { Robot } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["delete"]);

const props = defineProps({
  robots: {
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
      <LabelSlot :label="'Действия'" :no-print="true">
        <a
          href="#"
          @click="emit('delete', item['id'].toString(), 'robot')"
          title="Удалить"
        >
          <i class="bi bi-trash"></i>
        </a>
      </LabelSlot>
      <LabelSlot :label="'ID'">{{ item["id"] }}</LabelSlot>
      <LabelSlot :label="'Проверка по кадровым данным'">
        {{ item["employee"] }}
      </LabelSlot>
      <LabelSlot :label="'Проверка ИНН'">{{ item["inn"] }}</LabelSlot>
      <LabelSlot :label="'Проверка ФССП'">{{ item["debt"] }}</LabelSlot>
      <LabelSlot :label="'Проверка банкротства'">
        {{ item["bankruptcy"] }}
      </LabelSlot>
      <LabelSlot :label="'Проверка БКИ'">{{ item["bki"] }}</LabelSlot>
      <LabelSlot :label="'Проверка судебных решений'">
        {{ item["courts"] }}
      </LabelSlot>
      <LabelSlot :label="'Проверка по списку террористов'">
        {{ item["terrorist"] }}
      </LabelSlot>
      <LabelSlot :label="'Проверка в розыск'">{{ item["mvd"] }}</LabelSlot>
      <LabelSlot :label="'Дата'">
        {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
      </LabelSlot>
    </CollapseDiv>
  </div>
</template>
