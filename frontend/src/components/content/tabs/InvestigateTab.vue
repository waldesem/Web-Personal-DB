<script setup lang="ts">
import { ref, defineAsyncComponent } from "vue";
import { Inquisition } from "@/interfaces";
import { stateAnketa, submitFile } from "@/state";

const ActionIcons = defineAsyncComponent(
  () => import("@components/content/elements/ActionIcons.vue")
);
const InvestigationForm = defineAsyncComponent(
  () => import("@components/content/forms/InvestigationForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/content/forms/FileForm.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/content/elements/LabelSlot.vue")
);

const inquisition = ref({
  itemId: "",
  item: <Inquisition>{},
  showActions: false,
});

function cancelAction() {
  inquisition.value.itemId = "";
  Object.keys(inquisition.value.item).forEach(
    (key) =>
      delete inquisition.value.item[key as keyof typeof inquisition.value.item]
  );
  const collapseInvestigation = document.getElementById("investigate");
  collapseInvestigation?.setAttribute("class", "collapse card card-body");
}
</script>

<template>
  <div class="collapse card card-body" id="investigate">
    <InvestigationForm @cancel="cancelAction" />
  </div>
  <div v-if="stateAnketa.anketa.investigations.length">
    <div
      v-for="(item, idx) in stateAnketa.anketa.investigations"
      :key="idx"
      @mouseover="inquisition.showActions = true"
      @mouseout="inquisition.showActions = false"
      class="card card-body"
    >
      <InvestigationForm
        v-if="inquisition.itemId === item['id'].toString()"
        :investigation="inquisition.item"
        @cancel="cancelAction"
      />
      <div v-else>
        <LabelSlot>
          <ActionIcons
            v-show="inquisition.showActions"
            @delete="
              stateAnketa.deleteItem(item['id'].toString(), 'investigations')
            "
            @update="
              inquisition.item = item;
              inquisition.itemId = item['id'].toString();
            "
            :for-input="'investigations-file'"
          >
            <FileForm
              v-show="inquisition.showActions"
              :name-id="'investigations-file'"
              :accept="'*'"
              @submit="submitFile($event, 'investigations')"
            />
          </ActionIcons>
        </LabelSlot>
        <p class="fs-5 fw-medium text-primary p-1">
          {{ "Расследование/Проверка #" + (idx+1) }}
        </p>
        <LabelSlot :label="'Тема проверки'">{{ item["theme"] }}</LabelSlot>
        <LabelSlot :label="'Информация'">{{ item["info"] }}</LabelSlot>
        <LabelSlot :label="'Сотрудник'">{{ item["user"] }}</LabelSlot>
        <LabelSlot :label="'Дата записи'">
          {{ new Date(item["created"] + ' UTC').toLocaleString("ru-RU") }}
        </LabelSlot>
      </div>
    </div>
  </div>
  <p class="p-3" v-else>Расследования/Проверки не проводились</p>
</template>

<style scoped>
@media print {
  .card {
    margin: 1px !important;
    padding: 1px !important;
  }
}
</style>