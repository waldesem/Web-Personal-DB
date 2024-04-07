<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Robot } from "@/interfaces/interface";

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

const showActions = ref(false);
function handleMouse() {
  showActions.value = !showActions.value;
}
</script>

<template>
  <div
    v-if="props.robots.length"
    @mouseover="handleMouse"
    @mouseout="handleMouse"
  >
    <div v-if="props.robots.length" class="collapse" id="check"> 
      <div class="mb-3" v-for="(item, idx) in props.robots" :key="idx">
        <div class="card card-body">
          <LabelSlot v-show="showActions">
            <a
              href="#"
              @click="
                emit('delete', item['id'].toString(), 'robot');
                showActions = false;
              "
              title="Удалить"
            >
              <i class="bi bi-trash"></i>
            </a>
          </LabelSlot>
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
        </div>
      </div>
    </div>
  </div>
</template>
