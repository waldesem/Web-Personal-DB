<script setup lang="ts">
import { defineAsyncComponent, ref } from "vue";
import { Robot } from "@/interfaces";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const emit = defineEmits(["delete"]);

const props = defineProps({
  printPage: {
    type: Boolean,
    default: false,
  },
  robots: {
    type: Array as () => Array<Robot>,
    default: {},
  },
});

const showActions = ref(false);
</script>

<template>
  <div
    v-if="props.robots.length"
    @mouseover="showActions = true"
    @mouseout="showActions = false"
  >
    <div 
      v-if="props.robots.length" 
      :class="{'collapse show': !printPage}" 
      id="check"
    > 
      <div class="mb-3" v-for="(item, idx) in props.robots" :key="idx">
        <div class="card card-body">
          <LabelSlot>
            <a v-show="showActions"
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
