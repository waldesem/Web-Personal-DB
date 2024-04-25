<script setup lang="ts">
import { defineAsyncComponent, onBeforeMount, ref } from "vue";
import { stateAnketa } from "@/state";

const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

onBeforeMount(async () => {
  await stateAnketa.getItem("robot");
});

const showActions = ref(false);
</script>

<template>
  <div v-if="stateAnketa.anketa.robot.length" class='py-3'>
    <div
      v-for="(item, idx) in stateAnketa.anketa.robot"
      :key="idx"
      @mouseover="showActions = true"
      @mouseout="showActions = false"
      class="card card-body mb-3"
    >
      <LabelSlot>
        <button
          v-show="showActions"
          class="btn btn-link"
          @click="
            stateAnketa.deleteItem(item['id'].toString(), 'robot');
            showActions = false;
          "
          title="Удалить"
        >
          <i class="bi bi-trash"></i>
        </button>
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
</template>
