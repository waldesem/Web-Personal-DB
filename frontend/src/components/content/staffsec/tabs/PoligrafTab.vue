<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount, computed } from "vue";
import { Pfo } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const PoligrafForm = defineAsyncComponent(
  () => import("../forms/PoligrafForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
);

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(async () => {
  emit("get-item", "poligraf");
});

const props = defineProps({
  poligrafs: {
    type: Array as () => Array<Pfo>,
    default: () => [],
  },
});

const poligraf = ref({
  action: "",
  itemId: "",
  item: <Pfo>{},
});

const pfoObject = computed(() => {
  return props.poligrafs.map((item) => ({
    id: ["ID", item["id"]],
    theme: ["Тема проверки", item["theme"]],
    results: ["Результат", item["results"]],
    officer: ["Сотрудник", item["officer"]],
    deadline: [
      "Дата",
      new Date(String(item["deadline"])).toLocaleDateString(
        "ru-RU"
      ),
    ],
  }));
});

function submitForm(form: Object) {
  emit(
    "submit",
    poligraf.value.action,
    "poligraf",
    poligraf.value.itemId,
    form
  );
  poligraf.value.action = "";
}

function submitFile(event: Event) {
  emit("file", event);
}
</script>

<template>
  <div class="py-3">
    <PoligrafForm
      v-if="poligraf.action"
      :poligraf="poligraf.item"
      @submit="submitForm"
      @cancel="poligraf.action = ''"
    />
    <div v-else>
      <div v-if="pfoObject.length">
        <CollapseDiv
          v-for="(item, idx) in pfoObject"
          :key="idx"
          :id="'poligraf' + idx"
          :idx="idx.toString()"
          :label="'Полиграф #' + (idx + 1)"
        >
          <div class="row mb-3 d-print-none">
            <div class="col-md-3">
              <label class="form-label">Действия</label>
            </div>
            <div class="col-md-9">
              <a
                href="#"
                title="Удалить"
                @click="emit('delete', item.id[1].toString(), 'poligraf')"
              >
                <i class="bi bi-trash"></i>
              </a>
              &nbsp;
              <a
                href="#"
                title="Изменить"
                @click="
                  poligraf.action = 'update';
                  poligraf.item = props.poligrafs[idx];
                  poligraf.itemId = item.id[1].toString();
                "
              >
                <i class="bi bi-pencil-square"></i>
              </a>
            </div>
          </div>
          <LabelValue v-for="(value, key) in item" :key="key"
            :label="value[0]"
            :value="value[1]"
          />
        </CollapseDiv>
        <FileForm :accept="'*'" @submit="submitFile" />
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="poligraf.action = 'create'"
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
