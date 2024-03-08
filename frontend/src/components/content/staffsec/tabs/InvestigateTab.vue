<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const InvestigationForm = defineAsyncComponent(
  () => import("../forms/InvestigationForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(async () => {
  emit("get-item", "investigation");
});

const props = defineProps({
  inquisitions: {
    type: Array as () => Array<Record<any, string>>,
    default: () => [],
  },
});

const inquisition = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
});

function cancelEdit() {
  inquisition.value.action = "";
  inquisition.value.item = {};
}

function submitForm(form: Object) {
  emit("submit", [
    inquisition.value.action,
    "investigation",
    inquisition.value.itemId,
    form,
  ]);
}

function submitFile(event: Event) {
  emit("file", event);
}

function deleteItem(itemId: string) {
  emit("delete", [itemId, "investigation"]);
}
</script>

<template>
  <div class="py-3">
    <ModalWin
      :title="
        inquisition.action === 'update' ? 'Изменить запись' : 'Добавить запись'
      "
      :id="'modalInvestigation'"
      @cancel="cancelEdit"
    >
      <InvestigationForm :content="inquisition.item" @submit="submitForm" />
    </ModalWin>
    <div v-if="props.inquisitions.length">
      <CollapseDiv
        v-for="(item, idx) in props.inquisitions"
        :key="idx"
        :id="'investigation' + idx"
        :idx="idx.toString()"
        :label="'Расследование #' + (idx + 1)"
      >
        <LabelSlot>
          <a
            href="#"
            title="Удалить"
            @click="deleteItem(item['id'].toString())"
          >
            <i class="bi bi-trash"></i>
          </a>
          <a
            href="#"
            title="Изменить"
            data-bs-toggle="modal"
            data-bs-target="#modalInvestigation"
            @click="
              inquisition.action = 'update';
              inquisition.item = item;
              inquisition.itemId = item['id'].toString();
            "
          >
            <i class="bi bi-pencil-square"></i>
          </a>
        </LabelSlot>
        <LabelValue :label="'Тема'" :value="item['theme']" />
        <LabelValue :label="'Информация'" :value="item['info']" />
        <LabelValue :label="'Сотрудник'" :value="item['officer']" />
        <LabelValue
          :label="'Дата'"
          :value="
            new Date(String(item['deadline'])).toLocaleDateString('ru-RU')
          "
        />
      </CollapseDiv>
      <FileForm :accept="'*'" @submit="submitFile($event)" />
    </div>
    <p v-else>Данные отсутствуют</p>
    <div class="d-print-none py-3">
      <a
        data-bs-toggle="modal"
        data-bs-target="#modalInvestigation"
        class="btn btn-outline-primary"
        type="button"
        @click="inquisition.action = 'create'"
        >Добавить запись
      </a>
    </div>
  </div>
</template>
