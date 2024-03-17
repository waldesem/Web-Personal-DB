<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount, computed } from "vue";
import { Inquisition } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/layouts/CollapseDiv.vue")
);
const InvestigationForm = defineAsyncComponent(
  () => import("../forms/InvestigationForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/FileForm.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/LabelValue.vue")
);

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(async () => {
  emit("get-item", "investigation");
});

const props = defineProps({
  inquisitions: {
    type: Array as () => Array<Inquisition>,
    default: () => [],
  },
});

const inquisition = ref({
  action: "",
  itemId: "",
  item: <Inquisition>{},
});

const invsObj = computed(() => {
  return props.inquisitions.map((item) => ({
    id: ["ID", item["id"]],
    theme: ["Тема проверки", item["theme"]], 
    info: ["Информация", item["info"]],
    officer: ["Сотрудник", item["officer"]],
    deadline: [
      "Дата", new Date(String(item['deadline'])).toLocaleDateString('ru-RU')
    ]
  }))
});

function submitForm(form: Object) {
  emit(
    "submit", 
    inquisition.value.action,
    "investigation",
    inquisition.value.itemId,
    form,
  );
  inquisition.value.action = "";
}

function submitFile(event: Event) {
  emit("file", event);
};
</script>

<template>
  <div class="py-3">
    <InvestigationForm v-if="inquisition.action"
      :investigation="inquisition.item" 
      @submit="submitForm" 
      @cancel="inquisition.action = ''"
    />
    <div v-else>
      <div v-if="invsObj.length">
        <CollapseDiv
          v-for="(item, idx) in invsObj"
          :key="idx"
          :id="'investigation' + idx"
          :idx="idx.toString()"
          :label="'Расследование #' + (idx + 1)"
        >
          <div class="row mb-3 d-print-none">
            <div class="col-md-3">
              <label class="form-label">Действия</label>
            </div>
            <div class="col-md-9">
              <a
                href="#"
                title="Удалить"
                @click="emit('delete', item.id[1].toString(), 'investigation')"
              >
                <i class="bi bi-trash"></i>
              </a>
              &nbsp;
              <a
                href="#"
                title="Изменить"
                @click="
                  inquisition.action = 'update';
                  inquisition.item = props.inquisitions[idx];
                  inquisition.itemId = item.id[1].toString();
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
        <FileForm :accept="'*'" @submit="submitFile($event)" />
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="inquisition.action = 'create'"
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
