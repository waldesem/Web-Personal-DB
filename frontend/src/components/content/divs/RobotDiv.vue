<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { Robot } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/elements/CollapseDiv.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/elements/LabelValue.vue")
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
      <LabelValue :label="'Действия'" :no-print="true">
        <a
          href="#"
          @click="emit('delete', item['id'].toString(), 'robot')"
          title="Удалить"
        >
          <i class="bi bi-trash"></i>
        </a>
      </LabelValue>
      <LabelValue :label="'ID'">{{ item["id"] }}</LabelValue>
      <LabelValue :label="'Проверка по кадровым данным'">
        {{ item["employee"] }}
      </LabelValue>
      <LabelValue :label="'Проверка ИНН'">{{ item["inn"] }}</LabelValue>
      <LabelValue :label="'Проверка ФССП'">{{ item["debt"] }}</LabelValue>
      <LabelValue :label="'Проверка банкротства'">
        {{ item["bankruptcy"] }}
      </LabelValue>
      <LabelValue :label="'Проверка БКИ'">{{ item["bki"] }}</LabelValue>
      <LabelValue :label="'Проверка судебных решений'">
        {{ item["courts"] }}
      </LabelValue>
      <LabelValue :label="'Проверка по списку террористов'">
        {{ item["terrorist"] }}
      </LabelValue>
      <LabelValue :label="'Проверка в розыск'">{{ item["mvd"] }}</LabelValue>
      <LabelValue :label="'Дата'">
        {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
      </LabelValue>
    </CollapseDiv>
  </div>
</template>
