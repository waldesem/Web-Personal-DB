<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Inquisition } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/content/staffsec/elements/CollapseDiv.vue")
);
const InvestigationForm = defineAsyncComponent(
  () => import("../forms/InvestigationForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/staffsec/forms/FileForm.vue")
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
      <div v-if="props.inquisitions.length">
        <CollapseDiv
          v-for="(item, idx) in props.inquisitions"
          :key="idx"
          :id="'investigation' + idx"
          :idx="idx.toString()"
          :label="'Расследование #' + (idx + 1)"
        >
          <LabelValue :label="'Действия'">
            <a
              href="#"
              title="Удалить"
              @click="emit('delete', item['id'].toString(), 'investigation')"
            >
              <i class="bi bi-trash"></i>
            </a>
            &nbsp;
            <a
              href="#"
              title="Изменить"
              @click="
                inquisition.action = 'update';
                inquisition.item = item;
                inquisition.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </LabelValue>
          <LabelValue :label="'ID'">{{ item["id"] }}</LabelValue>
          <LabelValue :label="'Тема проверки'">{{ item["theme"] }}</LabelValue>
          <LabelValue :label="'Информация'">{{ item["info"] }}</LabelValue>
          <LabelValue :label="'Сотрудник'">{{ item["officer"] }}</LabelValue>
          <LabelValue :label="'Дата'">
            {{ new Date(String(item["deadline"])).toLocaleDateString("ru-RU") }}
          </LabelValue>
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
