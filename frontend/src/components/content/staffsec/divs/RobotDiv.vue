<script setup lang="ts">
import { computed, defineAsyncComponent } from "vue";
import { Robot } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);

const emit = defineEmits(["delete"]);

const props = defineProps({
  robots: {
    type: Array as () => Array<Robot>,
    default: {},
  },
});

const robotObjects = computed(() => {
  return props.robots.map((item) => ({
    id: ["ID", item["id"]],
    employee: ["Проверка по кадровым данным", item["employee"]],
    inn: ["Проверка ИНН", item["inn"]],
    fssp: ["Проверка ФССП", item["debt"]],
    bankruptcy: ["Проверка банкротства", item["bankruptcy"]],
    bki: ["Проверка БКИ", item["bki"]],
    courts: ["Проверка судебных решений", item["courts"]],
    terrorist: ["Проверка по списку террористов", item["terrorist"]],
    mvd: ["Проверка в розыск", item["mvd"]],
    deadline: [
      "Дата",
      new Date(String(item["deadline"])).toLocaleDateString("ru-RU"),
    ],
  }));
});
</script>

<template>
  <div v-if="robotObjects.length">
    <CollapseDiv
      v-for="(item, idx) in robotObjects"
      :key="idx"
      :id="'check' + idx"
      :idx="idx.toString()"
      :label="'Робот #' + (idx + 1)"
    >
      <div class="row mb-3 d-print-none">
        <div class="col-md-3">
          <label class="form-label">Действия</label>
        </div>
        <div class="col-md-9">
          <a
            href="#"
            @click="emit('delete', item.id[1].toString(), 'robot')"
            title="Удалить"
          >
            <i class="bi bi-trash"></i>
          </a>
        </div>
      </div>
      <div v-for="(value, key) in item" :key="key" class="row mb-3">
        <div class="col-md-3">
          <label class="form-label">
            {{ value[0] }}
          </label>
        </div>
        <div class="col-md-9">
          {{ value[1] }}
        </div>
      </div>
    </CollapseDiv>
  </div>
</template>
